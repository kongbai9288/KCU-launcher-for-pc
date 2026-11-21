#!/usr/bin/env python3
"""064：客户端 AI 只有一个内部口子，无监听、无页面、无凭据、默认拒绝。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ['TcpListener', 'bind(', '127.0.0.1', '/mcp', 'Token', 'token',
             'Codex', 'Cursor', 'McpSettings', 'screenshot', 'http://', 'https://']

def fail(reason):
    print('AI_GATE_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/client_ai.rs'
t = f.read_text()
for k in FORBIDDEN:
    if k in t:
        fail('gate_contains ' + k)
submit = re.search(r'pub fn submit\([^)]*\)[^{]*\{(.*?)\n    \}', t, re.S)
if not submit or 'Err(ClientAiError::NotEnabled)' not in submit.group(1):
    fail('not_deny_by_default')
if 'pub fn enabled(&self) -> bool {\n        false' not in t:
    fail('gate_not_disabled')
if t.count('pub struct ClientAiGate') != 1:
    fail('port_count')

api = (ROOT / 'src/api.rs').read_text()
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
ai = [l for l in lines if 'client_ai' in l]
if len(ai) != 1 or 'ClientAiGate' not in ai[0]:
    fail('v1_port_count=' + str(len(ai)))
if len(lines) != 4:
    fail('v1_use_lines=' + str(len(lines)))

for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file():
        s = p.read_text()
        for key in ['client_ai', 'ai_provider', 'mcp_settings', 'mcp_server']:
            if key in s:
                fail('ui_surface ' + rel + ':' + key)

for p in (ROOT / 'src').rglob('*.rs'):
    if p.name == 'client_ai.rs':
        continue
    s = p.read_text()
    if 'ClientAiGate' in s and p.name != 'api.rs':
        fail('gate_referenced_outside_api ' + str(p.relative_to(ROOT)))

print('AI_GATE_OK port=1 no_listener no_ui no_token deny_by_default')
