import json
from pathlib import Path
from PIL import Image
p=Path('research/expansion-content.json');d=json.loads(p.read_text(encoding='utf8'));m=json.loads(Path('research/expansion-image-credits.json').read_text(encoding='utf8'))
for a in d['artifacts']:
 if a['id'] not in m:
  a['cover']=a['museum']+'-exterior';a['gallery']=[a['cover']];a['label']='馆藏知识 · 配图为馆舍';a['sourceRemarks']='当前配图为'+next(x['name'] for x in d['museums'] if x['id']==a['museum'])+'馆舍资料照片，不是此文物照片。'+a['sourceRemarks']
for x in d['museums']:x['gallery']=[k for k in x['gallery'] if k in m]
for k,i in m.items():
 assert Path('dist',i['src']).exists(),k
 assert i['author'] and i['license'] and i['source'],k
 with Image.open(Path('dist',i['src'])) as im:im.verify()
d['images']=m;d['version']=1;d['updated']='2026-10-24';
Path('dist/expansion-data.js').write_text('(function(root){\n\"use strict\";\nconst data='+json.dumps(d,ensure_ascii=False,indent=2)+';\nif(typeof module!==\"undefined\"&&module.exports)module.exports=data;else root.GUANWU_EXPANSION=data;\n})(typeof window!==\"undefined\"?window:globalThis);\n',encoding='utf8')
print('READY:',len(d['museums']),'museums',len(d['artifacts']),'artifacts',len(m),'images');print('No object photo:',[a['id'] for a in d['artifacts'] if a['cover']!=a['id']])
