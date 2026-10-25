exec(open('research/city-museums-search-images.py',encoding='utf-8-sig').read().split('r={}')[0])
r=json.loads(Path('research/city-museums-image-candidates.json').read_text(encoding='utf8'))
qs={'nanjing-museum':'"南京博物院"','six-dynasties':'"六朝博物馆"','chengdu-museum':'"成都博物馆"','sichuan-museum':'"四川博物院"','guangdong-museum':'"广东省博物馆"','nanyue':'"南越王博物馆"','xian-museum':'"西安博物院"','suzhou-silk':'"苏州丝绸博物馆"','suzhou-brick':'"御窑金砖"','xinhai':'"辛亥革命博物馆"','zhengzhou-museum':'"郑州博物馆"','shangdu':'"商都遗址博物院"','changsha-museum':'"长沙博物馆"','changsha-slips':'"长沙简牍博物馆"'}
for k,qv in qs.items():
 _,r[k]=f((k,qv));Path('research/city-museums-image-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(k,':',' | '.join(a['title'] for a in r[k]) if isinstance(r[k],list) else r[k],flush=True);time.sleep(2)
