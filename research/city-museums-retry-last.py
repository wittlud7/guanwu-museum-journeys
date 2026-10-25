exec(open('research/city-museums-search-images.py',encoding='utf-8-sig').read().split('r={}')[0])
r=json.loads(Path('research/city-museums-image-candidates.json').read_text(encoding='utf8'))
qs={'zhengzhou-museum':'"郑州博物馆"','shangdu':'"郑州商都遗址博物院"','suzhou-brick':'"Suzhou Imperial Kiln"'}
for k,s in qs.items():
 _,r[k]=f((k,s));Path('research/city-museums-image-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(k,':',' | '.join(a['title'] for a in r[k]) if isinstance(r[k],list) else r[k],flush=True);time.sleep(3)
