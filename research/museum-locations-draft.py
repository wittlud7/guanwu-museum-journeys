import json
from pathlib import Path
C=json.loads(Path('research/museum-locations-catalog.json').read_text(encoding='utf8'));P=json.loads(Path('research/museum-locations-wikipedia-items.json').read_text(encoding='utf8'))['query'];E=json.loads(Path('research/museum-locations-wikidata.json').read_text(encoding='utf8'))['entities']
rename={'beijing':'中国工艺美术馆','hangzhou':'浙江省非物质文化遗产馆','chengdu':'成都蜀锦织绣博物馆','xinhai':'辛亥革命博物馆','nanyue':'南越王博物院王墓展区','changsha-museum':'长沙市博物馆','changsha':'湖南省博物馆'}
bytitle={p['title']:p.get('pageprops',{}).get('wikibase_item') for p in P['pages'].values()};out={}
for m in C:
 title=rename.get(m['id'],m['name']);q=bytitle.get(title);e=E.get(q,{})
 label=m['name'];address=m['address']
 branches={'shanghai':('上海博物馆 · 人民广场馆','上海市黄浦区人民大道201号'),'zhejiang-history':('浙江省博物馆 · 孤山馆区','杭州市西湖区孤山路25号'),'nanyue':('南越王博物院 · 王墓展区','广州市解放北路867号'),'zhengzhou-museum':('郑州博物馆 · 文翰街馆','郑州市中原区文翰街9号'),'xinhai':('辛亥革命博物院 · 南院','武汉市武昌区彭刘杨路258号')}
 if m['id'] in branches:label,address=branches[m['id']]
 v={'coordinateSystem':'WGS84','label':label,'address':address,'accuracyNote':'场馆区域参考点，不代表游客入口、检票口或可步行到达位置；不用于承诺实时导航。'}
 coords=[s['mainsnak'].get('datavalue',{}).get('value') for s in e.get('claims',{}).get('P625',[]) if s.get('rank')!='deprecated'];coords=[x for x in coords if x and x.get('globe')=='http://www.wikidata.org/entity/Q2']
 if coords and m['id']!='shanghai-nature':
  v.update(lat=coords[0]['latitude'],lng=coords[0]['longitude'],source={'title':'Wikidata · '+label+'（P625）','url':'https://www.wikidata.org/wiki/'+q})
 else:v.update(unavailable=True,accuracyNote='坐标待馆区核实；尚未提供地图参考点，不估算或使用拍摄者位置替代馆入口。')
 if m['id']=='shanghai-nature':v['accuracyNote']='Wikidata坐标指向旧馆一带，与北京西路510号新馆不匹配，已拒绝使用，正在核实新馆。'
 out[m['id']]=v
Path('research/museum-locations-reviewed.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
Path('dist/museum-locations.js').write_text('(function(root){"use strict";const data='+json.dumps(out,ensure_ascii=False,indent=2)+';if(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_LOCATIONS=data;})(typeof window!=="undefined"?window:globalThis);',encoding='utf8')
print('DRAFT',sum(not v.get('unavailable') for v in out.values()),'verified data points; pending',[k for k,v in out.items() if v.get('unavailable')])
