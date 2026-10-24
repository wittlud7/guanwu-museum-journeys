// Local byte-range preview uses the same DeepSeek implementation as the Worker.
import http from 'node:http';
import {createReadStream,statSync} from 'node:fs';
import {resolve,extname,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {handleGuide} from '../server-app/lib/guide.mjs';
import {privateConfig} from './private_config.mjs';
const privateEnv=privateConfig();
const require=createRequire(import.meta.url),root=fileURLToPath(new URL('../dist/',import.meta.url));
const a=require('../dist/heritage-data.js');let b={};try{b=require('../dist/expansion-data.js')}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}
const catalog={museums:[...a.museums,...(b.museums||[])],artifacts:b.artifacts||[],crafts:a.crafts};
const types={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.mp3':'audio/mpeg','.webp':'image/webp'};
const server=http.createServer(async(req,res)=>{
  const url=new URL(req.url,'http://localhost:4173');
  if(url.pathname.startsWith('/api/guide')){
    const chunks=[];let size=0;for await(const chunk of req){size+=chunk.length;if(size>24000){res.writeHead(413);res.end();return}chunks.push(chunk)}
    const request=new Request(url,{method:req.method,headers:req.headers,...(req.method==='POST'?{body:Buffer.concat(chunks)}:{})});
    const result=await handleGuide(request,privateEnv,catalog);res.writeHead(result.status,Object.fromEntries(result.headers));res.end(Buffer.from(await result.arrayBuffer()));return;
  }
  let path;try{path=resolve(root,'.'+decodeURIComponent(url.pathname==='/'?'/index.html':url.pathname))}catch{res.writeHead(400);res.end();return}
  if(!path.startsWith(root.endsWith(sep)?root:root+sep)){res.writeHead(403);res.end();return}
  let info;try{info=statSync(path);if(!info.isFile())throw Error()}catch{res.writeHead(404);res.end('Not found');return}
  const headers={'Content-Type':types[extname(path)]||'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
  const range=req.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
  if(range){const start=Number(range[1]),end=Math.min(Number(range[2]||info.size-1),info.size-1);if(start>end||start>=info.size){res.writeHead(416,{'Content-Range':`bytes */${info.size}`});res.end();return}res.writeHead(206,{...headers,'Content-Length':end-start+1,'Content-Range':`bytes ${start}-${end}/${info.size}`});createReadStream(path,{start,end}).pipe(res)}
  else{res.writeHead(200,{...headers,'Content-Length':info.size});if(req.method==='HEAD')res.end();else createReadStream(path).pipe(res)}
});
server.listen(4173,'127.0.0.1',()=>console.log('Local: http://localhost:4173 · DeepSeek '+(privateEnv.DEEPSEEK_API_KEY?'configured':'not configured')));
