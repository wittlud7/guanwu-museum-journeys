const read=(key,fallback)=>{try{return wx.getStorageSync('guanwu-v2-'+key)||fallback}catch(e){return fallback}};
const write=(key,value)=>{try{wx.setStorageSync('guanwu-v2-'+key,value)}catch(e){wx.showToast({title:'记录暂未保存，请检查设备空间',icon:'none'})}};
const toggle=(key,id)=>{let items=read(key,[]);items=items.indexOf(id)>=0?items.filter(x=>x!==id):items.concat(id);write(key,items);return items};
module.exports={read,write,toggle};
