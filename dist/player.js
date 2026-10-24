/* A single persistent player. Navigation never creates overlapping audio. */
(function(root){
'use strict';
class GuidePlayer{
 constructor(audio,options={}){
  this.audio=audio;this.options=options;this.queue=[];this.owner=null;this.index=0;this.loading=false;this.seeking=false;
  this.rate=1;this.pendingSeek=0;this.seekOnLoad=false;this.lastSaved=0;this.bookmarks={};this.subtitles=[];
  try{this.bookmarks=JSON.parse(localStorage.getItem('guanwu-audio-v2')||'{}');this.rate=Number(localStorage.getItem('guanwu-rate-v2'))||1}catch{}
  if(![.8,1,1.2,1.5].includes(this.rate))this.rate=1;
  audio.addEventListener('loadedmetadata',()=>{if(this.seekOnLoad){audio.currentTime=Math.min(this.pendingSeek,Math.max(0,audio.duration-.2));this.seekOnLoad=false}this.loading=false;this.emit()});
  audio.addEventListener('timeupdate',()=>{if(!this.seeking)this.emit();if(Date.now()-this.lastSaved>2000){this.save();this.lastSaved=Date.now()}});
  for(const evt of ['play','pause','ratechange'])audio.addEventListener(evt,()=>this.emit());
  audio.addEventListener('waiting',()=>{this.loading=true;this.emit()});audio.addEventListener('playing',()=>{this.loading=false;this.emit()});
  audio.addEventListener('error',()=>{this.loading=false;this.options.onError?.('音频暂未加载成功，请检查网络后重试。');this.emit()});
  audio.addEventListener('ended',()=>{this.save();if(this.index+1<this.queue.length&&this.options.canPlay?.(this.index+1)!==false)this.load(this.index+1,true);else this.emit()});
  window.addEventListener('pagehide',()=>this.save());
 }
 select(owner,queue,index=0,autoplay=true){
  if(this.options.canPlay?.(index)===false){this.options.onLocked?.();return}
  if(this.owner?.id===owner.id&&this.index===index){if(autoplay)this.toggle();return}
  this.save();this.owner=owner;this.queue=queue;this.load(index,autoplay,true);
 }
 load(index,autoplay,skipSave=false){
  if(index<0||index>=this.queue.length)return;
  if(this.options.canPlay?.(index)===false){this.options.onLocked?.();return}
  if(!skipSave)this.save();this.audio.pause();this.index=index;this.loading=true;
  const track=this.queue[index],mark=this.bookmarks[this.owner.id];
  this.pendingSeek=mark?.index===index?mark.time:0;this.seekOnLoad=true;
  this.audio.src=track.src;this.audio.playbackRate=this.rate;this.audio.load();this.subtitles=[];
  const key=track.src;fetch(track.src.replace(/\.mp3$/,'.json')).then(r=>r.ok?r.json():null).then(d=>{if(key===this.queue[this.index]?.src){this.subtitles=d?.sentences||[];this.emit()}}).catch(()=>{});
  if('mediaSession'in navigator&&typeof MediaMetadata!=='undefined'){
   navigator.mediaSession.metadata=new MediaMetadata({title:track.title,artist:'观物 · AI 合成普通话导览',album:this.owner.title});
   navigator.mediaSession.setActionHandler('play',()=>this.play());navigator.mediaSession.setActionHandler('pause',()=>this.audio.pause());
   navigator.mediaSession.setActionHandler('seekbackward',()=>this.skip(-15));navigator.mediaSession.setActionHandler('seekforward',()=>this.skip(15));
   navigator.mediaSession.setActionHandler('nexttrack',()=>this.load(this.index+1,true));navigator.mediaSession.setActionHandler('previoustrack',()=>this.load(this.index-1,true));
  }
  this.emit();if(autoplay)this.play();
 }
 async play(){try{await this.audio.play()}catch(e){if(e.name!=='AbortError'){this.loading=false;this.emit();this.options.onError?.('点击播放继续；若音频未就绪，请稍后重试。')}}}
 toggle(){if(this.audio.paused)this.play();else{this.audio.pause();this.save()}}
 seek(value){if(!Number.isFinite(this.audio.duration))return;this.audio.currentTime=Math.max(0,Math.min(Number(value),this.audio.duration));this.save();this.emit()}
 skip(delta){this.seek(this.audio.currentTime+delta)}
 setRate(rate){this.rate=Number(rate);this.audio.playbackRate=this.rate;try{localStorage.setItem('guanwu-rate-v2',this.rate)}catch{}this.emit()}
 save(){if(!this.owner||!this.audio.src||this.seekOnLoad)return;this.bookmarks[this.owner.id]={index:this.index,time:this.audio.currentTime||0};try{localStorage.setItem('guanwu-audio-v2',JSON.stringify(this.bookmarks))}catch{}}
 close(){this.save();this.audio.pause();this.owner=null;this.queue=[];this.emit()}
 emit(){this.options.onChange?.(this)}
 currentSentence(){const t=this.audio.currentTime;return this.subtitles.find(s=>t>=s.start&&t<=s.end)?.text||''}
}
root.GuidePlayer=GuidePlayer;
})(window);
