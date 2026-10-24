exec(open('research/expansion-search.py',encoding='utf-8-sig').read().split('with concurrent')[0])
r=json.loads(Path('research/expansion-candidates.json').read_text(encoding='utf8'))
qs={k:v for k,v in qs.items() if isinstance(r[k],dict)}
qs['pot']='"鸳鸯莲瓣"';qs['pan']='"子仲姜盘"';qs['measure']='"商鞅方升"';qs['lotus']='"莲花碗"';qs['pillar']='"真珠舍利宝幢"';qs['silver']='"Suzhou" "silver lian"';qs['owl']='"Henan" "owl"';qs['flute']='"Jiahu"';qs['gauze']='"素纱"'
import time
for k,q in qs.items():
 time.sleep(2);_,v=f((k,q));r[k]=v;Path('research/expansion-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(k,':', '\n '.join(x['title'] for x in v) if isinstance(v,list) else v,flush=True)
