"""Discover and reproduce reviewed Wikimedia Commons world-heritage photos.
Commons file descriptions and license metadata are retained in research evidence.
"""
import argparse, concurrent.futures, html, io, json, re, time
from pathlib import Path
import requests
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
UA='GuanwuMuseumGuide/5.0 (educational museum guide; research contact guide@example.org)'
def plain(v): return html.unescape(re.sub('<[^>]+>','',str(v))).strip()
QUERIES={
'1442':'Wild Goose Pagoda Xian','437':'Mount Tai temple','438':'Great Wall Mutianyu','439':'Forbidden City Beijing palace','440':'Mogao Caves exterior','441':'Terracotta Army Xian','449':'Zhoukoudian Peking Man site','703':'Chengde Mountain Resort','704':'Temple Confucius Qufu','705':'Wudang Mountains Golden Hall','707':'Potala Palace Lhasa','778':'Lushan National Park China','779':'Leshan Giant Buddha','812':'Pingyao ancient city','813':'Humble Administrators Garden Suzhou','880':'Summer Palace Beijing','881':'Temple of Heaven Beijing','912':'Dazu Rock Carvings Baodingshan','1001':'Dujiangyan irrigation system','1002':'Hongcun village Anhui','1003':'Longmen Grottoes Fengxian','1004':'Ming Xiaoling mausoleum','1039':'Yungang Grottoes','1110':'Ruins Saint Paul Macau','1114':'Yinxu ruins Anyang','1135':'Wunu Mountain City','1112':'Kaiping Diaolou Zili','1113':'Tianluokeng Tulou','1279':'Mount Wutai temple','1305':'Dengfeng Shaolin Pagoda Forest','1334':'West Lake Hangzhou','1389':'Xanadu site ruins','1111':'Honghe Hani Rice Terraces','547':'Huangshan mountain','811':'Lijiang old town','1474':'Laosicheng ruins','1508':'Huashan rock art','1541':'Gulangyu island Xiamen','1443':'Grand Canal Hangzhou Gongchen Bridge','911':'Wuyi Mountains Jiuqu','1592':'Liangzhu archaeological site park','1561':'Quanzhou Kaiyuan Temple','1665':'Jingmai mountain tea forest','1714':'Beijing Central Axis Jingshan','1736':'Western Xia tombs','1765':'Jingdezhen Imperial Kiln Museum'}
def search(entry):
 key,query=entry
 time.sleep(3)
 r=requests.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','format':'json','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':5,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':500},headers={'User-Agent':UA},timeout=60);r.raise_for_status()
 values=[]
 for p in sorted(r.json().get('query',{}).get('pages',{}).values(),key=lambda p:p.get('index',0)):
  i=p.get('imageinfo',[{}])[0];m=i.get('extmetadata',{});val=lambda k:plain(m.get(k,{}).get('value',''))
  values.append({'title':p['title'],'original':i.get('url',''),'thumbnail':i.get('thumburl',''),'source':i.get('descriptionurl',''),'author':val('Artist'),'license':val('LicenseShortName'),'licenseUrl':val('LicenseUrl'),'description':val('ImageDescription'),'categories':val('Categories'),'width':i.get('width',0),'height':i.get('height',0),'extmetadata':m})
 return key,{'query':query,'candidates':values}
def discover():
 target=ROOT/'research/world-heritage-photo-candidates.json';out=json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
 with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
  for f in concurrent.futures.as_completed([pool.submit(search,e) for e in QUERIES.items() if e[0] not in out]):
   try:k,v=f.result();out[k]=v;target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(k,len(v['candidates']),flush=True)
   except Exception as e:print('SEARCH FAILED',type(e).__name__,str(e),flush=True)
def reproduce():
 path=ROOT/'research/world-heritage-image-credits.json';data=json.loads(path.read_text(encoding='utf-8'))
 for k,v in data.items():
  target=ROOT/'dist'/v['src'];target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():
   original=v['original'].split('?')[0];prefix,name=original.rsplit('/',1);thumb=prefix.replace('/commons/','/commons/thumb/')+'/'+name+'/960px-'+name
   for url in [thumb,original,original]:
    try:
     r=requests.get(url,headers={'User-Agent':UA},timeout=60);r.raise_for_status();im=Image.open(io.BytesIO(r.content)).convert('RGB');im.thumbnail((960,960));im.save(target,quality=78,optimize=True)
     if target.stat().st_size>180000:im.save(target,quality=65,optimize=True)
     break
    except Exception as e:print('RETRY',k,type(e).__name__,flush=True);time.sleep(2)
   else:raise RuntimeError('No image '+k)
  with Image.open(target) as im:v['width'],v['height']=im.size;im.verify()
  print('VERIFIED',k,target.stat().st_size,flush=True);time.sleep(.25)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 cols=5;w=230;h=180;sheet=Image.new('RGB',(cols*w,((len(data)+cols-1)//cols)*h),'#eee9df');d=ImageDraw.Draw(sheet)
 for n,(k,v) in enumerate(data.items()):
  im=Image.open(ROOT/'dist'/v['src']);im.thumbnail((220,150));x=n%cols*w;y=n//cols*h;sheet.paste(im,(x+(w-im.width)//2,y));d.text((x+5,y+153),k,fill='#222')
 sheet.save(ROOT/'research/world-heritage-contact.jpg',quality=90)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--discover',action='store_true');a=p.parse_args();discover() if a.discover else reproduce()
