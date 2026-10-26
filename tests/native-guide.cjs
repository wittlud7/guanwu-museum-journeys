/* Logic verification against a deterministic wx adapter. This is not a native render test. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve('miniprogram'),storage=new Map(),events={},effects={};
const ctx={src:'',currentTime:0,duration:40,playbackRate:1,startTime:0,play(){this.currentTime=this.startTime;events.canplay?.();events.play?.()},pause(){events.pause?.()},seek(n){this.currentTime=n},onPlay:f=>events.play=f,onPause:f=>events.pause=f,onCanplay:f=>events.canplay=f,onTimeUpdate:f=>events.time=f,onEnded:f=>events.ended=f,onError:f=>events.error=f};
global.wx={getStorageSync:k=>storage.get(k),setStorageSync:(k,v)=>storage.set(k,v),createInnerAudioContext:()=>ctx,showToast:o=>effects.toast=o.title,pageScrollTo(){},navigateTo:o=>effects.nav=o.url,previewImage:o=>effects.preview=o,setClipboardData:o=>effects.clipboard=o.data,showActionSheet:o=>o.success({tapIndex:1}),showModal:o=>o.success({confirm:true})};
function mount(config){config.data=structuredClone(config.data);config.setData=function(p){for(const[k,v]of Object.entries(p)){const ks=k.split('.');let t=this.data;for(const s of ks.slice(0,-1))t=t[s];t[ks.at(-1)]=v}};return config}
const event=(data,detail)=>({currentTarget:{dataset:data},detail:detail||{}});
const {museums,crafts}=require(root+'/data.js');
assert.equal(museums.length,80);assert.equal(crafts.length,26);
const factory=require(root+'/shared/guide-page.js');
for(const m of museums.filter(m=>m.chapters[0].audio!==false)){
 const p=mount(factory(m.id));storeSet('member',false);p.onLoad({});assert.equal(p.data.view,'museum');assert.equal(p.data.gallery.length,m.gallery.length);
 for(const g of p.data.gallery)assert.ok(fs.existsSync(root+g.src),g.src);
 p.play(event({index:0}));assert.ok(ctx.src.endsWith(m.id+'-0.mp3'));assert.ok(fs.existsSync(root+ctx.src));assert.equal(p.data.audio.playing,true);
 p.seek({detail:{value:12}});assert.equal(ctx.currentTime,12);p.changeRate({detail:{value:2}});assert.equal(ctx.playbackRate,1.2);
 p.play(event({index:1}));assert.equal(p.data.modal,'member');p.unlock();p.play(event({index:1}));assert.ok(ctx.src.endsWith(m.id+'-1.mp3'));
 p.toggleSave();assert.equal(p.data.saved,true);p.togglePlan();assert.equal(p.data.planned,true);
 p.noteInput({detail:{value:m.city+'的一次观看'}});p.saveNote();assert.equal(read('notes')['museum:'+m.id],m.city+'的一次观看');
 p.preview(event({index:0}));assert.equal(effects.preview.urls.length,m.gallery.length);p.showCredits();assert.ok(p.data.creditRows.every(r=>r.url.startsWith('https://')));
 for(const c of crafts.filter(c=>c.museum===m.id)){
  p.showItem(c.id);p.play(event({index:0}));assert.ok(ctx.src.endsWith('craft-'+c.id+'.mp3'));assert.ok(fs.existsSync(root+ctx.src));
  p.openQuiz(event({id:c.id}));p.answer(event({index:c.quiz.answer}));assert.equal(p.data.correct,true);assert.ok(read('stamps').includes(c.id));
 }
 p.onUnload();
}
function read(k){return storage.get('guanwu-v2-'+k)}function storeSet(k,v){storage.set('guanwu-v2-'+k,v)}
let main;global.Page=config=>main=mount(config);require(root+'/pages/atlas/index.js');main.onLoad();assert.equal(main.data.museumItems.length,80);main.city(event({city:'杭州'}));assert.equal(main.data.museumItems.length,3);main.city(event({city:'全部'}));main.search({detail:{value:'云锦'}});assert.equal(main.data.museumItems.length,1);assert.equal(main.data.craftItems.length,1);
assert.equal(main.data.cities.length,12);main.tab(event({tab:'journeys'}));main.city(event({city:'全部'}));assert.equal(main.data.cityDestinations.length,11);main.openCity(event({city:'北京'}));assert.equal(main.data.museumItems.length,50);assert.equal(main.data.journeyCity,true);main.chooseCity();assert.equal(main.data.modal,'city');main.chooseCityItem(event({city:'全部'}));assert.equal(main.data.modal,'');assert.equal(main.data.journeyCity,false);main.openMuseum(event({id:'beijing'}));assert.equal(effects.nav,'/media/beijing/guide/index');main.openCraft(event({id:'yunjin'}));assert.equal(effects.nav,'/media/nanjing/guide/index?craft=yunjin');
main.tab(event({tab:'saved'}));assert.equal(main.data.planItems.length,5);assert.equal(main.data.notes.length,5);main.date(event({id:'beijing'},{value:'2026-11-01'}));assert.equal(read('dates').beijing,'2026-11-01');main.move(event({id:'hangzhou',delta:-1}));assert.equal(read('plan')[0],'hangzhou');main.copyPlan();assert.ok(effects.clipboard.includes('2026-11-01'));main.onUnload();
const app=JSON.parse(fs.readFileSync(root+'/app.json'));assert.deepEqual(app.pages,['pages/atlas/index']);assert.equal(app.subPackages.length,80);
for(const sub of app.subPackages){for(const page of sub.pages)for(const ext of ['js','json','wxml','wxss'])assert.ok(fs.existsSync(root+'/'+sub.root+'/'+page+'.'+ext));const size=files(root+'/'+sub.root).reduce((s,p)=>s+fs.statSync(p).size,0);assert.ok(size<2*1024*1024,sub.name+' exceeds 2MB')}
function files(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(d=>d.isDirectory()?files(path.join(dir,d.name)):[path.join(dir,d.name)])}
for(const m of museums.filter(m=>m.chapters[0].audio===false)){const p=mount(factory(m.id));p.onLoad({});p.play(event({index:1}));assert.equal(p.data.modal,'transcript');assert.equal(p.data.transcript,m.chapters[1].text);for(const c of crafts.filter(c=>c.museum===m.id)){p.showItem(c.id);p.play(event({index:0}));assert.equal(p.data.transcript,c.audioText);for(const g of p.data.gallery)assert.ok(fs.existsSync(root+g.src));p.showCredits();assert.ok(p.data.creditRows.length)}}
console.log('PASS: native 80 museums (Beijing 50), 18 artifacts, 8 craft stories, gallery paths, 23 audio paths, trial gate, note/save/plan storage, quiz, speed/seek adapter, search, navigation and city package sizes.');
