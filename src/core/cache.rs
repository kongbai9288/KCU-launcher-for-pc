use std::collections::{HashMap, HashSet, VecDeque};
use std::hash::Hash;
use std::sync::{Arc, Condvar, Mutex, Weak};
use std::time::{Duration, Instant};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CacheError<E> {
    Load(E),
    TimedOut,
    Cancelled,
}

struct Entry<V> {
    value: V,
    expires_at: Instant,
}

struct Flight<V> {
    done: Mutex<bool>,
    value: Mutex<Option<V>>,
    cv: Condvar,
}

impl<V> Flight<V> {
    fn new() -> Self {
        Self {
            done: Mutex::new(false),
            value: Mutex::new(None),
            cv: Condvar::new(),
        }
    }
}

struct Inner<K, V> {
    entries: HashMap<K, Entry<V>>,
    order: VecDeque<K>,
    inflight: HashMap<K, Weak<Flight<V>>>,
    evicted: u64,
}

pub struct Cache<K, V> {
    inner: Mutex<Inner<K, V>>,
    capacity: usize,
    ttl: Duration,
}

impl<K, V> Cache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    pub fn new(capacity: usize, ttl: Duration) -> Self {
        assert!(capacity > 0);
        Self {
            inner: Mutex::new(Inner {
                entries: HashMap::new(),
                order: VecDeque::new(),
                inflight: HashMap::new(),
                evicted: 0,
            }),
            capacity,
            ttl,
        }
    }

    pub fn len(&self) -> usize {
        self.inner.lock().unwrap().entries.len()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }

    pub fn evicted(&self) -> u64 {
        self.inner.lock().unwrap().evicted
    }

    pub fn inflight_count(&self) -> usize {
        self.inner.lock().unwrap().inflight.len()
    }

    pub fn order_len(&self) -> usize {
        self.inner.lock().unwrap().order.len()
    }

    pub fn clear(&self) {
        let mut g = self.inner.lock().unwrap();
        g.entries.clear();
        g.order.clear();
        g.inflight.clear();
    }

    pub fn get_or_load<F, E>(&self, key: K, timeout: Duration, loader: F) -> Result<V, CacheError<E>>
    where
        F: FnOnce() -> Result<V, E>,
    {
        let deadline = Instant::now() + timeout;
        let mut loader = Some(loader);
        loop {
            let waiting = {
                let mut g = self.inner.lock().unwrap();
                self.purge_locked(&mut g);
                if let Some(e) = g.entries.get(&key) {
                    return Ok(e.value.clone());
                }
                match g.inflight.get(&key) {
                    Some(w) => w.upgrade(),
                    None => None,
                }
            };

            if let Some(f) = waiting {
                let guard = f.done.lock().unwrap();
                let left = deadline.saturating_duration_since(Instant::now());
                let (held, wait) = f.cv.wait_timeout_while(guard, left, |d| !*d).unwrap();
                drop(held);
                if wait.timed_out() {
                    return Err(CacheError::TimedOut);
                }
                return f.value.lock().unwrap().clone().ok_or(CacheError::Cancelled);
            }

            let flight = Arc::new(Flight::new());
            {
                let mut g = self.inner.lock().unwrap();
                self.purge_locked(&mut g);
                if let Some(e) = g.entries.get(&key) {
                    return Ok(e.value.clone());
                }
                if g.inflight.get(&key).and_then(Weak::upgrade).is_some() {
                    continue;
                }
                g.inflight.insert(key.clone(), Arc::downgrade(&flight));
            }

            let load = (loader.take().expect("loader consumed once"))();
            let mut g = self.inner.lock().unwrap();
            g.inflight.remove(&key);

            match load {
                Ok(value) => {
                    *flight.value.lock().unwrap() = Some(value.clone());
                    let mut done = flight.done.lock().unwrap();
                    *done = true;
                    flight.cv.notify_all();
                    drop(done);
                    self.insert_locked(&mut g, key, value.clone());
                    return Ok(value);
                }
                Err(e) => {
                    let mut done = flight.done.lock().unwrap();
                    *done = true;
                    flight.cv.notify_all();
                    drop(done);
                    return Err(CacheError::Load(e));
                }
            }
        }
    }

    fn purge_locked(&self, g: &mut Inner<K, V>) {
        let now = Instant::now();
        let expired: Vec<K> = g
            .entries
            .iter()
            .filter(|(_, e)| e.expires_at <= now)
            .map(|(k, _)| k.clone())
            .collect();
        for k in expired {
            g.entries.remove(&k);
        }
        g.order.retain(|k| g.entries.contains_key(k));
        let mut seen = HashSet::new();
        g.order.retain(|k| seen.insert(k.clone()));
    }

    fn insert_locked(&self, g: &mut Inner<K, V>, key: K, value: V) {
        let expires_at = Instant::now() + self.ttl;
        if let Some(e) = g.entries.get_mut(&key) {
            e.value = value;
            e.expires_at = expires_at;
            return;
        }
        g.entries.insert(key.clone(), Entry { value, expires_at });
        g.order.push_back(key);
        while g.entries.len() > self.capacity {
            let mut removed = false;
            while let Some(old) = g.order.pop_front() {
                if g.entries.remove(&old).is_some() {
                    g.evicted += 1;
                    removed = true;
                    break;
                }
            }
            if !removed {
                break;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::thread;

    #[test]
    fn capacity_bounds_entry_count() {
        let c = Cache::<u32, u32>::new(2, Duration::from_secs(60));
        for i in 0..6 {
            let _ = c.get_or_load(i, Duration::from_secs(1), || Ok::<u32, ()>(i * 10));
        }
        assert!(c.len() <= 2);
        assert!(c.evicted() >= 4);
    }

    #[test]
    fn ttl_forces_reload() {
        let c = Cache::<&str, u32>::new(4, Duration::from_millis(15));
        let _ = c.get_or_load("k", Duration::from_secs(1), || Ok::<u32, ()>(1));
        thread::sleep(Duration::from_millis(30));
        let calls = AtomicUsize::new(0);
        let v = c
            .get_or_load("k", Duration::from_secs(1), || {
                calls.fetch_add(1, Ordering::SeqCst);
                Ok::<u32, ()>(2)
            })
            .unwrap();
        assert_eq!(v, 2);
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }

    #[test]
    fn single_flight_loads_once_for_concurrent_waiters() {
        let c = Arc::new(Cache::<String, u32>::new(8, Duration::from_secs(60)));
        let calls = Arc::new(AtomicUsize::new(0));
        let mut handles = Vec::new();
        for _ in 0..8 {
            let c = c.clone();
            let calls = calls.clone();
            handles.push(thread::spawn(move || {
                c.get_or_load("mod-a".to_string(), Duration::from_secs(2), || {
                    calls.fetch_add(1, Ordering::SeqCst);
                    thread::sleep(Duration::from_millis(40));
                    Ok::<u32, ()>(7)
                })
                .unwrap()
            }));
        }
        for h in handles {
            assert_eq!(h.join().unwrap(), 7);
        }
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }

    #[test]
    fn inflight_is_weak_and_never_dangles() {
        let c = Cache::<u32, u32>::new(4, Duration::from_secs(60));
        let _ = c.get_or_load(1, Duration::from_secs(1), || Ok::<u32, ()>(9));
        assert_eq!(c.inflight_count(), 0);
        let _ = c.get_or_load(2, Duration::from_secs(1), || Err::<u32, ()>(()));
        assert_eq!(c.inflight_count(), 0);
    }

    #[test]
    fn load_error_is_propagated_and_inflight_cleared() {
        let c = Cache::<u32, u32>::new(4, Duration::from_secs(60));
        assert_eq!(
            c.get_or_load(3, Duration::from_secs(1), || Err::<u32, &str>("E01")),
            Err(CacheError::Load("E01"))
        );
        assert_eq!(c.inflight_count(), 0);
        assert_eq!(c.len(), 0);
    }

    #[test]
    fn clear_resets_all_state() {
        let c = Cache::<u32, u32>::new(4, Duration::from_secs(60));
        for i in 0..3 {
            let _ = c.get_or_load(i, Duration::from_secs(1), || Ok::<u32, ()>(i));
        }
        c.clear();
        assert_eq!(c.len(), 0);
        assert_eq!(c.inflight_count(), 0);
        assert_eq!(c.order_len(), 0);
    }

    #[test]
    fn order_stays_bounded_after_many_inserts() {
        let c = Cache::<u32, u32>::new(3, Duration::from_secs(60));
        for i in 0..500 {
            let _ = c.get_or_load(i, Duration::from_secs(1), || Ok::<u32, ()>(i));
        }
        assert_eq!(c.len(), 3);
        assert!(c.order_len() <= 3, "order={}", c.order_len());
        assert_eq!(c.inflight_count(), 0);
    }

    #[test]
    fn zero_capacity_is_rejected() {
        assert!(std::panic::catch_unwind(|| Cache::<u32, u32>::new(0, Duration::from_secs(1))).is_err());
    }
}
