"""No sockets: capture the final urllib HTTP dispatch using a synthetic bearer."""
import io
import json
import sys
from unittest.mock import patch
import urllib.request
from urllib.response import addinfourl
sys.path.insert(0, '/workspace/project/tools')
from agent_mail import Client
observed = {}
def fake_http_open(self, request):
    observed.update(host=request.host, selector=request.selector,
                    authorization=request.get_header('Authorization'),
                    payload=json.loads(request.data))
    response = addinfourl(io.BytesIO(b'{"result":{"structuredContent":[]}}'), {}, request.full_url, 200)
    response.msg = 'OK'
    return response
with patch.dict('os.environ', {'http_proxy':'http://proxy.invalid:8080', 'no_proxy':''}, clear=True):
    with patch.object(urllib.request.HTTPHandler, 'http_open', fake_http_open):
        result = Client('http://127.0.0.1:8765/mcp/', 'SYNTHETIC-NOT-A-SECRET').call('fetch_inbox', {'project_key':'private-project', 'include_bodies':True})
print(json.dumps({'observed_dispatch':observed, 'result':result, 'network_used':False}, indent=2))
assert observed['host'] == 'proxy.invalid:8080'
assert observed['authorization'] == 'Bearer SYNTHETIC-NOT-A-SECRET'
