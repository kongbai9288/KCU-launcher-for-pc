from pathlib import Path
import io, json, re, shutil, tarfile, urllib.request

ROOT = Path(__file__).resolve().parents[1]


def tarball(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'}), timeout=90
    ) as r:
        return r.read()


def trim(text, drop_sections, drop_lines):
    for name in drop_sections:
        text = re.sub(r'\n\[' + re.escape(name) + r'\][\s\S]*?(?=\n\[|\Z)', '\n', text)
    for pat in drop_lines:
        text = re.sub(pat, '', text, flags=re.M)
    return text


def unpack(repo, tag, prefix, dst, keep_root):
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
            src_rel = rel[len(prefix):] if prefix and rel.startswith(prefix) else rel
            if prefix and rel.startswith(prefix):
                pass
            elif prefix:
                continue
            if src_rel.startswith('src/') or src_rel in keep_root or src_rel.startswith('LICENSE'):
                out = dst / src_rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tf.extractfile(m).read())
            elif not prefix and (rel in keep_root or rel.startswith('LICENSE')):
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tf.extractfile(m).read())
            elif prefix and rel in ('LICENSE-APACHE', 'LICENSE-MIT'):
                # mono-repo 子 crate 的 LICENSE 常是软链；tarball 里 m.isfile() 为 False，
                # 用仓库根的同名文件兜底（内容一致）。
                out = dst / rel
                out.write_bytes(tf.extractfile(m).read())
    (dst / '.cargo-checksum.json').write_text(json.dumps({'files': {}, 'package': None}))
    print('VENDOR', dst.name, sorted(str(x.relative_to(dst)) for x in dst.rglob('*') if x.is_file()))


def main():
    # percent-encoding 2.3.1：rust-url mono-repo 的 percent_encoding 子 crate
    pe = ROOT / 'vendor' / 'percent-encoding'
    unpack('servo/rust-url', 'v2.5.0', 'percent_encoding/', pe,
           {'Cargo.toml', 'README.md', 'LICENSE-MIT', 'LICENSE-APACHE'})
    p = pe / 'Cargo.toml'
    p.write_text(trim(p.read_text(), ['package.metadata.docs.rs'], []))
    print('PE_SECTIONS', re.findall(r'^\[([^\]]+)\]', p.read_text(), re.M))

    # hex 0.4.3：裁 optional serde、dev-dependencies、benches、docs.rs metadata
    hx = ROOT / 'vendor' / 'hex'
    unpack('KokaKiwi/rust-hex', 'v0.4.3', '', hx,
           {'Cargo.toml', 'README.md', 'LICENSE-MIT', 'LICENSE-APACHE'})
    p = hx / 'Cargo.toml'
    p.write_text(trim(
        p.read_text(),
        ['dev-dependencies', 'package.metadata.docs.rs', 'dependencies.serde', 'badges'],
        [r'^serde\s*=.*\n', r'^\[\[bench\]\][\s\S]*?(?=\n\[|\Z)'],
    ))
    # [[bench]] 是双括号段，单独裁
    t = p.read_text()
    t = re.sub(r'\n\[\[bench\]\][\s\S]*?(?=\n\[|\Z)', '\n', t)
    p.write_text(t)
    # optional serde feature 未启用，其源文件与空 [dependencies] 段一并裁掉
    serde_src = hx / 'src' / 'serde.rs'
    if serde_src.exists():
        serde_src.unlink()
    print('HEX_SECTIONS', re.findall(r'^\[([^\]]+)\]', p.read_text(), re.M))

    import base64
    import urllib.request

    def api_license(repo, tag, path):
        url = f'https://api.github.com/repos/{repo}/contents/{path}?ref={tag}'
        req = urllib.request.Request(url, headers={'User-Agent': 'KCU-Launcher'})
        with urllib.request.urlopen(req, timeout=30) as r:
            o = json.load(r)
        return base64.b64decode(o['content'])

    lic = ROOT / 'docs' / 'licenses'
    for src, name, repo, tag, path in [
        (pe / 'LICENSE-MIT', 'pe-LICENSE-MIT.txt', 'servo/rust-url', 'v2.5.0', 'LICENSE-MIT'),
        (pe / 'LICENSE-APACHE', 'pe-LICENSE-APACHE.txt', 'servo/rust-url', 'v2.5.0', 'LICENSE-APACHE'),
        (hx / 'LICENSE-MIT', 'hex-LICENSE-MIT.txt', 'KokaKiwi/rust-hex', 'v0.4.3', 'LICENSE-MIT'),
        (hx / 'LICENSE-APACHE', 'hex-LICENSE-APACHE.txt', 'KokaKiwi/rust-hex', 'v0.4.3', 'LICENSE-APACHE'),
    ]:
        content = src.read_bytes() if src.exists() else api_license(repo, tag, path)
        if not src.exists():
            src.write_bytes(content)
        (lic / name).write_bytes(content)
        print('LICENSE', name, (lic / name).stat().st_size)

    c = ROOT / 'Cargo.toml'
    s = c.read_text()
    needle = 'raw-window-handle = "0.6.2"\n'
    assert needle in s
    add = ''
    if 'percent-encoding = ' not in s:
        add += 'percent-encoding = "2.3.1"\n'
    if 'hex = ' not in s:
        add += 'hex = "0.4.3"\n'
    if add:
        c.write_text(s.replace(needle, needle + add, 1))
    print('CARGO_OK')
    print('VENDOR042_OK')


main()
