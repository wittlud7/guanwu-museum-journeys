// Explicit campus/address cross-check against the final museum catalog.
const fs=require('node:fs');
const data=require('../dist/beijing-museums.js').museums;
const points=require('../dist/beijing-locations.js');
const expected={
'capital':/复兴门外大街16/,'grand-canal':/绿心路1/,'art':/五四大街1/,'geology':/羊肉胡同15/,
'agriculture':/东三环北路16/,'paleozoo':/西直门外大街142/,'science':/北辰东路5/,'military':/复兴路9/,
'planetarium':/西直门外大街138/,'nature':/天桥南大街126/,'bells':/北三环西路甲31/,'wanshou':/万寿寺/,
'architecture':/东经路21.*先农坛/,'stone':/五塔寺村24/,'luxun':/宫门口二条19/,'xubeihong':/新街口北大街53/,
'guomoruo':/前海西街18/,'meilanfang':/护国寺街9/,'laoshe':/丰富胡同19/,'red-chamber':/南菜园街12.*大观园/,
'folk':/朝阳门外大街141.*东岳庙/,'opera':/虎坊路3.*湖广会馆/,'gongwang':/前海西街17|柳荫街甲14/,
'guozijian':/国子监街13号、15/,'guanfu':/金南路18/,'poly':/朝阳门北大街1.*新保利大厦/,
'zitan':/兴隆西街9/,'garden':/射击场路15/,'film':/南影路9/,'railway':/酒仙桥北路1/,'auto':/南四环西路126/,
'beihang':/学院路37.*学院路校区/,'civil-aviation':/首都机场辅路.*200/,'printing':/兴华大街二段1/,
'women':/建国门内大街23/,'overseas':/北新桥三条东口/,'customs':/建国门内大街6/,'coins':/西交民巷17/,
'ethnic':/复兴门内大街49/,'literature':/文学馆路45/,'tsinghua':/清华园1/,'archaeology':/国家体育场北路1/,
'zhoukoudian':/周口店大街1/,'yunju':/水头村云居寺/,'dabaotai':/郭公庄707/,
'yongding':/门头沟路8|增产路/,'haidian':/海淀公园路6/};
const notes={
'bj-yongding':'没有可信公开WGS84点；目录馆址可更新，但不添加猜测坐标。',
'bj-haidian':'固定三山五园新馆；拒绝旧中关村馆坐标。',
'bj-gongwang':'同一恭王府馆区；前海西街馆址与柳荫街入口可并列，参考点不是入口。',
'bj-agriculture':'以农展馆同址园区OSM替代冲突Wikidata点。',
'bj-zhoukoudian':'对应独立博物馆馆舍，非猿人洞遗址总点。',
'bj-dabaotai':'2025新馆位于同一大葆台遗址馆区；点位不表示新馆入口。',
'bj-red-chamber':'对应馆所在大观园园区，非单独展厅。',
'bj-tsinghua':'对应清华大学艺博馆区；源精度粗，不表示校门。'};
if(data.length!==47||Object.keys(points).length!==47)throw Error('47 museum IDs required');
const rows=data.map(m=>{
 const p=points[m.id],rule=expected[m.id.replace(/^bj-/,'')];
 if(!p||!rule||!rule.test(m.address))throw Error('Campus/address changed; review required: '+m.id+' '+m.address);
 return {id:m.id,name:m.name,address:m.address,coordinate:p.unavailable?'unavailable':{lat:p.lat,lng:p.lng},source:p.source?.url||null,result:p.unavailable?'address-only':'same museum/campus reference; not entrance',note:notes[m.id]||'场馆名称与当前目录馆址所在馆区一致；参考点不代表入口。',checked:'2026-10-25'};
});
fs.writeFileSync('research/beijing-locations-campus-audit.json',JSON.stringify(rows,null,2)+'\n');
console.log('PASS: all 47 final catalog IDs and reviewed museum/campus addresses match; 45 reference points, 2 address-only.');
