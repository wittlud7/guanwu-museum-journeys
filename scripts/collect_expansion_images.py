"""Download the reviewed, licensed expansion photographs. Metadata is curated separately.
Run from repository root. Existing valid JPEGs are left intact; optional failures are reported.
"""
import io,json,re,time,urllib.request
from pathlib import Path
from PIL import Image
manifest=json.loads(Path('research/expansion-image-credits.json').read_text(encoding='utf-8'))
for key,m in manifest.items():
 target=Path('dist')/m['src'];target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():
  with Image.open(target) as im:im.verify()
  print('EXISTS',key);continue
 original=m.get('original','').split('?')[0]
 if not original:print('NO ORIGINAL URL',key);continue
 parts=original.rsplit('/',1);thumb=parts[0].replace('/commons/','/commons/thumb/')+'/'+parts[1]+'/960px-'+parts[1]
 for u in [thumb,original]:
  try:
   req=urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/2.0 educational guide'})
   with urllib.request.urlopen(req,timeout=25) as response:raw=response.read()
   im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((1600,1600));im.save(target,quality=87,optimize=True);print('SAVED',key);break
  except Exception as e:print('OPTIONAL CANDIDATE FAILED',key,str(e))
 else:print('MISSING',key)
 time.sleep(1)
