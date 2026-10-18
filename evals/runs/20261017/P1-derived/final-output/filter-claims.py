import json
from pathlib import Path
r=Path('/workspace/output')
raw=json.loads((r/'claims-raw.json').read_text())
keep=('id','severity','kind','statement','source_locations')
filtered={'schema':'qore-filtered-claims/1','filter':'Whitelisted claim fields only; no role identities, full reports, confidence/votes or adjudicator verdict supplied. Source paths resolve in frozen input root.','claims':[{k:c[k] for k in keep} for c in raw['claims']]}
(r/'claims-filtered.json').write_text(json.dumps(filtered,indent=2))
