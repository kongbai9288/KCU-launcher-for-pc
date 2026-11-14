use crate::core::leak::WeakRegistry;
use crossbeam_channel::{bounded, Sender};
use lru::LruCache;
use std::hash::Hash;
use std::num::NonZeroUsize;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CacheError<E> {
    Load(E),
    TimedOut,
    Cancelled,
}

type Reply<V> = Result<V, ()>;

struct Entry<V> {
    value: V,
    expires_at: Instant,
}

struct FlightState<V> {
    completed: Option<Reply<V>>,
    waiters: Vec<Sender<Reply<V>>>,
}

struct Flight<V> {
    state: Mutex<FlightState<V>>,
}

impl<V> Flight<V> {
    fn new() -> Self {
        Self {
            state: Mutex::new(FlightState {
                completed: None,
                waiters: Vec::new(),
            }),
        }
    }
}

pub struct Cache<K, V> {
    store: Mutex<LruCache<K, Entry<V>>>,
    inflight: WeakRegistry<K, Flight<V>>,
    capacity: usize,
    ttl: Duration,
    inserted: AtomicU64,
}

impl<K, V> Cache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    pub fn new(capacity: usize, ttl: Duration) -> Self {
        assert!(capacity > 0);
        let cap = NonZeroUsize::new(capacity).expect("capacity > 0");
        Self {
            store: Mutex::new(LruCache::new(cap)),
            inflight: WeakRegistry::new(),
            capacity,
            ttl,
            inserted: AtomicU64::new(0),
        }
    }

    fn lookup(&self, key: &K) -> Option<V> {
        let mut s = self.store.lock().unwrap();
        let now = Instant::now();
        let hit = s
            .get(key)
            .filter(|e| e.expires_at > now)
            .map(|e| e.value.clone());
        if hit.is_none() && s.contains(key) {
            s.pop(key);
        }
        hit
    }

    pub fn len(&self) -> usize {
        self.store.lock().unwrap().len()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }

    pub fn evicted(&self) -> u64 {
        let len = self.store.lock().unwrap().len() as u64;
        self.inserted.load(Ordering::Relaxed).saturating_sub(len)
    }

    pub fn inflight_count(&self) -> usize {
        self.inflight.purge();
        self.inflight.len()
    }

    pub fn order_len(&self) -> usize {
        self.len()
    }

    pub fn clear(&self) {
        self.store.lock().unwrap().clear();
        self.inflight.clear();
        self.inserted.store(0, Ordering::Relaxed);
    }

    pub fn get_or_load<F, E>(&self, key: K, timeout: Duration, loader: F) -> Result<V, CacheError<E>>
    where
        F: FnOnce() -> Result<V, E>,
    {
        let deadline = Instant::now() + timeout;
        let mut loader = Some(loader);

        loop {
            if let Some(v) = self.lookup(&key) {
                return Ok(v);
            }

            self.inflight.purge();
            if let Some(f) = self.inflight.get(&key) {
                let (tx, rx) = bounded::<Reply<V>>(1);
                let mut st = f.state.lock().unwrap();
                if let Some(reply) = st.completed.clone() {
                    return finish_reply(reply);
                }
                st.waiters.push(tx);
                drop(st);
                let left = deadline.saturating_duration_since(Instant::now());
                return match rx.recv_timeout(left) {
                    Ok(reply) => finish_reply(reply),
                    Err(_) => Err(CacheError::TimedOut),
                };
            }

            let flight = Arc::new(Flight::new());
            self.inflight.insert(key.clone(), &flight);

            if let Some(v) = self.lookup(&key) {
                self.inflight.remove(&key);
                return Ok(v);
            }

            let load = (loader.take().expect("loader consumed once"))();
            let reply: Reply<V> = match &load {
                Ok(v) => Ok(v.clone()),
                Err(_) => Err(()),
            };
            {
                let mut st = flight.state.lock().unwrap();
                st.completed = Some(reply.clone());
                for tx in st.waiters.drain(..) {
                    let _ = tx.send(reply.clone());
                }
            }
            self.inflight.remove(&key);
            drop(flight);

            match load {
                Ok(value) => {
                    let mut s = self.store.lock().unwrap();
                    s.put(
                        key,
                        Entry {
                            value: value.clone(),
                            expires_at: Instant::now() + self.ttl,
                        },
                    );
                    self.inserted.fetch_add(1, Ordering::Relaxed);
                    return Ok(value);
                }
                Err(e) => return Err(CacheError::Load(e)),
            }
        }
    }
}

fn finish_reply<V, E>(reply: Reply<V>) -> Result<V, CacheError<E>> {
    match reply {
        Ok(v) => Ok(v),
        Err(()) => Err(CacheError::Cancelled),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::AtomicUsize;
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

    #[test]
    fn late_waiter_sees_completed_result() {
        let c = Arc::new(Cache::<String, u32>::new(4, Duration::from_secs(60)));
        let c2 = c.clone();
        let h = thread::spawn(move || {
            c2.get_or_load("k".to_string(), Duration::from_secs(2), || {
                thread::sleep(Duration::from_millis(30));
                Ok::<u32, ()>(5)
            })
            .unwrap()
        });
        thread::sleep(Duration::from_millis(5));
        assert_eq!(
            c.get_or_load("k".to_string(), Duration::from_secs(2), || Ok::<u32, ()>(99))
                .unwrap(),
            5
        );
        assert_eq!(h.join().unwrap(), 5);
    }

    #[test]
    fn cancelled_waiters_get_cancelled_not_spurious_value() {
        let c = Arc::new(Cache::<String, u32>::new(4, Duration::from_secs(60)));
        let c2 = c.clone();
        let h = thread::spawn(move || {
            c2.get_or_load("k".to_string(), Duration::from_secs(2), || {
                thread::sleep(Duration::from_millis(30));
                Err::<u32, &str>("E02")
            })
        });
        thread::sleep(Duration::from_millis(5));
        assert_eq!(
            c.get_or_load("k".to_string(), Duration::from_secs(2), || Ok::<u32, ()>(99)),
            Err(CacheError::Cancelled)
        );
        assert_eq!(h.join().unwrap(), Err(CacheError::Load("E02")));
    }
}
