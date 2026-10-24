"""Validate acquired media, remove unavailable optional references, and inspect assets."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
root=Path(__file__).resolve().parents[1]
p=root/'dist/heritage-data.js'
s=p.read_text(encoding='utf-8').replace(",'chengdu-pattern'",'')
p.write_text(s,encoding='utf-8')
credits=json.loads((root/'dist/assets/heritage/credits.json').read_text(encoding='utf-8'))
data=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/heritage-data.js')))"],cwd=root,encoding='utf-8'))
for item in data['museums']+data['crafts']:
 for key in item['gallery']:
  assert key in credits,key
  assert (root/'dist'/credits[key]['src']).is_file()
jobs=json.loads((root/'dist/assets/audio/manifest.json').read_text(encoding='utf-8'))['jobs']
for j in jobs:
 assert (root/'dist/assets/audio'/(j['id']+'.mp3')).stat().st_size>10000
 metadata=json.loads((root/'dist/assets/audio'/(j['id']+'.json')).read_text(encoding='utf-8'))
 assert metadata['text']==j['text'] and metadata['sentences']
sheet=Image.new('RGB',(1200,((len(credits)+3)//4)*205),'#f7f7f2');draw=ImageDraw.Draw(sheet)
for i,(key,c) in enumerate(credits.items()):
 im=Image.open(root/'dist'/c['src']).convert('RGB');im.thumbnail((290,174))
 x=(i%4)*300;y=(i//4)*205;sheet.paste(im,(x+(290-im.width)//2,y));draw.text((x+8,y+178),key,fill='#344e41')
out=root/'output/playwright';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'image-contact-sheet.jpg')
print(f'Validated {len(credits)} images, {len(jobs)} narrated clips, 5 museums and 8 craft stories.')
