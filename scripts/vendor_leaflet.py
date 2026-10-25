"""Pinned Leaflet release assets; no runtime CDN script dependency."""
from pathlib import Path
from urllib.request import urlopen,Request
root=Path(__file__).resolve().parents[1]/'dist/vendor/leaflet'
for name in ['leaflet.js','leaflet.css','images/layers.png','images/layers-2x.png','images/marker-icon.png','images/marker-icon-2x.png','images/marker-shadow.png','LICENSE']:
 path=root/name
 if path.exists():continue
 url='https://unpkg.com/leaflet@1.9.4/'+('LICENSE' if name=='LICENSE' else 'dist/'+name)
 path.parent.mkdir(parents=True,exist_ok=True)
 with urlopen(Request(url,headers={'User-Agent':'Guanwu-development/1.0'}),timeout=40) as response:path.write_bytes(response.read())
 print(name,path.stat().st_size)
