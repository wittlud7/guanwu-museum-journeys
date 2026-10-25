import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {executeTool,handleGuide} from '../server-app/lib/guide.mjs';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json');
assert.equal(catalog.museums.length,33);assert.equal(new Set(catalog.museums.map(m=>m.city)).size,11);
for(const city of new Set(catalog.museums.map(m=>m.city))){assert.equal(catalog.museums.filter(m=>m.city===city).length,3);const half=executeTool('plan_city_visit',{city,pace:'half'},catalog),day=executeTool('plan_city_visit',{city,pace:'day'},catalog);assert.equal(half.museums.length,1);assert.equal(day.museums.length,2);assert.equal(day.otherChoices.length,1);assert.ok(day.museums.every(m=>m.official));assert.ok(day.note.includes('不是导航'));}
assert.throws(()=>executeTool('plan_city_visit',{city:'北京',pace:'half',museum_ids:['beijing','palace']},catalog));
const custom=executeTool('plan_city_visit',{city:'北京',pace:'custom',museum_ids:['national-china','palace','beijing']},catalog);assert.equal(custom.museums.length,3);assert.deepEqual(custom.museums.map(m=>m.id),['national-china','palace','beijing']);
assert.throws(()=>executeTool('plan_city_visit',{city:'北京',pace:'day',museum_ids:['beijing','xian']},catalog));
assert.throws(()=>executeTool('compare_items',{ids:['du-tally','du-tally']},catalog));
const pair=executeTool('compare_items',{ids:['du-tally','goujian-sword']},catalog);assert.equal(pair.objects.length,2);assert.ok(pair.objects.every(a=>a.source.url));
const inquiry=executeTool('get_item',{id:'inquiry:authority'},catalog);assert.equal(inquiry.objects.length,2);
const ranking=executeTool('search_catalog',{query:'北京 博物馆'},catalog);assert.ok(ranking.slice(0,3).every(m=>m.city==='北京'));
const palace=executeTool('plan_visit',{museum:'palace',minutes:90},catalog);assert.equal(palace.stops.length,3);assert.ok(palace.stops.every(s=>s.source?.url));
let calls=0;const mock=async(url,options)=>{const body=JSON.parse(options.body);calls++;if(calls===1)return Response.json({choices:[{message:{role:'assistant',tool_calls:[{id:'city',type:'function',function:{name:'plan_city_visit',arguments:JSON.stringify({city:'北京',pace:'day',museum_ids:['palace','national-china']})}}]}}]});assert.ok(body.messages.some(m=>m.role==='tool'&&m.content.includes('故宫博物院')));return Response.json({choices:[{message:{content:'先核对各馆馆区与预约，再慢慢看。'}}]})};
const result=await handleGuide(new Request('https://test.local/api/guide',{method:'POST',body:JSON.stringify({message:'一天逛北京',context:'city:北京'})}),{DEEPSEEK_API_KEY:'test'},catalog,mock);assert.equal(result.status,200);assert.ok((await result.json()).references.length);
console.log('PASS: 33 museums in 11 cities; one/two-museum pacing; cross-city selection rejection; sourced comparisons; inquiry context; ranked search; highlight fallback; model tool loop (mock transport).');
