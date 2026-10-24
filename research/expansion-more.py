exec(open('research/expansion-search.py',encoding='utf-8-sig').read().split('with concurrent')[0])
r=json.loads(Path('research/expansion-candidates.json').read_text(encoding='utf8'))
import time
qs={'pot':'"鸳鸯"','pan':'"Zhong" "pan"','lotus':'"Suzhou" "celadon"','silver':'"Suzhou" "lian"','zun':'"Zeng" "zun"','owl':'"Henan" "owl"','gauze':'"Mawangdui" "gown"','banner':'"Mawangdui" "painting"','coffin':'"Mawangdui" "Second Coffin"'}
for k,q in qs.items():
 time.sleep(3);_,v=f((k,q));r[k]=v;Path('research/expansion-more-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(k,':', '\n '.join(x['title'] for x in v) if isinstance(v,list) else v,flush=True)
