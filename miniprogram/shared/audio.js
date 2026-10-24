// One audio context for every native page; authored recordings ship in city packages.
let singleton;
class AudioGuide {
 constructor(){
  this.context=wx.createInnerAudioContext();this.listeners=new Set();this.owner=null;this.queue=[];this.index=0;this.playing=false;this.time=0;this.duration=0;this.pendingSeek=0;this.lastSave=0;this.rate=1;this.marks={};
  try{this.marks=wx.getStorageSync('guanwu-native-progress')||{};this.rate=wx.getStorageSync('guanwu-native-rate')||1}catch(e){}
  this.context.onPlay(()=>{this.playing=true;this.emit()});this.context.onPause(()=>{this.playing=false;this.save();this.emit()});
  this.context.onCanplay(()=>{if(this.pendingSeek>0){this.context.seek(this.pendingSeek);this.pendingSeek=0}this.duration=this.context.duration||0;this.emit()});
  this.context.onTimeUpdate(()=>{this.time=this.context.currentTime||0;this.duration=this.context.duration||0;if(Date.now()-this.lastSave>2000){this.save();this.lastSave=Date.now()}this.emit()});
  this.context.onEnded(()=>{this.playing=false;this.save();this.emit()});
  this.context.onError(()=>{this.playing=false;this.emit();wx.showToast({title:'音频未能播放，请重新打开本馆导览后重试',icon:'none'})});
 }
 subscribe(fn){this.listeners.add(fn);fn(this.snapshot());return()=>this.listeners.delete(fn)}
 snapshot(){return{owner:this.owner,index:this.index,title:this.queue[this.index]&&this.queue[this.index].title,playing:this.playing,time:this.time,duration:this.duration,rate:this.rate}}
 emit(){const s=this.snapshot();this.listeners.forEach(f=>f(s))}
 select(owner,queue,index){
  if(this.owner&&this.owner.id===owner.id&&this.index===index){this.toggle();return}
  this.save();this.context.pause();this.owner=owner;this.queue=queue;this.index=index;this.time=0;this.duration=0;
  const mark=this.marks[owner.id];this.pendingSeek=mark&&mark.index===index?mark.time:0;
  this.context.startTime=this.pendingSeek;this.context.src=queue[index].src;this.context.playbackRate=this.rate;this.emit();this.context.play();
 }
 toggle(){if(!this.owner)return;if(this.playing)this.context.pause();else this.context.play()}
 seek(seconds){const target=Math.max(0,Math.min(Number(seconds),this.duration||0));this.context.seek(target);this.time=target;this.save();this.emit()}
 speed(rate){this.rate=Number(rate);this.context.playbackRate=this.rate;try{wx.setStorageSync('guanwu-native-rate',this.rate)}catch(e){}this.emit()}
 save(){if(!this.owner)return;this.marks[this.owner.id]={index:this.index,time:this.time};try{wx.setStorageSync('guanwu-native-progress',this.marks)}catch(e){}}
 close(){this.context.pause();this.save();this.owner=null;this.emit()}
}
module.exports=()=>singleton||(singleton=new AudioGuide());
