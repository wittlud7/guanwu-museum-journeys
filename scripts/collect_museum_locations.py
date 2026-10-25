"""Build and verify reviewed WGS84 museum reference points from preserved primary evidence.
Source review is explicit; no search result, camera position, guessed address or GCJ-02 value is auto-promoted.
Run from repository root. Raw Wikidata/OSM responses are under research/museum-locations-*.
"""
import json,math,xml.etree.ElementTree as ET
from pathlib import Path
D=json.loads(Path('research/museum-locations-reviewed.json').read_text(encoding='utf-8'))
C=json.loads(Path('research/museum-locations-catalog.json').read_text(encoding='utf-8'))
E=json.loads(Path('research/museum-locations-wikidata.json').read_text(encoding='utf-8'))['entities']
N=json.loads(Path('research/museum-locations-nominatim.json').read_text(encoding='utf-8'))
assert set(D)=={m['id'] for m in C}
verified=[]
for mid,d in D.items():
 assert d['coordinateSystem']=='WGS84' and d['label'] and d['address'] and d['accuracyNote']
 if d.get('unavailable'):
  assert 'lat' not in d and 'lng' not in d
  continue
 assert all(isinstance(d[k],(int,float)) and math.isfinite(d[k]) for k in ['lat','lng'])
 assert 18<d['lat']<54 and 73<d['lng']<135
 u=d['source']['url']
 if u.startswith('https://www.wikidata.org/wiki/'):
  q=u.rsplit('/',1)[-1]
  cs=[c['mainsnak'].get('datavalue',{}).get('value') for c in E[q]['claims']['P625'] if c.get('rank')!='deprecated']
  assert any(v and v.get('globe')=='http://www.wikidata.org/entity/Q2' and abs(d['lat']-v['latitude'])<1e-7 and abs(d['lng']-v['longitude'])<1e-7 for v in cs),mid
 elif u.startswith('https://www.openstreetmap.org/'):
  if mid in ['hangzhou','shangdu']:
   candidates=[v for v in N[mid] if v['category']=='tourism' and v['type']=='museum']
   assert any(str(v['osm_id'])==u.rsplit('/',1)[-1] and abs(float(v['lat'])-d['lat'])<1e-7 and abs(float(v['lon'])-d['lng'])<1e-7 for v in candidates),mid
   raw=ET.fromstring(Path('research/museum-locations-osm-'+mid+'.xml').read_bytes());typ='relation' if '/relation/' in u else 'way';ob=raw.find(typ);tags={t.attrib['k']:t.attrib['v'] for t in ob.findall('tag')};assert tags.get('tourism')=='museum',mid
  else:
   raw=ET.fromstring(Path('research/museum-locations-osm-'+mid+'.xml').read_bytes());ob=raw.find('way');tags={t.attrib['k']:t.attrib['v'] for t in ob.findall('tag')};assert tags.get('tourism')=='museum',mid
   nodes=[(float(n.attrib['lat']),float(n.attrib['lon'])) for n in raw.findall('node')];lat=(min(p[0] for p in nodes)+max(p[0] for p in nodes))/2;lng=(min(p[1] for p in nodes)+max(p[1] for p in nodes))/2;assert abs(lat-d['lat'])<1e-7 and abs(lng-d['lng'])<1e-7,mid
 else:raise AssertionError('Unreviewed coordinate source '+u)
 verified.append(mid)
assert len(D)==33 and len(verified)==32
Path('dist/museum-locations.js').write_text('(function(root){\n"use strict";\nconst data='+json.dumps(D,ensure_ascii=False,indent=2)+';\nif(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_LOCATIONS=data;\n})(typeof window!=="undefined"?window:globalThis);\n',encoding='utf-8')
print('PASS: 33 museum IDs; 32 coordinates match primary data; 1 explicit unavailable without fabricated coordinates.')
