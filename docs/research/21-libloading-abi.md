# 插件动态加载一手资料（038）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/nagisa/rust_libloading/blob/0.8.9/Cargo.toml | 0.8.9 ISC / MSRV 1.71 / edition 2015；Unix 依赖 cfg-if 1，Windows 依赖 windows-link 0.2，dev 依赖 libc 与 windows-sys 0.61 | 已证实（api.github.com 同 tag 内容） |
| https://github.com/nagisa/rust_libloading/blob/0.8.9/src/os/windows/mod.rs | `windows_link::link!("kernel32.dll" "system" fn LoadLibraryExW(...))`、`Library::new` 默认 flags=0、`LOAD_LIBRARY_SEARCH_DEFAULT_DIRS=0x00001000` 常量存在但默认不用 | 已证实（vendor 同源字节） |
| https://github.com/microsoft/windows-rs/blob/ec79074f76aa/crates/libs/link/Cargo.toml | windows-link 0.2.1 / MIT OR Apache-2.0 / edition 2024 / rust-version 1.85；`[lints] workspace = true` 脱离 workspace 需裁掉 | 已证实（api.github.com 同 commit 内容） |
| https://github.com/alexcrichton/cfg-if/blob/v1.0.5/Cargo.toml | cfg-if 1.0.5 / MIT OR Apache-2.0 / MSRV 1.32；optional `rustc-std-workspace-core` 只服务 rustc 自身构建 | 已证实（vendor 同源字节） |
| https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexw | LoadLibraryExW 标志与 Win7 KB2533623 的对应关系 | 未证实（本轮未直抓页面） |
| Win7 Tier 3 + build-std 下 windows-link raw-dylib 链接行为 | 运行时验证 | 受阻（无 Windows 运行环境） |

| 编号 | 结论 |
| --- | --- |
| R01 | 0.8.9 的闭包是 3 个 crate、零传递依赖，比 0.8.8 的 `windows-targets >=0.48,<0.54` 轻得多，选前者。 |
| R02 | Windows 目标依赖即便在 Linux 也会进 lock 解析，vendor 必须把 windows-link 一起放。 |
| R03 | `cargo check --target x86_64-pc-windows-gnu` 只证明编译，不证明 Win7 运行时；两者分开登记。 |
