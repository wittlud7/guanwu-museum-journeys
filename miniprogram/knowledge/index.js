const db=require('./data.js');
const labels={originalName:'馆方原名',creditLine:'馆方入藏说明',accession:'官方藏品编号',dateOriginal:'原始年代',medium:'材质',dimensions:'尺寸',technique:'工艺与纹饰',use:'用途记载',provenance:'出土或流传'};
const find=id=>db.objects.find(o=>o.id===id);
const source=id=>db.sources.find(s=>s.id===id);
Page({
 data:{title:'一盏茶里的中国生活',query:'',items:[],documents:db.documents,steps:db.topics[0].steps,scope:db.scope,selected:[],detail:null,fields:[],compare:[],rows:[],tab:'objects',show3d:false,viewerError:false},
 onLoad(){this.refresh()},
 refresh(){const q=this.data.query.trim().toLowerCase();this.setData({items:db.objects.filter(o=>!q||JSON.stringify([o.title,o.institution,o.fields,o.summary]).toLowerCase().includes(q)).map(o=>({...o,image:o.image.src?'/knowledge/assets/'+o.id.split('-').pop()+'.jpg':'',number:o.fields.accession.value||'编号未提供',picked:this.data.selected.includes(o.id)}))})},
 search(e){this.setData({query:e.detail.value});this.refresh()},
 tab(e){this.releaseViewer();this.setData({tab:e.currentTarget.dataset.tab,detail:null})},
 open(e){const o=find(e.currentTarget.dataset.id);if(!o)return;this.setData({detail:{...o,imageRights:o.image.rights,image:o.image.src?'/knowledge/assets/'+o.id.split('-').pop()+'.jpg':''},fields:Object.entries(labels).map(([key,label])=>({label,value:o.fields[key].value||'当前来源未说明',sourceId:o.fields[key].sourceIds[0]||''}))});wx.pageScrollTo({scrollTop:0,duration:150})},
 back(){this.releaseViewer();this.setData({detail:null})},
 releaseViewer(){this.viewer?.dispose();this.viewer=null;this.touch=null;this.setData({show3d:false,viewerError:false})},
 showViewer(){if(this.data.show3d){this.releaseViewer();return}this.setData({show3d:true,viewerError:false},()=>{wx.createSelectorQuery().in(this).select('#native-object-canvas').fields({node:true,size:true}).exec(results=>{try{const r=results[0];if(!r?.node)throw Error('canvas');const gl=r.node.getContext('webgl');if(!gl)throw Error('webgl');this.viewer=require('./viewer.js')(gl,r.node,this.data.detail,r.width,r.height)}catch{this.setData({viewerError:true})}})})},
 viewerStart(e){const t=e.touches[0];if(t)this.touch={x:t.x,y:t.y}},
 viewerMove(e){const t=e.touches[0];if(t&&this.touch){this.viewer?.rotate(t.x-this.touch.x,t.y-this.touch.y);this.touch={x:t.x,y:t.y}}},
 viewerEnd(){this.touch=null},
 viewerControl(e){this.viewer?.control(e.currentTarget.dataset.action)},
 onUnload(){this.viewer?.dispose()},
 onHide(){this.viewer?.dispose();this.viewer=null;this.setData({show3d:false})},
 pick(e){const id=e.currentTarget.dataset.id,list=this.data.selected;if(list.includes(id))this.setData({selected:list.filter(x=>x!==id)});else if(list.length<2)this.setData({selected:[...list,id]});else{wx.showToast({title:'请先移除一件茶器',icon:'none'});return}this.refresh()},
 compare(){if(this.data.selected.length!==2){wx.showToast({title:'请先选两件不同茶器',icon:'none'});return}this.releaseViewer();const pair=this.data.selected.map(find);this.setData({tab:'compare',detail:null,compare:pair,rows:Object.entries(labels).map(([key,label])=>({label,left:pair[0].fields[key].value||'当前来源未说明',right:pair[1].fields[key].value||'当前来源未说明'}))});wx.pageScrollTo({scrollTop:0,duration:150})},
 copySource(e){const s=source(e.currentTarget.dataset.id);if(s)wx.setClipboardData({data:s.title+'\n'+s.url+'\n核对日期：'+s.checkedAt+'\n文字：'+s.textRights})},
 webAssistant(){wx.setClipboardData({data:'https://guanwu-museum-journeys.youngcoin22.chatgpt.site/#knowledge/ask'})},
 onShareAppMessage(){return {title:'一盏茶里的中国生活 · 观物',path:'/knowledge/index'}},
});
