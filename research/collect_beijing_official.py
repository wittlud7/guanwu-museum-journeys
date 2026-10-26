import requests,json,concurrent.futures,pathlib,re,time
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parent
seeds=json.loads((root/'beijing-museums-seeds.json').read_text(encoding='utf8'))
def fetch(row):
 ident,name,url=row
 if not url.startswith('http'):url='https://s.visitbeijing.com.cn/attraction/'+url
 out={'id':'bj-'+ident,'name':name,'url':url,'checked':'2026-10-25'}
 try:
  r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=40)
  out['status']=r.status_code
  if r.status_code==200:
   soup=BeautifulSoup(r.content,'html.parser')
   for x in soup(['script','style']):x.decompose()
   txt=soup.get_text(' ',strip=True)
   i=txt.find('景区介绍')
   if i>=0:txt=txt[i:]
   out['text']=txt
 except Exception as e:out['error']=type(e).__name__
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:out=list(pool.map(fetch,seeds))
(root/'beijing-museums-source-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for x in out:
 t=x.get('text','');m=re.search(r'地址[:：]\s*([^。]{1,100})',t)
 print(x['id'],x.get('status',x.get('error')),m.group(0)[:100] if m else '',t[:650])
