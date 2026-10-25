import json
from pathlib import Path
from PIL import Image
p=Path('research/city-museums-content.json');d=json.loads(p.read_text(encoding='utf8'));museums=d['museums']
p=Path('research/city-museums-image-credits.json');images=json.loads(p.read_text(encoding='utf8'))
old='suzhou-silk-exterior';new='suzhou-silk-interior'
if old in images:
 v=images.pop(old);src=Path('dist')/v['src'];dst=src.with_name(new+'.jpg')
 if src.exists():src.rename(dst)
 v.update(id=new,src='assets/city-museums/'+new+'.jpg',caption='苏州丝绸博物馆“蚕桑全身宝”室内展陈资料图，非馆舍外观，非当天展出保证');images[new]=v
name={m['id']:m['name'] for m in museums}
special={'zhejiang-history-exterior':'浙江省博物馆孤山馆区主楼资料图，非之江馆区','six-dynasties-exterior':'六朝博物馆大厅建筑空间资料图，非馆舍外观','nanyue-exterior':'南越王博物院王墓展区馆舍资料图，非王宫展区','shanghai-history-exterior':'上海市历史博物馆入口标识资料图','shanghai-nature-exterior':'上海自然博物馆新馆外墙资料图','xinhai-exterior':'辛亥革命博物院南院馆舍资料图，非北院旧址','zhengzhou-museum-exterior':'郑州博物馆文翰街馆资料图，非嵩山路馆','suzhou-garden-exterior':'苏州园林博物馆新馆主入口资料图，非苏州博物馆或独立园林景点'}
for key,v in images.items():
 if key==new:continue
 mid=key.removesuffix('-exterior');v['caption']=special.get(key,name.get(mid,mid)+'馆舍资料图')
for m in museums:
 key=m['id']+'-exterior'
 if m['id']=='suzhou-silk':key=new
 assert key in images,(m['id'],key)
 m['cover']=key;m['gallery']=[key];m['imageStatus']='馆内展陈资料图' if m['id']=='suzhou-silk' else '对应馆舍资料图'
 if m['id']=='six-dynasties':m['imageStatus']='馆舍大厅资料图'
 if m['id']=='shanghai-history':m['fullName']='上海市历史博物馆（上海革命历史博物馆）'
 if m['id']=='xinhai':m['sources'].append({'title':'辛亥革命博物院 · 参观须知（院区安排）','url':'https://www.1911museum.cn/list_37.html'});m['tips'].insert(0,'南北两院并非同一入口，且有错峰开放安排；请从官方须知确认拟到访院区。')
 if m['id']=='nanyue':m['tips'].insert(0,'王墓与王宫是不同地址的展区；本页封面对应王墓展区。')
 if m['id']=='zhejiang-history':m['sources'].append({'title':'浙江省博物馆 · 孤山馆区地址与文澜阁','url':'https://www.zjmuseum.com.cn/cn/msp/'});m['tips'].insert(0,'孤山与之江馆区相距较远；图片为孤山，主题介绍同时提及之江，请明确选择一个馆区。')
 if m['id']=='suzhou-silk':m['tips'].insert(0,'封面为本馆蚕桑知识室内展陈资料图，不是建筑外观；不将图片认定为当天可见展陈。')
 extra={
 'palace':('故宫博物院 · 建筑与典藏入口','https://www.dpm.org.cn/'),
 'national-china':('中国国家博物馆 · 联系地址','https://www.chnmuseum.cn/shxg/lxwm/201901/t20190102_37017.shtml'),
 'nanjing-museum':('南京博物院 · 地址与交通','https://www.njmuseum.org.cn/es/visitIndex'),
 'sichuan-museum':('四川省人民政府 · 四川博物院地址','https://www.sc.gov.cn/10462/10778/10876/2013/10/22/10282097.shtml'),
 'guangdong-museum':('广东省博物馆 · 交通与地址','https://www.gdmuseum.org.cn/col666/list'),
 'changsha-museum':('长沙博物馆 · 馆方入口与地址','https://www.csm.hn.cn/cbo/culture/main.html?id=&origin=app')}
 if m['id'] in extra:t,u=extra[m['id']];m['sources'].append({'title':t,'url':u})
 for v in m['highlights']:
  if m['id']=='palace':v['source']={'title':'故宫博物院 · 建筑与藏品','url':'https://www.dpm.org.cn/'}
 assert len(m['highlights'])==3
for museum in museums:
 museum['tips']=list(dict.fromkeys(museum['tips']))
 museum['sources']=list({x['url']:x for x in museum['sources']}.values())
p.write_text(json.dumps(images,ensure_ascii=False,indent=2),encoding='utf8')
Path('research/city-museums-content.json').write_text(json.dumps({'museums':museums},ensure_ascii=False,indent=2),encoding='utf8')
for key,v in images.items():
 assert v['author'] and v['license'] and v['licenseUrl'] and v['source'],key
 with Image.open(Path('dist')/v['src']) as im:im.verify()
out={'version':1,'updated':'2026-10-25','museums':museums,'images':images}
Path('dist/city-museums.js').write_text('(function(root){\n"use strict";\nconst data='+json.dumps(out,ensure_ascii=False,indent=2)+';\nif(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_CITY_MUSEUMS=data;\n})(typeof window!=="undefined"?window:globalThis);\n',encoding='utf8')
print('READY',len(museums),'museums',len(images),'licensed photos',sum(len(m['highlights']) for m in museums),'highlights')
