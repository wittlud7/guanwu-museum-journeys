"""Fail closed if the user's private configuration appears in publishable files."""
import json,subprocess,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
settings=root/'settings.json'
if settings.exists():
 config=json.loads(settings.read_text(encoding='utf-8-sig'));env=config.get('env',config);secret=env.get('DEEPSEEK_API_KEY') or env.get('ANTHROPIC_AUTH_TOKEN')
 assert secret and len(secret)>10,'No private credential to check'
 files=subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z'],cwd=root).decode('utf-8').split('\0')
 forbidden=[]
 for name in files:
  path=root/name
  if path.is_file() and secret.encode() in path.read_bytes():forbidden.append(name)
 for directory in [root/'dist',root/'server-app/dist',root/'miniprogram']:
  for path in directory.rglob('*'):
   if path.is_file() and secret.encode() in path.read_bytes():forbidden.append(str(path.relative_to(root)))
 archive=root/'output/观物-微信小程序.zip'
 if archive.exists():
  with zipfile.ZipFile(archive) as z:
   assert not any(secret.encode() in z.read(n) for n in z.namelist() if not n.endswith('/'))
 assert not forbidden,'Private configuration appeared in release files: '+str(forbidden)
 assert subprocess.run(['git','check-ignore','-q','settings.json'],cwd=root).returncode==0
 print('PASS: private settings ignored; credential absent from source candidates, web assets, Worker output and native archive.')
else:print('No local private settings to scan.')
