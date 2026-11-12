use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::mpsc::{channel, Receiver};
use std::sync::Arc;
use std::thread::{self, JoinHandle};
use std::time::Duration;

#[derive(Clone)]
pub struct CancelToken {
    flag: Arc<AtomicBool>,
}

impl CancelToken {
    pub fn new() -> Self {
        Self {
            flag: Arc::new(AtomicBool::new(false)),
        }
    }

    pub fn cancel(&self) {
        self.flag.store(true, Ordering::SeqCst);
    }

    pub fn is_cancelled(&self) -> bool {
        self.flag.load(Ordering::SeqCst)
    }
}

impl Default for CancelToken {
    fn default() -> Self {
        Self::new()
    }
}

struct LiveGuard {
    n: Arc<AtomicUsize>,
}

impl Drop for LiveGuard {
    fn drop(&mut self) {
        self.n.fetch_sub(1, Ordering::SeqCst);
    }
}

pub struct TaskGroup {
    handles: Vec<JoinHandle<()>>,
    cancel: CancelToken,
    live: Arc<AtomicUsize>,
}

impl TaskGroup {
    pub fn new() -> Self {
        Self {
            handles: Vec::new(),
            cancel: CancelToken::new(),
            live: Arc::new(AtomicUsize::new(0)),
        }
    }

    pub fn spawn<F>(&mut self, f: F)
    where
        F: FnOnce(CancelToken) + Send + 'static,
    {
        self.live.fetch_add(1, Ordering::SeqCst);
        let n = self.live.clone();
        let c = self.cancel.clone();
        self.handles.push(thread::spawn(move || {
            let _g = LiveGuard { n };
            f(c);
        }));
    }

    pub fn cancel_token(&self) -> CancelToken {
        self.cancel.clone()
    }

    pub fn cancel(&self) {
        self.cancel.cancel();
    }

    pub fn live(&self) -> usize {
        self.live.load(Ordering::SeqCst)
    }

    pub fn shutdown(&mut self) -> usize {
        self.cancel.cancel();
        let mut joined = 0;
        for h in self.handles.drain(..) {
            let _ = h.join();
            joined += 1;
        }
        joined
    }
}

impl Default for TaskGroup {
    fn default() -> Self {
        Self::new()
    }
}

impl Drop for TaskGroup {
    fn drop(&mut self) {
        self.cancel.cancel();
        for h in self.handles.drain(..) {
            let _ = h.join();
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RaceError {
    TimedOut,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RaceResult<T> {
    pub index: usize,
    pub value: T,
    pub live_after_join: usize,
}

pub fn race<T, F, I>(loaders: I, timeout: Duration) -> Result<RaceResult<T>, RaceError>
where
    I: IntoIterator<Item = F>,
    F: FnOnce(CancelToken) -> Option<T> + Send + 'static,
    T: Send + 'static,
{
    let cancel = CancelToken::new();
    let live = Arc::new(AtomicUsize::new(0));
    let (tx, rx): (_, Receiver<(usize, T)>) = channel();
    let mut handles = Vec::new();

    for (i, f) in loaders.into_iter().enumerate() {
        let c = cancel.clone();
        let tx = tx.clone();
        let n = live.clone();
        n.fetch_add(1, Ordering::SeqCst);
        handles.push(thread::spawn(move || {
            let _g = LiveGuard { n };
            if c.is_cancelled() {
                return;
            }
            if let Some(v) = f(c.clone()) {
                let _ = tx.send((i, v));
            }
        }));
    }
    drop(tx);

    let first = rx.recv_timeout(timeout);
    cancel.cancel();
    for h in handles {
        let _ = h.join();
    }

    match first {
        Ok((index, value)) => Ok(RaceResult {
            index,
            value,
            live_after_join: live.load(Ordering::SeqCst),
        }),
        Err(_) => Err(RaceError::TimedOut),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cancel_stops_worker() {
        let mut g = TaskGroup::new();
        g.spawn(|c| {
            while !c.is_cancelled() {
                thread::yield_now();
            }
        });
        g.cancel();
        assert_eq!(g.shutdown(), 1);
        assert_eq!(g.live(), 0);
    }

    #[test]
    fn shutdown_joins_every_handle() {
        let mut g = TaskGroup::new();
        for _ in 0..5 {
            g.spawn(|_| {});
        }
        assert_eq!(g.shutdown(), 5);
        assert_eq!(g.live(), 0);
    }

    #[test]
    fn drop_joins_without_explicit_shutdown() {
        let done = Arc::new(AtomicUsize::new(0));
        {
            let mut g = TaskGroup::new();
            for _ in 0..4 {
                let d = done.clone();
                g.spawn(move |_| {
                    d.fetch_add(1, Ordering::SeqCst);
                });
            }
        }
        assert_eq!(done.load(Ordering::SeqCst), 4);
    }

    #[test]
    fn race_returns_first_and_cancels_other_sources() {
        let loaders: Vec<Box<dyn FnOnce(CancelToken) -> Option<u32> + Send>> = vec![
            Box::new(|_| Some(11)),
            Box::new(|c| {
                for _ in 0..200 {
                    if c.is_cancelled() {
                        return None;
                    }
                    thread::sleep(Duration::from_millis(1));
                }
                Some(22)
            }),
            Box::new(|c| {
                for _ in 0..200 {
                    if c.is_cancelled() {
                        return None;
                    }
                    thread::sleep(Duration::from_millis(1));
                }
                Some(33)
            }),
        ];
        let r = race(loaders, Duration::from_secs(2)).unwrap();
        assert_eq!(r.index, 0);
        assert_eq!(r.value, 11);
        assert_eq!(r.live_after_join, 0);
    }

    #[test]
    fn race_timeout_reports_error_and_releases_threads() {
        let loaders: Vec<Box<dyn FnOnce(CancelToken) -> Option<u32> + Send>> = vec![
            Box::new(|c| {
                while !c.is_cancelled() {
                    thread::sleep(Duration::from_millis(1));
                }
                None
            }),
        ];
        assert_eq!(race(loaders, Duration::from_millis(20)), Err(RaceError::TimedOut));
    }

    #[test]
    fn cancel_token_clones_share_flag() {
        let a = CancelToken::new();
        let b = a.clone();
        assert!(!b.is_cancelled());
        a.cancel();
        assert!(b.is_cancelled());
    }
}
