// Site dispatch owns authentication. Never accept an author id from the request body.
const reply=(data,status=200)=>Response.json(data,{status,headers:{'Cache-Control':'no-store'}});
const fail=(message,status=400)=>{const error=new Error(message);error.status=status;throw error};
const clean=(value,min,max,label)=>{if(typeof value!=='string')fail(label+'格式不正确');const text=value.trim();if(text.length<min||text.length>max)fail(`${label}须为 ${min}–${max} 字`);if(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(text))fail(label+'含无效字符');return text};
const windows=new Map();
function actor(request,env){const id=request.headers.get('oai-authenticated-user-id'),email=request.headers.get('oai-authenticated-user-email');if(!id||!email)return null;return {id,moderator:String(env.COMMUNITY_MODERATOR_EMAILS||'').split(',').map(x=>x.trim().toLowerCase()).filter(Boolean).includes(email.toLowerCase())}}
async function bodyOf(request){if(Number(request.headers.get('content-length')||0)>18000)fail('内容过长',413);const reader=request.body?.getReader();if(!reader)fail('请求正文不能为空');const chunks=[];let size=0;for(;;){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;if(size>18000){await reader.cancel();fail('内容过长',413)}chunks.push(value)}const bytes=new Uint8Array(size);let cursor=0;for(const chunk of chunks){bytes.set(chunk,cursor);cursor+=chunk.length}try{return JSON.parse(new TextDecoder().decode(bytes))}catch{fail('请求格式不正确')}}
const profile=async(db,id)=>db.prepare('SELECT nickname FROM community_profiles WHERE user_id = ?').bind(id).first();
const selectPost=`SELECT p.*, COALESCE(u.nickname,'观物旅人') AS nickname,(SELECT COUNT(*) FROM community_comments c WHERE c.post_id=p.id) AS comment_count,(SELECT COUNT(*) FROM community_likes l WHERE l.post_id=p.id) AS like_count FROM community_posts p LEFT JOIN community_profiles u ON u.user_id=p.author_id`;
function postView(row,user){let route=null;try{route=row.route_json?JSON.parse(row.route_json):null}catch{}return {id:row.id,title:row.title,body:row.body,topic:row.topic,city:row.city,museumId:row.museum_id,route,author:{nickname:row.nickname,isSelf:row.author_id===user?.id},commentCount:row.comment_count||0,likeCount:row.like_count||0,createdAt:row.created_at,updatedAt:row.updated_at,status:row.status}}
export async function handleCommunity(request,env,catalog){
 const url=new URL(request.url),path=url.pathname,user=actor(request,env),write=!['GET','HEAD'].includes(request.method),db=env.DB;
 try{
  if(path==='/api/community/me'){
   if(!db)return reply({error:'交流区正在准备，请稍后再来。'},503);
   const p=user?await profile(db,user.id):null;
   return reply({authenticated:!!user,nickname:p?.nickname||'',moderator:user?.moderator||false,signIn:'/signin-with-chatgpt?return_to='+encodeURIComponent('/#community'),signOut:'/signout-with-chatgpt?return_to='+encodeURIComponent('/#community')});
  }
  if(write){
   if(!user)fail('登录后就能分享、回复和收藏交流。',401);
   const origin=request.headers.get('Origin');if(!origin||origin!==url.origin)fail('请求来源无效，请在本站操作。',403);
   const key=user.id,now=Date.now();let w=windows.get(key);if(!w||now-w.start>60000){w={start:now,count:0};windows.set(key,w)}if(++w.count>20)fail('操作有些频繁，请一分钟后再试。',429);
   if(windows.size>2000)for(const [id,v] of windows)if(now-v.start>60000)windows.delete(id);
  }
  if(!db)fail('交流区正在准备，请稍后再来。',503);
  if(path==='/api/community/profile'&&request.method==='PUT'){
   const input=await bodyOf(request),nickname=clean(input.nickname,2,20,'昵称');
   await db.prepare('INSERT INTO community_profiles (user_id,nickname,created_at) VALUES (?,?,?) ON CONFLICT(user_id) DO UPDATE SET nickname=excluded.nickname').bind(user.id,nickname,new Date().toISOString()).run();return reply({nickname});
  }
  if(write&&request.method!=='DELETE'&&!path.endsWith('/moderate')&&!(await profile(db,user.id)))fail('请先设置公开昵称，再参与交流。',409);
  if(path==='/api/community/posts'&&request.method==='GET'){
   const city=url.searchParams.get('city'),museum=url.searchParams.get('museum'),topic=url.searchParams.get('topic'),mine=url.searchParams.get('mine')==='1',cursor=url.searchParams.get('before');
   if(mine&&!user)fail('登录后查看自己的分享。',401);
   const where=[mine?"p.status IN ('published','hidden')":"p.status='published'"],values=[];
   if(city){where.push('p.city=?');values.push(city)}if(museum){where.push('p.museum_id=?');values.push(museum)}if(topic){where.push('p.topic=?');values.push(topic)}if(mine){where.push('p.author_id=?');values.push(user.id)}
   // Cursor includes the id, so same-timestamp posts cannot disappear between pages.
   if(cursor){const [time,id]=cursor.split('|');if(!time||!id||cursor.length>120)fail('分页标记无效');where.push('(p.created_at < ? OR (p.created_at = ? AND p.id < ?))');values.push(time,time,id)}
   const data=await db.prepare(selectPost+' WHERE '+where.join(' AND ')+' ORDER BY p.created_at DESC,p.id DESC LIMIT 21').bind(...values).all(),rows=data.results||[],more=rows.length>20,items=rows.slice(0,20),last=items.at(-1);
   return reply({posts:items.map(p=>postView(p,user)),next:more&&last?last.created_at+'|'+last.id:null});
  }
  if(path==='/api/community/posts'&&request.method==='POST'){
   const input=await bodyOf(request),title=clean(input.title,2,80,'标题'),body=clean(input.body,5,3000,'正文'),topic=clean(input.topic||'观察',1,10,'话题');if(!['观察','问题','行程','分享'].includes(topic))fail('请选择已有话题');
   const museum=input.museumId?catalog.museums.find(m=>m.id===input.museumId):null;if(input.museumId&&!museum)fail('场馆暂未收录');
   const city=museum?.city||input.city||null;if(city&&!catalog.museums.some(m=>m.city===city))fail('城市暂未收录');
   let route=null;if(input.route){const r=input.route;if(!Array.isArray(r.ids)||r.ids.length<1||r.ids.length>8||new Set(r.ids).size!==r.ids.length||r.ids.some(id=>!catalog.museums.some(m=>m.id===id&&m.city===city)))fail('分享的行程须为同一城市的已收录场馆');if(!['walk','transit','driving'].includes(r.mode))fail('出行方式无效');route={ids:r.ids,mode:r.mode,name:clean(r.name||city+'的博物之旅',1,60,'行程名')};}
   const id=crypto.randomUUID(),now=new Date().toISOString();await db.prepare('INSERT INTO community_posts (id,author_id,title,body,topic,city,museum_id,route_json,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)').bind(id,user.id,title,body,topic,city,museum?.id||null,route?JSON.stringify(route):null,'published',now,now).run();return reply({id},201);
  }
  const match=path.match(/^\/api\/community\/posts\/([a-zA-Z0-9-]{1,80})(?:\/(comments|like|report|moderate))?$/);
  if(match){
   const id=match[1],action=match[2],post=await db.prepare(selectPost+' WHERE p.id=?').bind(id).first();if(!post||(post.status!=='published'&&!user?.moderator&&post.author_id!==user?.id))fail('这篇分享暂时不可见。',404);
   if(!action&&request.method==='GET'){
    const comments=await db.prepare('SELECT c.*,u.nickname FROM community_comments c LEFT JOIN community_profiles u ON c.author_id=u.user_id WHERE c.post_id=? ORDER BY c.created_at ASC,c.id ASC LIMIT 101').bind(id).all();
    const liked=user?!!await db.prepare('SELECT 1 AS yes FROM community_likes WHERE post_id=? AND user_id=?').bind(id,user.id).first():false;
    return reply({post:postView(post,user),liked,comments:(comments.results||[]).slice(0,100).map(c=>({id:c.id,body:c.body,nickname:c.nickname||'观物旅人',isSelf:c.author_id===user?.id,createdAt:c.created_at})),commentsLimited:(comments.results||[]).length>100});
   }
   if(!action&&request.method==='DELETE'){
    if(post.author_id!==user.id&&!user.moderator)fail('只能删除自己的分享。',403);await db.prepare('DELETE FROM community_posts WHERE id=?').bind(id).run();return reply({deleted:true});
   }
   if(action==='comments'&&request.method==='POST'){
    if(post.status!=='published')fail('这篇分享暂时不可回复。',409);const input=await bodyOf(request),body=clean(input.body,1,1000,'回复'),commentId=crypto.randomUUID();
    const count=await db.prepare('SELECT COUNT(*) AS n FROM community_comments WHERE post_id=?').bind(id).first();if(count.n>=100)fail('这篇分享的回复已满，请另开一篇继续交流。',409);
    await db.prepare('INSERT INTO community_comments (id,post_id,author_id,body,created_at) VALUES (?,?,?,?,?)').bind(commentId,id,user.id,body,new Date().toISOString()).run();return reply({id:commentId},201);
   }
   if(action==='like'&&['PUT','DELETE'].includes(request.method)){
    if(request.method==='PUT')await db.prepare('INSERT INTO community_likes (post_id,user_id,created_at) VALUES (?,?,?) ON CONFLICT(post_id,user_id) DO NOTHING').bind(id,user.id,new Date().toISOString()).run();
    else await db.prepare('DELETE FROM community_likes WHERE post_id=? AND user_id=?').bind(id,user.id).run();return reply({liked:request.method==='PUT'});
   }
   if(action==='report'&&request.method==='POST'){
    const input=await bodyOf(request),reason=clean(input.reason,2,200,'举报原因');await db.prepare('INSERT INTO community_reports (id,post_id,reporter_id,reason,status,created_at) VALUES (?,?,?,?,?,?) ON CONFLICT(post_id,reporter_id) DO UPDATE SET reason=excluded.reason,status=excluded.status').bind(crypto.randomUUID(),id,user.id,reason,'pending',new Date().toISOString()).run();return reply({reported:true});
   }
   if(action==='moderate'&&request.method==='PUT'){
    if(!user.moderator)fail('没有管理权限。',403);const input=await bodyOf(request);if(!['published','hidden'].includes(input.status))fail('状态无效');await db.batch([db.prepare('UPDATE community_posts SET status=?,updated_at=? WHERE id=?').bind(input.status,new Date().toISOString(),id),db.prepare("UPDATE community_reports SET status='reviewed' WHERE post_id=?").bind(id)]);return reply({status:input.status});
   }
  }
  const comment=path.match(/^\/api\/community\/comments\/([a-zA-Z0-9-]{1,80})$/);if(comment&&request.method==='DELETE'){
   const row=await db.prepare('SELECT author_id FROM community_comments WHERE id=?').bind(comment[1]).first();if(!row)fail('回复不存在。',404);if(row.author_id!==user.id&&!user.moderator)fail('只能删除自己的回复。',403);await db.prepare('DELETE FROM community_comments WHERE id=?').bind(comment[1]).run();return reply({deleted:true});
  }
  if(path==='/api/community/reports'&&request.method==='GET'){
   if(!user?.moderator)fail('没有管理权限。',403);const data=await db.prepare("SELECT r.id,r.post_id,r.reason,r.created_at,p.title,p.status,u.nickname FROM community_reports r JOIN community_posts p ON p.id=r.post_id LEFT JOIN community_profiles u ON u.user_id=r.reporter_id WHERE r.status='pending' ORDER BY r.created_at DESC LIMIT 100").all();return reply({reports:data.results||[]});
  }
  return reply({error:'未找到该接口。'},404);
 }catch(error){if(error.status)return reply({error:error.message},error.status);console.error('community_request_failed',error.name,error.message);return reply({error:'交流服务暂时不可用，请稍后重试。'},503)}
}
