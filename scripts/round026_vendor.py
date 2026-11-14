"""Fetch crate sources into vendor/ using GitHub tarballs, close over Cargo's
missing-package / version-mismatch errors until `cargo build --offline` resolves."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor"
CACHE = Path("/data/workspace/_probe3")
CACHE.mkdir(exist_ok=True)
TOKEN = Path("/data/workspace/.kcu_pat").read_text().strip()

# name -> github repo; optional exact tag / branch override lives in PIN
KNOWN = {
    "moka": "moka-rs/moka",
    "mini-moka": "moka-rs/mini-moka",
    "triomphe": "Manishearth/triomphe",
    "stable_deref_trait": "Storyyeller/stable_deref_trait",
    "dashmap": "xacrimon/dashmap",
    "lock_api": "Amanieu/parking_lot",
    "parking_lot_core": "Amanieu/parking_lot",
    "once_cell": "matklad/once_cell",
    "serde": "serde-rs/serde",
    "crossbeam-channel": "crossbeam-rs/crossbeam",
    "crossbeam-epoch": "crossbeam-rs/crossbeam",
    "crossbeam-utils": "crossbeam-rs/crossbeam",
    "crossbeam-queue": "crossbeam-rs/crossbeam",
    "crossbeam-deque": "crossbeam-rs/crossbeam",
    "parking_lot": "Amanieu/parking_lot",
    "parking_lot_core": "Amanieu/parking_lot",
    "lock_api": "Amanieu/parking_lot",
    "smallvec": "servo/rust-smallvec",
    "cfg-if": "rust-lang/cfg-if",
    "once_cell": "matklad/once_cell",
    "scopeguard": "bluss/scopeguard",
    "memoffset": "Gilnaa/memoffset",
    "portable-atomic": "taiki-e/portable-atomic",
    "tagptr": "oliver-giersch/tagptr",
    "thiserror": "dtolnay/thiserror",
    "thiserror-impl": "dtolnay/thiserror",
    "syn": "dtolnay/syn",
    "quote": "dtolnay/quote",
    "proc-macro2": "dtolnay/proc-macro2",
    "unicode-ident": "dtolnay/unicode-ident",
    "uuid": "uuid-rs/uuid",
    "getrandom": "rust-random/getrandom",
    "libc": "rust-lang/libc",
    "autocfg": "cuviper/autocfg",
    "equivalent": "indexmap-rs/equivalent",
    "hashbrown": "rust-lang/hashbrown",
    "ahash": "tkaitchuck/aHash",
    "zerocopy": "google/zerocopy",
    "tokio": "tokio-rs/tokio",
    "bytes": "tokio-rs/bytes",
    "mio": "tokio-rs/mio",
    "pin-project-lite": "taiki-e/pin-project-lite",
    "socket2": "rust-lang/socket2",
    "signal-hook-registry": "vorner/signal-hook",
    "num_cpus": "seanmonstar/num_cpus",
    "hermit-abi": "hermit-os/hermit-abi",
    "wasm-bindgen": "rustwasm/wasm-bindgen",
    "js-sys": "rustwasm/wasm-bindgen",
    "windows-sys": "microsoft/windows-rs",
    "windows-targets": "microsoft/windows-rs",
    "winapi": "retep998/winapi-rs",
    "redox_syscall": "redox-os/syscall",
    "log": "rust-lang/log",
    "futures-util": "rust-lang/futures-rs",
    "event-listener": "smol-rs/event-listener",
    "async-lock": "smol-rs/async-lock",
    "quanta": "metrics-rs/quanta",
    "r-efi": "r-efi/r-efi",
    "cc": "rust-lang/cc-rs",
    "bumpalo": "fitzgen/bumpalo",
    "wit-bindgen": "bytecodealliance/wit-bindgen",
}

# pin (ref, is_branch) for crates whose tags are absent or whose newest tag
# would violate a parent requirement.
PIN = {
    "mini-moka": ("v0.10.3", False),
    "triomphe": ("v0.1.15", False),
    "dashmap": ("v5.5.2", False),
    "hashbrown": ("v0.14.5", False),
    "tagptr": ("v0.2.0", True),
    "smallvec": ("v1.15.1", False),
    "thiserror": ("1.0.69", False),
    "portable-atomic": ("v1.15.0", False),
    "parking_lot": ("parking_lot-v0.12.4", False),
    "lock_api": ("lock_api-v0.4.13", False),
    "parking_lot_core": ("parking_lot_core-v0.9.11", False),
}

GH = "https://api.github.com"
UA = {"User-Agent": "KCU-Launcher",
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Authorization": "token " + TOKEN}


def api(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def find_repo(pkg: str) -> str:
    if pkg in KNOWN:
        return KNOWN[pkg]
    q = urllib.parse.quote(f"{pkg} in:name language:rust")
    obj = api(f"{GH}/search/repositories?q={q}&per_page=5")
    items = obj.get("items", [])
    if not items:
        raise RuntimeError(f"no repo for {pkg}")
    for it in items:
        if it["name"].lower().replace("_", "-") == pkg.lower().replace("_", "-"):
            return it["full_name"]
    return items[0]["full_name"]


def tags(repo: str) -> list[str]:
    out = []
    for page in (1, 2, 3, 4):
        try:
            arr = api(f"{GH}/repos/{repo}/tags?per_page=100&page={page}")
        except Exception:
            break
        if not arr:
            break
        out += [t["name"] for t in arr]
        if len(arr) < 100:
            break
    return out


def semver(tag: str):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)$", tag)
    if not m:
        return None
    if re.search(r"(alpha|beta|rc|pre|dev)", tag, re.I):
        return None
    return tuple(int(x) for x in m.groups())


def compatible(v, want):
    if want is None:
        return True
    major, minor = want
    if major >= 1:
        return v[0] == major
    if major == 0:
        return v[0] == 0 and v[1] == minor
    return True


def ordered_tags(pkg: str, repo: str, want=None):
    scored = []
    for t in tags(repo):
        v = semver(t)
        if not v or not compatible(v, want):
            continue
        pref = 1 if t.lower().startswith(pkg.lower().replace("_", "-")) else 0
        scored.append((pref, v, t))
    scored.sort(reverse=True)
    return [t for _, _, t in scored]


def download(repo: str, ref: str, is_branch: bool = False) -> Path:
    key = re.sub(r"[^A-Za-z0-9._-]", "_", repo + "@" + ref)
    dst = CACHE / key
    arc = CACHE / (key + ".tgz")
    if dst.exists() and any(dst.rglob("Cargo.toml")):
        return dst
    kind = "heads" if is_branch else "tags"
    url = f"https://codeload.github.com/{repo}/tar.gz/refs/{kind}/{ref}"
    req = urllib.request.Request(url, headers={"User-Agent": "KCU-Launcher"})
    with urllib.request.urlopen(req, timeout=45) as r:
        arc.write_bytes(r.read())
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    subprocess.run(["tar", "-xzf", str(arc), "-C", str(dst), "--strip-components=1"],
                   check=True, timeout=120)
    return dst


def crate_dir(root: Path, pkg: str) -> Path | None:
    for p in sorted(root.rglob("Cargo.toml")):
        try:
            t = p.read_text(errors="ignore")
        except Exception:
            continue
        m = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"', t[:1500])
        if m and m.group(1) == pkg:
            return p.parent
    return None


def clean_manifest(t: str, version: str, pkg: str = "") -> str:
    t = re.sub(r"\n\[dev-dependencies\][\s\S]*?(?=\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"\n\[target\.[^\]]*\.dev-dependencies\][\s\S]*?(?=\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"\n\[target\.'cfg\(any\(\)\)'\.dependencies\][\s\S]*?(?=\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"\n\[\[(example|bench|test)\]\][\s\S]*?(?=\n\[\[|\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"\n\[workspace\][\s\S]*?(?=\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"\n\[lints[^\]]*\][\s\S]*?(?=\n\[[A-Za-z]|\Z)", "\n", t)
    t = re.sub(r"(?m)^\s*workspace\s*=\s*true\s*$", "", t)
    t = re.sub(r",\s*path\s*=\s*\"[^\"]*\"", "", t)
    t = re.sub(r"(?m)^version\.workspace\s*=\s*true\s*$", f'version = "{version}"', t)
    t = re.sub(r"(?m)^edition\.workspace\s*=\s*true\s*$", 'edition = "2021"', t)
    t = re.sub(r"(?m)^license\.workspace\s*=\s*true\s*$", 'license = "MIT OR Apache-2.0"', t)
    for k in ("repository", "authors", "rust-version", "homepage", "keywords",
              "categories", "readme", "description", "documentation", "exclude",
              "include"):
        t = re.sub(rf"(?m)^{k}\.workspace\s*=\s*true\s*$", "", t)
    # Drop sections that cannot activate on x86/i686/aarch64 Windows/Linux.
    out, skipping = [], False
    for ln in t.splitlines(keepends=True):
        st = ln.strip()
        if st.startswith("[") and not st.startswith("[["):
            skipping = (
                "wasm" in st
                or "moka_loom" in st
                or ".dev-dependencies" in st
                or "dev-dependencies." in st
                or "trybuild" in st
                or "skeptic" in st
                or st.startswith("[dev-dependencies")
                or st.startswith("[profile.")
                or st.startswith("[lints")
            )
        if st.startswith("[[") and any(x in st for x in ("example", "bench", "test")):
            skipping = True
        if not skipping:
            out.append(ln)
    t = "".join(out)
    if pkg == "hashbrown":
        # Only `inline-more` / `raw` are used by our parent (dashmap).
        # Drop optional deps that belong to nightly / allocator / serde features.
        t = re.sub(r"\n\[dependencies\][\s\S]*?(?=\n\[[A-Za-z]|\Z)",
                   "\n[dependencies]\n", t, count=1)
        t = re.sub(r"\n\[features\][\s\S]*?(?=\n\[[A-Za-z]|\Z)",
                   "\n[features]\ndefault = []\ninline-more = []\nraw = []\n", t, count=1)
    return t


def install(pkg: str, want=None, force: bool = False) -> bool:
    dst = VENDOR / pkg
    if (dst / "Cargo.toml").exists() and not force:
        print("SKIP", pkg, "already vendored", flush=True)
        return True
    try:
        repo = find_repo(pkg)
    except Exception as e:
        print("REPO_ERR", pkg, repr(e)[:140], flush=True)
        return False
    cands = []
    if pkg in PIN:
        ref, branch = PIN[pkg]
        cands = [(ref, branch)]
    else:
        cands = [(t, False) for t in ordered_tags(pkg, repo, want)]
        if not cands and want is None:
            cands = [(b, True) for b in ("master", "main")]
    if not cands:
        print("NO_TAG", pkg, repo, "want", want, flush=True)
        return False
    for ref, branch in cands[:14]:
        try:
            root = download(repo, ref, branch)
        except Exception as e:
            print("DL_ERR", pkg, repo, ref, repr(e)[:90], flush=True)
            continue
        cd = crate_dir(root, pkg)
        if cd is None:
            continue
        v = semver(ref)
        version = ".".join(map(str, v)) if v else "0.0.0"
        tmp = VENDOR / (".tmp-" + pkg)
        if tmp.exists():
            shutil.rmtree(tmp)
        shutil.move(str(cd), str(tmp))
        for junk in ("target", ".git", ".github", "tests", "benches", "examples", "fuzz"):
            j = tmp / junk
            if j.is_dir() and not j.is_symlink():
                shutil.rmtree(j, ignore_errors=True)
        # M05: mono-repo crates symlink build helpers to the repo root.
        parent = cd.parent
        for helper in ("no_atomic.rs", "build-common.rs"):
            h = tmp / helper
            if h.is_symlink() or (h.exists() and not h.is_file()):
                h.unlink()
            if (tmp / "build.rs").exists() and f'include!("{helper}")' in (tmp / "build.rs").read_text(errors="ignore"):
                src_h = parent / helper
                if src_h.exists() and not h.exists():
                    shutil.copy2(src_h, h)
        mp = tmp / "Cargo.toml"
        mp.write_text(clean_manifest(mp.read_text(), version, pkg))
        (tmp / ".cargo-checksum.json").write_text(json.dumps({"files": {}, "package": None}))
        if dst.exists():
            shutil.rmtree(dst)
        os.replace(tmp, dst)
        print("OK", pkg, version, repo, ref,
              "lib=", (dst / "src" / "lib.rs").exists(), flush=True)
        return True
    print("NO_MATCH", pkg, repo, "tried", len(cands[:14]), flush=True)
    return False


def cargo_build():
    env = dict(os.environ)
    env.update(CARGO_HOME="/data/workspace/.cargo-home",
               RUSTUP_HOME="/data/workspace/.rustup-home",
               CARGO_INCREMENTAL="0")
    env["PATH"] = "/data/workspace/.cargo-home/bin:" + env["PATH"]
    p = subprocess.run(["cargo", "build", "--offline"], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def main():
    VENDOR.mkdir(exist_ok=True)
    KEEP_025 = {"itoa", "memchr", "ryu", "serde_core", "serde_json"}
    for d in list(VENDOR.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith(".tmp-"):
            shutil.rmtree(d)
            continue
        if d.name not in KEEP_025 and not (d / "src" / "lib.rs").exists() \
                and not (d / "src" / "main.rs").exists():
            print("PURGE_INCOMPLETE", d.name, flush=True)
            shutil.rmtree(d)
    seen = set()
    log = []
    limit = int(os.environ.get("KCU_MAX_ITER", "45"))
    for i in range(limit):
        print("ITER", i, flush=True)
        rc, out = cargo_build()
        if rc == 0:
            print("BUILD_OK after", i, "iterations", flush=True)
            log.append("BUILD_OK")
            break
        miss = re.search(r"no matching package named `([^`]+)` found", out)
        mismatch = re.search(r'failed to select a version for the requirement `([^`=]+?)\s*=\s*"\^?(\d+)\.(\d+)', out)
        if miss:
            pkg, want, force = miss.group(1), None, False
        elif mismatch:
            pkg = mismatch.group(1).strip()
            want = (int(mismatch.group(2)), int(mismatch.group(3)))
            force = True
            if pkg in seen and (VENDOR / pkg / "Cargo.toml").exists():
                print("REPLACE_INCOMPATIBLE", pkg, want, flush=True)
        else:
            print("BUILD_FAIL_NON_MISSING", flush=True)
            print(out[-2200:], flush=True)
            log.append("BUILD_FAIL_NON_MISSING")
            break
        key = (pkg, want)
        if key in seen:
            print("STUCK", key, flush=True)
            log.append("STUCK " + str(key))
            break
        seen.add(key)
        log.append(f"MISSING {pkg} want={want}")
        ok = install(pkg, want, force)
        if not ok:
            log.append("FETCH_FAIL " + pkg)
            break
    else:
        log.append("ITER_LIMIT")
    with (ROOT / "docs" / "records" / "vendor-fetch-log.txt").open("a") as fh:
        fh.write("\n".join(log) + "\n")
    print("LOG", log, flush=True)


if __name__ == "__main__":
    main()
