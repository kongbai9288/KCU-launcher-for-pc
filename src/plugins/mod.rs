pub mod fault;
pub mod icon;
pub mod identity;
pub mod upgrade;

pub use fault::{handle_fault, FaultAction, PluginFault, StartupPlan};
pub use icon::{PluginIcon, FALLBACK_GLYPH};
pub use identity::{identity_hash, Identity};
pub use upgrade::{decide_upgrade, UpgradeDecision, UpgradeRequest};
