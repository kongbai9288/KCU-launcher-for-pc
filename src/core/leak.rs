use std::collections::HashMap;
use std::hash::Hash;
use std::sync::{Arc, Mutex, Weak};

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

    pub fn remove(&self, key: &K) -> Option<Weak<V>> {
        self.map.lock().unwrap().remove(key)
    }

    pub fn clear(&self) {
        self.map.lock().unwrap().clear();
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
    fn weak_link_breaks_cycle() {
        struct Node {
            next: Mutex<Option<Weak<Node>>>,
        }
        let a = Arc::new(Node { next: Mutex::new(None) });
        let b = Arc::new(Node { next: Mutex::new(None) });
        *a.next.lock().unwrap() = Some(Arc::downgrade(&b));
        *b.next.lock().unwrap() = Some(Arc::downgrade(&a));
        assert_eq!(Arc::strong_count(&a), 1);
        assert_eq!(Arc::strong_count(&b), 1);
        let wa = Arc::downgrade(&a);
        let wb = Arc::downgrade(&b);
        drop(a);
        drop(b);
        assert!(wa.upgrade().is_none());
        assert!(wb.upgrade().is_none());
    }
}
