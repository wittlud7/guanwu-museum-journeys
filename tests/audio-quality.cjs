async(page)=>{
 await page.goto('http://localhost:4173/');
 const report=await page.evaluate(async()=>{
  const manifest=await(await fetch('assets/audio/manifest.json')).json(),context=new AudioContext(),clips=[];
  for(const j of manifest.jobs){
   const response=await fetch('assets/audio/'+j.id+'.mp3');if(!response.ok)throw Error('Missing audio: '+j.id);
   const audio=await context.decodeAudioData(await response.arrayBuffer()),samples=audio.getChannelData(0);let power=0,peak=0,clipped=0;
   for(let i=0;i<samples.length;i++){const x=Math.abs(samples[i]);power+=x*x;peak=Math.max(peak,x);if(x>.999)clipped++}
   const rms=Math.sqrt(power/samples.length),ratio=clipped/samples.length;
   if(!(audio.duration>8&&audio.duration<120&&rms>.003&&rms<.8&&ratio<.01))throw Error('Invalid/silent/clipped audio: '+j.id);
   const meta=await(await fetch('assets/audio/'+j.id+'.json')).json();
   if(!meta.sentences.length||meta.sentences.at(-1).end>audio.duration+1)throw Error('Subtitle timing: '+j.id);
   clips.push({id:j.id,seconds:Math.round(audio.duration*100)/100,rms:Math.round(rms*1000)/1000,peak:Math.round(peak*1000)/1000});
  }
  await context.close();return {status:'passed',voice:manifest.voice,clips:clips.length,totalMinutes:Math.round(clips.reduce((n,c)=>n+c.seconds,0)/6)/10,details:clips};
 });
 return report;
}
