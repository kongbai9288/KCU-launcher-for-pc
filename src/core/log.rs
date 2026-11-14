use log::{Level, Log, Metadata, Record};
use std::fmt;
use std::sync::Mutex;

struct Inner {
    current: Vec<String>,
    shards: Vec<Vec<String>>,
}

pub struct LogBuffer {
    per_file: usize,
    inner: Mutex<Inner>,
}

impl LogBuffer {
    pub fn new(per_file: usize) -> Self {
        assert!(per_file > 0);
        Self {
            per_file,
            inner: Mutex::new(Inner {
                current: Vec::new(),
                shards: Vec::new(),
            }),
        }
    }

    pub fn record(&self, args: fmt::Arguments<'_>, level: Level, target: &str) {
        let rec = Record::builder()
            .args(args)
            .level(level)
            .target(target)
            .build();
        Log::log(self, &rec);
    }

    pub fn shard_count(&self) -> usize {
        self.inner.lock().expect("log mutex").shards.len()
    }

    pub fn pending(&self) -> usize {
        self.inner.lock().expect("log mutex").current.len()
    }

    pub fn take_shards(&self) -> Vec<Vec<String>> {
        let mut g = self.inner.lock().expect("log mutex");
        let mut out = std::mem::take(&mut g.shards);
        if !g.current.is_empty() {
            out.push(std::mem::take(&mut g.current));
        }
        out
    }
}

impl Log for LogBuffer {
    fn enabled(&self, _metadata: &Metadata<'_>) -> bool {
        true
    }

    fn log(&self, record: &Record<'_>) {
        let mut g = self.inner.lock().expect("log mutex");
        g.current.push(record.args().to_string());
        if g.current.len() >= self.per_file {
            let done = std::mem::take(&mut g.current);
            g.shards.push(done);
        }
    }

    fn flush(&self) {
        let _ = self.take_shards();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use log::Record;

    fn write(buf: &LogBuffer, i: usize) {
        let text = format!("line {}", i);
        let args = format_args!("{}", text);
        let rec = Record::builder()
            .args(args)
            .level(Level::Info)
            .target("kcu.test")
            .build();
        Log::log(buf, &rec);
    }

    #[test]
    fn hundred_lines_form_one_shard() {
        let b = LogBuffer::new(100);
        for i in 0..100 {
            write(&b, i);
        }
        assert_eq!(b.shard_count(), 1);
        assert_eq!(b.pending(), 0);
    }

    #[test]
    fn flush_returns_every_line() {
        let b = LogBuffer::new(100);
        for i in 0..250 {
            write(&b, i);
        }
        let parts = b.take_shards();
        assert_eq!(parts.len(), 3);
        assert_eq!(parts.iter().map(Vec::len).sum::<usize>(), 250);
        assert_eq!(b.shard_count(), 0);
        assert_eq!(b.pending(), 0);
    }

    #[test]
    fn zero_per_file_is_rejected() {
        assert!(std::panic::catch_unwind(|| LogBuffer::new(0)).is_err());
    }

    #[test]
    fn enabled_is_true_for_all_levels() {
        let b = LogBuffer::new(10);
        let m = Metadata::builder().level(Level::Trace).target("kcu").build();
        assert!(Log::enabled(&b, &m));
    }

    #[test]
    fn record_helper_goes_through_the_facade() {
        let b = LogBuffer::new(4);
        b.record(format_args!("[KCU] core start paths OK"), Level::Info, "kcu.core");
        assert_eq!(b.pending(), 1);
        let parts = b.take_shards();
        assert_eq!(parts[0][0], "[KCU] core start paths OK");
    }

    #[test]
    fn flush_trait_method_drains() {
        let b = LogBuffer::new(2);
        write(&b, 1);
        write(&b, 2);
        assert_eq!(b.shard_count(), 1);
        Log::flush(&b);
        assert_eq!(b.shard_count(), 0);
        assert_eq!(b.pending(), 0);
    }
}
