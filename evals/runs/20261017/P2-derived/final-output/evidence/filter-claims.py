from pathlib import Path
import json,hashlib,datetime
out=Path('/workspace/output');roles=['product','architecture','ux','delivery','qa'];fields=('id','claim','source_locations','proposed_change','severity','refutation')
filtered=[];inputs=[]
for role in roles:
 p=out/f'reports/{role}-claims.json';raw=json.loads(p.read_text())
 if not isinstance(raw,list):raise TypeError(str(p)+' must be a list')
 inputs.append({'path':str(p.relative_to(out)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'count':len(raw)})
 for c in raw:
  if not isinstance(c,dict) or any(k not in c for k in fields):raise ValueError(str(p)+' missing required field')
  filtered.append({k:c[k] for k in fields})
p=out/'evidence/filtered-claims.json';p.write_text(json.dumps(filtered,indent=2))
(out/'evidence/filter-log.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'JSON field whitelist only; preserve every claim, source location, proposed change, severity and refutation unchanged; drop all other fields; no semantic ranking, summary or selection.','whitelist':fields,'inputs':inputs,'output':{'path':'evidence/filtered-claims.json','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'claim_count':len(filtered)},'verifier_exclusions':['full role reports','peer discussion','lead draft/specification','role identity wrappers']},indent=2))
print('Mechanically filtered',len(filtered),'claims')
