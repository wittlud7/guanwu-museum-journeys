# 中国世界文化遗产与混合遗产核验

核验日期：2026-10-26。资料来源均为 UNESCO 世界遗产中心或中国政府、文物主管机构的一手资料。

## 范围与计数

[UNESCO 中国缔约国页](https://whc.unesco.org/en/statesparties/cn)当前列出中国 **61 项**世界遗产，其中 **42 项文化遗产、4 项混合遗产、15 项自然遗产**。本次完整收录前两类 **46 项**。不把自然遗产、世界遗产预备名单、非物质文化遗产、世界记忆项目或一般景区混入这一计数。

2026 年新增的 [景德镇手工瓷业遗存（1765）](https://whc.unesco.org/en/list/1765/)已在正式名录和国家页中，原文题名、列入年份及五个组成部分均以 UNESCO 为准。2025 年列入的[西夏陵（1736）](https://whc.unesco.org/en/list/1736/)也已收录。

本次条目是 **46 项遗产的整体导览，不是逐一覆盖全部遗产组成部分**。跨国、跨省、串联项目各按 UNESCO 一个项目计数，不把故宫、天坛、北京中轴线的重叠空间重复宣称成全新遗产。目录保留 UNESCO `unescoId`、`category`、`year` 和正式页面来源，可程序化核对完整性。

## 保存的可复核证据

- `world-heritage/china-country.html`：国家页当日快照。
- `world-heritage/unesco-list.xml`：官方全名录 XML 原始响应；`china-unesco-rows.json` 为提取的中国 61 项。
- `world-heritage/{id}.html`：46 个正式遗产页面原始响应，包含概述、突出普遍价值和地图引用。
- `world-heritage/map-{id}.json`：各正式页面所引用 UNESCO 地图服务的原始响应，含组成部分名称、国家、编号及经纬度。
- `world-heritage/official-brief-syntheses.json`：官方英文突出普遍价值摘要的证据摘取，用于内部核验，不直接展示为我们的原创内容。
- `world-heritage/curation.txt` / `curation.json`：逐项中文原创策展要点；`scripts/build_world_heritage.py` 根据固定证据构建 UMD 目录。
- `scripts/verify_world_heritage.mjs`：检查与官方名录集合相等、42+4 分类、年份、来源、138 看点/138 阅读章节、46 参考坐标原样匹配及既有博物馆关联 ID。

官方地图响应地址形如 `https://whc.unesco.org/?cid=31&l=en&id_site=1765&mode=json`。坐标采用该服务公布的 WGS84 遗产/组成部分参考点，**不是入口、售票处、停车场或可步行抵达的导航目的地**。跨国丝绸之路明确取中国组成点，未用可能落在境外的整体几何中心。页面 `components` 保存官方提供的组成部分，未自行编造入口或交通时长。

## 省份映射与串联边界

目录共涉及 **28 个已核实省级地区标签**，仅表示目录中这些遗产的已核实所在地或代表地区，不表示其他省份没有文化资源或没有世界遗产。长城尤其需要区分国家资源认定、整体世界遗产与具体参观地。

- **长城（438）**：UNESCO 官方地图提供八达岭、山海关、嘉峪关三个参考点，目录 `provinces` 保守列北京、河北、甘肃。另保留 `resourceProvinces` 15 省资源分布口径及独立解释，**不作为“15 省每段均获世遗认定”的依据**。资源分布来源：[北京市文物局长城介绍](https://wwj.beijing.gov.cn/bjww/wwjzzcslm/1737418/1738088/1742735/364326/index.html)，与[国家文物局保护通知](https://app.www.gov.cn/govdata/gov/202312/11/510157/article.html)互证。
- **大运河（1443）**：北京、天津、河北、山东、江苏、浙江、河南、安徽。31 个组成部分整体计一项，不将所有现代运河或沿线建筑自动纳入世界遗产。八省范围辅证：[国家发展改革委分省实施说明](https://www.ndrc.gov.cn/xwdt/ztzl/dyhgjwhgy/202010/t20201021_1301677.html)。
- **丝绸之路：长安—天山廊道的路网（1442）**：三国 33 个组成部分，中国 22 处位于陕西、河南、甘肃、新疆，官方地图逐点国家字段可复核。省份与各点辅证：[铁门关市政府公布的中国组成点清单](https://www.tmg.gov.cn/ztzl/zrzyhghzt/zrzydt/155098.htm)。不是全部丝绸之路遗址名录。
- **明清故宫（439）**：北京与辽宁沈阳，两宫共同计一项。
- **明清皇家陵寝（1004）**：北京、河北、辽宁、江苏、湖北；官方突出普遍价值明确列五省市，不当作单一参观入口。
- **高句丽王城、王陵及贵族墓葬（1135）**：辽宁桓仁与吉林集安，城址及相关墓葬共同计一项。
- **土司遗址（1474）**：湖南老司城、湖北唐崖土司城址、贵州海龙屯，三处共同计一项。
- **武夷山（911）**：福建、江西，两省的相关遗产区域共同计一项混合遗产。
- **泉州（1561）**：22 个组成遗产点共同计一项。
- **北京中轴线（1714）**：15 个组成部分共同计一项，和已列故宫、天坛等有空间关联。
- **景德镇（1765）**：城区制瓷中心、湖田古窑址、高岭瓷土矿业遗址、长岭瓷石矿业遗址、蛟潭柴薪产地共五个组成部分，整体计一项。

## 文案、图片与声音的证据边界

每项三条事实看点均链接到正式 UNESCO 页面，三章阅读内容加入的是明确的现场观察建议。观察问题、感受与个人解释不能当作历史事实。没有编造馆藏、开放时间、票价、展厅号或特定人物故事。

每项 `narrationText` 为固定的 118–147 字中文简介，事实来自相应官方条目；三种声音必须朗读同一原文。三章阅读章节仍标注 `audio:false`，不得把简介音轨冒充逐章完整讲解。关于当日开放、预约及入口的提示不代表已逐一核实实时营运信息。

照片许可另见 `world-heritage-image-credits.json`；串联项目只展示实际组成部分或代表地点的照片，图注明确具体地点，不能据一张代表照片宣称全部组成部分已实地拍摄。

## 46 项逐项来源

| UNESCO ID | 中文展示名 | 类型 | 首次列入年 | 已核实省级地区 |
| --- | --- | --- | --- | --- |
| [437](https://whc.unesco.org/en/list/437/) | 泰山 | 混合 | 1987 | 山东 |
| [438](https://whc.unesco.org/en/list/438/) | 长城 | 文化 | 1987 | 北京,河北,甘肃 |
| [439](https://whc.unesco.org/en/list/439/) | 明清故宫 | 文化 | 1987 | 北京,辽宁 |
| [440](https://whc.unesco.org/en/list/440/) | 莫高窟 | 文化 | 1987 | 甘肃 |
| [441](https://whc.unesco.org/en/list/441/) | 秦始皇陵及兵马俑坑 | 文化 | 1987 | 陕西 |
| [449](https://whc.unesco.org/en/list/449/) | 周口店北京人遗址 | 文化 | 1987 | 北京 |
| [547](https://whc.unesco.org/en/list/547/) | 黄山 | 混合 | 1990 | 安徽 |
| [703](https://whc.unesco.org/en/list/703/) | 承德避暑山庄及周围寺庙 | 文化 | 1994 | 河北 |
| [704](https://whc.unesco.org/en/list/704/) | 曲阜孔庙、孔林和孔府 | 文化 | 1994 | 山东 |
| [705](https://whc.unesco.org/en/list/705/) | 武当山古建筑群 | 文化 | 1994 | 湖北 |
| [707](https://whc.unesco.org/en/list/707/) | 拉萨布达拉宫历史建筑群 | 文化 | 1994 | 西藏 |
| [778](https://whc.unesco.org/en/list/778/) | 庐山国家公园 | 文化 | 1996 | 江西 |
| [779](https://whc.unesco.org/en/list/779/) | 峨眉山—乐山大佛 | 混合 | 1996 | 四川 |
| [811](https://whc.unesco.org/en/list/811/) | 丽江古城 | 文化 | 1997 | 云南 |
| [812](https://whc.unesco.org/en/list/812/) | 平遥古城 | 文化 | 1997 | 山西 |
| [813](https://whc.unesco.org/en/list/813/) | 苏州古典园林 | 文化 | 1997 | 江苏 |
| [880](https://whc.unesco.org/en/list/880/) | 颐和园 | 文化 | 1998 | 北京 |
| [881](https://whc.unesco.org/en/list/881/) | 天坛 | 文化 | 1998 | 北京 |
| [911](https://whc.unesco.org/en/list/911/) | 武夷山 | 混合 | 1999 | 福建,江西 |
| [912](https://whc.unesco.org/en/list/912/) | 大足石刻 | 文化 | 1999 | 重庆 |
| [1001](https://whc.unesco.org/en/list/1001/) | 青城山—都江堰 | 文化 | 2000 | 四川 |
| [1002](https://whc.unesco.org/en/list/1002/) | 皖南古村落：西递、宏村 | 文化 | 2000 | 安徽 |
| [1003](https://whc.unesco.org/en/list/1003/) | 龙门石窟 | 文化 | 2000 | 河南 |
| [1004](https://whc.unesco.org/en/list/1004/) | 明清皇家陵寝 | 文化 | 2000 | 北京,河北,辽宁,江苏,湖北 |
| [1039](https://whc.unesco.org/en/list/1039/) | 云冈石窟 | 文化 | 2001 | 山西 |
| [1135](https://whc.unesco.org/en/list/1135/) | 高句丽王城、王陵及贵族墓葬 | 文化 | 2004 | 吉林,辽宁 |
| [1110](https://whc.unesco.org/en/list/1110/) | 澳门历史城区 | 文化 | 2005 | 澳门 |
| [1114](https://whc.unesco.org/en/list/1114/) | 殷墟 | 文化 | 2006 | 河南 |
| [1112](https://whc.unesco.org/en/list/1112/) | 开平碉楼与村落 | 文化 | 2007 | 广东 |
| [1113](https://whc.unesco.org/en/list/1113/) | 福建土楼 | 文化 | 2008 | 福建 |
| [1279](https://whc.unesco.org/en/list/1279/) | 五台山 | 文化 | 2009 | 山西 |
| [1305](https://whc.unesco.org/en/list/1305/) | 登封“天地之中”历史建筑群 | 文化 | 2010 | 河南 |
| [1334](https://whc.unesco.org/en/list/1334/) | 杭州西湖文化景观 | 文化 | 2011 | 浙江 |
| [1389](https://whc.unesco.org/en/list/1389/) | 元上都遗址 | 文化 | 2012 | 内蒙古 |
| [1111](https://whc.unesco.org/en/list/1111/) | 红河哈尼梯田文化景观 | 文化 | 2013 | 云南 |
| [1442](https://whc.unesco.org/en/list/1442/) | 丝绸之路：长安—天山廊道的路网 | 文化 | 2014 | 陕西,河南,甘肃,新疆 |
| [1443](https://whc.unesco.org/en/list/1443/) | 大运河 | 文化 | 2014 | 北京,天津,河北,山东,江苏,浙江,河南,安徽 |
| [1474](https://whc.unesco.org/en/list/1474/) | 土司遗址 | 文化 | 2015 | 湖南,湖北,贵州 |
| [1508](https://whc.unesco.org/en/list/1508/) | 左江花山岩画文化景观 | 文化 | 2016 | 广西 |
| [1541](https://whc.unesco.org/en/list/1541/) | 鼓浪屿：历史国际社区 | 文化 | 2017 | 福建 |
| [1592](https://whc.unesco.org/en/list/1592/) | 良渚古城遗址 | 文化 | 2019 | 浙江 |
| [1561](https://whc.unesco.org/en/list/1561/) | 泉州：宋元中国的世界海洋商贸中心 | 文化 | 2021 | 福建 |
| [1665](https://whc.unesco.org/en/list/1665/) | 普洱景迈山古茶林文化景观 | 文化 | 2023 | 云南 |
| [1714](https://whc.unesco.org/en/list/1714/) | 北京中轴线：体现中国理想都城秩序的建筑群 | 文化 | 2024 | 北京 |
| [1736](https://whc.unesco.org/en/list/1736/) | 西夏陵 | 文化 | 2025 | 宁夏 |
| [1765](https://whc.unesco.org/en/list/1765/) | 景德镇手工瓷业遗存 | 文化 | 2026 | 江西 |
