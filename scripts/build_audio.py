"""Render the authored Mandarin guide with Edge's neural voice, offline at runtime.

OpenAI speech was attempted first; the configured API credential returned 401.
This alternative uses edge-tts (https://github.com/rany2/edge-tts), not OpenAI.
Only our original guide text is submitted; no visitor data is sent.
"""
import asyncio,json,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.runtime'))
import edge_tts
data=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./dist/heritage-data.js')))"],cwd=ROOT,encoding='utf-8'))
out=ROOT/'dist/assets/audio';out.mkdir(exist_ok=True,parents=True)
jobs=[]
for m in data['museums']:
 for i,c in enumerate(m['chapters']):jobs.append({'id':f"{m['id']}-{i}",'title':c['title'],'text':c['text']})
for c in data['crafts']:jobs.append({'id':'craft-'+c['id'],'title':c['title'],'text':c['audioText']})
VOICE='zh-CN-XiaoxiaoNeural';RATE='-8%'
async def render(job):
 dest=out/(job['id']+'.mp3');subtitle=out/(job['id']+'.json')
 fingerprint=hashlib.sha256((job['text']+VOICE+RATE).encode()).hexdigest()
 if dest.exists() and subtitle.exists() and json.loads(subtitle.read_text(encoding='utf-8')).get('hash')==fingerprint:
  print('CACHED',job['id'],flush=True);return
 for attempt in range(3):
  try:
   comm=edge_tts.Communicate(job['text'],VOICE,rate=RATE,boundary='SentenceBoundary');boundaries=[]
   with dest.open('wb') as f:
    async for chunk in comm.stream():
     if chunk['type']=='audio':f.write(chunk['data'])
     elif chunk['type'] in ('WordBoundary','SentenceBoundary'):boundaries.append({'start':round(chunk['offset']/1e7,3),'end':round((chunk['offset']+chunk['duration'])/1e7,3),'text':chunk['text']})
   assert dest.stat().st_size>3000
   subtitle.write_text(json.dumps({'hash':fingerprint,'voice':VOICE,'rate':RATE,'synthetic':True,'text':job['text'],'sentences':boundaries},ensure_ascii=False,indent=2),encoding='utf-8')
   print('OK',job['id'],dest.stat().st_size,flush=True);return
  except Exception:
   if attempt==2:raise
   await asyncio.sleep(2+attempt*3)
async def main():
 # Keep service requests modest; reuse all completed clips on a rerun.
 for job in jobs:
  await render(job);await asyncio.sleep(.5)
 (out/'manifest.json').write_text(json.dumps({'provider':'Microsoft Edge neural TTS via edge-tts','voice':VOICE,'rate':RATE,'disclosure':'AI 合成普通话导览，非真人录音或戏曲唱段','jobs':jobs},ensure_ascii=False,indent=2),encoding='utf-8')
asyncio.run(main())
