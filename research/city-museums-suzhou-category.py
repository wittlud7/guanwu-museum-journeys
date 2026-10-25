import urllib.request,urllib.parse,json,time
from pathlib import Path
p={'action':'query','generator':'categorymembers','gcmtitle':'Category:Museums in Suzhou','gcmtype':'file','gcmlimit':100,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960,'format':'json','requestid':str(time.time())}
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p);d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0'}),timeout=25));r=list(d.get('query',{}).get('pages',{}).values());Path('research/city-museums-suzhou-category.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
for i in r:print(i['title'])
