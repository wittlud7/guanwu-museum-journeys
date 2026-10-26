import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {existsSync} from 'node:fs';
import {executeTool} from '../server-app/lib/guide.mjs';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json'),extra=require('../dist/beijing-museums.js'),locations=require('../dist/beijing-locations.js');
const beijing=catalog.museums.filter(m=>m.city==='北京');
assert.equal(beijing.length,50);assert.equal(extra.museums.length,47);assert.equal(catalog.museums.length,80);
assert.equal(new Set(beijing.map(m=>m.id)).size,50);assert.equal(new Set(beijing.map(m=>m.name)).size,50);
assert.ok(new Set(beijing.map(m=>m.district)).size>=8);
for(const m of beijing){assert.ok(m.district&&m.address&&m.official.startsWith('https://'),m.id);assert.ok(m.sources.length,m.id);}
for(const m of extra.museums){
 assert.equal(m.highlights.length,3,m.id);assert.equal(m.chapters.length,3,m.id);assert.ok(m.checked,m.id);
 for(const h of m.highlights)assert.ok(h.title&&h.text.length>=20&&h.source?.url.startsWith('https://'),m.id);
 for(const c of m.chapters)assert.ok(c.title&&c.text.length>=40&&c.audio===false,m.id);
 assert.equal(m.cover,m.gallery[0]||null);
 for(const key of m.gallery){const i=extra.images[key];assert.ok(i?.author&&i.license&&i.source,m.id);assert.ok(existsSync(new URL('../dist/'+i.src,import.meta.url)),i.src);}
 const point=locations[m.id];assert.ok(point,m.id);if(!point.unavailable){assert.ok(point.lat>39&&point.lat<41.2&&point.lng>115&&point.lng<118,m.id);assert.ok(point.source?.url,m.id);}
}
const ids=beijing.slice(-9).map(m=>m.id);
assert.throws(()=>executeTool('plan_city_visit',{city:'北京',pace:'custom',museum_ids:ids},catalog));
const custom=executeTool('plan_city_visit',{city:'北京',pace:'custom',museum_ids:ids.slice(0,8)},catalog);assert.equal(custom.museums.length,8);
const summary=executeTool('get_item',{id:'city:北京'},catalog);assert.equal(summary.museums.length,50);assert.ok(summary.museums.every(m=>!m.chapters&&!m.highlights));
const query=extra.museums.find(m=>m.kind.includes('自然')||m.kind.includes('科技'))||extra.museums[0];assert.ok(executeTool('search_catalog',{query:query.name},catalog).some(m=>m.id===query.id));
console.log('PASS: Beijing 50 unique museums; district coverage; 141 sourced highlights and reading chapters; image provenance; coordinate bounds; eight-stop limit; compact AI city index and new-museum search.');
