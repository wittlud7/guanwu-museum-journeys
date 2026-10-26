"""Push and package this static Site; credentials are read only from stdin.

Portable fallback for the bundled Node package helper's Windows native-copy crash.
Never prints credentials or stores them in Git configuration.
"""
import json,os,subprocess,sys,tarfile,io
from pathlib import Path
restore=None
if sys.stdin.isatty():
 if os.name!='nt':raise RuntimeError('Use piped stdin on this platform.')
 import ctypes
 from ctypes import wintypes
 kernel=ctypes.windll.kernel32;kernel.GetStdHandle.restype=wintypes.HANDLE
 handle=kernel.GetStdHandle(-10);mode=wintypes.DWORD()
 if not kernel.GetConsoleMode(handle,ctypes.byref(mode)):raise RuntimeError('Cannot disable terminal echo.')
 if not kernel.SetConsoleMode(handle,mode.value&~4):raise RuntimeError('Cannot disable terminal echo.')
 restore=lambda:kernel.SetConsoleMode(handle,mode.value)
print('Ready for publishing JSON on stdin (input is hidden).',flush=True)
try:payload=json.loads(sys.stdin.readline())
finally:
 if restore:restore()
credential=payload['credential'];project_id=payload['project_id']
root=Path.cwd().resolve();manifest=json.loads((root/'.openai/hosting.json').read_text(encoding='utf-8'))
assert manifest['project_id']==project_id
worker='static' not in manifest
if not worker:assert manifest['static']['directory']=='dist'
env=os.environ.copy();remote=credential['remote_url'];branch=credential['branch'];auth=[]
if credential.get('auth_mode')=='http_extra_header':
 token=credential['token'];assert token and not any(c in token for c in '\r\n\0')
 env['GUANWU_GIT_AUTHORIZATION']='Authorization: Bearer '+token
 auth=['-c','credential.helper=','-c','http.extraHeader=','-c','http.followRedirects=false','--config-env=http.'+remote+'.extraHeader=GUANWU_GIT_AUTHORIZATION']
else:assert credential.get('auth_mode')=='work_proxy'
def git(args,network=False):
 network_options=['-c','http.postBuffer=134217728','-c','http.version=HTTP/1.1'] if network else []
 p=subprocess.run(['git']+network_options+(auth if network else [])+args,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8')
 if p.returncode:
  detail=p.stderr.replace(credential.get('token','__no_token__'),'[redacted]')
  raise RuntimeError(detail)
 return p.stdout.strip()
git(['add','--all','--','.'])
if git(['diff','--cached','--name-only']):git(['-c','user.name=Sites','-c','user.email=sites@users.noreply.openai.com','commit','-m','Add all 46 China cultural and mixed World Heritage sites with three selectable voice packs'])
sha=git(['rev-parse','HEAD']);assert not git(['status','--porcelain'])
git(['push',remote,sha+':refs/heads/'+branch],network=True)
pushed=git(['ls-remote','--heads',remote,'refs/heads/'+branch],network=True).split()[0]
assert pushed==sha and not git(['status','--porcelain'])
archive=Path(payload['archivePath']).resolve();assert root not in archive.parents
assets=root/('server-app/dist' if worker else 'dist');assert not any(p.is_symlink() for p in assets.rglob('*'))
assert assets.is_dir()
with tarfile.open(archive,'w:gz') as tar:
 tar.add(assets,arcname='dist')
 body=(root/'.openai/hosting.json').read_bytes()
 if (assets/'.openai/hosting.json').exists():assert json.loads((assets/'.openai/hosting.json').read_bytes())==json.loads(body)
 else:
  entry=tarfile.TarInfo('dist/.openai/hosting.json');entry.size=len(body);tar.addfile(entry,io.BytesIO(body))
with tarfile.open(archive) as tar:
 assert len(tar.getnames())==len(set(tar.getnames())),'Duplicate archive paths'
 assert ('dist/server/index.js' if worker else 'dist/index.html') in tar.getnames() and 'dist/.openai/hosting.json' in tar.getnames()
 if worker:assert 'dist/client/index.html' in tar.getnames()
assert git(['rev-parse','HEAD'])==sha and not git(['status','--porcelain'])
print(json.dumps({'project_id':project_id,'commit_sha':sha,'archive':str(archive)},ensure_ascii=False))
