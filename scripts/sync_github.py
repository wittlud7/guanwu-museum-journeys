"""Push a completed commit and verify GitHub matches this Codex project.

Uses existing Git Credential Manager authentication, never stores a credential.
Intentionally refuses dirty working trees, the wrong remote, and force pushes.
"""
import json,os,subprocess,sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
config=json.loads((root/'.openai/project-sync.json').read_text(encoding='utf-8'))
env=os.environ.copy();env['GIT_TERMINAL_PROMPT']='0';env['GCM_INTERACTIVE']='never'

def git(*args):
 result=subprocess.run(['git',*args],cwd=root,env=env,text=True,capture_output=True,encoding='utf-8')
 if result.returncode:
  raise RuntimeError('Git operation failed: '+result.stderr.strip())
 return result.stdout.strip()

def main():
 remote=config['github_remote'];branch=config['github_branch']
 allowed='https://github.com/'+config['github_repository']+'.git'
 if git('remote','get-url',remote)!=allowed:raise RuntimeError('GitHub remote does not match the configured project.')
 if git('branch','--show-current')!=branch:raise RuntimeError('Finish and merge the completed update into '+branch+' before synchronization.')
 if git('status','--porcelain'):raise RuntimeError('Commit the completed update first; working tree must be clean.')
 subprocess.run([sys.executable,str(root/'scripts/check_private_release.py')],cwd=root,env=env,check=True)
 sha=git('rev-parse','HEAD')
 git('-c','http.postBuffer=134217728','-c','http.version=HTTP/1.1','push',remote,'HEAD:refs/heads/'+branch)
 refs=git('ls-remote','--heads',remote,'refs/heads/'+branch).split()
 if not refs or refs[0]!=sha:raise RuntimeError('GitHub SHA differs from the local project; synchronization is incomplete.')
 if git('status','--porcelain') or git('rev-parse','HEAD')!=sha:raise RuntimeError('Local project changed during synchronization; recheck before reporting completion.')
 print(json.dumps({'repository':'https://github.com/'+config['github_repository'],'branch':branch,'commit_sha':sha,'local_matches_github':True},ensure_ascii=False))

if __name__=='__main__':main()
