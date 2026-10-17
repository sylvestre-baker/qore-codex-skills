import json,pathlib,datetime,hashlib
OUT=pathlib.Path('/workspace/output')
CANDIDATE='8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d'
TARGET='3131271b248dda5824cc374eb7f519d1bc3c16b0da28ee676ec7a00471859f3b'
def phase(phase_id,payload,observed_at=None):
 path=OUT/'evidence'/('phase-'+phase_id.replace('.','-')+'.json')
 identity={'candidate_sha256':CANDIDATE,'target_snapshot_sha256':TARGET,'observed_at':observed_at or datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase_id':phase_id}
 path.write_text(json.dumps({'qore_evidence':identity,'payload':payload},indent=2)+'\n')
 return str(path.relative_to(OUT))
