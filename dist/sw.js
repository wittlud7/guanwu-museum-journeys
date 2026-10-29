const VERSION='2026102901',SHELL='guanwu-shell-v2-'+VERSION,LIBRARY='guanwu-library-v2';
const shellFiles=['./','index.html','mini.html','object-viewer.js','knowledge-data.js','knowledge-core.js','knowledge.js','knowledge.css','style.css','heritage.css','companion.css','companion.js','expansion-data.js','city-museums.js','world-heritage-data.js','world-heritage.js','world-heritage.css','voice-packs-data.js','voices.js','beijing-museums.js','beijing-locations.js','inquiries-data.js','experience.js','experience.css','museum-locations.js','route-planner.js','community.js','social-planner.css','vendor/leaflet/leaflet.js','vendor/leaflet/leaflet.css','heritage-data.js','heritage-app.js','player.js','assets/favicon.svg','assets/heritage/credits.json'].map(f=>/\.(js|css)$/.test(f)?f+'?v='+VERSION:f);
self.addEventListener('install',e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(shellFiles)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('guanwu-shell-')&&k!==SHELL).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
 const req=e.request,url=new URL(req.url);if(req.method!=='GET'||url.origin!==self.location.origin||url.pathname.startsWith('/api/'))return;
 e.respondWith((async()=>{
  const cached=await caches.match(req.url,{ignoreVary:true});
  if(req.headers.has('range')&&cached){const buffer=await cached.arrayBuffer(),m=/bytes=(\d+)-(\d*)/.exec(req.headers.get('range'));if(m){const start=Number(m[1]),end=Math.min(Number(m[2]||buffer.byteLength-1),buffer.byteLength-1);if(start>=buffer.byteLength||start>end)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${buffer.byteLength}`}});return new Response(buffer.slice(start,end+1),{status:206,headers:{'Content-Type':cached.headers.get('Content-Type')||'audio/mpeg','Accept-Ranges':'bytes','Content-Range':`bytes ${start}-${end}/${buffer.byteLength}`,'Content-Length':String(end-start+1)}})}}
  const media=/\/assets\/(audio|heritage|expansion|city-museums)\//.test(url.pathname)&&!url.pathname.endsWith('/credits.json');
  if(media&&cached)return cached;
  try{const r=await fetch(req);if(r.ok&&!req.headers.has('range')&&!media){const c=await caches.open(SHELL);await c.put(req,r.clone())}return r}catch{if(cached)return cached;if(req.mode==='navigate')return (await caches.match('index.html'))||Response.error();return Response.error()}
 })());
});
