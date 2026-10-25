exec(open('research/city-museums-search-images.py',encoding='utf-8-sig').read().split('r={}')[0])
r=json.loads(Path('research/city-museums-image-candidates.json').read_text(encoding='utf8'))
for k,s in [('suzhou-garden','"苏州园林博物馆"'),('suzhou-silk-alt','"Silk Museum" Suzhou')]:
 _,r[k]=f((k,s));print(k,':',' | '.join(a['title'] for a in r[k]) if isinstance(r[k],list) else r[k],flush=True)
Path('research/city-museums-image-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
