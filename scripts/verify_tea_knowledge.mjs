import {handleKnowledge} from '../server-app/lib/knowledge.mjs';
import {privateConfig} from './private_config.mjs';
import {createRequire} from 'node:module';
import {writeFileSync} from 'node:fs';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json'),env=privateConfig(),results=[];
// Ten fixed questions are run against the real provider. Review the saved answers,
// not just HTTP success: source-ID validity alone cannot prove entailment.
for(const entry of catalog.knowledge.questions){
 const response=await handleKnowledge(new Request('https://test/api/knowledge/ask',{method:'POST',body:JSON.stringify({question:entry.question,ids:entry.objects.slice(0,2)})}),env,catalog);
 const result=await response.json();results.push({question:entry.question,status:response.status,answer:result.answer,error:result.error,evidenceIds:result.evidence?.sources.map(s=>s.id),reviewAgainst:entry});
 console.log(JSON.stringify({question:entry.question,status:response.status,citations:result.answer?.citations?.length,error:result.error}));
}
writeFileSync('output/tea-live-evaluation.json',JSON.stringify(results,null,2));
if(results.some(r=>r.status!==200))process.exitCode=1;
