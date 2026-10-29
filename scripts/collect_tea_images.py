"""Fetch only the four individually reviewed Met public-domain images.

The collection page and CC0 policy are recorded separately in tea-knowledge.json.
Existing outputs are validated; no unrestricted image search or substitution.
"""
import io,json,hashlib
from pathlib import Path
import requests
from PIL import Image
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'research/tea-knowledge.json').read_text(encoding='utf-8'));manifest=[]
for obj in data['objects']:
 image=obj['image']
 if image['status']!='cc0':continue
 p=root/'dist'/image['src'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  r=requests.get(image['sourceUrl'],timeout=45);r.raise_for_status();im=Image.open(io.BytesIO(r.content)).convert('RGB');im.thumbnail((1200,1200));im.save(p,quality=87,optimize=True)
 with Image.open(p) as im:im.verify()
 target=root/'miniprogram/knowledge/assets'/p.name;target.parent.mkdir(parents=True,exist_ok=True)
 with Image.open(p) as im:im.thumbnail((640,640));im.convert('RGB').save(target,quality=78,optimize=True)
 manifest.append(dict(id=obj['id'],src=image['src'],sourceUrl=image['sourceUrl'],collectionUrl=next(s['url'] for s in data['sources'] if s['id']==obj['sourceIds'][0]),license='CC0',policyUrl=image['policyUrl'],credit=image['credit'],checkedAt=data['updated'],sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(root/'research/tea-image-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Verified four individually licensed images and native copies.')
