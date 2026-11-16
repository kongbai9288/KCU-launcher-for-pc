use anyhow::{anyhow, Result};
use std::path::{Component, Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Mutex, MutexGuard, PoisonError};
use std::time::Instant;

pub const MAX_IDS_TOTAL: usize = 10_000;
pub const MAX_ID_BYTES: usize = 256;
pub const MAX_TEXT_BYTES: usize = 4096;
pub const MAX_PATH_BYTES: usize = 1024;
pub const MAX_REL_DEPTH: usize = 32;
pub const MAX_OPS_PER_WINDOW: usize = 64;
pub const OPS_WINDOW_SECS: u64 = 1;

const WINDOWS_RESERVED: &[&str] = &[
    "con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "com5",
    "com6", "com7", "com8", "com9", "lpt1", "lpt2", "lpt3", "lpt4",
    "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
];

/// 用户输入的长度、空值与控制字符边界。返回 Err，不 panic。
pub fn check_text(s: &str, limit: usize) -> Result<()> {
    if s.is_empty() {
        return Err(anyhow!("empty input"));
    }
    if s.len() > limit {
        return Err(anyhow!("input too long: {} > {}", s.len(), limit));
    }
    if s.bytes().any(|b| b < 0x20 || b == 0x7f) {
        return Err(anyhow!("control character in input"));
    }
    Ok(())
}

/// 批量 id 的总量与单项边界。构造请求前调用。
pub fn check_ids(ids: &[String]) -> Result<()> {
    if ids.is_empty() {
        return Ok(());
    }
    if ids.len() > MAX_IDS_TOTAL {
        return Err(anyhow!("too many ids: {} > {}", ids.len(), MAX_IDS_TOTAL));
    }
    for id in ids {
        check_text(id, MAX_ID_BYTES)?;
    }
    Ok(())
}

fn reserved_name(name: &str) -> bool {
    let stem = name.split('.').next().unwrap_or(name).to_ascii_lowercase();
    WINDOWS_RESERVED.contains(&stem.as_str())
}

/// 相对路径只允许落在 root 内。遍历由 std::path::Component 完成，
/// 项目侧只做策略判定（拒绝绝对、越界、保留名、控制字符、超深）。
pub fn safe_join(root: &Path, rel: &str) -> Result<PathBuf> {
    check_text(rel, MAX_PATH_BYTES)?;
    let mut stack: Vec<&std::ffi::OsStr> = Vec::new();
    for c in Path::new(rel).components() {
        match c {
            Component::Prefix(_) | Component::RootDir => {
                return Err(anyhow!("absolute path rejected"));
            }
            Component::CurDir => {}
            Component::ParentDir => {
                if stack.pop().is_none() {
                    return Err(anyhow!("path escapes root"));
                }
            }
            Component::Normal(part) => {
                let s = part.to_string_lossy();
                if s.is_empty() || s.len() > MAX_ID_BYTES {
                    return Err(anyhow!("invalid path component length"));
                }
                if s.bytes().any(|b| b < 0x20 || matches!(b, b'<' | b'>' | b':' | b'"' | b'|' | b'?' | b'*')) {
                    return Err(anyhow!("invalid path component character"));
                }
                if reserved_name(&s) {
                    return Err(anyhow!("reserved device name rejected"));
                }
                stack.push(part);
            }
        }
        if stack.len() > MAX_REL_DEPTH {
            return Err(anyhow!("path too deep"));
        }
    }
    if stack.is_empty() {
        return Err(anyhow!("empty relative path"));
    }
    let mut out = root.to_path_buf();
    for part in stack {
        out.push(part);
    }
    Ok(out)
}

/// 文件被删除、损坏、权限不足时回退到默认值；返回是否发生过回退。
pub fn read_or_default(path: &Path, fallback: &str) -> (String, bool) {
    match std::fs::read_to_string(path) {
        Ok(s) if !s.is_empty() => (s, false),
        _ => (fallback.to_string(), true),
    }
}

/// 必需文件缺失不给静默默认值，返回明确错误。
pub fn require_file(path: &Path) -> Result<String> {
    std::fs::read_to_string(path).map_err(|e| anyhow!("required file unusable: {}", e))
}

/// 高频重复操作的有界计数。窗口按秒滚动，锁中毒时不连锁 panic。
pub struct OpBudget {
    count: AtomicU64,
    window: Mutex<Instant>,
    max: u64,
}

impl OpBudget {
    pub fn new(max: usize) -> Self {
        Self {
            count: AtomicU64::new(0),
            window: Mutex::new(Instant::now()),
            max: max.max(1) as u64,
        }
    }

    fn lock(&self) -> MutexGuard<'_, Instant> {
        self.window.lock().unwrap_or_else(PoisonError::into_inner)
    }

    pub fn try_op(&self) -> bool {
        let mut start = self.lock();
        let now = Instant::now();
        if now.duration_since(*start).as_secs() >= OPS_WINDOW_SECS {
            *start = now;
            self.count.store(0, Ordering::SeqCst);
        }
        let n = self.count.fetch_add(1, Ordering::SeqCst) + 1;
        n <= self.max
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn rejects_empty_too_long_and_control_chars() {
        assert!(check_text("", 10).is_err());
        assert!(check_text(&"x".repeat(11), 10).is_err());
        assert!(check_text("a\nb", 10).is_err());
        assert!(check_text("ok", 10).is_ok());
    }

    #[test]
    fn rejects_id_flood_and_oversized_single_id() {
        let many: Vec<String> = (0..MAX_IDS_TOTAL + 1).map(|i| i.to_string()).collect();
        assert!(check_ids(&many).is_err());
        assert!(check_ids(&["x".repeat(MAX_ID_BYTES + 1)].to_vec()).is_err());
        assert!(check_ids(&Vec::<String>::new()).is_ok());
        assert!(check_ids(&["mod-a".into(), "mod-b".into()]).is_ok());
    }

    #[test]
    fn rejects_absolute_traversal_and_reserved_names() {
        let root = Path::new("KCU");
        assert!(safe_join(root, "/etc/passwd").is_err());
        assert!(safe_join(root, "../outside").is_err());
        assert!(safe_join(root, "a/../../outside").is_err());
        assert!(safe_join(root, concat!("C", ":", "\\", "Windows")).is_err());
        assert!(safe_join(root, "CON").is_err());
        assert!(safe_join(root, "nul.txt").is_err());
        assert!(safe_join(root, "a/./b.txt").is_ok());
        assert_eq!(safe_join(root, "a/b.txt").unwrap(), PathBuf::from("KCU/a/b.txt"));
    }

    #[test]
    fn rejects_control_chars_and_excessive_depth() {
        let root = Path::new("KCU");
        assert!(safe_join(root, "a\0b").is_err());
        assert!(safe_join(root, "a<b").is_err());
        let deep = (0..MAX_REL_DEPTH + 1).map(|_| "d").collect::<Vec<_>>().join("/");
        assert!(safe_join(root, &deep).is_err());
    }

    #[test]
    fn deleted_or_corrupt_file_falls_back_without_panic() {
        let dir = std::env::temp_dir().join("kcu_robust_048");
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        let p = dir.join("config.json");
        assert_eq!(read_or_default(&p, "default"), ("default".to_string(), true));
        std::fs::write(&p, "").unwrap();
        assert_eq!(read_or_default(&p, "default"), ("default".to_string(), true));
        std::fs::write(&p, "real").unwrap();
        assert_eq!(read_or_default(&p, "default"), ("real".to_string(), false));
        assert!(require_file(&p).is_ok());
        std::fs::remove_file(&p).unwrap();
        assert!(require_file(&p).is_err());
        assert_eq!(read_or_default(&p, "default"), ("default".to_string(), true));
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn op_budget_caps_heavy_repeat() {
        let b = OpBudget::new(3);
        assert!(b.try_op());
        assert!(b.try_op());
        assert!(b.try_op());
        assert!(!b.try_op());
        assert!(!b.try_op());
    }

    #[test]
    fn op_budget_is_atomic_under_concurrency() {
        let b = OpBudget::new(16);
        let ok = thread::scope(|s| {
            let handles: Vec<_> = (0..8)
                .map(|_| s.spawn(|| (0..8).filter(|_| b.try_op()).count()))
                .collect();
            handles.into_iter().map(|h| h.join().unwrap_or(0)).sum::<usize>()
        });
        assert!(ok <= 16);
        assert!(ok >= 1);
    }

    #[test]
    fn poisoned_budget_still_serves() {
        let b = OpBudget::new(10);
        thread::scope(|s| {
            let r = s.spawn(|| {
                let _g = b.window.lock().unwrap();
                panic!("poison budget");
            });
            assert!(r.join().is_err());
        });
        assert!(b.try_op());
    }
}
