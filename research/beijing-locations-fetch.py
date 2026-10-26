import json,time,requests
from pathlib import Path
names={'bj-red-chamber':'北京大观园','bj-yongding':'永定河文化博物馆 北京 门头沟','bj-haidian':'三山五园文化艺术中心','bj-archaeology':'中国考古博物馆 北京','bj-agriculture':'中国农业博物馆','bj-dabaotai':'北京大葆台遗址博物馆'}
out={}
for k,n in names.items():
    try:
        r=requests.get('https://nominatim.openstreetmap.org/search',params={'q':n,'format':'jsonv2','countrycodes':'cn','limit':4},headers={'User-Agent':'GuanwuMuseumSourceVerification/1.0'},timeout=30);r.raise_for_status();out[k]=r.json()
    except Exception as e:out[k]={'error':str(e)}
    time.sleep(1.1)
Path('research/beijing-locations-nominatim-extra.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in out.items():print(k,v)
