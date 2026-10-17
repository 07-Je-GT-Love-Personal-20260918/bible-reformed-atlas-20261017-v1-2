"""Store a Surge deployment token in GitHub Actions secrets, never in source."""
import base64, getpass, json, os, subprocess, urllib.request, urllib.error

github=getpass.getpass('GitHub token (hidden): ')
password=getpass.getpass('Surge password (hidden): ')
request=urllib.request.Request('https://surge.surge.sh/token',data=json.dumps({
    'msg':'GitHub Actions bible-reformed-atlas-20261017-v1-2'}).encode(),method='POST',headers={
    'Authorization':'Basic '+base64.b64encode(('nieweide@outlook.com:'+password).encode()).decode(),
    'Content-Type':'application/json','User-Agent':'bible-atlas-ci'})
try:
    with urllib.request.urlopen(request,timeout=40) as response: token=json.load(response)['token']
    env=os.environ.copy();env['GH_TOKEN']=github
    subprocess.run(['gh','secret','set','SURGE_TOKEN','--repo',
        '07-Je-GT-Love-Personal-20260918/bible-reformed-atlas-20261017-v1-2'],
        input=token,text=True,env=env,check=True)
    print('SURGE_TOKEN stored in GitHub Actions repository secrets.')
except Exception as error:
    print('CI configuration failed:',type(error).__name__)
    raise SystemExit(1)
