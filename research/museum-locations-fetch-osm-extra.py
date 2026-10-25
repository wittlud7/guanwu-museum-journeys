import urllib.request,xml.etree.ElementTree as ET,json,concurrent.futures
from pathlib import Path
objs={'hangzhou':('relation',19222156),'shangdu':('way',1341987750),'chengdu-candidate':('node',4130339065)}
def f(it):
 k,(typ,oid)=it;u=f'https://api.openstreetmap.org/api/0.6/{typ}/{oid}'+('/full' if typ!='node' else '')
 try:
  raw=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0 educational guide'}),timeout=20).read();Path('research/museum-locations-osm-'+k+'.xml').write_bytes(raw);r=ET.fromstring(raw);obj=r.find(typ);return k,{'source':f'https://www.openstreetmap.org/{typ}/{oid}','tags':{t.attrib['k']:t.attrib['v'] for t in obj.findall('tag')}}
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:d=dict(ex.map(f,objs.items()))
Path('research/museum-locations-osm-extra-reviewed.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(d,ensure_ascii=False,indent=2))
