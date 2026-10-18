import hashlib, json, re, subprocess, sys
from pathlib import Path
root=Path('/workspace/worker')
paths=['target/verification-protocol.md','surface-contract.json','checks/check_contract.py','observation-policy.json']
for rel in paths:
    raw=(root/rel).read_bytes()
    print('SNAPSHOT',rel,'sha256='+hashlib.sha256(raw).hexdigest())
    for n,line in enumerate(raw.decode().splitlines(),1):
        print(f'{rel}:{n}: {line}')
protocol=(root/paths[0]).read_text()
contract=json.loads((root/paths[1]).read_text())
policy=json.loads((root/paths[3]).read_text())
steps=[(int(m[1]),m[2]) for line in protocol.splitlines() if (m:=re.fullmatch(r'(\d+)\. (.*)',line))]
transitions={t['id']:t for t in contract['transitions']}
print('\nBATCH 1: C-1 actual document action versus required action')
back=[(n,s) for n,s in steps if 'Back' in s]
print('INPUT actual Back instructions:',json.dumps(back))
print('EXPECTED transition:',json.dumps(transitions['back'],sort_keys=True))
assert len(back)==1 and back[0][1].startswith('Click Back,')
assert transitions['back']['traversal']=='Tab' and transitions['back']['activation']=='Enter'
print('ACTUAL MISMATCH: sole Back instruction prescribes Click; required Back instruction prescribes sequential Tab and Enter.')
print('REFUTATION SEARCH: all keyboard/focus instructions:',json.dumps([(n,s) for n,s in steps if re.search(r'Tab|Enter|focus|keyboard',s,re.I)]))
print('CONTRARY EVIDENCE: step 4 explicitly uses Tab/Shift+Tab and Enter for Close; step 6 explicitly asserts final heading focus. These satisfy different controls/properties and do not prescribe traversal or activation for Back.')
print('\nBATCH 2: C-2 actual ordered help route versus required ordered help route')
help_steps=[(n,s) for n,s in steps if re.search(r'help|summary|Close',s)]
print('INPUT actual help instructions:',json.dumps(help_steps))
print('EXPECTED help route:',json.dumps([transitions[k] for k in ['open-help','toggle-help','reopen-help','close-help']],sort_keys=True))
space_steps=[(n,s) for n,s in steps if re.search(r'\bSpace\b',s)]
reopen_steps=[(n,s) for n,s in steps if re.search(r'reopen|re-open|open.*again|again.*open',s,re.I)]
print('ACTUAL Space instructions:',json.dumps(space_steps))
print('ACTUAL reopen instructions:',json.dumps(reopen_steps))
assert not space_steps and not reopen_steps
assert steps[2][1]=='Open help using its summary control.'
assert steps[3][1].startswith('Reach Close with Tab or Shift+Tab, activate with Enter,')
print('ACTUAL MISMATCH: help is opened once, then closed by Close; no instruction toggles the summary with Space or reopens help after closure.')
print('REFUTATION SEARCH: entire six-step procedure printed above; no loops or cross-references extend the route.')
print('CONTRARY EVIDENCE: opening via summary and asserting closure via Close do exercise opening and closure, but not the separately required toggle-help and reopen-help transitions.')
print('\nBATCH 3: C-3 policy preconditions and observations')
print('EXPECTED method restriction:',json.dumps(contract['scope']['allowed_methods']))
print('EXPECTED origin restriction:',json.dumps(policy['allowed_origins']))
print('EXPECTED required checks:',json.dumps(contract['required_checks']))
print('EXPECTED analytics condition:',json.dumps(contract['limits'][2]))
policy_terms=re.compile(r'\b(?:GET|HEAD|OPTIONS|POST)\b|origin|allowlist|intercept|request|block|analytics|read.only|policy|restrict',re.I)
policy_lines=[(n,line) for n,line in enumerate(protocol.splitlines(),1) if policy_terms.search(line)]
print('ACTUAL policy-related lines anywhere in target:',json.dumps(policy_lines))
assert not policy_lines
print('ACTUAL first instruction:',json.dumps(steps[0]))
print('ACTUAL DOCUMENT OMISSION: no method/origin restriction setup or validation and no blocked analytics observation instructions.')
print('REFUTATION SEARCH: target contains no external setup reference or precondition. However, the provided sources do not establish whether the eventual runner has an independent preconfigured request guard. No browser ran, so actual emitted/blocked requests remain unobserved.')
print('CONTRARY EVIDENCE: contract and observation-policy declare constraints; they may be consumed by an external runner. The contract checker only checks declarations, never contacts the website, and does not enforce browser restrictions.')
print('\nACTUAL existing contract checker invocation:')
cmd=[sys.executable,'-B',str(root/'checks/check_contract.py'),str(root/'surface-contract.json')]
result=subprocess.run(cmd,capture_output=True,text=True)
print('COMMAND',json.dumps(cmd))
print('STDOUT BEGIN'); print(result.stdout,end=''); print('STDOUT END')
print('STDERR BEGIN'); print(result.stderr,end=''); print('STDERR END')
print('EXIT',result.returncode)
assert result.returncode==0
print('LIMIT: all observations above are offline source/document checks. No website behavior was observed; no modeled browser was executed.')
