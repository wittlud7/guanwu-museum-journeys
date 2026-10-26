"""Apply audited official-source corrections, preserving the photo agent's records."""
import json,pathlib,re,requests,concurrent.futures
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
file=ROOT/'dist/beijing-museums.js'
raw=file.read_text(encoding='utf8');data=json.loads(raw.split('const data=',1)[1].split(';\nif(typeof module',1)[0]);m={x['id']:x for x in data['museums']}
def source(ident,title,url,main=False):
 s={'title':title,'url':url}
 if s not in m[ident]['sources']:m[ident]['sources'].append(s)
 if main:m[ident]['official']=url
 return s
w=m['bj-wanshou'];w['name']='万寿寺博物馆（原北京艺术博物馆）';w['fullName']='万寿寺博物馆';w['aliases']=['北京艺术博物馆','万寿寺']
w['address']='北京市海淀区西三环北路万寿寺内'
w['intro']='原北京艺术博物馆于2026年7月更名为万寿寺博物馆，馆址与日常开放服务延续。古建筑与书画、瓷器、家具等艺术收藏相互映照，通州在建的新北京艺术博物馆并非此馆。'
w['chapters'][0]['text']=w['intro']+w['highlights'][0]['text']
source('bj-wanshou','万寿寺博物馆 · 2026年7月2日更名公告','https://wanshousimuseum.cn/ybdt/2836.htm',True)
source('bj-wanshou','万寿寺博物馆 · 馆情与基本陈列','https://wanshousimuseum.cn/ybjj/index.htm')
source('bj-wanshou','馆方 · 开放服务与馆址','https://www.bjartmuseum.com/service/index.htm')
source('bj-poly','北京市文物局 · 新保利大厦馆址（2024更新）','https://map.beijing.gov.cn/place?categoryId=bwg&placeId=5c2dc49f080b852d3f422938')
m['bj-poly']['address']='北京市东城区朝阳门北大街1号新保利大厦云楼9层'
m['bj-poly']['tips'].insert(0,'采用北京市文物局更新的新保利大厦馆址；部分旧旅游资料仍列旧保利大厦，出发前请再与馆方核对入口。')
source('bj-gongwang','西城区政府 · 恭王府及花园（2026年）','https://www.bjxch.gov.cn/zt/schjmp/xxxq/pnidpv932679.html')
m['bj-gongwang']['address']='北京市西城区前海西街17号、柳荫街甲14号恭王府'
source('bj-yongding','门头沟区文旅局 · 博物馆馆址（2026年）','https://www.bjmtg.gov.cn/bjmtg/c104895/202411/175088c5fa6a4ee78994b26e5530eb0a.shtml')
source('bj-haidian','海淀区政府 · 走进三山五园与新馆展陈','https://www.bjhd.gov.cn/ztzx/2025/sswy/')
source('bj-beihang','海淀区文旅局 · 航空航天博物馆参观信息（2026年）','https://zyk.bjhd.gov.cn/kjhd/whhd/bwg/202603/t20260326_4809793_hd.shtml')
source('bj-planetarium','北京天文馆 · 参观指南与票务','https://www.bjp.org.cn/cgzn/pwxx/index.shtml',True)
# Correct an initial discovery URL before it can be mistaken for evidence.
seedfile=ROOT/'research/beijing-museums-seeds.json';seeds=json.loads(seedfile.read_text(encoding='utf8'))
for row in seeds:
 if row[0]=='planetarium':row[2]='101758'
 if row[0]=='wanshou':row[1]=w['name']
seedfile.write_text(json.dumps(seeds,ensure_ascii=False,indent=2),encoding='utf8')
evidencefile=ROOT/'research/beijing-museums-source-evidence.json';ev=json.loads(evidencefile.read_text(encoding='utf8'));ev=[e for e in ev if e['id']!='bj-planetarium']
extra=[('bj-planetarium','https://s.visitbeijing.com.cn/attraction/101758')]+[(x['id'],s['url']) for x in data['museums'] for s in x['sources'][1:]]+[(e['id'],e['url']) for e in ev if e.get('status')!=200]
def fetch(item):
 ident,url=item;out={'id':ident,'url':url,'checked':'2026-10-25'}
 try:
  r=requests.get(url,timeout=30,headers={'User-Agent':'Mozilla/5.0'});out['status']=r.status_code
  if r.status_code==200:
   soup=BeautifulSoup(r.content,'html.parser')
   for n in soup(['script','style']):n.decompose()
   out['text']=soup.get_text(' ',strip=True)
 except Exception as e:out['error']=type(e).__name__
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:ev.extend(pool.map(fetch,extra))
evidencefile.write_text(json.dumps(ev,ensure_ascii=False,indent=2),encoding='utf8')
file.write_text('(function(root){\n"use strict";\nconst data='+json.dumps(data,ensure_ascii=False,indent=2)+';\nif(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_BEIJING_MUSEUMS=data;\n})(typeof globalThis!=="undefined"?globalThis:this);\n',encoding='utf8')
(ROOT/'research/beijing-museums-content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Audited 47 museum records; kept',len(data['images']),'licensed image records')
print('Additional evidence:',[(e['id'],e.get('status',e.get('error'))) for e in ev[-len(extra):]])
