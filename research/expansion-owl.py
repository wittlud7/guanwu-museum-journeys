import urllib.request,urllib.parse,json,time
from pathlib import Path
p={'action':'query','titles':'File:Fuhao Owl Zun front.jpg','prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960,'format':'json','requestid':str(time.time())}
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/2.0'}),timeout=20));v=list(d['query']['pages'].values());Path('research/expansion-owl-alt.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8');print(v[0]['imageinfo'][0]['extmetadata'].get('ImageDescription',{}))
