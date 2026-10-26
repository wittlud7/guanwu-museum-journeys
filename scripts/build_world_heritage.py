"""Build original Chinese reading notes from frozen UNESCO official evidence.

Rebuild only: downloading/updating source evidence is a separate reviewed action.
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'research/world-heritage'
rows = json.loads((EVIDENCE / 'china-unesco-rows.json').read_text(encoding='utf-8'))
rows = {x['id_number']: x for x in rows if x['category'] in ('Cultural', 'Mixed')}
curation = []
keys = ['unescoId', 'name', 'provinces', 'cities', 'theme', 'title1', 'text1', 'title2', 'text2', 'title3', 'text3']
for line in (EVIDENCE / 'curation.txt').read_text(encoding='utf-8').splitlines():
    fields = line.split('|')
    assert len(fields) == len(keys)
    curation.append(dict(zip(keys, fields)))
assert len(curation) == len(rows) == 46
assert set(x['unescoId'] for x in curation) == set(rows)
(EVIDENCE / 'curation.json').write_text(json.dumps(curation, ensure_ascii=False, indent=2), encoding='utf-8')

RELATED = {
    '439': ['palace'], '449': ['bj-zhoukoudian'], '813': ['suzhou', 'suzhou-garden'],
    '1443': ['bj-grand-canal', 'zhejiang-history'], '441': ['xian'], '1442': ['xian-museum', 'national-silk'],
    '1114': ['zhengzhou'], '1592': ['zhejiang-history'], '1714': ['palace', 'national-china', 'bj-architecture'],
}
NOTES = {
    '438': '本页省份仅列已核实的北京、河北、甘肃代表地区，非全部长城分布。中国长城资源分布于十五个省级行政区；资源分布不等于每段均在世界遗产认定边界内。本页按一项遗产介绍，未逐段收录。',
    '439': '北京故宫与沈阳故宫共同组成一项遗产；两地分开管理与预约。',
    '707': '包含布达拉宫、大昭寺与罗布林卡；本页整体计一项，未逐座展开管理入口。',
    '779': '峨眉山与乐山大佛共同组成一项混合遗产，两地不是同一参观入口。',
    '813': '这项串联遗产由九座列入名录的苏州古典园林组成；并非全苏州所有园林。',
    '1004': '明清皇家陵寝跨北京、河北、辽宁、江苏、湖北，由多处陵寝组成；整体计一项，未逐陵收录。',
    '1135': '辽宁桓仁与吉林集安的三座王城遗址及相关王陵、贵族墓葬共同组成一项遗产。',
    '1474': '湖南老司城、湖北唐崖土司城址、贵州海龙屯共同组成一项遗产；整体计一项。',
    '1442': '中国、哈萨克斯坦、吉尔吉斯斯坦三国共有三十三个组成部分，其中中国二十二处，位于陕西、河南、甘肃、新疆。本页按一项跨国遗产介绍，非全部丝绸之路遗址名录。',
    '1443': '大运河串联北京、天津、河北、山东、江苏、浙江、河南、安徽八省市的选定河段及相关遗存。整项计一项，非沿线所有河道均属世界遗产。',
    '911': '武夷山为跨福建、江西的混合遗产；省份按已核实的遗产组成区域标示。',
    '1561': '二十二个遗产组成点共同构成一项遗产，覆盖城市管理、生产、交通和宗教等系统，未逐点制作独立条目。',
    '1714': '由十五个组成部分构成一项遗产；与故宫、天坛等已有遗产存在空间关联，不能将组成部分重复计作新增世遗项目。',
    '1765': '五个组成部分包括城区制瓷中心、湖田古窑址、高岭瓷土矿业遗址、长岭瓷石矿业遗址、蛟潭柴薪产地，整体计一项。',
}
CHAPTER_QUESTIONS = [
    '现场可以先退后几步看整体，再靠近观察细节。试着记录：眼前哪些部分彼此依存，哪些边界需要借助遗址图才能辨认？这是一条观察提示，不代表现场所有区域都已开放。',
    '选择一个可见细节，写下你实际看到的形状、材料或位置，再把它与说明牌上的年代和用途对照。把直接观察与自己的解释分开记录，会让这次观看更清楚。',
    '离开之前，可以画一张简单的关系图，标出人、建筑与环境怎样联系。本文提供的是遗产理解线索；当日开放、预约、交通及保护要求，请以具体管理机构发布的信息为准。',
]
sites = []
briefs = {}
for c in curation:
    uid = c['unescoId']; r = rows[uid]; official = f'https://whc.unesco.org/en/list/{uid}/'
    soup = BeautifulSoup((EVIDENCE / f'{uid}.html').read_text(encoding='utf-8'), 'html.parser')
    heading = soup.select_one('h1')
    english = heading.get_text(' ', strip=True) if heading else BeautifulSoup(r['site'], 'html.parser').get_text()
    # Actual property h1 is the name, not the navigation heading.
    if len(english) < 4 or english in ('World Heritage', 'UNESCO'): english = BeautifulSoup(r['site'], 'html.parser').get_text()
    for container in soup.select('.rich-text'):
        t = container.get_text(' ', strip=True)
        if t.startswith('Brief synthesis'): briefs[uid] = t; break
    source = {'title': 'UNESCO 世界遗产中心｜' + c['name'], 'url': official}
    map_data = json.loads((EVIDENCE / f'map-{uid}.json').read_text(encoding='utf-8'))
    query = map_data.get('QUERYRESULT', {})
    components = [dict(zip([k.lower() for k in query.get('COLUMNS', [])], row)) for row in query.get('DATA', [])]
    chinese = [x for x in components if 'China' in str(x.get('stateparty', ''))]
    point = (chinese or components or [None])[0]
    location = {'unavailable': True, 'note': '未提供可靠公开参考坐标，请按官方入口信息安排行程。'}
    if point and point.get('latitude') is not None and point.get('longitude') is not None:
        location = {'lat': float(point['latitude']), 'lng': float(point['longitude']), 'datum': 'WGS84',
                    'label': point.get('name', c['name']), 'note': 'UNESCO 遗产或组成部分参考点，不是入口、停车场或精确导航终点。',
                    'source': {'title': 'UNESCO 官方地图数据', 'url': f'https://whc.unesco.org/?cid=31&l=en&id_site={uid}&mode=json'}}
    intro = c['text1'] + c['text3']
    category = r['category'].lower()
    narration = f"{c['name']}，{r['date_inscribed']}年列入世界{'文化与自然双重' if category == 'mixed' else '文化'}遗产。{c['text1']}{c['text2']}参观时，可以先看整体，再选择一个细节慢慢观察。具体开放与预约，请以管理机构信息为准。"
    site = {'id': 'wh-' + uid, 'unescoId': uid, 'name': c['name'], 'englishName': english,
            'category': category, 'year': int(r['date_inscribed']), 'provinces': c['provinces'].split(','),
            'cities': c['cities'].split(','), 'theme': c['theme'], 'intro': intro, 'narrationText': narration,
            'highlights': [{'title': c[f'title{i}'], 'text': c[f'text{i}'], 'source': source} for i in range(1, 4)],
            'chapters': [{'title': c[f'title{i}'], 'text': c[f'text{i}'] + CHAPTER_QUESTIONS[i-1], 'audio': False, 'source': source} for i in range(1, 4)],
            'tips': ['遗产条目提供知识导览；当日开放、预约、门票及参观入口请查管理机构官方公告。', '坐标是遗产参考点，分散组成部分应分别确认位置与交通；不建议据此直接徒步前往。', '遵守保护步道与拍摄规定，尊重当地居民和仍在延续的宗教、生产与生活秩序。'],
            'official': official, 'sources': [source], 'cover': None, 'gallery': [], 'image': 'wh-' + uid + '-photo',
            'location': location, 'relatedMuseums': RELATED.get(uid, []),
            'componentsNote': NOTES.get(uid, '本页按 UNESCO 一项正式列入名录的遗产介绍；参考点不表示遗产完整边界或全部开放区域。'),
            'provinceScope': '已核实遗产所在地；长城仅列代表地区，串联项目不表示全部组成部分已逐一收录。',
            'components': [{'name': x.get('name'), 'serialNumber': x.get('serial_number'), 'country': x.get('stateparty'), 'lat': x.get('latitude'), 'lng': x.get('longitude')} for x in components]}
    if uid == '438':
        site['resourceProvinces'] = '北京,天津,河北,山西,内蒙古,辽宁,吉林,黑龙江,山东,河南,陕西,甘肃,青海,宁夏,新疆'.split(',')
        site['resourceProvincesNote'] = '国家文物局长城资源分布口径，不等于世界遗产认定边界。'
        site['sources'].append({'title': '北京市文物局｜长城资源分布说明', 'url': 'https://wwj.beijing.gov.cn/bjww/wwjzzcslm/1737418/1738088/1742735/364326/index.html'})
    sites.append(site)
sites.sort(key=lambda x: (x['year'], int(x['unescoId'])))
data = {'updated': '2026-10-26', 'source': 'https://whc.unesco.org/en/statesparties/cn', 'scope': '中国列入 UNESCO 世界遗产名录的文化遗产与混合遗产；不含自然遗产、预备名单或非物质文化遗产。', 'counts': {'cultural': 42, 'mixed': 4, 'total': 46}, 'sites': sites}
credits_path = ROOT / 'research/world-heritage-image-credits.json'
if credits_path.exists():
    data['images'] = json.loads(credits_path.read_text(encoding='utf-8'))
    for site in data['sites']:
        if site['image'] in data['images']:
            site['cover'] = site['image']; site['gallery'] = [site['image']]
out = '(function(root){"use strict";const data=' + json.dumps(data, ensure_ascii=False, indent=2) + ';if(typeof module==="object"&&module.exports)module.exports=data;root.GUANWU_WORLD_HERITAGE=data;})(typeof globalThis!=="undefined"?globalThis:this);\n'
(ROOT / 'dist/world-heritage-data.js').write_text(out, encoding='utf-8')
(EVIDENCE / 'official-brief-syntheses.json').write_text(json.dumps(briefs, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Built {len(sites)} sites, {sum(len(x["highlights"]) for x in sites)} highlights; coordinates {sum("lat" in x["location"] for x in sites)}.')
