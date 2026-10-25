import urllib.request,json,xml.etree.ElementTree as ET,concurrent.futures
from pathlib import Path
ids={'shanghai-nature':425762388,'suzhou-garden':542534200,'guangzhou':965382977}
def f(it):
 k,n=it;u=f'https://api.openstreetmap.org/api/0.6/way/{n}/full'
 try:
  raw=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0'}),timeout=25).read();Path('research/museum-locations-osm-'+k+'.xml').write_bytes(raw);r=ET.fromstring(raw);w=r.find('way');tags={t.attrib['k']:t.attrib['v'] for t in w.findall('tag')};coords=[(float(v.attrib['lat']),float(v.attrib['lon'])) for v in r.findall('node')];center=((min(x[0] for x in coords)+max(x[0] for x in coords))/2,(min(x[1] for x in coords)+max(x[1] for x in coords))/2);return k,{'lat':center[0],'lng':center[1],'tags':tags,'source':'https://www.openstreetmap.org/way/'+str(n),'geometryType':'way bounding-box center','nodeCount':len(coords)}
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:d=dict(ex.map(f,ids.items()))
Path('research/museum-locations-osm-reviewed.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(d,ensure_ascii=False,indent=2))
