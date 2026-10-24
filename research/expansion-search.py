import urllib.request,urllib.parse,json,concurrent.futures
from pathlib import Path
qs={'xian':'"Shaanxi History Museum"','shanghai':'"Shanghai Museum" exterior','suzhou':'"Suzhou Museum"','wuhan':'"Hubei Museum"','zhengzhou':'"Henan Museum"','changsha':'"Hunan Museum"','agate':'"Agate" "Shaanxi"','tiger':'"Du" "tiger tally"','pot':'"Shaanxi" "silver"','ding':'"Da Ke Ding"','pan':'"Zi Zhong Jiang"','measure':'"Shang Yang" measure','lotus':'"Suzhou Museum" "lotus"','pillar':'"Suzhou Museum" "pearl"','silver':'"Suzhou Museum" "silver"','sword':'"Sword of Goujian"','bells':'"Bianzhong of Marquis Yi"','zun':'"Marquis Yi" "zun"','crane':'"Lotus and crane"','owl':'"Fu Hao" "zun"','flute':'"Jiahu" "flute"','gauze':'"Mawangdui" "gauze"','banner':'"Mawangdui" "banner"','coffin':'"Mawangdui" "coffin"'}
def f(it):
 k,q=it;p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':5,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1280,'format':'json','requestid':str(__import__('time').time())}
 try:
  r=urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p),headers={'User-Agent':'GuanwuMuseumGuide/2.0'});d=json.load(urllib.request.urlopen(r,timeout=40));a=list(d.get('query',{}).get('pages',{}).values());a.sort(key=lambda x:x.get('index',0));return k,a
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:r=dict(ex.map(f,qs.items()))
Path('research/expansion-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
for k,v in r.items():
 print(k,':', '\n '.join(x['title'] for x in v) if isinstance(v,list) else v)

