from pathlib import Path
import base64, io, json, re, shutil, tarfile, urllib.request

ROOT = Path(__file__).resolve().parents[1]
TOK = Path('/data/workspace/.kcu_pat').read_text().strip()
H = {'User-Agent': 'KCU-Launcher', 'Accept': 'application/vnd.github+json',
     'X-GitHub-Api-Version': '2022-11-28', 'Authorization': 'token ' + TOK}


def tarball(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90) as r:
        return r.read()


def gh_file(repo, ref, path):
    u = f'https://api.github.com/repos/{repo}/contents/{path}?ref={ref}'
    with urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=45) as r:
        o = json.load(r)
    return base64.b64decode(o['content'])


def checksum(dst):
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))


def trim(text, sections):
    for sec in sections:
        text = re.sub(r'\n\[' + re.escape(sec) + r'\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    return text


# --- libloading 0.8.9 ---
b = tarball('https://codeload.github.com/nagisa/rust_libloading/tar.gz/refs/tags/0.8.9')
d = ROOT / 'vendor' / 'libloading'
if d.exists(): shutil.rmtree(d)
with tarfile.open(fileobj=io.BytesIO(b), mode='r:gz') as tf:
    for m in tf.getmembers():
        if not m.isfile():
            continue
        rel = m.name.split('/', 1)[1]
        if rel.startswith('src/') or rel in ('Cargo.toml', 'LICENSE', 'README.mkd'):
            out = d / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(tf.extractfile(m).read())
p = d / 'Cargo.toml'
t = trim(p.read_text(), ["target.'cfg(windows)'.dev-dependencies.windows-sys", 'dev-dependencies'])
p.write_text(t)
print('LIBLOADING', sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_file()))
checksum(d)

# --- cfg-if 1.0.5 ---
b = tarball('https://codeload.github.com/alexcrichton/cfg-if/tar.gz/refs/tags/v1.0.5')
d = ROOT / 'vendor' / 'cfg-if'
if d.exists(): shutil.rmtree(d)
with tarfile.open(fileobj=io.BytesIO(b), mode='r:gz') as tf:
    for m in tf.getmembers():
        if not m.isfile():
            continue
        rel = m.name.split('/', 1)[1]
        if rel.startswith('src/') or rel in ('Cargo.toml', 'LICENSE-MIT', 'LICENSE-APACHE', 'README.md'):
            out = d / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(tf.extractfile(m).read())
p = d / 'Cargo.toml'
t = trim(p.read_text(), ['dependencies', 'features'])
p.write_text(t)
print('CFG_IF', sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_file()))
checksum(d)

# --- windows-link 0.2.1 @ ec79074f76aa ---
REF = 'ec79074f76aa'
REPO = 'microsoft/windows-rs'
BASE = 'crates/libs/link/'
d = ROOT / 'vendor' / 'windows-link'
if d.exists(): shutil.rmtree(d)
for src, dst in [('Cargo.toml', 'Cargo.toml'), ('src/lib.rs', 'src/lib.rs'),
                 ('readme.md', 'readme.md'), ('license-mit', 'license-mit'),
                 ('license-apache-2.0', 'license-apache-2.0')]:
    out = d / dst
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(gh_file(REPO, REF, BASE + src))
p = d / 'Cargo.toml'
t = p.read_text()
t = trim(t, ['lints'])
t = t.replace('\n[package]\n', '\n[package]\nreadme = "readme.md"\n', 1)
p.write_text(t)
print('WINDOWS_LINK', sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_file()))
print('WL_VERSION', [l for l in t.splitlines() if l.startswith('version')])
checksum(d)

# --- LICENSE 全文 ---
L = ROOT / 'docs' / 'licenses'
copies = [
    ('vendor/libloading/LICENSE', 'libloading-LICENSE.txt'),
    ('vendor/cfg-if/LICENSE-MIT', 'cfg-if-LICENSE-MIT.txt'),
    ('vendor/cfg-if/LICENSE-APACHE', 'cfg-if-LICENSE-APACHE.txt'),
    ('vendor/windows-link/license-mit', 'windows-link-LICENSE-MIT.txt'),
    ('vendor/windows-link/license-apache-2.0', 'windows-link-LICENSE-APACHE.txt'),
]
for src, dst in copies:
    shutil.copy2(ROOT / src, L / dst)
    print('LICENSE', dst, (L / dst).stat().st_size)

# --- Cargo.toml ---
c = ROOT / 'Cargo.toml'
s = c.read_text()
needle = 'ed25519-compact = { version = "2.6.1", default-features = false, features = ["std"] }\n'
assert needle in s
if 'libloading' not in s:
    s = s.replace(needle, needle + 'libloading = "0.8.9"\n', 1)
    c.write_text(s)
print('CARGO_OK')
print('VENDOR038_OK')
