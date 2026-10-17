"""Publish built static assets; password and token remain in process memory."""
import base64, getpass, json, os, pathlib, subprocess, urllib.request, urllib.error

ROOT=pathlib.Path(__file__).resolve().parent.parent
password=getpass.getpass('Surge password (hidden): ')
request=urllib.request.Request('https://surge.surge.sh/token',data=b'{}',method='POST',headers={
    'Authorization':'Basic '+base64.b64encode(('nieweide@outlook.com:'+password).encode()).decode(),
    'Content-Type':'application/json','User-Agent':'bible-atlas-publisher'})
try:
    with urllib.request.urlopen(request,timeout=40) as response:
        token=json.load(response)['token']
    env=os.environ.copy();env['SURGE_TOKEN']=token
    cli=ROOT/'.deploy/tools/node_modules/surge/bin/surge'
    subprocess.run(['node',str(cli),str(ROOT/'dist'),'bible-reformed-atlas-20261017-v1-2.surge.sh'],
                   cwd=ROOT,env=env,check=True)
except urllib.error.HTTPError as error:
    print('Surge authentication HTTP',error.code)
    raise SystemExit(1)
except Exception as error:
    print('Surge publish failed:',type(error).__name__)
    raise SystemExit(1)
