"""Review manifest and reproducible coordinates from preserved primary records. No geocoding guesses."""
import json,math,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parent.parent
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
# Immutable reviewed ID/name snapshot owned by this coordinate workflow.
# Photo query candidates and content seeds are independently edited and not inputs.
catalog=read('research/beijing-locations-catalog.json')
assert len(catalog)==47 and len({m['id'] for m in catalog})==47
entities=read('research/beijing-locations-wikidata.json')['entities']
mapping={
'capital':'Q1189666','grand-canal':'Q105718642','art':'Q233705','geology':'Q585544',
'paleozoo':'Q846592','science':'Q1074292','military':'Q1789184','planetarium':'Q4348118','nature':'Q846583',
'wanshou':'Q2063448','architecture':'Q341718','stone':'Q1208573','luxun':'Q4881160','xubeihong':'Q11070647',
'guomoruo':'Q4165193','meilanfang':'Q4165212','laoshe':'Q10902396','folk':'Q814721','opera':'Q24131484',
'gongwang':'Q2666344','guozijian':'Q28417597','guanfu':'Q15310035','poly':'Q18651572','zitan':'Q126373489',
'garden':'Q18651344','film':'Q5099799','railway':'Q1074280','auto':'Q16928682','beihang':'Q10902402',
'civil-aviation':'Q65171962','printing':'Q9384146','women':'Q4306266','overseas':'Q28418208','customs':'Q19851717',
'coins':'Q10874154','ethnic':'Q1791802','literature':'Q10873917','tsinghua':'Q28412420','yunju':'Q1528443'}
osm={}
for f in ['research/beijing-locations-nominatim.json','research/beijing-locations-nominatim-extra.json']:
    osm.update({k:v[0] for k,v in read(f).items() if isinstance(v,list) and v})
approved_osm={'bj-bells':1303228717,'bj-red-chamber':24825443,'bj-zhoukoudian':1090515798,'bj-archaeology':610079824,'bj-agriculture':129187924,'bj-dabaotai':1012672989}
notes={
'bj-wanshou':'万寿寺内的北京艺术博物馆馆区；不是未来建设中的同名新美术馆。',
'bj-architecture':'先农坛馆区参考点；不代表太岁殿入口。',
'bj-stone':'真觉寺馆区参考点；不代表金刚宝座塔或游客入口。',
'bj-folk':'东岳庙馆区参考点。',
'bj-yunju':'云居寺馆区参考点；石经陈列及具体入口须另查馆方导览。',
'bj-tsinghua':'Wikidata 原始精度约 0.0117°，仅作馆区示意；不代表校门或游客入口。',
'bj-science':'已排除北三环北京科学中心旧馆点，选择奥林匹克公园现馆。',
'bj-luxun':'阜成门宫门口鲁迅馆区参考点；非新街口八道湾旧居。',
'bj-railway':'酒仙桥北路东郊展馆参考点；非正阳门展馆。',
'bj-red-chamber':'博物馆所在北京大观园园区的参考点，非单独展厅位置。',
'bj-agriculture':'全国农业展览馆与中国农业博物馆同址园区参考点；Wikidata 两个冲突候选已弃用。',
'bj-dabaotai':'大葆台遗址博物馆馆区参考点；不是旧版粗精度汉墓坐标。',
'bj-zhoukoudian':'独立博物馆馆舍参考点，非猿人洞或世界遗产遗址总点。'}
out={}
for m in catalog:
    mid=m['id'];k=mid.removeprefix('bj-')
    d={'coordinateSystem':'WGS84','label':m['name'],'checked':'2026-10-25'}
    if k in mapping:
        q=mapping[k];claims=[c for c in entities[q]['claims'].get('P625',[]) if c.get('rank')!='deprecated' and c['mainsnak'].get('datavalue',{}).get('value',{}).get('globe')=='http://www.wikidata.org/entity/Q2']
        if mid=='bj-science':claims=[c for c in claims if c['mainsnak']['datavalue']['value']['latitude']>40]
        assert len(claims)==1,(mid,len(claims))
        val=claims[0]['mainsnak']['datavalue']['value']
        d.update(lat=val['latitude'],lng=val['longitude'],sourcePrecisionDegrees=val['precision'],source={'title':'Wikidata · '+m['name']+'（P625）','url':'https://www.wikidata.org/wiki/'+q})
        d['accuracyNote']=notes.get(mid,'')+'Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。'
    elif mid in approved_osm:
        val=osm[mid];assert val['osm_type']=='way' and val['osm_id']==approved_osm[mid]
        raw=ET.fromstring((root/f'research/beijing-locations-osm-{mid}.xml').read_bytes());way=raw.find('way');assert int(way.attrib['id'])==val['osm_id'];tags={t.attrib['k']:t.attrib['v'] for t in way.findall('tag')}
        assert tags.get('name')==val['name'],(mid,tags.get('name'),val['name'])
        d.update(lat=float(val['lat']),lng=float(val['lon']),source={'title':'OpenStreetMap · '+val['name'],'url':'https://www.openstreetmap.org/way/'+str(val['osm_id'])})
        d['accuracyNote']=notes.get(mid,'')+'OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。'
    else:
        assert mid in ['bj-haidian','bj-yongding'],mid
        d['unavailable']=True
        d['accuracyNote']='三山五园文化艺术中心新馆尚无可靠公开 WGS84 点位；已拒绝旧海淀馆坐标，先按最新中文馆址查询。' if mid=='bj-haidian' else '尚未取得可核验的场馆 WGS84 点位，先按中文馆址查询；不使用河流或门头沟区中心点代替。'
    if not d.get('unavailable'):assert 39.4<d['lat']<41.1 and 115.4<d['lng']<117.6
    out[mid]=d
assert len(out)==47 and sum(not x.get('unavailable') for x in out.values())==45
(root/'dist/beijing-locations.js').write_text('(function(root){\n"use strict";\nconst data='+json.dumps(out,ensure_ascii=False,indent=2)+';\nif(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_BEIJING_LOCATIONS=data;\n})(typeof window!=="undefined"?window:globalThis);\n',encoding='utf-8')
(root/'research/beijing-locations-reviewed.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 47 museum IDs; 45 source-verified WGS84 reference points; 2 explicitly unavailable.')
