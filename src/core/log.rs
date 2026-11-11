#[derive(Debug, Clone)]
pub struct LogBuffer {
    per_file: usize,
    current: Vec<String>,
    shards: Vec<Vec<String>>,
}

impl LogBuffer {
    pub fn new(per_file: usize) -> Self {
        assert!(per_file > 0);
        Self {
            per_file,
            current: Vec::new(),
            shards: Vec::new(),
        }
    }

    pub fn push(&mut self, line: impl Into<String>) {
        self.current.push(line.into());
        if self.current.len() >= self.per_file {
            self.shards.push(std::mem::take(&mut self.current));
        }
    }

    pub fn shard_count(&self) -> usize {
        self.shards.len()
    }

    pub fn pending(&self) -> usize {
        self.current.len()
    }

    pub fn flush(&mut self) -> Vec<Vec<String>> {
        let mut out = std::mem::take(&mut self.shards);
        if !self.current.is_empty() {
            out.push(std::mem::take(&mut self.current));
        }
        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hundred_lines_form_one_shard() {
        let mut b = LogBuffer::new(100);
        for i in 0..100 {
            b.push(format!("line {}", i));
        }
        assert_eq!(b.shard_count(), 1);
        assert_eq!(b.pending(), 0);
    }

    #[test]
    fn flush_returns_every_line() {
        let mut b = LogBuffer::new(100);
        for i in 0..250 {
            b.push(format!("line {}", i));
        }
        let parts = b.flush();
        assert_eq!(parts.len(), 3);
        let total: usize = parts.iter().map(Vec::len).sum();
        assert_eq!(total, 250);
        assert_eq!(b.shard_count(), 0);
        assert_eq!(b.pending(), 0);
    }

    #[test]
    fn zero_per_file_is_rejected() {
        assert!(std::panic::catch_unwind(|| LogBuffer::new(0)).is_err());
    }
}
