from pathlib import Path
import io, json, tarfile, urllib.request, shutil

ROOT = Path(__file__).resolve().parents[1]


def tarball(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90
    ) as r:
        return r.read()


def api_license(repo, tag, path):
    import base64
    url = f'https://api.github.com/repos/{repo}/contents/{path}?ref={tag}'
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=30
    ) as r:
        o = json.load(r)
    return base64.b64decode(o['content'])


def unpack(repo, tag, dst, src_prefix='', extra_root=()):
    if dst.exists():
        shutil.rmtree(dst)
    with tarfile.open(
        fileobj=io.BytesIO(tarball(f'https://codeload.github.com/{repo}/tar.gz/refs/tags/{tag}')),
        mode='r:gz',
    ) as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = m.name.split('/', 1)[1]
            if rel.startswith('src/') or rel in extra_root or rel.startswith('LICENSE'):
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tf.extractfile(m).read())
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))
    print('VENDOR', dst.name, len(list(dst.rglob('*'))), 'files')


def package_block(text):
    """保留上游 [package] 段原文，其余段落按 043 明裁剪。"""
    head = text.split('[package]', 1)[1]
    # 下一个顶层 [xxx] 段开始处截断（数组元素不以行首 [ 开头）
    for line in head.splitlines():
        if line.startswith('[') and not line.startswith('[['):
            head = head.split('\n' + line, 1)[0]
            break
    return '[package]' + head.rstrip() + '\n'


def main():
    # uuid 1.18.1：v5 只需 sha1_smol；其余 optional 依赖 / target 段 / dev / workspace 全裁
    ud = ROOT / 'vendor' / 'uuid'
    unpack('uuid-rs/uuid', 'v1.18.1', ud,
           extra_root=('Cargo.toml', 'README.md'))
    up = ud / 'Cargo.toml'
    raw = up.read_text()
    trimmed = package_block(raw) + '''
[features]
default = ["std"]
std = []
v5 = ["sha1"]
sha1 = ["dep:sha1_smol"]

[dependencies.sha1_smol]
version = "1"
default-features = false
optional = true
'''
    up.write_text(trimmed)
    print('UUID_SECTIONS', ['package', 'features', 'dependencies.sha1_smol'])

    # sha1_smol 1.0.1：BSD-3-Clause / minimal dependency-free；裁 optional serde 与 dev
    sh = ROOT / 'vendor' / 'sha1_smol'
    unpack('mitsuhiko/sha1-smol', '1.0.1', sh,
           extra_root=('Cargo.toml', 'README.md', 'AUTHORS'))
    sp = sh / 'Cargo.toml'
    raw = sp.read_text()
    sp.write_text(package_block(raw) + '''
[features]
std = ["alloc"]
alloc = []
''')
    print('SHA1_SECTIONS', ['package', 'features'])

    # 4 份许可证全文（uuid 双许可 + sha1_smol BSD-3-Clause）
    lic = ROOT / 'docs' / 'licenses'
    for name, repo, tag, path in [
        ('uuid-LICENSE-APACHE.txt', 'uuid-rs/uuid', 'v1.18.1', 'LICENSE-APACHE'),
        ('uuid-LICENSE-MIT.txt', 'uuid-rs/uuid', 'v1.18.1', 'LICENSE-MIT'),
        ('sha1_smol-LICENSE.txt', 'mitsuhiko/sha1-smol', '1.0.1', 'LICENSE'),
    ]:
        content = api_license(repo, tag, path)
        (lic / name).write_bytes(content)
        src = (ud / path) if repo.endswith('uuid') else (sh / path)
        src.write_bytes(content)
        print('LICENSE', name, len(content))

    c = ROOT / 'Cargo.toml'
    s = c.read_text()
    needle = 'hex = "0.4.3"\n'
    assert needle in s
    if 'uuid = ' not in s:
        c.write_text(s.replace(
            needle,
            needle + 'uuid = { version = "1.18.1", default-features = false, features = ["std", "v5"] }\n',
            1,
        ))
    print('CARGO_OK')
    print('VENDOR043_OK')


main()
