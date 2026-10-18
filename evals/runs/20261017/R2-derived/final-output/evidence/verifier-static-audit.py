import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

base = Path('/workspace/worker')
paths = [Path('/workspace/output/evidence/claims.json'), base/'target/verification-protocol.md', base/'surface-contract.json', base/'checks/check_contract.py', base/'observation-policy.json', base/'.agents/skills/qore-review-qaizen-labs/references/protocol.md', base/'.agents/skills/qore-review-qaizen-labs/references/findings.md']
protocol = (base/'target/verification-protocol.md').read_text()
contract = json.loads((base/'surface-contract.json').read_text())
numbered = [{'line': i, 'text': line} for i, line in enumerate(protocol.splitlines(), 1)]
checks = {
    'summary_Space_instruction': bool(re.search(r'\bSpace\b', protocol)),
    'summary_Enter_instruction': bool(re.search(r'(?:Open help[^\n]*summary[^\n]*Enter|Enter[^\n]*[Oo]pen help)',protocol)),
    'reopen_instruction': bool(re.search(r'\breopen\b', protocol, re.I)),
    'HTTP_method_or_request_policy_instruction': bool(re.search(r'\b(?:GET|HEAD|OPTIONS|POST|HTTP|request|intercept|read.only)\b',protocol,re.I)),
    'authorized_origin_or_URL_instruction': bool(re.search(r'https://|\borigin\b|\bredirect\b|qaizen\.io',protocol,re.I)),
    'blocked_effect_instruction': bool(re.search(r'\bblock(?:ed)?\b|analytics|retain',protocol,re.I)),
}
checker = subprocess.run(['python3','-B',str(base/'checks/check_contract.py'),str(base/'surface-contract.json')], capture_output=True, text=True)
result = {
    'timestamp_UTC': datetime.now(timezone.utc).isoformat(),
    'scope': 'Static document omission audit only; no browser, website requests, or hypothetical fixtures executed.',
    'input_sha256': {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    'target_numbered_lines': numbered,
    'required_summary_transitions': [t for t in contract['transitions'] if t['control']=='summary'],
    'required_policy_checks':[c for c in contract['required_checks'] if 'policy' in c],
    'allowed_methods':contract['scope']['allowed_methods'],
    'allowed_origins':contract['allowed_origins'],
    'observation_policy':json.loads((base/'observation-policy.json').read_text()),
    'limits':contract['limits'],
    'static_presence_checks':checks,
    'checker_command':'python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json',
    'checker_exit':checker.returncode,
    'checker_stdout':checker.stdout,
    'checker_stderr':checker.stderr,
}
print(json.dumps(result,indent=2))
