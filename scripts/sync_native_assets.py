"""Build a small native shell with per-city, local media subpackages."""
from pathlib import Path
from PIL import Image
import json,subprocess,shutil
root=Path(__file__).resolve().parents[1];native=root/'miniprogram'
data=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/heritage-data.js')))"],cwd=root,encoding='utf-8'))
expansion=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/expansion-data.js')))"],cwd=root,encoding='utf-8'))
data['museums']+=expansion['museums']
city_museums=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/city-museums.js')))"],cwd=root,encoding='utf-8'))
data['museums']+=city_museums['museums']
beijing=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/beijing-museums.js')))"],cwd=root,encoding='utf-8'))
data['museums']+=beijing['museums']
data['crafts']+=[dict(a,audio=False,category='文物 · '+a['material']) for a in expansion['artifacts']]
credits=json.loads((root/'dist/assets/heritage/credits.json').read_text(encoding='utf-8'))
credits.update({p['id']:p for p in (expansion['images'] if isinstance(expansion['images'],list) else expansion['images'].values())})
credits.update(city_museums['images'])
credits.update(beijing['images'])
world=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/world-heritage-data.js')))"],cwd=root,encoding='utf-8'))
data['heritage']=world['sites']
credits.update(world['images'])
(native/'data.js').write_text('module.exports='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
(native/'credits.js').write_text('module.exports='+json.dumps(credits,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
thumb=native/'thumbs';thumb.mkdir(exist_ok=True)
for key,c in credits.items():
 im=Image.open(root/'dist'/c['src']).convert('RGB');im.thumbnail((220,220));im.save(thumb/(key+'.jpg'),quality=66,optimize=True)
config=json.loads((native/'app.json').read_text(encoding='utf-8'));config['subPackages']=[];config['pages']=['pages/atlas/index'];config['window']['navigationBarTitleText']='观物 · 城市博物馆指南'
for m in data['museums']:
 city=m['id'];sub=native/'media'/city;assets=sub/'assets';assets.mkdir(parents=True,exist_ok=True)
 cs=[c for c in data['crafts'] if c['museum']==city];keys=set(m['gallery'])
 for c in cs:keys.update(c['gallery'])
 for key in keys:
  im=Image.open(root/'dist'/credits[key]['src']).convert('RGB');im.thumbnail((720,720));im.save(assets/(key+'.jpg'),quality=68,optimize=True)
 audio=[f'{city}-{i}' for i,c in enumerate(m['chapters']) if c.get('audio') is not False]+['craft-'+c['id'] for c in cs if c.get('audio') is not False]
 for clip in audio:shutil.copyfile(root/'dist/assets/audio'/(clip+'.mp3'),assets/(clip+'.mp3'))
 guide=sub/'guide';guide.mkdir(exist_ok=True)
 (guide/'index.js').write_text("Page(require('../../../shared/guide-page.js')('"+city+"'));",encoding='utf-8')
 shutil.copyfile(native/'shared/guide.wxml',guide/'index.wxml')
 (guide/'index.wxss').write_text('@import "/shared/guide.wxss";',encoding='utf-8')
 (guide/'index.json').write_text('{"navigationBarTitleText":"观物 · 城市博物馆导览"}',encoding='utf-8')
 config['subPackages'].append({'root':'media/'+city,'name':city,'pages':['guide/index']})
 size=sum(p.stat().st_size for p in sub.rglob('*') if p.is_file());assert size<2*1024*1024,(city,size)
 print(city,round(size/1024),'KB')
# Heritage pages use shared reading UI; the web version offers all three audio introductions.
for site in world['sites']:
 sub=native/'media'/site['id'];assets=sub/'assets';assets.mkdir(parents=True,exist_ok=True)
 for key in site['gallery']:
  im=Image.open(root/'dist'/credits[key]['src']).convert('RGB');im.thumbnail((720,720));im.save(assets/(key+'.jpg'),quality=68,optimize=True)
 guide=sub/'guide';guide.mkdir(exist_ok=True)
 (guide/'index.js').write_text("Page(require('../../../shared/heritage-page.js')('"+site['id']+"'));",encoding='utf-8')
 shutil.copyfile(native/'shared/heritage.wxml',guide/'index.wxml')
 (guide/'index.wxss').write_text('@import "/shared/guide.wxss";',encoding='utf-8')
 (guide/'index.json').write_text('{"navigationBarTitleText":"观物 · 世界遗产"}',encoding='utf-8')
 config['subPackages'].append({'root':'media/'+site['id'],'name':site['id'],'pages':['guide/index']})
# Keep alternate voices in separate audio-only subpackages so each museum remains below 2MB.
packs=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/voice-packs-data.js')))"],cwd=root,encoding='utf-8'))
(native/'voice-packs.js').write_text('module.exports='+json.dumps(packs,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
for voice in ['yunxi','xiaoyi']:
 for museum in data['museums']:
  if museum['chapters'][0].get('audio') is False:continue
  mid=museum['id'];name='voice-'+voice+'-'+mid;sub=native/'media'/name;assets=sub/'assets';assets.mkdir(parents=True,exist_ok=True)
  clips=[mid+'-'+str(i) for i in range(len(museum['chapters']))]+['craft-'+c['id'] for c in data['crafts'] if c['museum']==mid and c.get('audio') is not False]
  for clip in clips:shutil.copyfile(root/'dist/assets/audio/packs'/voice/(clip+'.mp3'),assets/(clip+'.mp3'))
  guide=sub/'guide';guide.mkdir(exist_ok=True)
  (guide/'index.js').write_text('Page({onLoad(){wx.navigateBack()}});',encoding='utf-8')
  (guide/'index.wxml').write_text('<view>语音资源</view>',encoding='utf-8')
  (guide/'index.wxss').write_text('',encoding='utf-8');(guide/'index.json').write_text('{}',encoding='utf-8')
  size=sum(f.stat().st_size for f in sub.rglob('*') if f.is_file());assert size<2*1024*1024,(name,size)
  config['subPackages'].append({'root':'media/'+name,'name':name,'pages':['guide/index']})
(native/'app.json').write_text(json.dumps(config,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
project=json.loads((native/'project.config.json').read_text(encoding='utf-8'))
project['packOptions']={'ignore':[{'type':'folder','value':'assets'},{'type':'folder','value':'media/suzhou-brick'},{'type':'file','value':'README.md'}]}
(native/'project.config.json').write_text(json.dumps(project,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
main=sum(p.stat().st_size for p in native.rglob('*') if p.is_file() and 'media' not in p.relative_to(native).parts and 'assets' not in p.relative_to(native).parts)
assert main<2*1024*1024,main
print('main package',round(main/1024),'KB')

selected=[native / package['root'] for package in config['subPackages']]
total=main+sum(f.stat().st_size for folder in selected for f in folder.rglob('*') if f.is_file())
assert total<30*1024*1024,('Combined native packages',total)
print('all declared packages',round(total/1048576,2),'MB')
