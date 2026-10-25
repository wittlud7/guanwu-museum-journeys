import urllib.request,urllib.parse,json,time,concurrent.futures
from pathlib import Path
q={'palace':'"Palace Museum" "Meridian Gate"','national-china':'"National Museum of China" exterior','zhejiang-history':'"Zhejiang Provincial Museum"','national-silk':'"China National Silk Museum"','nanjing-museum':'"Nanjing Museum" exterior','six-dynasties':'"Six Dynasties Museum"','chengdu-museum':'"Chengdu Museum" exterior','jinsha':'"Jinsha Site Museum"','guangdong-museum':'"Guangdong Museum" exterior','nanyue':'"Museum of the Nanyue King"','xian-museum':'"Xi’an Museum"','beilin':'"Beilin Museum"','shanghai-history':'"Shanghai History Museum"','shanghai-nature':'"Shanghai Natural History Museum" exterior','suzhou-silk':'"Suzhou Silk Museum"','suzhou-brick':'"Suzhou" "Imperial" "Brick"','wuhan-museum':'"Wuhan Museum"','xinhai':'"1911 Revolution Museum"','zhengzhou-museum':'"Zhengzhou Museum"','shangdu':'"Zhengzhou Shang" "Museum"','changsha-museum':'"Changsha Museum" exterior','changsha-slips':'"Changsha" "Bamboo Slips Museum"'}
def f(it):
 k,s=it;p={'action':'query','generator':'search','gsrsearch':s,'gsrnamespace':6,'gsrlimit':5,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960,'format':'json','requestid':str(time.time())}
 try:
  u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p);r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0'}),timeout=25);d=json.load(r);a=list(d.get('query',{}).get('pages',{}).values());a.sort(key=lambda a:a.get('index',0));return k,a
 except Exception as e:return k,{'error':str(e)}
r={}
for k,v in q.items():
 _,r[k]=f((k,v));Path('research/city-museums-image-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(k,':',' | '.join(a['title'] for a in r[k]) if isinstance(r[k],list) else r[k],flush=True);time.sleep(1)
