pub mod core;
pub mod dispatcher;
pub mod lightweight;

pub use core::envelope::{Envelope, Kind};
pub use core::diagnostics::diag_line;
pub use core::popup::Popup;
pub use core::userflow::{simulate, Step, FlowReport};
pub use core::cache::Cache;
pub use core::asynk::{CancelToken, TaskGroup, RaceResult, race};
pub use core::leak::WeakRegistry;
pub use dispatcher::{Dispatcher, DispatchInput, LaunchOutcome, LaunchTask, Mode, ModeSelector, TaskSet};
pub use lightweight::{AuthKind, Downloader, LightweightView, LoaderRegistry, LoginSession, ProviderConfig, ViewAction};
