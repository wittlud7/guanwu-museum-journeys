import urllib.request,json,re,html,time
from pathlib import Path
from PIL import Image
ROOT=Path('dist/assets/heritage');ROOT.mkdir(parents=True,exist_ok=True)
candidates=json.loads(Path('research/image-candidates.json').read_text(encoding='utf-8'))
selected={
'beijing-exterior':('beijing',0,'中国工艺美术馆（中国非遗馆）外观'),
'beijing-front':('beijing',1,'中国工艺美术馆（中国非遗馆）建筑资料图'),
'hangzhou-exterior':('hangzhou',3,'浙江省非物质文化遗产馆外观'),
'hangzhou-fan':('hangzhou',0,'浙江省非遗馆：折扇与醒木'),
'hangzhou-percussion':('hangzhou',1,'浙江省非遗馆：小锣与板'),
'hangzhou-robe':('hangzhou',2,'浙江省非遗馆：彩绣服饰'),
'hangzhou-campus':('hangzhou2',4,'之江文化中心建筑群'),
'nanjing-exterior':('nanjing',5,'南京云锦研究所与博物馆建筑资料图'),
'nanjing-loom':('nanjing',3,'南京云锦织机资料图'),
'nanjing-weaving':('nanjing',4,'织锦木机资料图'),
'nanjing-institute':('nanjing',5,'南京云锦研究所资料图'),
'chengdu-brocade':('chengdu',0,'四川织锦双龙纹资料图，非当前展陈承诺'),
'chengdu-embroidery':('chengdu',6,'四川刺绣资料图，非本馆特定藏品'),
'chengdu-embroidery-back':('chengdu',5,'四川刺绣作品资料图，来源文件标记为反面，与另一张图非同一作品'),
'guangzhou-exterior':('guangzhou',0,'广州粤剧艺术博物馆建筑与水景'),
'guangzhou-garden':('guangzhou',2,'广州粤剧艺术博物馆园林建筑'),
'guangzhou-court':('guangzhou',3,'广州粤剧艺术博物馆庭院'),
'guangzhou-stage':('guangzhou',5,'广州粤剧艺术博物馆馆墙与导览牌'),
'cloisonne':('cloisonne',1,'明代掐丝珐琅菱花口碟，The Met 开放藏品，工艺参照图'),
'cloisonne-box':('cloisonne',6,'景泰蓝香炉历史资料图'),
'papercut':('papercut',1,'中国剪纸工艺资料图，非北京馆特定藏品'),
'papercut-pattern':('papercut',0,'狗年主题剪纸工艺资料图'),
}
def clean(x):return html.unescape(re.sub('<[^>]+>','',x)).strip()
manifest={}
for key,(group,index,caption) in selected.items():
 p=candidates[group][index];i=p['imageinfo'][0];m=i.get('extmetadata',{});get=lambda k:clean(m.get(k,{}).get('value',''))
 url=i.get('thumburl',i['url']).replace('https://thumb.wikimedia.org/','https://upload.wikimedia.org/')
 raw=ROOT/(key+'.download');target=ROOT/(key+'.jpg')
 if not target.exists():
  for attempt in range(3):
   try:
    req=urllib.request.Request(url,headers={'User-Agent':'GuanwuMuseumGuide/1.0 educational prototype'})
    raw.write_bytes(urllib.request.urlopen(req,timeout=15).read());break
   except Exception as e:
    if attempt==2:print('FAILED',key,str(e),flush=True);break
    if attempt==0:url=re.sub(r'/\d+px-', '/960px-',i.get('thumburl',i['url'])).split('?')[0]
    if attempt==1:url=i['url']
    time.sleep(2)
  if not raw.exists() or raw.stat().st_size==0:continue
  im=Image.open(raw).convert('RGB');im.thumbnail((1600,1600));im.save(target,quality=86,optimize=True);raw.unlink()
  time.sleep(1)
 manifest[key]={'id':key,'src':'assets/heritage/'+key+'.jpg','caption':caption,'title':p['title'],'author':get('Artist') or '作者未标注，详见原始来源','license':get('LicenseShortName'),'licenseUrl':get('LicenseUrl'),'source':i['descriptionurl'],'original':i['url'].split('?')[0],'changes':'缩放并转为 JPEG；界面可能裁切，照片沿用原许可','width':Image.open(target).width,'height':Image.open(target).height}
 print('OK',key)
(ROOT/'credits.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved',len(manifest),'licensed images')
