"""Find licensed reference photographs; selection is reviewed before downloading."""
import urllib.request,urllib.parse,json,concurrent.futures
from pathlib import Path
QUERIES={
 'beijing':'"China National Arts and Crafts Museum"',
 'hangzhou':'"Zhejiang Intangible"',
 'hangzhou2':'"之江文化中心"',
 'nanjing':'"Yunjin"',
 'chengdu':'"Shu brocade"',
 'guangzhou':'"Cantonese Opera Art Museum"',
 'cloisonne':'"cloisonne" "China"',
 'papercut':'"Chinese paper cutting"',
 'silk':'"silk weaving" "China"',
 'woodblock':'"woodblock printing" "China"',
 'opera':'"Cantonese opera" costumes',
 'embroidery':'"Shu embroidery"',
}
def search(item):
 key,q=item
 params={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1400,'format':'json'}
 req=urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),headers={'User-Agent':'GuanwuMuseumGuide/1.0 educational prototype'})
 try:
  data=json.load(urllib.request.urlopen(req,timeout=40));pages=list(data.get('query',{}).get('pages',{}).values());pages.sort(key=lambda p:p.get('index',0));return key,pages
 except Exception as e:return key,{'error':str(e)}
Path('research').mkdir(exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=dict(pool.map(search,QUERIES.items()))
Path('research/image-candidates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for key,pages in results.items():
 print('\n'+key)
 if isinstance(pages,list):
  for p in pages:
   i=p['imageinfo'][0];print(p['title'],i.get('extmetadata',{}).get('LicenseShortName',{}).get('value',''))
 else: print(pages)
