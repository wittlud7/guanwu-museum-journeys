from pathlib import Path
import json,re,subprocess,xml.etree.ElementTree as ET
from PIL import Image
root=Path(__file__).resolve().parents[1]
data=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/heritage-data.js')))"],cwd=root,encoding='utf-8'))
credits=json.loads((root/'dist/assets/heritage/credits.json').read_text(encoding='utf-8'))
expansion=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/expansion-data.js')))"],cwd=root,encoding='utf-8'))
credits.update(expansion['images'])
for item in data['museums']+data['crafts']+expansion['museums']+expansion['artifacts']:
 assert item['cover']==item['gallery'][0],item['id']+' cover/gallery mismatch'
 for key in item['gallery']:
  credit=credits[key];assert credit['license'] and credit['source'] and credit['author']
  with Image.open(root/'dist'/credit['src']) as im:im.verify()
for path in (root/'miniprogram').rglob('*.json'):json.loads(path.read_text(encoding='utf-8'))
for path in (root/'miniprogram').rglob('*.wxml'):
 # Normalize wx directives/boolean attributes only for XML structure validation.
 source=path.read_text(encoding='utf-8').replace('wx:','wx_').replace('&&','&amp;&amp;')
 source=re.sub(r'\{\{.*?\}\}',lambda m:m.group(0).replace('<','&lt;'),source,flags=re.S)
 source=re.sub(r'\b(wx_else|indicator-dots|scroll-x)(?=[\s>])',r'\1=""',source)
 ET.fromstring('<root>'+source+'</root>')
manifest=json.loads((root/'dist/assets/audio/manifest.json').read_text(encoding='utf-8'))
assert len(manifest['jobs'])==23
for j in manifest['jobs']:
 meta=json.loads((root/'dist/assets/audio'/(j['id']+'.json')).read_text(encoding='utf-8'))
 expected=next((m['chapters'][int(j['id'][-1])]['text'] for m in data['museums'] if j['id'].startswith(m['id']+'-')),None)
 if expected is None:expected=next(c['audioText'] for c in data['crafts'] if j['id']=='craft-'+c['id'])
 assert expected==meta['text']==j['text'],j['id']+' outdated narration'
 assert meta['sentences'] and (root/'dist/assets/audio'/(j['id']+'.mp3')).stat().st_size>10000
print('PASS: sources, all gallery images, JSON/WXML structure and 23 narration/transcript matches.')
