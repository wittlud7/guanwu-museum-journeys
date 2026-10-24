import {privateConfig} from './private_config.mjs';
import {handleGuide} from '../server-app/lib/guide.mjs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json');
const env=privateConfig();
const response=await handleGuide(new Request('http://localhost/api/guide',{method:'POST',body:JSON.stringify({context:'yunjin',message:'用两句话介绍云锦，附上资料来源。'})}),env,catalog);
const body=await response.json();
console.log(JSON.stringify({status:response.status,model:env.DEEPSEEK_MODEL,answer:body.answer,references:body.references,error:body.error},null,2));
if(!response.ok)process.exitCode=1;
