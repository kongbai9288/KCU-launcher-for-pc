use crossbeam_channel::{unbounded, RecvTimeoutError};
use crossbeam_utils::sync::WaitGroup;
use crossbeam_utils::thread;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
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

pub struct TaskGroup {
    cancel: CancelToken,
    wg: Option<WaitGroup>,
    spawned: usize,
    drained: bool,
}

impl TaskGroup {
    pub fn new() -> Self {
        Self {
            cancel: CancelToken::new(),
            wg: Some(WaitGroup::new()),
            spawned: 0,
            drained: false,
        }
    }

    pub fn spawn<F>(&mut self, f: F)
    where
        F: FnOnce(CancelToken) + Send + 'static,
    {
        let w = self.wg.clone();
        let c = self.cancel.clone();
        self.spawned += 1;
        std::thread::spawn(move || {
            let _w = w;
            f(c);
        });
    }

    pub fn cancel_token(&self) -> CancelToken {
        self.cancel.clone()
    }

    pub fn cancel(&self) {
        self.cancel.cancel();
    }

    pub fn live(&self) -> usize {
        if self.drained {
            0
        } else {
            self.spawned
        }
    }

    pub fn shutdown(&mut self) -> usize {
        self.cancel.cancel();
        if let Some(wg) = self.wg.take() {
            wg.wait();
        }
        self.drained = true;
        self.spawned
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
        if let Some(wg) = self.wg.take() {
            wg.wait();
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
    let (tx, rx) = unbounded::<(usize, T)>();

    let first = thread::scope(|s| {
        for (i, f) in loaders.into_iter().enumerate() {
            let c = cancel.clone();
            let tx = tx.clone();
            s.spawn(move |_| {
                if c.is_cancelled() {
                    return;
                }
                if let Some(v) = f(c.clone()) {
                    let _ = tx.send((i, v));
                }
            });
        }
        drop(tx);
        let got = rx.recv_timeout(timeout);
        cancel.cancel();
        got
    });

    match first {
        Ok(Ok((index, value))) => Ok(RaceResult {
            index,
            value,
            live_after_join: 0,
        }),
        Ok(Err(RecvTimeoutError::Timeout | RecvTimeoutError::Disconnected)) | Err(_) => {
            Err(RaceError::TimedOut)
        }
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
                std::thread::yield_now();
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
        let done = Arc::new(std::sync::atomic::AtomicUsize::new(0));
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
                    std::thread::sleep(Duration::from_millis(1));
                }
                Some(22)
            }),
            Box::new(|c| {
                for _ in 0..200 {
                    if c.is_cancelled() {
                        return None;
                    }
                    std::thread::sleep(Duration::from_millis(1));
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
                    std::thread::sleep(Duration::from_millis(1));
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
