import json,re,urllib.request,io,html
from pathlib import Path
from PIL import Image
r=json.load(open('research/expansion-candidates.json',encoding='utf8'));extra=json.load(open('research/expansion-final-candidates.json',encoding='utf8'));m=json.load(open('research/expansion-image-credits.json',encoding='utf8'))
for key,p,caption in [('mandarin-gold-bowl',extra['gold'][4],'鸳鸯莲瓣纹金碗资料照片'),('lotus-crane-hu',r['crane'][0],'河南博物院莲鹤方壶资料照片')]:
 i=p['imageinfo'][0];u=i.get('thumburl',i['url']).split('?')[0];urls=[u,u.replace('thumb.wikimedia.org','upload.wikimedia.org'),re.sub('/1280px-','/500px-',u).replace('thumb.wikimedia.org','upload.wikimedia.org'),i['url'].split('?')[0]]
 for u in urls:
  try:
   im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"GuanwuMuseumGuide/2.0"}),timeout=15).read())).convert('RGB');im.thumbnail((1600,1600));im.save('dist/assets/expansion/'+key+'.jpg',quality=87);break
  except Exception as e:print(key,str(e),flush=True)
 else:continue
 clean=lambda x:html.unescape(re.sub('<[^>]+>','',x));meta=i['extmetadata'];g=lambda k:clean(meta.get(k,{}).get('value',''))
 m[key]={'id':key,'src':'assets/expansion/'+key+'.jpg','caption':caption,'title':p['title'],'author':g('Artist'),'license':g('LicenseShortName'),'licenseUrl':g('LicenseUrl'),'source':i['descriptionurl'],'changes':'缩放并转为 JPEG；界面可能裁切，沿用原许可','width':im.width,'height':im.height};print('OK',key,flush=True)
Path('research/expansion-image-credits.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
