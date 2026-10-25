import urllib.request,urllib.parse,json,time
from pathlib import Path
qs={'hangzhou':'浙江省非物质文化遗产馆 杭州','chengdu':'成都蜀锦织绣博物馆 成都','shangdu':'郑州商都遗址博物院 郑州'};r={}
for k,q in qs.items():
 try:
  u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','addressdetails':1,'limit':3,'countrycodes':'cn'});d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0 museum itinerary research'}),timeout=20));r[k]=d;print(k,json.dumps(d,ensure_ascii=False)[:1300],flush=True)
 except Exception as e:r[k]={'error':str(e)};print(k,e,flush=True)
 time.sleep(1.1)
Path('research/museum-locations-nominatim.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
