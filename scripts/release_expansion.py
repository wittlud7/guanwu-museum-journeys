import json,re,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'dist/heritage-app.js';s=p.read_text(encoding='utf-8');s=s.replace('首批走进北京、杭州、南京、成都、广州的 5 座非遗相关场馆，整理 8 个工艺与表演观察专题、15 章场馆导览和 8 段工艺讲解。','现在覆盖 11 城 11 馆、18 件文物与 8 个工艺专题。原有 5 馆提供 23 段合成语音；新增 6 馆提供阅读手记。DeepSeek 伴游会查询收录资料并给出来源。');s=s.replace('城市非遗计划','城市博物馆计划').replace('<b>0${state.hero+1}</b>','<b>${String(state.hero+1).padStart(2,\'0\')}</b>');p.write_text(s,encoding='utf-8')
p=root/'dist/index.html';s=p.read_text(encoding='utf-8');s=s.replace('观物，随身的中国城市非遗指南。探索北京、杭州、南京、成都与广州的手艺、场馆与故事。','观物，随身的城市博物馆指南。探索11城11馆、18件文物与8门手艺，和AI伴游一起细看。');p.write_text(s,encoding='utf-8')
p=root/'dist/style.css';s=p.read_text(encoding='utf-8');s=re.sub(r"^@import url\('https://fonts.googleapis.com/[^\n]+\n",'',s);p.write_text(s,encoding='utf-8')
# This is the actual source project, not a compiled native package.
out=root/'output';out.mkdir(exist_ok=True)
shutil.make_archive(str(out/'观物-微信小程序'),'zip',root_dir=root/'miniprogram')
print('Release labels and native source archive ready.')
