import urllib.request,urllib.parse,json
from pathlib import Path
c=json.loads(Path('research/museum-locations-catalog.json').read_text(encoding='utf8'));names=[x['name'] for x in c]+['中国工艺美术馆','中国非物质文化遗产馆','郑州商代都城遗址博物院','辛亥革命博物馆','西汉南越王博物馆','浙江省非物质文化遗产馆','中国工艺美术馆 中国非物质文化遗产馆']
regex='^('+'|'.join(names)+')$';q='[out:json][timeout:90];nwr["name"~"'+regex+'"]["tourism"="museum"](18,73,54,135);out center tags;'
u='https://overpass.kumi.systems/api/interpreter?'+urllib.parse.urlencode({'data':q})
try:
 d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0 educational guide'}),timeout=50));Path('research/museum-locations-osm.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print([(i['type'],i['id'],i.get('tags',{}).get('name'),i.get('center',{'lat':i.get('lat'),'lon':i.get('lon')})) for i in d.get('elements',[])])
except Exception as e:print(e)
