"""Build a small native shell with per-city, local media subpackages."""
from pathlib import Path
from PIL import Image
import json,subprocess,shutil
root=Path(__file__).resolve().parents[1];native=root/'miniprogram'
data=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/heritage-data.js')))"],cwd=root,encoding='utf-8'))
credits=json.loads((root/'dist/assets/heritage/credits.json').read_text(encoding='utf-8'))
(native/'data.js').write_text('module.exports='+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
(native/'credits.js').write_text('module.exports='+json.dumps(credits,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
thumb=native/'thumbs';thumb.mkdir(exist_ok=True)
for key,c in credits.items():
 im=Image.open(root/'dist'/c['src']).convert('RGB');im.thumbnail((480,480));im.save(thumb/(key+'.jpg'),quality=77,optimize=True)
config=json.loads((native/'app.json').read_text(encoding='utf-8'));config['subPackages']=[];config['pages']=['pages/atlas/index'];config['window']['navigationBarTitleText']='观物 · 城市非遗指南'
for m in data['museums']:
 city=m['id'];sub=native/'media'/city;assets=sub/'assets';assets.mkdir(parents=True,exist_ok=True)
 cs=[c for c in data['crafts'] if c['museum']==city];keys=set(m['gallery'])
 for c in cs:keys.update(c['gallery'])
 for key in keys:
  im=Image.open(root/'dist'/credits[key]['src']).convert('RGB');im.thumbnail((1000,1000));im.save(assets/(key+'.jpg'),quality=77,optimize=True)
 audio=[f'{city}-{i}' for i in range(3)]+['craft-'+c['id'] for c in cs]
 for clip in audio:shutil.copyfile(root/'dist/assets/audio'/(clip+'.mp3'),assets/(clip+'.mp3'))
 guide=sub/'guide';guide.mkdir(exist_ok=True)
 (guide/'index.js').write_text("Page(require('../../../shared/guide-page.js')('"+city+"'));",encoding='utf-8')
 shutil.copyfile(native/'shared/guide.wxml',guide/'index.wxml')
 (guide/'index.wxss').write_text('@import "/shared/guide.wxss";',encoding='utf-8')
 (guide/'index.json').write_text('{"navigationBarTitleText":"观物 · 城市非遗导览"}',encoding='utf-8')
 config['subPackages'].append({'root':'media/'+city,'name':city,'pages':['guide/index']})
 size=sum(p.stat().st_size for p in sub.rglob('*') if p.is_file());assert size<2*1024*1024,(city,size)
 print(city,round(size/1024),'KB')
(native/'app.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
project=json.loads((native/'project.config.json').read_text(encoding='utf-8'))
project['packOptions']={'ignore':[{'type':'folder','value':'assets'},{'type':'file','value':'README.md'}]}
(native/'project.config.json').write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
main=sum(p.stat().st_size for p in native.rglob('*') if p.is_file() and 'media' not in p.relative_to(native).parts and 'assets' not in p.relative_to(native).parts)
assert main<2*1024*1024,main
print('main package',round(main/1024),'KB')
