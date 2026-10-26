import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import collect_world_heritage_images as c
p=c.ROOT/'research/world-heritage-photo-candidates.json';data=json.loads(p.read_text(encoding='utf-8'))
for uid,q in [('1474','Hailongtun'),('1592','Liangzhu ancient city ruins'),('1765','Jingdezhen imperial kiln ruins')]:
 try:
  k,v=c.search((uid,q));data[k]=v;print(k,[(x['title'],x['license'],x['description'][:60]) for x in v['candidates']],flush=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 except Exception as e:print(type(e).__name__,str(e),flush=True)
