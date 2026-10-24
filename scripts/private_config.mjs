import {readFileSync} from 'node:fs';
// Optional user-provided local file. This file is ignored by Git and never packaged.
export function privateConfig(){
  const env={...process.env};
  try {
    const config=JSON.parse(readFileSync(new URL('../settings.json',import.meta.url),'utf8').replace(/^\uFEFF/,'')),values=config.env||config;
    if(!env.DEEPSEEK_API_KEY){
      if(values.DEEPSEEK_API_KEY)env.DEEPSEEK_API_KEY=values.DEEPSEEK_API_KEY;
      else if(new URL(values.ANTHROPIC_BASE_URL||'https://invalid.local').hostname==='api.deepseek.com')env.DEEPSEEK_API_KEY=values.ANTHROPIC_AUTH_TOKEN;
    }
    env.DEEPSEEK_MODEL ||= values.DEEPSEEK_MODEL||values.ANTHROPIC_MODEL||'deepseek-flash';
  } catch(error) { if(error.code!=='ENOENT')throw new Error('本机 settings.json 配置格式无效，请检查 JSON。'); }
  return env;
}
