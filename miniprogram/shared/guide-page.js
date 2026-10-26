const {museums,crafts}=require('../data.js');
const credits=require('../credits.js'),store=require('./store.js'),getAudio=require('./audio.js');
const time=s=>Math.floor((s||0)/60)+':'+Math.floor((s||0)%60).toString().padStart(2,'0');
module.exports=function(city){
 const museum=museums.find(m=>m.id===city),prefix='/media/'+city+'/assets/';
 return{
 data:{museum,craft:null,view:'museum',prefix,gallery:[],saved:false,planned:false,member:false,note:'',modal:'',quiz:null,quizResult:'',answers:[],audio:null,elapsed:'0:00',total:'0:00',rates:['0.8×','1×','1.2×','1.5×'],rateIndex:1,chapters:[],related:[],creditsText:''},
 onLoad(query){this.audio=getAudio();this.unsubscribe=this.audio.subscribe(s=>this.setData({audio:s,elapsed:time(s.time),total:time(s.duration)}));this.showItem(query&&query.craft);},
 onShow(){if(this.data.museum)this.refreshFlags()},
 onHide(){this.audio.save()},onUnload(){this.audio.save();if(this.unsubscribe)this.unsubscribe()},
 onShareAppMessage(){const craft=this.data.craft;return{title:craft?craft.title:museum.name,path:'/media/'+city+'/guide/index'+(craft?'?craft='+craft.id:'')}},
 refreshFlags(){const key=this.key();this.setData({saved:store.read('saved',[]).indexOf(key)>=0,planned:store.read('plan',[]).indexOf(city)>=0,member:!!store.read('member',false),note:store.read('notes',{})[key]||''})},
 key(){return this.data.view==='craft'?'craft:'+this.data.craft.id:'museum:'+city},
 showItem(id){const c=crafts.find(c=>c.id===id&&c.museum===city);const item=c||museum;this.setData({craft:c||null,view:c?'craft':'museum',gallery:item.gallery.map(k=>({key:k,src:prefix+k+'.jpg',caption:credits[k].caption})),related:crafts.filter(c=>c.museum===city).map(c=>({...c,image:prefix+c.cover+'.jpg'})),chapters:museum.chapters.map((c,i)=>({...c,index:i})),creditsText:''});this.refreshFlags();wx.pageScrollTo({scrollTop:0,duration:0})},
 openCraft(e){this.showItem(e.currentTarget.dataset.id)},backMuseum(){this.showItem(null)},
 preview(e){const i=Number(e.currentTarget.dataset.index)||0;wx.previewImage({current:this.data.gallery[i].src,urls:this.data.gallery.map(g=>g.src)})},
 toggleSave(){const list=store.toggle('saved',this.key());this.setData({saved:list.indexOf(this.key())>=0});wx.showToast({title:this.data.saved?'已收藏':'已取消收藏',icon:'none'})},
 togglePlan(){const list=store.toggle('plan',city);this.setData({planned:list.indexOf(city)>=0});wx.showToast({title:this.data.planned?'已加入行程':'已移除行程',icon:'none'})},
 noteInput(e){this.setData({note:e.detail.value})},saveNote(){const notes=store.read('notes',{});notes[this.key()]=this.data.note.trim();store.write('notes',notes);wx.showToast({title:'手记已保存',icon:'success'})},
 play(e){if(this.data.craft?.audio===false||(!this.data.craft&&museum.chapters[0].audio===false)){const n=Number(e.currentTarget.dataset.index)||0;this.setData({modal:'transcript',transcript:this.data.craft?this.data.craft.audioText:museum.chapters[n].text});return}const n=Number(e.currentTarget.dataset.index)||0;if(this.data.view==='museum'&&n>0&&!this.data.member){this.setData({modal:'member'});return}const c=this.data.craft;const owner={id:this.key(),title:c?c.title:museum.name,city};const queue=c?[{title:c.title,text:c.audioText,src:prefix+'craft-'+c.id+'.mp3'}]:museum.chapters.map((v,i)=>({title:v.title,text:v.text,src:prefix+city+'-'+i+'.mp3'}));this.audio.select(owner,queue,n)},
 chooseVoice(){const packs=require('../voice-packs.js').packs;wx.showActionSheet({itemList:packs.map(p=>p.name),success:r=>this.audio.setVoice(packs[r.tapIndex].id)})},
 toggleAudio(){this.audio.toggle()},closeAudio(){this.audio.close()},seek(e){this.audio.seek(e.detail.value)},skip(e){this.audio.seek(this.audio.time+Number(e.currentTarget.dataset.delta))},
 changeRate(e){const i=Number(e.detail.value);this.setData({rateIndex:i});this.audio.speed([.8,1,1.2,1.5][i])},
 nextChapter(){if(!this.audio.owner||this.audio.owner.id!=='museum:'+city)return;const next=this.audio.index+1;if(next<3)this.play({currentTarget:{dataset:{index:next}}})},
 openMember(){this.setData({modal:'member'})},unlock(){store.write('member',true);this.setData({member:true,modal:''});wx.showToast({title:'完整导览已免费解锁',icon:'none'})},
 showTranscript(){let text;if(this.audio.owner&&this.audio.owner.id===this.key()){text=this.audio.queue[this.audio.index].text}else text=this.data.craft?this.data.craft.audioText:museum.chapters[0].text;this.setData({modal:'transcript',transcript:text})},
 openQuiz(e){const id=e.currentTarget.dataset.id||(this.data.craft&&this.data.craft.id),c=crafts.find(c=>c.id===id);if(c)this.setData({modal:'quiz',quiz:c,quizResult:'',answers:c.quiz.options.map((text,i)=>({text,index:i})),correct:false})},
 answer(e){if(this.data.correct)return;const c=this.data.quiz,yes=Number(e.currentTarget.dataset.index)===c.quiz.answer;this.setData({correct:yes,quizResult:yes?'◈ '+c.quiz.explain:'再想一想，可以返回图片看看材料与动作。'});if(yes){const stamps=store.read('stamps',[]);if(stamps.indexOf(c.id)<0)store.write('stamps',stamps.concat(c.id))}},
 showCredits(){const item=this.data.craft||museum;this.setData({modal:'credits',creditRows:item.gallery.map(k=>({caption:credits[k].caption,author:credits[k].author,license:credits[k].license,url:credits[k].source,licenseUrl:credits[k].licenseUrl||credits[k].source}))})},
 copySource(e){const item=this.data.craft;wx.setClipboardData({data:e.currentTarget.dataset.url||(item?item.source.url:museum.official)})},
 closeModal(){this.setData({modal:''})},stop(){},
 };
};
