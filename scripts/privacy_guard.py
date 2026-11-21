#!/usr/bin/env python3
"""064：隐私政策逐字副本、版本一致、同意闸门与注册表弹窗绑定。"""
from pathlib import Path
import hashlib, re, sys

ROOT = Path(__file__).resolve().parents[1]
EXPECT = 'de3b07c70f6747ae220db8e67c6168eed0b35e992c80334581b154cd80a3e8b8'

def fail(reason):
    print('PRIVACY_GUARD_FAIL reason=' + reason)
    sys.exit(1)

spec = ROOT / 'docs/spec/64-privacy-policy-v1.1.txt'
if not spec.is_file():
    fail('policy_missing')
policy = spec.read_bytes()
if hashlib.sha256(policy).hexdigest() != EXPECT:
    fail('policy_not_verbatim')
text = policy.decode('utf-8')
if '版本： v1.1' not in text or '生效日期： 2026年11月21日' not in text:
    fail('version_or_date_mismatch')

c = (ROOT / 'src/core/consent.rs').read_text()
if 'include_str!("../../docs/spec/64-privacy-policy-v1.1.txt")' not in c:
    fail('text_not_included_from_spec')
if 'POLICY_VERSION: &str = "v1.1"' not in c:
    fail('version_constant_mismatch')
if 'POLICY_EFFECTIVE: &str = "2026-11-21"' not in c:
    fail('effective_constant_mismatch')
if 'POPUP_ID: &str = "privacy"' not in c:
    fail('popup_id_mismatch')
if 'ConsentAction::Decline' not in c or 'CloseAction::Timeout' not in c:
    fail('timeout_not_declined')

popup = (ROOT / 'src/core/popup.rs').read_text()
ids = set(re.findall(r'id:\s*"([^"]+)"', popup))
if 'privacy' not in ids:
    fail('privacy_popup_not_registered')

for p in (ROOT / 'src').rglob('*.rs'):
    if '《KCU Launcher 隐私政策》' in p.read_text():
        fail('policy_text_duplicated_in_src ' + str(p.relative_to(ROOT)))

ux = ROOT / 'demos/ui-full-kcu-paper.html'
if '《KCU Launcher 隐私政策》' in ux.read_text():
    fail('policy_text_hardcoded_in_ux')

print('PRIVACY_GUARD_OK verbatim policy=v1.1 effective=2026-11-21 popup=privacy')
