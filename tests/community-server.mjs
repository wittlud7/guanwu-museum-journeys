import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync,readdirSync} from 'node:fs';
import {createRequire} from 'node:module';
import {handleCommunity} from '../server-app/lib/community.mjs';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json'),sqlite=new DatabaseSync(':memory:');sqlite.exec('PRAGMA foreign_keys=ON');
for(const file of readdirSync('server-app/drizzle').filter(x=>x.endsWith('.sql')).sort())sqlite.exec(readFileSync('server-app/drizzle/'+file,'utf8'));
class Statement{constructor(sql,values=[]){this.sql=sql;this.values=values}bind(...values){return new Statement(this.sql,values)}async first(){return sqlite.prepare(this.sql).get(...this.values)||null}async all(){return {results:sqlite.prepare(this.sql).all(...this.values)}}async run(){const result=sqlite.prepare(this.sql).run(...this.values);return {meta:{changes:result.changes},success:true}}}
const DB={prepare:sql=>new Statement(sql),batch:async statements=>{sqlite.exec('BEGIN');try{const out=[];for(const statement of statements)out.push(await statement.run());sqlite.exec('COMMIT');return out}catch(error){sqlite.exec('ROLLBACK');throw error}}},env={DB,COMMUNITY_MODERATOR_EMAILS:'moderator@example.invalid'};
async function call(path,{method='GET',user,body,origin='https://community.test'}={}){const headers={};if(user){headers['oai-authenticated-user-id']=user;headers['oai-authenticated-user-email']=user+'@example.invalid'}if(method!=='GET'){headers.Origin=origin;headers['Content-Type']='application/json'}const response=await handleCommunity(new Request('https://community.test/api/community'+path,{method,headers,...(body?{body:JSON.stringify(body)}:{})}),env,catalog);return {...await response.json(),status:response.status}}
assert.equal((await call('/me')).authenticated,false);assert.equal((await call('/posts',{method:'POST',body:{title:'未经登录',body:'不应写入'}})).status,401);
assert.equal((await call('/posts',{method:'POST',user:'alice',origin:'https://evil.example',body:{title:'跨站请求',body:'不应写入'}})).status,403);
for(const user of ['alice','bob'])assert.equal((await call('/profile',{method:'PUT',user,body:{nickname:user==='alice'?'慢看旅人':'另一个观看者'}})).status,200);
assert.equal((await call('/posts',{method:'POST',user:'alice',body:{title:'未知场馆',body:'这条应当被拒绝',museumId:'does-not-exist'}})).status,400);
assert.equal((await call('/posts',{method:'POST',user:'alice',body:{title:'跨城错配',body:'这条应当被拒绝',city:'北京',route:{ids:['palace','xian'],mode:'walk'}}})).status,400);
const created=await call('/posts',{method:'POST',user:'alice',body:{title:'从故宫到国博，慢慢看',body:'先看院落，再对照器物。<script>这是普通文本</script>',topic:'行程',city:'北京',authorId:'bob',route:{name:'自己的北京路线',ids:['palace','national-china'],mode:'transit'}}});assert.equal(created.status,201);const id=created.id;
const publicFeed=await call('/posts');assert.equal(publicFeed.posts.length,1);assert.equal(publicFeed.posts[0].author.nickname,'慢看旅人');assert.ok(!JSON.stringify(publicFeed).includes('example.invalid'));assert.ok(!JSON.stringify(publicFeed).includes('author_id'));
assert.equal((await call('/posts/'+id,{user:'alice'})).post.author.isSelf,true);assert.equal((await call('/posts/'+id,{user:'bob'})).post.author.isSelf,false);assert.equal((await call('/posts?mine=1',{user:'bob'})).posts.length,0);
assert.equal((await call('/posts/'+id,{method:'DELETE',user:'bob'})).status,403);
const comment=await call('/posts/'+id+'/comments',{method:'POST',user:'bob',body:{body:'我想先看文字与尺度，再看纹样。'}});assert.equal(comment.status,201);assert.equal((await call('/posts/'+id)).comments.length,1);
assert.equal((await call('/comments/'+comment.id,{method:'DELETE',user:'alice'})).status,403);
await call('/posts/'+id+'/like',{method:'PUT',user:'bob'});await call('/posts/'+id+'/like',{method:'PUT',user:'bob'});assert.equal((await call('/posts/'+id)).post.likeCount,1);await call('/posts/'+id+'/like',{method:'DELETE',user:'bob'});assert.equal((await call('/posts/'+id)).post.likeCount,0);
await call('/posts/'+id+'/report',{method:'POST',user:'bob',body:{reason:'测试报告流程，仅本机数据。'}});await call('/posts/'+id+'/report',{method:'POST',user:'bob',body:{reason:'同一用户更新原因，不重复记录。'}});assert.equal((await call('/reports',{user:'bob'})).status,403);assert.equal((await call('/reports',{user:'moderator'})).reports.length,1);
assert.equal((await call('/posts/'+id+'/moderate',{method:'PUT',user:'moderator',body:{status:'hidden'}})).status,200);assert.equal((await call('/posts')).posts.length,0);assert.equal((await call('/posts?mine=1',{user:'alice'})).posts[0].status,'hidden');assert.equal((await call('/posts/'+id)).status,404);assert.equal((await call('/reports',{user:'moderator'})).reports.length,0);
await call('/posts/'+id+'/moderate',{method:'PUT',user:'moderator',body:{status:'published'}});assert.equal((await call('/posts')).posts.length,1);
assert.equal((await call('/comments/'+comment.id,{method:'DELETE',user:'bob'})).status,200);assert.equal((await call('/posts/'+id)).comments.length,0);
await call('/posts/'+id,{method:'DELETE',user:'alice'});assert.equal((await call('/posts')).posts.length,0);assert.equal(sqlite.prepare('SELECT COUNT(*) AS n FROM community_reports').get().n,0);sqlite.close();
console.log('PASS: actual SQLite schema; two-user posts/replies; identity binding; ownership; CSRF; unique likes/reports; moderator hide/restore; route validation; cascading deletion; no email or author-id leaks. Local data only.');
