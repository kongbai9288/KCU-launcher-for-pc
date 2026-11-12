use std::collections::HashMap;
use std::hash::Hash;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex, Weak};

pub struct Tracker {
    n: Arc<AtomicUsize>,
}

impl Tracker {
    pub fn new() -> Self {
        Self {
            n: Arc::new(AtomicUsize::new(0)),
        }
    }

    pub fn track<T>(&self, value: T) -> Tracked<T> {
        self.n.fetch_add(1, Ordering::SeqCst);
        Tracked {
            inner: Arc::new(value),
            n: self.n.clone(),
        }
    }

    pub fn live(&self) -> usize {
        self.n.load(Ordering::SeqCst)
    }
}

impl Default for Tracker {
    fn default() -> Self {
        Self::new()
    }
}

pub struct Tracked<T> {
    inner: Arc<T>,
    n: Arc<AtomicUsize>,
}

impl<T> Tracked<T> {
    pub fn get(&self) -> &T {
        &self.inner
    }

    pub fn downgrade(&self) -> Weak<T> {
        Arc::downgrade(&self.inner)
    }

    pub fn strong_count(&self) -> usize {
        Arc::strong_count(&self.inner)
    }
}

impl<T> Clone for Tracked<T> {
    fn clone(&self) -> Self {
        self.n.fetch_add(1, Ordering::SeqCst);
        Self {
            inner: self.inner.clone(),
            n: self.n.clone(),
        }
    }
}

impl<T> Drop for Tracked<T> {
    fn drop(&mut self) {
        self.n.fetch_sub(1, Ordering::SeqCst);
    }
}

pub struct WeakRegistry<K, V> {
    map: Mutex<HashMap<K, Weak<V>>>,
}

impl<K, V> WeakRegistry<K, V>
where
    K: Eq + Hash + Clone,
{
    pub fn new() -> Self {
        Self {
            map: Mutex::new(HashMap::new()),
        }
    }

    pub fn insert(&self, key: K, value: &Arc<V>) {
        self.map.lock().unwrap().insert(key, Arc::downgrade(value));
    }

    pub fn get(&self, key: &K) -> Option<Arc<V>> {
        self.map
            .lock()
            .unwrap()
            .get(key)
            .and_then(Weak::upgrade)
    }

    pub fn purge(&self) -> usize {
        let mut g = self.map.lock().unwrap();
        let before = g.len();
        g.retain(|_, w| w.upgrade().is_some());
        before - g.len()
    }

    pub fn len(&self) -> usize {
        self.map.lock().unwrap().len()
    }
}

impl<K, V> Default for WeakRegistry<K, V>
where
    K: Eq + Hash + Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tracked_releases_on_drop() {
        let t = Tracker::new();
        {
            let a = t.track(7u32);
            assert_eq!(*a.get(), 7);
            assert_eq!(t.live(), 1);
        }
        assert_eq!(t.live(), 0);
    }

    #[test]
    fn clone_increments_and_all_drops_return_to_zero() {
        let t = Tracker::new();
        let a = t.track(1u32);
        let b = a.clone();
        assert_eq!(t.live(), 2);
        drop(a);
        assert_eq!(t.live(), 1);
        drop(b);
        assert_eq!(t.live(), 0);
    }

    #[test]
    fn weak_registry_does_not_keep_value_alive() {
        let reg = WeakRegistry::<String, u32>::new();
        let v = Arc::new(42u32);
        reg.insert("k".to_string(), &v);
        assert_eq!(reg.get(&"k".to_string()), Some(Arc::new(42u32)));
        drop(v);
        assert_eq!(reg.get(&"k".to_string()), None);
        assert_eq!(reg.purge(), 1);
        assert_eq!(reg.len(), 0);
    }

    #[test]
    fn purge_removes_only_dead_entries() {
        let reg = WeakRegistry::<u32, u32>::new();
        let a = Arc::new(1u32);
        let b = Arc::new(2u32);
        reg.insert(1, &a);
        reg.insert(2, &b);
        drop(b);
        assert_eq!(reg.purge(), 1);
        assert_eq!(reg.len(), 1);
        assert!(reg.get(&1).is_some());
    }

    #[test]
    fn weak_link_breaks_cycle_and_reaches_zero() {
        struct Node {
            next: Mutex<Option<Weak<Node>>>,
        }
        let t = Tracker::new();
        let a = t.track(Node {
            next: Mutex::new(None),
        });
        let b = t.track(Node {
            next: Mutex::new(None),
        });
        *a.get().next.lock().unwrap() = Some(b.downgrade());
        *b.get().next.lock().unwrap() = Some(a.downgrade());
        assert_eq!(a.strong_count(), 1);
        assert_eq!(b.strong_count(), 1);
        assert_eq!(t.live(), 2);
        drop(a);
        drop(b);
        assert_eq!(t.live(), 0);
    }
}
