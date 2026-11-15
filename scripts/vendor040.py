from pathlib import Path
import io, json, re, shutil, tarfile, urllib.request

ROOT = Path(__file__).resolve().parents[1]


def tarball(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90
    ) as r:
        return r.read()


def checksum(dst):
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))


def trim(text):
    # dev-dependencies (含 target.'cfg(...)'.dev-dependencies) 一律裁掉
    text = re.sub(r'\n\[[^\]]*dev-dependencies[^\]]*\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    # 脱离上游 workspace 后，引用 workspace 属性的段无法解析
    text = re.sub(r'\n\[workspace\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    text = re.sub(r'\n\[lints[^\]]*\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    text = re.sub(r'\n\[package\.metadata\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    return text


def extract(url, dst, keep):
    if dst.exists():
        shutil.rmtree(dst)
    with tarfile.open(fileobj=io.BytesIO(tarball(url)), mode='r:gz') as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = m.name.split('/', 1)[1]
            if rel.startswith('src/') or rel in keep:
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tf.extractfile(m).read())
    p = dst / 'Cargo.toml'
    p.write_text(trim(p.read_text()))
    print('VENDOR', dst.name, sorted(str(x.relative_to(dst)) for x in dst.rglob('*') if x.is_file()))
    checksum(dst)


extract(
    'https://codeload.github.com/hyperium/http/tar.gz/refs/tags/v1.3.1',
    ROOT / 'vendor' / 'http',
    {'Cargo.toml', 'LICENSE-MIT', 'LICENSE-APACHE', 'README.md'},
)

extract(
    'https://codeload.github.com/tokio-rs/bytes/tar.gz/refs/tags/v1.11.1',
    ROOT / 'vendor' / 'bytes',
    {'Cargo.toml', 'LICENSE', 'README.md'},
)

extract(
    'https://codeload.github.com/servo/rust-fnv/tar.gz/refs/tags/v1.0.7',
    ROOT / 'vendor' / 'fnv',
    {'Cargo.toml', 'LICENSE-MIT', 'LICENSE-APACHE', 'README.md', 'lib.rs'},
)

c = ROOT / 'Cargo.toml'
s = c.read_text()
needle = 'libloading = "0.8.9"\n'
assert needle in s
if 'http = ' not in s:
    c.write_text(s.replace(needle, needle + 'http = "1.3.1"\n', 1))
print('CARGO_OK')
print('VENDOR040_OK')
