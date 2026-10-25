import urllib.request,urllib.parse,json,time
from pathlib import Path
p={'action':'query','generator':'categorymembers','gcmtitle':'Category:Zhengzhou Shang Capital Site Museum','gcmtype':'file','gcmlimit':20,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960,'format':'json','requestid':str(time.time())}
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p);d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0'}),timeout=25));r=json.loads(Path('research/city-museums-image-candidates.json').read_text(encoding='utf8'));r['shangdu']=list(d.get('query',{}).get('pages',{}).values());Path('research/city-museums-image-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
for i in r['shangdu']:print(i['title'],i['imageinfo'][0]['extmetadata'].get('ImageDescription',{}).get('value',''))
