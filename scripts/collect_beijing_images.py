"""Fetch auditable Commons candidates, then reproduce only reviewed museum images.

Discovery input: research/beijing-photo-queries.json [{id,name,query}].
Reviewed input: research/beijing-museums-image-credits.json (keyed image records).
No unrelated fallback images are substituted when a museum has no suitable photo.
"""
import argparse, concurrent.futures, html, io, json, re, time
from pathlib import Path
import requests
from PIL import Image, ImageDraw

UA = 'GuanwuMuseumGuide/5.0 (educational museum guide; research contact guide@example.org)'
ROOT = Path(__file__).resolve().parents[1]

def plain(v):
    return html.unescape(re.sub('<[^>]+>', '', str(v))).strip()

def search(row):
    r = requests.get('https://commons.wikimedia.org/w/api.php', params={
        'action':'query','format':'json','generator':'search','gsrsearch':row['query'],
        'gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo','iiprop':'url|size|extmetadata',
        'iiurlwidth':640}, headers={'User-Agent':UA}, timeout=45)
    r.raise_for_status()
    candidates=[]
    for page in sorted(r.json().get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
        info=page.get('imageinfo',[{}])[0];meta=info.get('extmetadata',{})
        val=lambda k:plain(meta.get(k,{}).get('value',''))
        candidates.append({'title':page['title'],'original':info.get('url','').split('?')[0],
            'thumbnail':info.get('thumburl',''),'source':info.get('descriptionurl',''),
            'author':val('Artist'),'license':val('LicenseShortName'),'licenseUrl':val('LicenseUrl'),
            'description':val('ImageDescription'),'categories':val('Categories'),
            'width':info.get('width',0),'height':info.get('height',0)})
    return row['id'],dict(row,candidates=candidates)

def discover():
    rows=json.loads((ROOT/'research/beijing-photo-queries.json').read_text(encoding='utf-8'))
    output={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for future in concurrent.futures.as_completed([pool.submit(search,row) for row in rows]):
            try:
                key,value=future.result();output[key]=value;print(key,len(value['candidates']),flush=True)
            except Exception as exc:print('SEARCH FAILED',type(exc).__name__,str(exc),flush=True)
    target=ROOT/'research/beijing-photo-candidates.json'
    target.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')

def download(entry):
    key,v=entry;target=ROOT/'dist'/v['src'];target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        original=v['original'].split('?')[0];prefix,filename=original.rsplit('/',1)
        thumb=prefix.replace('/commons/','/commons/thumb/')+'/'+filename+'/960px-'+filename
        for url in [thumb,original,original]:
            try:
                response=requests.get(url,headers={'User-Agent':UA},timeout=50);response.raise_for_status()
                im=Image.open(io.BytesIO(response.content)).convert('RGB');im.thumbnail((960,960))
                im.save(target,quality=81,optimize=True)
                if target.stat().st_size>220000:im.save(target,quality=70,optimize=True)
                break
            except Exception as exc:
                print('RETRY',key,type(exc).__name__,str(exc)[:100],flush=True)
                time.sleep(3)
        else:raise RuntimeError('Missing reviewed photo '+key)
    with Image.open(target) as im:
        v['width'],v['height']=im.size;im.verify()
    print('VERIFIED',key,target.stat().st_size,flush=True)
    return key,v

def reproduce():
    path=ROOT/'research/beijing-museums-image-credits.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    results={}
    for entry in data.items():
        key,value=download(entry);results[key]=value;time.sleep(0.7)
    path.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    cols=5;w=230;h=175;sheet=Image.new('RGB',(cols*w,((len(results)+cols-1)//cols)*h),'#ece8de');draw=ImageDraw.Draw(sheet)
    for i,(key,v) in enumerate(results.items()):
        im=Image.open(ROOT/'dist'/v['src']);im.thumbnail((220,145));x=(i%cols)*w;y=(i//cols)*h
        sheet.paste(im,(x+(w-im.width)//2,y));draw.text((x+5,y+148),key,fill='#222222')
    sheet.save(ROOT/'research/beijing-museums-contact.jpg',quality=90)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--discover',action='store_true');args=p.parse_args()
    discover() if args.discover else reproduce()
