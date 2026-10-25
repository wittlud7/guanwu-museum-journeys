import urllib.request,urllib.parse,json,time
from pathlib import Path
qs=['Shu Brocade and Embroidery Museum Chengdu','蜀锦 博物馆 成都','蜀江锦院 成都','成都 蜀绣博物馆'];r={}
for q in qs:
 try:
  u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','addressdetails':1,'limit':5,'countrycodes':'cn'});d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0 museum itinerary research'}),timeout=20));r[q]=d;print(q,json.dumps(d,ensure_ascii=False)[:2500],flush=True)
 except Exception as e:r[q]={'error':str(e)};print(e,flush=True)
 time.sleep(1.1)
Path('research/museum-locations-chengdu-nominatim.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
