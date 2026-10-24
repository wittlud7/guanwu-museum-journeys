exec(open('research/expansion-search.py',encoding='utf-8-sig').read().split('with concurrent')[0])
import time
r={}
for k,q in {'pan':'intitle:子仲姜','lotus':'intitle:莲花 intitle:碗','silver':'intitle:银奁','owl':'intitle:妇好','crane':'"Henan" "lotus"'}.items():
 time.sleep(2);_,r[k]=f((k,q));print(k,':', '\n '.join(x['title'] for x in r[k]) if isinstance(r[k],list) else r[k],flush=True)
Path('research/expansion-last-candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
