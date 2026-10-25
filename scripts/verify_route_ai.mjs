import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {privateConfig} from './private_config.mjs';
import {handleGuide} from '../server-app/lib/guide.mjs';
const require=createRequire(import.meta.url),catalog=require('../server-app/lib/catalog.json');
const response=await handleGuide(new Request('https://local.test/api/guide',{method:'POST',body:JSON.stringify({context:'city:北京',message:'我自定义中国国家博物馆、故宫博物院、中国工艺美术馆这三家馆，打算分两天慢看。请先查资料，给一个主题观看顺序建议，附来源。不估算交通，不代预约。'})}),privateConfig(),catalog);
const data=await response.json();console.log(JSON.stringify({status:response.status,provider:data.provider,answer:data.answer,references:data.references,error:data.error},null,2));assert.equal(response.status,200);assert.ok(data.answer.includes('故宫')&&data.answer.includes('国家博物馆')&&data.answer.includes('工艺'));assert.ok(data.references.length>=3);
