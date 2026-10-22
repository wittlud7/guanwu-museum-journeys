import urllib.request, json, concurrent.futures
from pathlib import Path
root=Path('dist/assets')
def fetch(oid):
    d=json.load(urllib.request.urlopen(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}',timeout=30))
    assert d['isPublicDomain'] and d['primaryImageSmall']
    urllib.request.urlretrieve(d['primaryImageSmall'],root/f'{oid}.jpg')
    return {k:d[k] for k in ['objectID','title','objectDate','medium','creditLine','objectURL','isPublicDomain','primaryImageSmall']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    data=list(pool.map(fetch,[53960,52930,49055,58526]))
(root/'sources.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
urllib.request.urlretrieve('https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=2000&q=85',root/'great-wall.jpg')
print('Downloaded 5 images; museum sources saved.')
