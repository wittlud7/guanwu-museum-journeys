# 北京新增47馆核验记录

核验日期：2026-10-25。北京原有3处（故宫、中国国家博物馆、中国工艺美术馆/中国非遗馆）不在新增列表中。新增47处，合计北京50处独立参观馆或馆区。

## 方法与信息边界

基础来源为北京市文化和旅游局宣传中心运营的北京旅游网资源库，结合馆方、北京市文物局、市政府及区文旅局资料校正。逐页HTTP取回的文字证据保存在 beijing-museums-source-evidence.json；人工网页核验片段保存在 bjbatch*-evidence.txt。正文以原创概述和观察建议为主，不逐字复制来源。

每馆收录区域、固定馆址、主题、简介、3个带来源看点和3段文字阅读。audio:false 明确本轮无新增真人或合成讲解音频。建议停留时长是编辑建议；没有实时开放、票价、余票或展品在展保证。

## 关键订正

- 中国航空博物馆北京原址2025-10-09起闭馆，未收录；替为北航学院路校区的北京航空航天博物馆（bj-beihang），避免给出闭馆参观路线。闭馆原始公告由馆方发布、京报转载：https://news.bjd.com.cn/2025/10/08/11341813.shtml 。
- 万寿寺内原北京艺术博物馆2026-07-02更名为万寿寺博物馆，馆舍和点位延续；使用新名保留旧名检索。通州新北京艺术博物馆在建，不当作开放场馆。
- 北京大运河博物馆明确为首都博物馆东馆，按可独立参观馆区计数，不声称为另一法人机构。
- 保利采用市文物局2024年更新的新保利大厦云楼9层馆址，舍弃旅游资源库旧保利大厦地址。恭王府前海西街与柳荫街为同园区地址，不把地图参考点称作入场口。
- 北京天文馆初始候选URL误指航天博物馆，已彻底更换为正确的101758及馆方bjp.org.cn参观资料；旧误链已从source-evidence和seed记录中移除。
- 大葆台采用2025年改建重开后的郭公庄707号；海淀采用2026年区文旅局公布海淀公园路6号新馆，舍弃中关村旧址。永定河采用区文旅局2026年门头沟路8号而非旅游页模糊增产路。
- 红楼馆说明为文学/影视创作相关园林，不能当小说人物真实故居；周口店区分遗址与博物馆；铁道只收东郊馆区；鲁迅只收宫门口馆区。
- 地图45个WGS84馆区参考点经独立审计，海淀和永定河缺可信点标注不可用，未猜测。地图点不代表入口，未提供虚构交通时长。
- 45张许可图片另由照片任务核验，见 beijing-museums-image-credits.json。徐悲鸿和永定河未获取许可对应实景图，留空而不借用别馆图片。

## 分馆与地址逐条核验

| ID | 场馆 | 区域 | 固定馆址 | 官方资料 |
| --- | --- | --- | --- | --- |
| bj-capital | 首都博物馆 | 西城区 | 北京市西城区复兴门外大街16号 | [北京市文旅局宣传中心 · 首都博物馆介绍](https://s.visitbeijing.com.cn/attraction/117799) |
| bj-grand-canal | 北京大运河博物馆（首都博物馆东馆） | 通州区 | 北京市通州区绿心路1号院5号楼 | [北京市政府或主管部门 · 北京大运河博物馆（首都博物馆东馆）介绍](https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/tzxx/202312/t20231224_3508754.html) |
| bj-art | 中国美术馆 | 东城区 | 北京市东城区五四大街1号 | [北京市文旅局宣传中心 · 中国美术馆介绍](https://s.visitbeijing.com.cn/attraction/101747) |
| bj-geology | 中国地质博物馆 | 西城区 | 北京市西城区西四羊肉胡同15号 | [北京市文旅局宣传中心 · 中国地质博物馆介绍](https://s.visitbeijing.com.cn/attraction/101820) |
| bj-agriculture | 中国农业博物馆 | 朝阳区 | 北京市朝阳区东三环北路16号 | [北京市文旅局宣传中心 · 中国农业博物馆介绍](https://s.visitbeijing.com.cn/attraction/118142) |
| bj-paleozoo | 中国古动物馆 | 西城区 | 北京市西城区西直门外大街142号 | [北京市文旅局宣传中心 · 中国古动物馆介绍](https://s.visitbeijing.com.cn/attraction/118089) |
| bj-science | 中国科学技术馆 | 朝阳区 | 北京市朝阳区北辰东路5号 | [北京市文旅局宣传中心 · 中国科学技术馆介绍](https://s.visitbeijing.com.cn/attraction/117814) |
| bj-military | 中国人民革命军事博物馆 | 海淀区 | 北京市海淀区复兴路9号 | [北京市文旅局宣传中心 · 中国人民革命军事博物馆介绍](https://s.visitbeijing.com.cn/attraction/119065) |
| bj-planetarium | 北京天文馆 | 西城区 | 北京市西城区西直门外大街138号 | [北京市文旅局宣传中心 · 北京天文馆介绍](https://s.visitbeijing.com.cn/attraction/101758)、[北京天文馆 · 参观指南与票务](https://www.bjp.org.cn/cgzn/pwxx/index.shtml) |
| bj-nature | 国家自然博物馆 | 东城区 | 北京市东城区天桥南大街126号 | [北京市文旅局宣传中心 · 国家自然博物馆介绍](https://s.visitbeijing.com.cn/attraction/118099) |
| bj-bells | 大钟寺古钟博物馆 | 海淀区 | 北京市海淀区北三环西路甲31号 | [北京市文旅局宣传中心 · 大钟寺古钟博物馆介绍](https://s.visitbeijing.com.cn/attraction/118041) |
| bj-wanshou | 万寿寺博物馆（原北京艺术博物馆） | 海淀区 | 北京市海淀区西三环北路万寿寺内 | [北京市文旅局宣传中心 · 北京艺术博物馆介绍](https://s.visitbeijing.com.cn/attraction/118096)、[万寿寺博物馆 · 2026年7月2日更名公告](https://wanshousimuseum.cn/ybdt/2836.htm)、[万寿寺博物馆 · 馆情与基本陈列](https://wanshousimuseum.cn/ybjj/index.htm)、[万寿寺博物馆 · 官方入口与开放服务](https://wanshousimuseum.cn/) |
| bj-architecture | 北京古代建筑博物馆 | 西城区 | 北京市西城区东经路21号先农坛内 | [北京市文旅局宣传中心 · 北京古代建筑博物馆介绍](https://s.visitbeijing.com.cn/attraction/119967) |
| bj-stone | 北京石刻艺术博物馆 | 海淀区 | 北京市海淀区五塔寺村24号 | [北京市文旅局宣传中心 · 北京石刻艺术博物馆介绍](https://s.visitbeijing.com.cn/attraction/119047) |
| bj-luxun | 北京鲁迅博物馆 | 西城区 | 北京市西城区阜成门内大街宫门口二条19号 | [北京市文旅局宣传中心 · 北京鲁迅博物馆介绍](https://s.visitbeijing.com.cn/attraction/120369) |
| bj-xubeihong | 徐悲鸿纪念馆 | 西城区 | 北京市西城区新街口北大街53号 | [北京市文旅局宣传中心 · 徐悲鸿纪念馆介绍](https://s.visitbeijing.com.cn/attraction/117897) |
| bj-guomoruo | 郭沫若纪念馆 | 西城区 | 北京市西城区前海西街18号 | [北京市文旅局宣传中心 · 郭沫若纪念馆介绍](https://s.visitbeijing.com.cn/attraction/118107) |
| bj-meilanfang | 梅兰芳纪念馆 | 西城区 | 北京市西城区护国寺街9号 | [北京市文旅局宣传中心 · 梅兰芳纪念馆介绍](https://s.visitbeijing.com.cn/attraction/101789) |
| bj-laoshe | 老舍纪念馆 | 东城区 | 北京市东城区灯市口西街丰富胡同19号 | [北京市文旅局宣传中心 · 老舍纪念馆介绍](https://s.visitbeijing.com.cn/attraction/101721) |
| bj-red-chamber | 北京红楼文化艺术博物馆 | 西城区 | 北京市西城区南菜园街12号大观园内 | [北京市文旅局宣传中心 · 北京红楼文化艺术博物馆介绍](https://s.visitbeijing.com.cn/attraction/118150) |
| bj-folk | 北京民俗博物馆 | 朝阳区 | 北京市朝阳区朝阳门外大街141号东岳庙内 | [北京市文旅局宣传中心 · 北京民俗博物馆介绍](https://s.visitbeijing.com.cn/attraction/118111) |
| bj-opera | 北京戏曲博物馆 | 西城区 | 北京市西城区虎坊路3号湖广会馆内 | [北京市文旅局宣传中心 · 北京戏曲博物馆介绍](https://s.visitbeijing.com.cn/attraction/118165) |
| bj-gongwang | 恭王府博物馆 | 西城区 | 北京市西城区前海西街17号、柳荫街甲14号恭王府 | [北京市文旅局宣传中心 · 恭王府博物馆介绍](https://s.visitbeijing.com.cn/attraction/117810)、[西城区政府 · 恭王府及花园（2026年）](https://www.bjxch.gov.cn/zt/schjmp/xxxq/pnidpv932679.html) |
| bj-guozijian | 孔庙和国子监博物馆 | 东城区 | 北京市东城区国子监街13号、15号 | [北京市文旅局宣传中心 · 孔庙和国子监博物馆介绍](https://s.visitbeijing.com.cn/attraction/117801) |
| bj-guanfu | 观复博物馆 | 朝阳区 | 北京市朝阳区金盏乡张万坟金南路18号 | [北京市文旅局宣传中心 · 观复博物馆介绍](https://s.visitbeijing.com.cn/attraction/120347) |
| bj-poly | 保利艺术博物馆 | 东城区 | 北京市东城区朝阳门北大街1号新保利大厦云楼9层 | [北京市文旅局宣传中心 · 保利艺术博物馆介绍](https://s.visitbeijing.com.cn/attraction/118166)、[北京市文物局 · 新保利大厦馆址（2024更新）](https://map.beijing.gov.cn/place?categoryId=bwg&placeId=5c2dc49f080b852d3f422938) |
| bj-zitan | 中国紫檀博物馆 | 朝阳区 | 北京市朝阳区兴隆西街9号 | [北京市文旅局宣传中心 · 中国紫檀博物馆介绍](https://s.visitbeijing.com.cn/attraction/117822) |
| bj-garden | 中国园林博物馆 | 丰台区 | 北京市丰台区射击场路15号 | [北京市文旅局宣传中心 · 中国园林博物馆介绍](https://s.visitbeijing.com.cn/attraction/118284) |
| bj-film | 中国电影博物馆 | 朝阳区 | 北京市朝阳区南影路9号 | [北京市文旅局宣传中心 · 中国电影博物馆介绍](https://s.visitbeijing.com.cn/attraction/118102) |
| bj-railway | 中国铁道博物馆（东郊展馆） | 朝阳区 | 北京市朝阳区酒仙桥北路1号院北侧 | [北京市文旅局宣传中心 · 中国铁道博物馆（东郊展馆）介绍](https://s.visitbeijing.com.cn/attraction/120341) |
| bj-auto | 北京汽车博物馆 | 丰台区 | 北京市丰台区南四环西路126号 | [北京市文旅局宣传中心 · 北京汽车博物馆介绍](https://s.visitbeijing.com.cn/attraction/118093) |
| bj-beihang | 北京航空航天博物馆 | 海淀区 | 北京市海淀区学院路37号北京航空航天大学学院路校区内 | [北京市文旅局宣传中心 · 北京航空航天博物馆介绍](https://s.visitbeijing.com.cn/attraction/118108)、[海淀区文旅局 · 航空航天博物馆参观信息（2026年）](https://zyk.bjhd.gov.cn/kjhd/whhd/bwg/202603/t20260326_4809793_hd.shtml) |
| bj-civil-aviation | 民航博物馆 | 朝阳区 | 北京市朝阳区首都机场辅路民航200号地区 | [北京市政府或主管部门 · 民航博物馆介绍](https://www.beijing.gov.cn/tsbj/sys/wxp/202111/t20211101_2526248.html) |
| bj-printing | 中国印刷博物馆 | 大兴区 | 北京市大兴区兴华大街二段1号 | [北京市文旅局宣传中心 · 中国印刷博物馆介绍](https://s.visitbeijing.com.cn/attraction/117938) |
| bj-women | 中国妇女儿童博物馆 | 东城区 | 北京市东城区建国门内大街23号 | [北京市文旅局宣传中心 · 中国妇女儿童博物馆介绍](https://s.visitbeijing.com.cn/attraction/118061) |
| bj-overseas | 中国华侨历史博物馆 | 东城区 | 北京市东城区北新桥三条东口 | [北京市文旅局宣传中心 · 中国华侨历史博物馆介绍](https://s.visitbeijing.com.cn/attraction/121018) |
| bj-customs | 中国海关博物馆 | 东城区 | 北京市东城区建国门内大街6号 | [北京市文旅局宣传中心 · 中国海关博物馆介绍](https://s.visitbeijing.com.cn/attraction/119552) |
| bj-coins | 中国钱币博物馆 | 西城区 | 北京市西城区西交民巷17号院 | [北京市文旅局宣传中心 · 中国钱币博物馆介绍](https://s.visitbeijing.com.cn/attraction/101823) |
| bj-ethnic | 民族文化宫博物馆 | 西城区 | 北京市西城区复兴门内大街49号 | [北京市文旅局宣传中心 · 民族文化宫博物馆介绍](https://s.visitbeijing.com.cn/attraction/120314) |
| bj-literature | 中国现代文学馆 | 朝阳区 | 北京市朝阳区文学馆路45号 | [北京市文旅局宣传中心 · 中国现代文学馆介绍](https://s.visitbeijing.com.cn/attraction/118159) |
| bj-tsinghua | 清华大学艺术博物馆 | 海淀区 | 北京市海淀区清华园1号清华大学艺术博物馆 | [北京市文旅局宣传中心 · 清华大学艺术博物馆介绍](https://s.visitbeijing.com.cn/attraction/120342) |
| bj-archaeology | 中国考古博物馆 | 朝阳区 | 北京市朝阳区国家体育场北路1号院1号楼 | [北京市政府或主管部门 · 中国考古博物馆介绍](https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/tzxx/202309/t20230915_3260182.html) |
| bj-zhoukoudian | 周口店北京人遗址博物馆 | 房山区 | 北京市房山区周口店大街1号 | [北京市文旅局宣传中心 · 周口店北京人遗址博物馆介绍](https://s.visitbeijing.com.cn/attraction/101537) |
| bj-yunju | 北京房山云居寺石经博物馆 | 房山区 | 北京市房山区大石窝镇水头村云居寺 | [北京市文旅局宣传中心 · 北京房山云居寺石经博物馆介绍](https://s.visitbeijing.com.cn/attraction/101425) |
| bj-dabaotai | 北京大葆台遗址博物馆 | 丰台区 | 北京市丰台区郭公庄707号 | [北京市政府或主管部门 · 北京大葆台遗址博物馆介绍](https://wwj.beijing.gov.cn/bjww/362679/362680/482911/743621451/index.html) |
| bj-yongding | 永定河文化博物馆 | 门头沟区 | 北京市门头沟区门头沟路8号 | [北京市文旅局宣传中心 · 永定河文化博物馆介绍](https://s.visitbeijing.com.cn/attraction/121081)、[门头沟区文旅局 · 博物馆馆址（2026年）](https://www.bjmtg.gov.cn/bjmtg/c104895/202411/175088c5fa6a4ee78994b26e5530eb0a.shtml) |
| bj-haidian | 北京市海淀区博物馆（三山五园文化艺术中心） | 海淀区 | 北京市海淀区海淀公园路6号 | [北京市政府或主管部门 · 北京市海淀区博物馆（三山五园文化艺术中心）介绍](https://zyk.bjhd.gov.cn/kjhd/whhd/bwg/202603/t20260326_4809789_hd.shtml)、[海淀区政府 · 走进三山五园与新馆展陈](https://www.bjhd.gov.cn/ztzx/2025/sswy/) |
