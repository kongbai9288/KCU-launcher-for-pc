from pathlib import Path
import io, json, re, shutil, tarfile, urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = 'rust-windowing/raw-window-handle'
TAG = 'v0.6.2'


def tarball(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90
    ) as r:
        return r.read()


def trim(text):
    # dev-dependencies / docs.rs metadata / 引用了可选 wasm-bindgen 的 feature 行与 target 段
    text = re.sub(r"\n\[dev-dependencies\][\s\S]*?(?=\n\[|\Z)", '\n', text)
    text = re.sub(r"\n\[package\.metadata\.docs\.rs\][\s\S]*?(?=\n\[|\Z)", '\n', text)
    text = re.sub(r"\n\[target\.'cfg\(target_family = \"wasm\"\)'\.dependencies\.wasm-bindgen\][\s\S]*?(?=\n\[|\Z)", '\n', text)
    text = re.sub(r'^wasm-bindgen-0-2\s*=\s*\[.*\]\n', '', text, flags=re.M)
    return text


def main():
    dst = ROOT / 'vendor' / 'raw-window-handle'
    if dst.exists():
        shutil.rmtree(dst)
    keep = {'Cargo.toml', 'README.md', 'LICENSE-MIT.md', 'LICENSE-APACHE.md', 'LICENSE-ZLIB.md'}
    with tarfile.open(
        fileobj=io.BytesIO(tarball(f'https://codeload.github.com/{REPO}/tar.gz/refs/tags/{TAG}')),
        mode='r:gz',
    ) as tf:
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
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))
    print('VENDOR', dst.name, sorted(str(x.relative_to(dst)) for x in dst.rglob('*') if x.is_file()))
    print('MANIFEST_SECTIONS', re.findall(r'^\[([^\]]+)\]', (dst / 'Cargo.toml').read_text(), re.M))

    lic = ROOT / 'docs' / 'licenses'
    for src, name in [('LICENSE-MIT.md', 'rwh-LICENSE-MIT.md'),
                      ('LICENSE-APACHE.md', 'rwh-LICENSE-APACHE.md'),
                      ('LICENSE-ZLIB.md', 'rwh-LICENSE-ZLIB.md')]:
        (lic / name).write_bytes((dst / src).read_bytes())
        print('LICENSE', name, (lic / name).stat().st_size)

    c = ROOT / 'Cargo.toml'
    s = c.read_text()
    needle = 'http = "1.3.1"\n'
    assert needle in s
    if 'raw-window-handle = ' not in s:
        c.write_text(s.replace(needle, needle + 'raw-window-handle = "0.6.2"\n', 1))
    print('CARGO_OK')
    print('VENDOR041_OK')


main()
