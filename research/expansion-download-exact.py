import json,re,urllib.request,html,io
from pathlib import Path
from PIL import Image
v=json.load(open('research/expansion-exact-images.json',encoding='utf8'));m=json.load(open('research/expansion-image-credits.json',encoding='utf8'))
for key,match,caption in [('fuhao-owl','20210220','河南博物院妇好鸮尊资料照片'),('zi-zhong-pan','Zi Zhong','子仲姜盘资料照片')]:
 p=next(x for x in v if match in x['title']);i=p['imageinfo'][0];u=i.get('thumburl',i['url']).split('?')[0]
 for u in [re.sub(r'/1280px-','/960px-',u),re.sub(r'/1280px-','/960px-',u).replace('thumb.wikimedia.org','upload.wikimedia.org'),i['url'].split('?')[0]]:
  try:
   im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/2.0'}),timeout=20).read())).convert('RGB');im.thumbnail((1600,1600));im.save('dist/assets/expansion/'+key+'.jpg',quality=87);break
  except Exception as e:print(key,str(e),flush=True)
 else:continue
 clean=lambda x:html.unescape(re.sub('<[^>]+>','',x));meta=i['extmetadata'];g=lambda k:clean(meta.get(k,{}).get('value',''));m[key]={'id':key,'src':'assets/expansion/'+key+'.jpg','caption':caption,'title':p['title'],'author':g('Artist'),'license':g('LicenseShortName'),'licenseUrl':g('LicenseUrl'),'source':i['descriptionurl'],'changes':'缩放并转为 JPEG；界面可能裁切，沿用原许可','width':im.width,'height':im.height};print('OK',key,flush=True)
Path('research/expansion-image-credits.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
