import urllib.request,urllib.parse,json,time
from pathlib import Path
r=json.load(open('research/expansion-candidates.json',encoding='utf8'));ex=json.load(open('research/expansion-final-candidates.json',encoding='utf8'));last=json.load(open('research/expansion-last-candidates.json',encoding='utf8'))
titles=['File:20210220 Bronze owl-shaped Zun with inscriptions of Fu Hao, Henan Museum.jpg','File:Zi Zhong Jiang pan bronzeware.jpg','File:Tang Gold Bowl (9949909874).jpg','File:Spring & Autumn Bronze Hu (10342187523).jpg']
p={'action':'query','titles':'|'.join(titles),'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1280,'format':'json','requestid':str(time.time())}
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"GuanwuMuseumGuide/2.0"}),timeout=30));v=list(d['query']['pages'].values());Path('research/expansion-exact-images.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
for p in v:print(p['title'],p.get('imageinfo',[{}])[0].get('extmetadata',{}).get('ImageDescription',{}).get('value',''))
