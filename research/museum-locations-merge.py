import json
from pathlib import Path
p=Path('research/museum-locations-reviewed.json');D=json.loads(p.read_text(encoding='utf8'));O=json.loads(Path('research/museum-locations-osm-reviewed.json').read_text(encoding='utf8'));N=json.loads(Path('research/museum-locations-nominatim.json').read_text(encoding='utf8'));X=json.loads(Path('research/museum-locations-osm-extra-reviewed.json').read_text(encoding='utf8'))
for mid,v in O.items():
 if 'error' in v:continue
 d=D[mid];d.pop('unavailable',None);d.update(lat=v['lat'],lng=v['lng'],source={'title':'OpenStreetMap · '+d['label']+'馆舍范围','url':v['source']},accuracyNote='按OpenStreetMap对应馆舍轮廓的经纬范围中心生成的区域参考点；不是实测游客入口、检票口或实时导航终点。')
for mid in ['hangzhou','shangdu']:
 a=next(x for x in N[mid] if x['category']=='tourism' and x['type']=='museum');assert a['osm_type'] in X[mid]['source'] and str(a['osm_id']) in X[mid]['source'];d=D[mid];d.pop('unavailable',None);d.update(lat=float(a['lat']),lng=float(a['lon']),source={'title':'OpenStreetMap · '+d['label']+'馆舍POI','url':X[mid]['source']},accuracyNote='OpenStreetMap对应博物馆建筑/馆区POI的参考点（Nominatim提供代表点），不是入口或导航终点。已区分同名公交站与博物馆实体。' if mid=='hangzhou' else 'OpenStreetMap对应博物馆馆区POI的参考点（Nominatim提供代表点），不是入口、检票口或实时导航终点。')
D['chengdu'].update(unavailable=True,source={'title':'成都青年志愿服务 · 场馆活动地点','url':'https://cdyouth.cdcyl.org.cn/volunteer/site/project/204094'},accuracyNote='地址存在未解决冲突：当前目录与志愿服务来源写草堂东路18号；唯一同名OSM馆点标为草堂东路2号，可能为旧址。未证实馆区一致，暂不提供经纬度；请按中文地址向馆方核实。')
for mid,d in D.items():
 if d.get('unavailable'):continue
 if d['source']['url'].startswith('https://www.wikidata.org'):
  d['accuracyNote']='Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。'+({'palace':'故宫点位在宫城区域内，不能用于判断入院方向。','shanghai':'固定为人民广场馆，非浦东东馆。','zhejiang-history':'固定为孤山馆区，非之江馆区。','nanyue':'固定为解放北路王墓展区，非中山四路王宫展区。','zhengzhou-museum':'固定为文翰街馆，非嵩山路馆。','xinhai':'固定为彭刘杨路南院，非武珞路北院。'}.get(mid,''))
 # Retain source precision, but never add decimals to coarse values.
 if isinstance(d.get('lat'),float):d['lat']=round(d['lat'],8)
 if isinstance(d.get('lng'),float):d['lng']=round(d['lng'],8)
p.write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8')
print('Reviewed',sum(not d.get('unavailable') for d in D.values()),'available',sum(bool(d.get('unavailable')) for d in D.values()),'unavailable')
