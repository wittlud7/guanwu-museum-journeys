"""Reproduce the reviewed city museum assets without reselecting or changing their credits.
Run from repository root. Existing files are verified; missing JPEGs are downloaded from Commons.
"""
import io,json,time,urllib.request
from pathlib import Path
from PIL import Image
manifest=json.loads(Path('research/city-museums-image-credits.json').read_text(encoding='utf-8'))
failed=[]
for key,v in manifest.items():
 target=Path('dist')/v['src'];target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():
  with Image.open(target) as im:im.verify()
  print('VERIFIED',key);continue
 original=v['original'].split('?')[0];prefix,filename=original.rsplit('/',1);thumb=prefix.replace('/commons/','/commons/thumb/')+'/'+filename+'/960px-'+filename
 for url in [thumb,original]:
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'GuanwuMuseumGuide/3.0 educational guide'})
   with urllib.request.urlopen(req,timeout=25) as response:raw=response.read()
   im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((1600,1600));im.save(target,quality=87,optimize=True);print('SAVED',key);break
  except Exception as e:print('CANDIDATE FAILED',key,str(e))
 else:failed.append(key)
 time.sleep(1)
if failed:raise SystemExit('Missing reviewed photos: '+', '.join(failed))
