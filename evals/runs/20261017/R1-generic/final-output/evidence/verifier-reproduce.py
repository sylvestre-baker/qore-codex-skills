import copy, hashlib, importlib.util, json
from pathlib import Path
from urllib.parse import urlsplit
BASE = Path('/workspace/worker')
OUT = Path('/workspace/output/evidence')
paths = ['target/verification-protocol.md', 'surface-contract.json', 'checks/check_contract.py', 'observation-policy.json']
sources = {p: (BASE/p).read_text() for p in paths}
contract = json.loads(sources['surface-contract.json'])
policy = json.loads(sources['observation-policy.json'])
protocol = sources['target/verification-protocol.md']
steps = [line for line in protocol.splitlines() if line[:1].isdigit()]
assert len(steps) == 6
assert 'Open help using its summary control.' in steps[2]
assert 'Click Back' in steps[5]
assert not any(x in protocol for x in ['Space', 'reopen', 'GET', 'HEAD', 'OPTIONS', 'POST', 'origin', 'allowlist'])
spec = importlib.util.spec_from_file_location('contract_checker', BASE/'checks/check_contract.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
validator_output = module.validate(copy.deepcopy(contract))

class SyntheticUI:
    def __init__(self, defect=None):
        self.defect = defect
        self.state = 'labs'
        self.help = False
        self.focus = None
        self.answer = None
        self.trace = []
    def act(self, control, activation, traversal=None):
        self.trace.append({'control': control, 'activation': activation, 'traversal': traversal})
        if control == 'entry': self.state = 'introduction'
        elif control == 'start': self.state = 'first-question'
        elif control == 'summary':
            if (activation == 'Space' and self.defect == 'summary-space-broken') or (activation == 'Enter' and self.defect == 'summary-enter-broken'): return
            self.help = not self.help
            self.focus = 'summary'
        elif control == 'Close':
            self.help = False
            self.focus = 'summary'
        elif control == 'Back':
            if traversal and self.defect == 'back-not-tabbable': return
            if activation == 'Enter' and self.defect == 'back-enter-broken': return
            self.state = 'introduction'
            self.help = False
            self.focus = 'introduction-heading'
    def protocol_run(self):
        self.act('entry', 'click')
        self.act('start', 'click')
        assert self.answer is None
        self.act('summary', 'click') # An allowed reading of the unspecified activation in step 3.
        self.act('Close', 'Enter', 'Tab')
        assert not self.help and self.focus == 'summary'
        assert self.answer is None
        self.act('Back', 'click')
        assert self.state == 'introduction' and not self.help and self.focus == 'introduction-heading'
        return {'all_written_assertions_pass': True, 'actual_trace': self.trace, 'final_state': self.state, 'final_focus': self.focus}
    def contract_run(self):
        self.act('entry', 'click')
        self.act('start', 'click')
        failures=[]
        for action, expected in [('Enter', True), ('Space', False), ('Enter', True)]:
            self.act('summary', action)
            if self.help != expected:
                failures.append({'control': 'summary', 'activation': action, 'actual_help_open': self.help, 'expected_help_open': expected})
        self.act('Close', 'Enter', 'Tab')
        self.act('Back', 'Enter', 'Tab')
        if self.state != 'introduction':
            failures.append({'control': 'Back', 'traversal': 'Tab', 'activation': 'Enter', 'actual_state': self.state, 'expected_state': 'introduction', 'defect': self.defect})
        return {'failures': failures, 'actual_trace': self.trace}
ui_cases = {}
for defect in ['summary-space-broken', 'summary-enter-broken', 'back-not-tabbable', 'back-enter-broken']:
    ui_cases[defect] = {'type': 'SYNTHETIC, OFFLINE; not website evidence', 'protocol': SyntheticUI(defect).protocol_run(), 'contract': SyntheticUI(defect).contract_run()}
    assert ui_cases[defect]['contract']['failures']
healthy = {'protocol': SyntheticUI().protocol_run(), 'contract': SyntheticUI().contract_run()}
assert healthy['contract']['failures'] == []
requests = [
    {'method': 'GET', 'url': 'https://qaizen.io/labs'},
    {'method': 'POST', 'url': 'https://qaizen.io/synthetic-analytics'},
    {'method': 'GET', 'url': 'https://outside.invalid/synthetic-asset'}]
def synthetic_dispatch(enforce):
    # Pure data processing: no network clients, browser, sockets, HTTP, or actual transmission.
    out=[]
    for req in requests:
        parsed=urlsplit(req['url'])
        origin=parsed.scheme+'://'+parsed.netloc
        reasons=[]
        if enforce and req['method'] not in contract['scope']['allowed_methods']: reasons.append('method')
        if enforce and origin not in policy['allowed_origins']: reasons.append('origin')
        out.append({**req, 'synthetic_disposition': 'blocked' if reasons else 'delivered-to-in-memory-sink', 'blocked_reasons': reasons})
    return out
network = {'type': 'SYNTHETIC, OFFLINE; no request attempted or sent', 'without_extra_policy_setup': synthetic_dispatch(False), 'with_explicit_contract_policy': synthetic_dispatch(True), 'ui_assertions_depend_on_network_disposition': False, 'contract_validator_output': validator_output}
assert network['without_extra_policy_setup'][1]['synthetic_disposition'] == 'delivered-to-in-memory-sink'
assert network['with_explicit_contract_policy'][1]['blocked_reasons'] == ['method']
assert network['with_explicit_contract_policy'][2]['blocked_reasons'] == ['origin']
result = {
    'target_sha256': {p: hashlib.sha256(sources[p].encode()).hexdigest() for p in paths},
    'written_steps': steps,
    'static_omissions': {'summary_space': 'Space' not in protocol, 'summary_reopen': 'reopen' not in protocol, 'back_requires_click': 'Click Back' in protocol, 'network_policy_not_named_or_loaded': not any(x in protocol for x in ['observation-policy', 'surface-contract', 'origin', 'GET', 'POST', 'allowlist'])},
    'batch_1_network': network,
    'batch_2_ui': ui_cases,
    'refutation_controls': {'healthy_ui': healthy, 'externally_applied_policy': network['with_explicit_contract_policy'], 'scope_limit': 'Supplementary harness can enforce the contract, but the six-step target does not request or verify such a harness. Countermodels establish missing documentary coverage only.'},
    'claim_coverage': {'S-1': ['batch_1_network', 'refutation_controls.externally_applied_policy'], 'S-2': ['batch_1_network', 'refutation_controls.externally_applied_policy'], 'F-203': ['batch_1_network', 'refutation_controls.externally_applied_policy'], 'C-1': ['batch_2_ui.back-not-tabbable', 'batch_2_ui.back-enter-broken', 'refutation_controls.healthy_ui'], 'F-202': ['batch_2_ui.back-not-tabbable', 'batch_2_ui.back-enter-broken', 'refutation_controls.healthy_ui'], 'C-2': ['batch_2_ui.summary-space-broken', 'batch_2_ui.summary-enter-broken', 'refutation_controls.healthy_ui'], 'F-201': ['batch_2_ui.summary-space-broken', 'batch_2_ui.summary-enter-broken', 'refutation_controls.healthy_ui']}
}
(OUT/'verifier-checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status':'PASS', 'scope':'synthetic documentary-coverage countermodels only', 'batch_1': ['S-1','S-2','F-203'], 'batch_2': ['C-1','F-202','C-2','F-201'], 'ui_defects_with_protocol_pass_and_contract_failure':list(ui_cases), 'healthy_control_contract_failures':healthy['contract']['failures'], 'synthetic_network_without_policy':network['without_extra_policy_setup'], 'synthetic_network_with_policy':network['with_explicit_contract_policy'], 'validator_output':validator_output}, indent=2))
