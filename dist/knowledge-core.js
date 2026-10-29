/* Shared deterministic retrieval, used in the browser and the Worker. */
(function(root){
 const groups=[['点茶','击拂','打茶','打泡','泡沫','白沫','宋代怎么喝茶','宋人喝茶'],['黑色','黑盏','黑釉','斗茶','白色'],['兔毫','兔毛','结晶','画上去','条纹'],['木叶','树叶','叶子','桑叶','吉州'],['茶壶','紫砂','泡茶','冲泡'],['金属','口沿','包口','修补','破了'],['编号','同名','同一件','名称','两件'],['乾隆','出门','出行','随身','茶籝'],['断代','年代','南宋','世纪'],['天目','日本','传播','跨海'],['材质','材料','瓷器','陶器'],['尺寸','大小','直径','高度']];
 const normalize=x=>String(x||'').normalize('NFKC').toLowerCase().replace(/[“”"'，。？！、；：,.?!\s]/g,'');
 function terms(q){const n=normalize(q),set=new Set();for(const word of String(q).toLowerCase().match(/[a-z0-9.-]{2,}|[\u3400-\u9fff]+/g)||[]){set.add(word);if(/[\u3400-\u9fff]/.test(word))for(let i=0;i<word.length-1;i++)set.add(word.slice(i,i+2))}for(const group of groups)if(group.some(w=>n.includes(normalize(w))))for(const w of group)set.add(w);return [...set].filter(Boolean)}
 function score(q,text,title){const n=normalize(text),t=normalize(title),v=terms(q);return v.reduce((sum,w)=>sum+(n.includes(normalize(w))?Math.min(4,w.length)* (t.includes(normalize(w))?2.4:1):0),0)}
 function search(data,{query='',institution='',period='',objectType='',limit=12}={}){
  const match=o=>(!institution||o.institution===institution)&&(!period||o.period===period)&&(!objectType||o.objectType===objectType);
  const objects=data.objects.filter(match).map(o=>({item:o,score:query?score(query,JSON.stringify([o.title,o.aliases,o.fields,o.summary]),o.title+' '+(o.fields.accession.value||'')):1})).filter(r=>r.score>0).sort((a,b)=>b.score-a.score||a.item.id.localeCompare(b.item.id)).slice(0,Math.min(30,Math.max(1,limit)));
  // Institution/period/type constrain object facts only; context documents remain background.
  const documents=data.documents.map(d=>({item:d,score:query?score(query,JSON.stringify(d),d.title+' '+d.tags):1})).filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,5);
  return {objects:objects.map(r=>r.item),documents:documents.map(r=>r.item),method:'词项检索＋同义问法扩展；结构化条件精确筛选',scope:data.scope};
 }
 function evidence(data,params={}){const found=search(data,params),ids=Array.isArray(params.ids)?params.ids.slice(0,2):[],selected=ids.map(id=>data.objects.find(o=>o.id===id)).filter(Boolean);const objects=[...new Map([...selected,...found.objects].map(o=>[o.id,o])).values()].slice(0,8),docs=found.documents;const sourceIds=new Set([...objects.flatMap(o=>[...o.sourceIds,...Object.values(o.fields).flatMap(f=>f.sourceIds)]),...docs.flatMap(d=>d.sourceIds)]);return {objects,documents:docs,sources:data.sources.filter(s=>sourceIds.has(s.id)),method:found.method,scope:data.scope}}
 root.GuanwuKnowledgeCore={search,evidence,terms};
 if(typeof module!=='undefined')module.exports=root.GuanwuKnowledgeCore;
})(globalThis);
