"""Build reviewed, field-sourced tea records. Never scrape unrestricted full text.

Source facts were checked on 2026-10-29. Missing identifiers stay null.
Run after editing this file to regenerate web, server and native topic data.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
sources=[]
objects=[]
def source(id,title,url,institution,kind='collection',rights='未取得全文转载许可；仅整理事实、撰写摘要并链接原站。'):
 row=dict(id=id,title=title,url=url,institution=institution,kind=kind,checkedAt=DATE,textRights=rights)
 sources.append(row)
 return id
def obj(id,title,institution,museum,accession,period,date,medium,dimensions,technique,summary,url,**extra):
 sid=source('src-'+id,title+' · '+institution,url,institution,rights='基础藏品数据 CC0；策展文章不包含在此许可内。' if institution=='大都会艺术博物馆' else '未取得全文转载许可；仅整理事实、撰写摘要并链接原站。')
 fields=dict(title=title,originalName=title,institution=institution,accession=accession,period=period,dateOriginal=date,medium=medium,dimensions=dimensions,technique=technique,creditLine=None,provenance=None,use=None)
 fields.update(extra.pop('fields',{}))
 row=dict(id=id,title=title,aliases=[],institution=institution,museum=museum,period=period,objectType='茶壶' if '壶' in title else '茶盏',stage='泡茶' if period=='清' else '点茶',fields={k:dict(value=v,sourceIds=[sid] if v is not None else [],status='documented' if v is not None else 'missing') for k,v in fields.items()},summary=summary,summarySourceIds=[sid],sourceIds=[sid],interpretations=[],dateViews=[],image=dict(src=None,sourceUrl=url,status='link_only',rights='未确认本项目图片展示许可；请到馆方页面看原图。',policyUrl=None),checkedAt=DATE)
 row.update(extra)
 objects.append(row)
 return row

obj('tea-dpm-227128','建阳窑黑釉兔毫盏','故宫博物院','palace','故00143126','宋','宋','瓷','高5.8厘米；口径12.8厘米；足径3.9厘米','黑釉、兔毫结晶','釉层中出现细长结晶，形似兔毛。馆方同时提醒，宋金时期多地都烧兔毫盏，不能见到兔毫就断定产自建阳。','https://www.dpm.org.cn/collection/ceramic/227128.html')
obj('tea-dpm-227178','建阳窑黑釉盏','故宫博物院','palace','新00196618','宋','宋','瓷','高7.5厘米；口径18厘米；足径5厘米','黑釉、兔毫纹','这件大口径黑釉盏的灰白胎与典型建阳窑紫黑胎有别；馆方仍将它归入建阳窑类型器物。分类不等于能确定具体窑址。','https://www.dpm.org.cn/collection/ceramic/227178.html')
obj('tea-dpm-227688','紫砂题诗茶壶','故宫博物院','palace','新00119682','清','清代','紫砂陶',None,'陶刻题诗','壶腹刻诗并署“南林”款。可以观察诗、书与日用茶具如何相遇；现有条目未提供尺寸，不补填。','https://www.dpm.org.cn/collection/ceramic/227688.html',fields={'use':'茶壶；具体使用者未说明'})
obj('tea-dpm-227616','紫砂御题诗句烹茶图六方壶','故宫博物院','palace','故00157135','清','清乾隆','紫砂陶','高16.2厘米；口径4.2厘米；足径4.3厘米','堆泥绘、印刻御题诗','一面以堆泥表现烹茶，一面印刻乾隆七年（1742年）所作御题诗。它与同纹紫砂茶叶罐、瓷质盖碗成套，放入随行茶籝。','https://www.dpm.org.cn/collection/ceramic/227616.html',fields={'use':'此壶与同纹紫砂茶叶罐、青花松竹梅诗句盖碗、矾红松梅纹诗句盖碗等成套，置入紫檀或藤编茶籝，供皇帝出行携带；不是对每次出行清单的完整记录。'})
obj('tea-sh-619','建窑黑釉兔毫盏','上海博物馆','shanghai',None,'宋元','宋；详细年代：宋-元','瓷','高8.1厘米；口径18.4厘米；底径5.8厘米','黑釉、兔毫','馆方从建盏传入日本及其鉴藏地位解释这件器物。页面的时代与详细年代粒度不同，两者均保留。','https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00160019',aliases=['建窑兔毫盏'],dateViews=[{'label':'时代','value':'宋','sourceIds':['src-tea-sh-619']},{'label':'详细年代','value':'宋-元','sourceIds':['src-tea-sh-619']}])
obj('tea-sh-leaf','黑釉木叶纹盏','上海博物馆','shanghai',None,'南宋','南宋','瓷','高4.6厘米；口径10.7厘米；底径3.0厘米','吉州窑、黑釉、木叶纹','盏心木叶脉络与深色釉面形成对照。馆方将其放在宋代茶色审美中解释；关于桑叶与禅宗的联系，原站以学者研究观点表述。','https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00004968',aliases=['吉州窑黑釉木叶纹盏'])

met=[
 (42455,'建窑兔毫釉茶碗','91.1.226','宋','11th–12th century','Stoneware with "hare’s-fur" glaze (Jian ware)','高7.0厘米；直径12.7厘米','兔毫釉','英文断代为11至12世纪；页面中文题名含“南宋”。本专题保留两项原始表述，不擅自将它们合并成精确断代。'),
 (48117,'建窑兔毫茶盏','79.2.1358','宋','11th–12th century','Stoneware with “hare’s-fur” glaze (Jian ware)','高7.3厘米；直径12.1厘米','兔毫釉','馆方说明此类茶碗盛放经击拂形成白色泡沫的茶；深色釉面帮助观察茶色。'),
 (51071,'建窑铁釉包金属口茶碗','29.100.240','宋','11th–12th century','Stoneware with iron-oxide glaze, metal rim (Jian ware)','高5.7厘米；直径11.4厘米','铁氧化物釉、金属口沿','金属口沿是馆方材料记录的一部分。来源未说明加装年代及原因，不能直接讲成原装或修补。'),
 (51072,'建窑铁釉包金属口茶碗','29.100.239','宋','11th–12th century','Stoneware with iron-oxide glaze, metal rim (Jian ware)','高7.3厘米；直径12.4厘米','铁氧化物釉、金属口沿','与29.100.240同名同类但编号、尺寸不同，是两件藏品。名称相同不能据此合并。'),
 (42457,'建窑铁釉茶碗','29.100.226','宋','11th–12th century','Stoneware with iron-oxide glaze (Jian ware)','高6.4厘米；直径11.7厘米','铁氧化物釉','馆方将建窑器与赴日僧侣、天目山及日本天目称谓联系起来。不能因此推断本件的具体传入路线。'),
 (48100,'建窑铁釉茶碗','16.60','宋','11th–12th century','Stoneware with iron-oxide glaze (Jian ware)','高4.1厘米；直径11.4厘米','铁氧化物釉','尺寸较浅。可以与其他建窑茶碗比较高与径，但不能仅凭尺寸推断主人的身份。'),
 (48107,'茶洋窑铁釉茶碗','17.179.5','南宋','12th–late 13th century"','Stoneware with iron-oxide glaze (Chayang ware)','高5.4厘米；直径13厘米','铁氧化物釉','馆方归类为茶洋窑，不是建窑。原始日期字段末尾有引号，保留原文以便追溯。'),
 (52598,'茶洋窑铁釉茶碗','17.179.4','南宋','12th–late 13th century','Stoneware with iron-oxide glaze (Chayang ware)','高5.1厘米；直径12.4厘米','铁氧化物釉','与17.179.5均为茶洋窑茶碗，尺寸和编号不同。保留独立条目，不把同类器当成同一件。'),
 (48105,'建窑铁釉茶碗','17.179.3','宋','11th–12th century','Stoneware with iron-oxide glaze (Jian ware)','高6.4厘米；直径11.7厘米','铁氧化物釉','与29.100.226尺寸接近，仍是独立编号的两件器物。比较时要先看身份信息。'),
 (51226,'吉州窑彩绘玳瑁釉茶碗','93.1.2','南宋','13th century','Stoneware with painted decoration on dark brown glaze, tortoise-shell glaze on reverse (Jizhou ware)','高4.4厘米；直径14.6厘米','深褐釉彩绘、外壁玳瑁釉','同一件器物的内外釉饰不同。馆方材料项将彩绘与外壁玳瑁釉分别记述，可与木叶纹盏对看。'),
 (48812,'当阳峪窑褐釉茶碗','17.175.10','宋','11th–12th century','Stoneware with brown glaze (Dangyangyu ware)','高7.0厘米；宽13.7厘米','褐釉','材料项标为当阳峪窑褐釉。深色茶碗不只出自福建，不能把所有黑褐釉茶碗统称为建盏。'),
 (48104,'四川窑褐釉茶碗','29.100.228','南宋','13th century','Stoneware with brown glaze (Sichuan ware)','高5.4厘米；直径12.4厘米','褐釉','馆方使用四川窑这一材料分类。具体窑址和使用者在当前整理字段中均未确认。'),
 (47545,'景德镇青花加彩茶壶','79.2.510a, b','清','18th century','Porcelain painted in underglaze blue and overglaze polychrome enamels of a later date (Jingdezhen ware)','高11.7厘米；宽17.5厘米；深10.5厘米','釉下青花、后加釉上彩','材料字段特别注明釉上彩为后加，不能将所有装饰都归为同一烧造阶段。'),
 (47879,'景德镇青花欧洲镶装茶壶','79.2.189a, b','清','late 17th–early 18th century','Porcelain painted with cobalt blue under transparent glaze (Jingdezhen ware); European mount','高10.8厘米','釉下青花、欧洲镶装','一件中国瓷壶与欧洲镶装相结合。来源只确认镶装类别，不能擅自补写具体作坊或订单故事。')
]
for n,title,acc,period,date,medium,size,tech,summary in met:
 row=obj('tea-met-'+str(n),title,'大都会艺术博物馆',None,acc,period,date,medium,size,tech,summary,'https://www.metmuseum.org/art/collection/search/'+str(n),aliases=['Teapot' if period=='清' else 'Tea bowl'],fields={'use':'馆方名称为茶壶' if period=='清' else '馆方名称为茶碗；具体使用者未说明'})
 if n==42455:row['dateViews']=[dict(label='英文 Date',value='11th–12th century',sourceIds=row['sourceIds']),dict(label='中文题名',value='中國 南宋 建窯 兔毫釉茶碗',sourceIds=row['sourceIds'])]
 row['fields']['originalName']['value']='Teapot' if period=='清' else 'Tea bowl'
 credit={42455:'Edward C. Moore Collection, Bequest of Edward C. Moore, 1891',48117:'Purchase by subscription, 1879',51071:'H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929',51072:'H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929',42457:'H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929',48100:'The Howard Mansfield Collection, Gift of Howard Mansfield, 1916',48107:'Rogers Fund, 1917',52598:'Rogers Fund',48105:'Rogers Fund, 1917',51226:'Gift of Mr. and Mrs. Samuel Colman, 1893',48812:'Rogers Fund, 1917',48104:'H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929',47545:'Purchase by subscription, 1879',47879:'Purchase by subscription, 1879'}[n]
 row['fields']['creditLine']=dict(value=credit,sourceIds=row['sourceIds'],status='documented')
 if n in [42455,48117,47545,51226]:
  imageIds={42455:1551585,48117:1912447,47545:66579,51226:195524}
  row['image']=dict(src='assets/knowledge/'+str(n)+'.jpg',sourceUrl='https://collectionapi.metmuseum.org/api/collection/v1/iiif/'+str(n)+'/'+str(imageIds[n])+'/main-image',status='cc0',rights='Public Domain · CC0；仅适用于此件馆方标记的开放图片。',policyUrl='https://www.metmuseum.org/policies/image-resources',credit='The Metropolitan Museum of Art · '+acc)

articles=[
 ('tea-world','一片叶子，如何改变生活','故宫博物院','https://www.dpm.org.cn/subject_tea/index.html','展览专题','饮茶方法、器具和文化交流共同变化。陆羽的茶书、宋代的茶事及明代品茗，给器物比较提供背景。','备茶 饮茶 用途 唐 宋 明 清 煎茶 点茶 泡茶 茶经 茶录',[
  '陆羽《茶经》从生产、备茶方法到饮茶器具系统讨论茶事。',
  '蔡襄《茶录》与《大观茶论》构成理解宋代茶事审美的重要背景。',
  '展览将明代视作饮茶文化的重要转变阶段，强调品茗环境与交游。']),
 ('tea-stand','茶盏为什么要配一个托','故宫博物院','https://www.dpm.org.cn/lemmas/244576.html','器物词条','盏托用来承托茶盏。它是理解端持动作与器物组合的线索，不能把任意碟子都判为盏托。','茶盏 茶托 盏托 用途 端持 防烫 宋',[
  '馆方把盏托解释为与茶盏配套的承托器。',
  '瓷质盏托始见于东晋；宋代多个窑口都有烧造。',
  '口沿既有圆形，也有花瓣形。']),
 ('tea-black','黑色茶盏，为什么适合看白沫','上海博物馆','https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00004855','藏品与背景解读','这件出土黑釉盏的解读，解释了宋代斗茶对黑釉器生产的影响，也给出真实的考古来源。','宋 点茶 斗茶 黑色 白色 泡沫 建窑 兔毫 釉色 为什么',[
  '该条目记载的黑釉盏来自上海青浦青龙镇遗址。',
  '馆方将斗茶重视白色茶汤与便于比试的黑盏联系起来。',
  '建窑周边其他窑口也生产黑釉器，器色不能单独确定产地。']),
 ('tea-east','从中国茶器，走向东亚茶文化','台北故宫博物院','https://south.npm.gov.tw/ExhibitionsDetailC003110.aspx?Cond=9963f5e2-df38-4cb3-bfdf-b689c14ca3f7','展览专题','茶法随制茶方式变化，并在不同地区形成各自习惯；同样喝茶，并不意味着使用同一套仪式。','煎茶 点茶 泡茶 方法 变化 唐 宋 明 日本 蒙藏 奶茶 工夫茶',[
  '展览将中国、日本、蒙藏与台湾茶文化放在相互交流的脉络中观察。',
  '茶器形式与品饮方法随制茶方式而变化。',
  '唐宋时期使者、僧侣与贸易参与了茶文化向日本的传播。']),
 ('tea-japan','茶会里的器物，怎样获得新意义','大都会艺术博物馆','https://www.metmuseum.org/essays/the-japanese-tea-ceremony','馆方策展文章','日本茶会使用的中国陶瓷，并不只是饮用工具，还成为被鉴赏、收藏的对象；这是跨文化背景，而非每件器物的流传证明。','日本 天目 建窑 僧侣 茶会 茶碗 文化 传播 茶道',[
  '馆方区分了茶具的实用价值与审美价值。',
  '日本茶会曾重视传承下来的中国古陶瓷，后来也吸收朝鲜与日本陶瓷。',
  '不能将整个器物类型的交流史，直接写成某一件藏品的完整经历。'])
]
documents=[]
for id,title,inst,url,kind,summary,tags,claims in articles:
 sid=source('doc-'+id,title, url,inst,'background')
 documents.append(dict(id=id,title=title,institution=inst,kind=kind,summary=summary,tags=tags,claims=[dict(text=t,sourceIds=[sid]) for t in claims],sourceIds=[sid],checkedAt=DATE))
topics=[
 dict(id='tea',title='一盏茶里的中国生活',subtitle='从怎么喝，到为什么这样做。',intro='把不同博物馆的茶器放在同一张桌上，看见饮茶方法、手艺与交往的变化。',steps=[
  dict(title='先看动作：茶是怎样备好的？',text='从煎煮、击拂到冲泡，先读方法的变化。它们不是朝代之间整齐切开的唯一喝法。',objects=['tea-dpm-227128','tea-dpm-227688'],documents=['tea-world','tea-east']),
  dict(title='再看颜色：黑盏为什么流行？',text='从白色泡沫与黑色釉面的关系，回到具体茶盏；再比较兔毫、木叶与玳瑁釉。',objects=['tea-met-48117','tea-sh-leaf','tea-met-51226'],documents=['tea-black']),
  dict(title='最后看交往：谁在使用、收藏它？',text='从宫廷随行茶具到跨海鉴藏。类型史不能替代单件流传史，缺少记录的部分继续留白。',objects=['tea-dpm-227616','tea-met-47879'],documents=['tea-japan','tea-east'])])
]
questions=[
 dict(question='宋代人怎么喝茶？',keywords=['点茶','击拂','茶沫'],objects=['tea-met-48117'],documents=['tea-black','tea-east'],mustNot='将宋代所有饮茶方式写成只有点茶'),
 dict(question='为什么喝茶要用黑色的碗？',keywords=['白沫','黑盏','斗茶'],objects=['tea-dpm-227128'],documents=['tea-black'],mustNot='所有黑釉碗都来自建窑'),
 dict(question='兔毫是画上去的吗？',keywords=['结晶','釉','烧制'],objects=['tea-dpm-227128'],documents=[],mustNot='兔毫是画出的兔子毛'),
 dict(question='木叶盏和兔毫盏有什么不同？',keywords=['木叶','兔毫','窑'],objects=['tea-sh-leaf','tea-dpm-227128'],documents=['tea-black'],mustNot='把所有木叶都是桑叶写成已无争议的单件事实'),
 dict(question='两件都叫茶碗，是同一件吗？',keywords=['编号','尺寸'],objects=['tea-met-51071','tea-met-51072'],documents=[],mustNot='按名称合并藏品'),
 dict(question='紫砂壶是瓷器吗？',keywords=['紫砂','陶','材质'],objects=['tea-dpm-227688','tea-met-47545'],documents=[],mustNot='紫砂一律是瓷'),
 dict(question='乾隆出门怎样带茶具？',keywords=['茶籝','配套','出行'],objects=['tea-dpm-227616'],documents=[],mustNot='编造实际携带清单或容量'),
 dict(question='包金属口沿是不是破了才修的？',keywords=['口沿','未说明'],objects=['tea-met-51071'],documents=[],mustNot='断定包口沿就是修补'),
 dict(question='91.1.226到底是南宋还是11至12世纪？',keywords=['断代','不同','原始'],objects=['tea-met-42455'],documents=[],mustNot='强行消除原站不同字段的差异'),
 dict(question='这些茶器现在在哪个展厅，今天能看到吗？',keywords=['实时','展出','核对'],objects=[],documents=[],mustNot='编造实时展厅或当前展出承诺')
]
relations=[dict(fromId='tea-dpm-227128',toId='tea-met-48117',title='同样是兔毫，怎样衬托茶色？',text='两馆都以兔毫描述釉面；大都会的条目补充此类器物与击拂茶沫的关系。这是类型对照，不证明两件曾一起使用。',sourceIds=['src-tea-dpm-227128','src-tea-met-48117']),dict(fromId='tea-sh-leaf',toId='tea-met-51226',title='同一个窑口，不同的釉面语言',text='馆方均将器物归为吉州窑；一件是木叶纹，一件记有彩绘与外壁玳瑁釉。比较装饰，不假定同一工匠。',sourceIds=['src-tea-sh-leaf','src-tea-met-51226']),dict(fromId='tea-dpm-227688',toId='tea-met-47545',title='都是茶壶，陶与瓷如何相遇？',text='一件以紫砂呈现题诗，一件使用釉下青花与后加釉上彩。名称对应饮茶器具，材料与装饰各有线索。',sourceIds=['src-tea-dpm-227688','src-tea-met-47545'])]
data=dict(version=1,updated=DATE,scope='首批20件茶器、3家收藏机构、5篇背景资料；不等于已完整收录80家博物馆的全部公开藏品。',objects=objects,documents=documents,topics=topics,sources=sources,questions=questions,relations=relations)
assert len(objects)==20 and len(documents)==5
(ROOT/'research/tea-knowledge.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'dist/knowledge-data.js').write_text('const GUANWU_KNOWLEDGE='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\nif(typeof module!=="undefined")module.exports=GUANWU_KNOWLEDGE;\n',encoding='utf-8')
native=ROOT/'miniprogram/knowledge';native.mkdir(exist_ok=True)
(native/'data.js').write_text('module.exports='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('Knowledge: 20 objects, 3 collection institutions, 5 documents, 10 evaluation questions.')
