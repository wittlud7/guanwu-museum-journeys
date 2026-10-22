const artifacts=require('../../data.js');
const imageBase='/assets/';
Page({
 data:{tab:'discover',view:'discover',filter:'全部',filters:['全部','青铜','陶瓷','书画'],query:'',items:[],saved:[],member:false,activeRoute:false,detail:null,modal:'',city:'全部目的地',cities:['全部目的地','北京','纽约'],imageBase},
 onLoad(){let saved=[],member=false,activeRoute=false;try{saved=wx.getStorageSync('saved')||[];member=!!wx.getStorageSync('member');activeRoute=!!wx.getStorageSync('activeRoute')}catch(e){}this.setData({saved,member,activeRoute});this.refresh()},
 onShareAppMessage(){return {title:'观物 · 让每一次驻足，都与美相遇',path:'/pages/index/index'}},
 refresh(){const {filter,query,saved,view}=this.data;const items=artifacts.filter(a=>(view!=='saved'||saved.indexOf(a.id)>=0)&&(filter==='全部'||a.type===filter)&&(!query||(a.title+a.type+a.material+a.period).indexOf(query)>=0)).map(a=>({...a,saved:saved.indexOf(a.id)>=0,image:imageBase+a.id+'.jpg'}));this.setData({items});},
 write(key,value){try{wx.setStorageSync(key,value)}catch(e){wx.showToast({title:'存储暂不可用',icon:'none'})}},
 navigate(e){const tab=e.currentTarget.dataset.tab;this.setData({tab,view:tab,query:'',filter:'全部'});this.refresh();wx.pageScrollTo({scrollTop:0,duration:200})},
 setFilter(e){this.setData({filter:e.currentTarget.dataset.value});this.refresh()},
 search(e){this.setData({query:e.detail.value});this.refresh()},
 openDetail(e){const a=artifacts.find(x=>x.id===e.currentTarget.dataset.id);if(!a)return;this.setData({view:'detail',detail:{...a,image:imageBase+a.id+'.jpg',saved:this.data.saved.indexOf(a.id)>=0}});wx.pageScrollTo({scrollTop:0,duration:0})},
 back(){this.setData({view:this.data.tab});this.refresh();wx.pageScrollTo({scrollTop:0,duration:0})},
 save(e){const id=e.currentTarget.dataset.id;let saved=this.data.saved.slice();saved=saved.indexOf(id)>=0?saved.filter(x=>x!==id):saved.concat(id);this.setData({saved});if(this.data.detail&&this.data.detail.id===id)this.setData({'detail.saved':saved.indexOf(id)>=0});this.write('saved',saved);this.refresh();wx.showToast({title:saved.indexOf(id)>=0?'已加入收藏':'已取消收藏',icon:'none'})},
 openRoute(){this.setData({view:'route',tab:'journeys'});wx.pageScrollTo({scrollTop:0,duration:0})},
 toggleRoute(){const activeRoute=!this.data.activeRoute;this.setData({activeRoute});this.write('activeRoute',activeRoute);wx.showToast({title:activeRoute?'已加入我的行程':'已移除行程',icon:'none'})},
 openModal(e){this.setData({modal:e.currentTarget.dataset.modal})},
 closeModal(){this.setData({modal:''})},
 stop(){},
 unlock(){this.setData({member:true,modal:''});this.write('member',true);wx.showToast({title:'免费体验已解锁',icon:'none'})},
 selectCity(e){const city=e.currentTarget.dataset.city;const tab=city==='纽约'?'collection':'journeys';this.setData({city,tab,view:tab,modal:'',query:'',filter:'全部'});this.refresh()},
 showSource(){wx.setClipboardData({data:this.data.detail.source,success:()=>wx.showToast({title:'馆方资料链接已复制',icon:'none'})})},
 daily(){const id=artifacts[new Date().getDate()%artifacts.length].id;this.openDetail({currentTarget:{dataset:{id}}})}
});
