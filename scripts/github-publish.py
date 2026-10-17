"""Publish through GitHub's API; read credentials only from a hidden prompt.

No credentials are stored or printed. Existing files/history are preserved.
"""
import argparse, base64, getpass, json, pathlib, sys, urllib.request, urllib.error, time, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

OWNER = '07-Je-GT-Love-Personal-20260918'
OLD = 'bible-reformed-atlas-20260919'
NEW = 'bible-reformed-atlas-20261017-v1-2'
ROOT = pathlib.Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--readme-only', action='store_true')
    args = parser.parse_args()
    token = getpass.getpass('GitHub token (hidden): ')
    def api(path, method='GET', data=None):
        request = urllib.request.Request('https://api.github.com'+path,
            headers={'Authorization': 'Bearer '+token, 'Accept':'application/vnd.github+json',
                     'X-GitHub-Api-Version':'2022-11-28', 'User-Agent':'bible-atlas-publisher'},
            data=None if data is None else json.dumps(data).encode(), method=method)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request,timeout=50) as response:
                    return json.load(response) if response.status != 204 else {}
            except (urllib.error.URLError, TimeoutError) as error:
                if isinstance(error,urllib.error.HTTPError) and error.code < 500: raise
                if attempt==3: raise
                print('Retrying GitHub request:',method,path.split('?')[0],flush=True)
                time.sleep(1+attempt)
    try:
        user = api('/user')
        print('Authenticated GitHub account:',user['login'],flush=True)
        try:
            repo = api(f'/repos/{OWNER}/{OLD}')
        except urllib.error.HTTPError as error:
            if error.code != 404: raise
            repo = api(f'/repos/{OWNER}/{NEW}')
        print('Existing repository:',repo['full_name'],'branch:',repo['default_branch'],
              'push:',repo.get('permissions',{}).get('push'),flush=True)
        if args.status:
            prefix='/repos/'+repo['full_name']
            pages=api(prefix+'/pages')
            runs=api(prefix+'/actions/runs?per_page=3')
            print(json.dumps({'pages':pages.get('html_url'),'status':pages.get('status'),
                'runs':[{'name':r['name'],'status':r['status'],'conclusion':r['conclusion'],
                         'url':r['html_url']} for r in runs['workflow_runs']]},indent=2),flush=True)
            return
        if args.readme_only:
            prefix='/repos/'+repo['full_name']
            old=api(prefix+'/contents/README.md')
            result=api(prefix+'/contents/README.md','PUT',{'message':'Document verified public deployments',
                'content':base64.b64encode((ROOT/'README.md').read_bytes()).decode(),'sha':old['sha']})
            print('README updated:',result['content']['html_url'],flush=True)
            return
        if not args.publish: return
        if repo['name'] != NEW:
            repo = api(f'/repos/{repo["full_name"]}','PATCH',{'name':NEW})
            print('Renamed existing repository:',repo['html_url'],flush=True)
        prefix='/repos/'+repo['full_name']
        branch=repo['default_branch']
        ref=api(prefix+'/git/ref/heads/'+branch)
        parent=ref['object']['sha']
        commit=api(prefix+'/git/commits/'+parent)
        existing=api(prefix+'/git/trees/'+commit['tree']['sha']+'?recursive=1')
        known={entry['path']:entry['sha'] for entry in existing['tree'] if entry['type']=='blob'}
        tree=[]
        roots=['index.html','study.html','bible-66-overview.html','reformed-bible-66-study.html',
               'bible_66_quick_frontend_guide.html','README.md','package.json','package-lock.json',
               'vercel.json','.gitignore','assets','books','scripts','build','.github']
        files=[]
        for name in roots:
            p=ROOT/name
            files.extend(p.rglob('*') if p.is_dir() else [p])
        files=[p for p in files if p.is_file() and '__pycache__' not in p.parts]
        def upload(p):
            content=p.read_bytes()
            path=p.relative_to(ROOT).as_posix()
            digest=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
            if known.get(path)==digest:
                return {'path':path,'mode':'100644','type':'blob','sha':digest}
            blob=api(prefix+'/git/blobs','POST',{
                'content':base64.b64encode(content).decode(),'encoding':'base64'})
            return {'path':path,'mode':'100644','type':'blob','sha':blob['sha']}
        with ThreadPoolExecutor(max_workers=4) as pool:
            for task in as_completed([pool.submit(upload,p) for p in files]):
                tree.append(task.result())
                if len(tree)%10==0: print('Uploaded source files:',len(tree),'/',len(files),flush=True)
        newtree=api(prefix+'/git/trees','POST',{'base_tree':commit['tree']['sha'],'tree':tree})
        created=api(prefix+'/git/commits','POST',{
            'message':'Add animated Bible atlas and static deployment workflows (2026-10-17 v1.2)',
            'tree':newtree['sha'],'parents':[parent]})
        api(prefix+'/git/refs/heads/'+branch,'PATCH',{'sha':created['sha'],'force':False})
        print('Published commit:',created['html_url'],flush=True)
        try:
            pages=api(prefix+'/pages')
            if pages.get('build_type')!='workflow':
                pages=api(prefix+'/pages','PUT',{'build_type':'workflow'})
        except urllib.error.HTTPError as error:
            if error.code!=404: raise
            pages=api(prefix+'/pages','POST',{'build_type':'workflow'})
        print('Pages configured:',pages.get('html_url','workflow deployment enabled'),flush=True)
    except urllib.error.HTTPError as error:
        # Only GitHub's error message is printed; never request headers.
        try: message=json.load(error).get('message','request failed')
        except Exception: message='request failed'
        print(f'GitHub HTTP {error.code}: {message}',flush=True)
        sys.exit(1)
    except Exception as error:
        print('Publishing failed:',type(error).__name__,flush=True)
        sys.exit(1)

if __name__=='__main__': main()
