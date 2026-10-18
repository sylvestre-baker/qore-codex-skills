#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from urllib.parse import urlsplit
out=Path('/workspace/output')
root=Path('/workspace/worker')
initial=json.loads((out/'input-sha256.json').read_text())
current={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
report={'input_files_unchanged':initial==current,'responses':[],'limit':'Mechanical integrity, event summaries and assertion outcomes only; this check does not establish reasoning correctness or visual quality.'}
for i in (1,2):
    p=out/'evidence'/f'response-{i}'
    receipt=json.loads((p/'relay.json').read_text())
    events=json.loads((p/'events.json').read_text())
    result=json.loads((p/'result.json').read_text())
    req=out/f'browser-request-{i}.json'
    a=json.loads(req.read_text())
    recorded_url_events=[x for k in ('network','navigation','requests_failed','blocked_mutations','blocked_navigation') for x in events[k] if 'url' in x]
    origins=sorted({urlsplit(x['url']).scheme+'://'+urlsplit(x['url']).netloc for x in recorded_url_events})
    report['responses'].append({
      'request':i,'submitted_action_count':len(a),'within_40_action_limit':len(a)<=40,
      'request_sha256_matches_receipt':hashlib.sha256(req.read_bytes()).hexdigest()==receipt['request_sha256'],
      'all_receipt_file_hashes_match':all(hashlib.sha256((p/f).read_bytes()).hexdigest()==digest for f,digest in receipt['files'].items()),
      'fresh_context':receipt['fresh_context'],'input_actions_modified':receipt['input_actions_modified'],
      'relay_exit_code':receipt['exit_code'],'probe_status':result['status'],
      'observed_origins':origins,'only_authorized_origin_observed':origins==['https://qaizen.io'],
      'network_count':len(events['network']),'network_response_methods':sorted({x['method'] for x in events['network']}),
      'blocked_mutations':events['blocked_mutations'],'console':events['console'],'page_errors':events['page_errors'],
      'blocked_activations':events['blocked_activations'],
      'assertions':[{'event_index':j,**x} for j,x in enumerate(events['actions']) if x['type'].startswith('assert-')],
      'keyboard_and_traversal':[{'event_index':j,**x} for j,x in enumerate(events['actions']) if x['type'] in ('keyboard','focus-step','traverse-focus')],
      'trace_and_video_availability':'Referenced by result.json but not included in relay files; not available to this actor.'})
(out/'evidence-check.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['input_files_unchanged']
assert all(r['request_sha256_matches_receipt'] and r['all_receipt_file_hashes_match'] and r['within_40_action_limit'] and r['only_authorized_origin_observed'] for r in report['responses'])
assert report['responses'][1]['probe_status']=='COMPLETE'
assert all(x['outcome']=='completed' for x in report['responses'][1]['assertions'])
print(json.dumps({'integrity_checks_passed':True,'inputs_unchanged':True,'requests':2,'request2_assertions_completed':len(report['responses'][1]['assertions']),'detail':'evidence-check.json'},indent=2))
