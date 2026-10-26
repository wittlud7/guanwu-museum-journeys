const {heritage}=require('../data.js'),credits=require('../credits.js'),store=require('./store.js');
module.exports=id=>({
 data:{site:heritage.find(s=>s.id===id),prefix:'/media/'+id+'/assets/',saved:false,note:'',provinceLabel:'',chapterOpen:0},
 onLoad(){const s=this.data.site;this.setData({saved:store.read('saved',[]).includes('heritage:'+id),note:store.read('notes',{})['heritage:'+id]||'',provinceLabel:s.provinces.join(' · ')})},
 preview(){const s=this.data.site;wx.previewImage({current:this.data.prefix+s.cover+'.jpg',urls:s.gallery.map(k=>this.data.prefix+k+'.jpg')})},
 toggleSave(){const saved=store.toggle('saved','heritage:'+id);this.setData({saved:saved.includes('heritage:'+id)})},
 noteInput(e){this.setData({note:e.detail.value})},saveNote(){const notes=store.read('notes',{});notes['heritage:'+id]=this.data.note.trim();store.write('notes',notes);wx.showToast({title:'手记已保存',icon:'none'})},
 copySource(e){wx.setClipboardData({data:e.currentTarget.dataset.url})},
 credits(){const p=credits[this.data.site.cover];wx.setClipboardData({data:p.caption+'\n'+p.author+' · '+p.license+'\n'+p.source+'\n'+p.licenseUrl})},
 onShareAppMessage(){return {title:this.data.site.name+' · 观物世界遗产',path:'/media/'+id+'/guide/index'}}
});
