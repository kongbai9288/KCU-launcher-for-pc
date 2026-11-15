from pathlib import Path
import io, json, re, shutil, tarfile, urllib.request, base64

ROOT = Path(__file__).resolve().parents[1]
REPO = 'tafia/quick-xml'
TAG = 'v0.38.4'


def tarball(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90
    ) as r:
        return r.read()


def api_license(path):
    # tarball 里已有 LICENSE 时直接复用，避免撞未认证 API 限流
    local = ROOT / 'vendor' / 'quick-xml' / path
    if local.exists():
        return local.read_bytes()
    tok = Path('/data/workspace/.kcu_pat').read_text().strip()
    url = f'https://api.github.com/repos/{REPO}/contents/{path}?ref={TAG}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'KCU-Launcher', 'Authorization': 'token ' + tok,
        'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        o = json.load(r)
    return base64.b64decode(o['content'])


def package_block(text):
    head = text.split('[package]', 1)[1]
    for line in head.splitlines():
        if line.startswith('[') and not line.startswith('[['):
            head = head.split('\n' + line, 1)[0]
            break
    return '[package]' + head.rstrip() + '\n'


def main():
    dst = ROOT / 'vendor' / 'quick-xml'
    if dst.exists():
        shutil.rmtree(dst)
    with tarfile.open(
        fileobj=io.BytesIO(tarball(f'https://codeload.github.com/{REPO}/tar.gz/refs/tags/{TAG}')),
        mode='r:gz',
    ) as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = m.name.split('/', 1)[1]
            if rel.startswith('src/') or rel in ('Cargo.toml', 'README.md', 'LICENSE-MIT.md'):
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tf.extractfile(m).read())
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))
    print('VENDOR', dst.name, len([x for x in dst.rglob('*') if x.is_file()]), 'files')

    p = dst / 'Cargo.toml'
    raw = p.read_text()
    # 上游唯一非 optional 依赖是 memchr 2.1（025 已在构建中 2.7.6）；
    # encoding_rs / serde / tokio 全 optional，连同 features / dev / benches / metadata / lib.bench 一起裁。
    trimmed = package_block(raw) + '''
[dependencies]
memchr = "2.7"

[features]
default = []
serialize = []
serde-types = []
encoding = []
async-tokio = []
overlapped-lists = []

[lints.rust]
unexpected_cfgs = { level = "allow" }
'''
    p.write_text(trimmed)
    print('SECTIONS', re.findall(r'^\[([^\]]+)\]', trimmed, re.M))

    lic = api_license('LICENSE-MIT.md')
    (dst / 'LICENSE-MIT.md').write_bytes(lic)
    (ROOT / 'docs' / 'licenses' / 'quick-xml-LICENSE-MIT.txt').write_bytes(lic)
    print('LICENSE', len(lic))

    c = ROOT / 'Cargo.toml'
    s = c.read_text()
    needle = 'uuid = { version = "1.18.1", default-features = false, features = ["std", "v5"] }\n'
    assert needle in s
    if 'quick-xml = ' not in s:
        c.write_text(s.replace(needle, needle + 'quick-xml = { version = "0.38.4", default-features = false }\n', 1))
    print('CARGO_OK')
    print('VENDOR044_OK')


main()
