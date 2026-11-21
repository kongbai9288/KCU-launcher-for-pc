//! 唯一稳定公共面。内部模块的具体类型不再在 crate 顶层平铺再导出。
//! 破坏性变更升 `v2` 并给迁移步骤，`v1` 调用面保持不动。

pub mod v1 {
    pub use crate::core::asynk::CancelToken;
    pub use crate::core::envelope::{Envelope, Kind};
    pub use crate::core::popup::{CloseAction, PopupOpenError, PopupRegistry};
}
