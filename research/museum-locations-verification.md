# 33 馆 WGS84 地图参考点核查

交付：`dist/museum-locations.js`。UMD `window.GUANWU_LOCATIONS` / CommonJS `module.exports`，以现有 museum id 为键。

结果：33 个馆 ID 完整覆盖；32 个有可核验场馆参考点；成都蜀锦织绣博物馆因馆址冲突标记 `unavailable:true`，不含 lat/lng。

## 来源和坐标含义

- 26 点来自实际读取并保存的 Wikidata P625（Earth/Q2，排除 deprecated）。P625 官方说明仅支持地球 WGS84：https://www.wikidata.org/wiki/Property:P625 。
- 6 点来自 OpenStreetMap 对应馆舍/馆区 POI。4 个用已命名馆舍轮廓的经纬范围中心；杭州与郑州商都使用 Nominatim 对对应 OSM 馆区实体返回的代表点。
- 全部 OSM 原始对象已经通过 `api.openstreetmap.org/api/0.6/...` 实际读取，馆名/地址或馆区与目录核对。Nominatim 原始结果包括 ODbL 归属，展示时保留 © OpenStreetMap contributors；Wikidata 结构化数据为 CC0。
- 没有将照片拍摄点当成建筑或入口坐标，没有把高德/百度的 GCJ-02/BD-09 数字直接写为 WGS84，没有猜测缺失点。
- 这些点只用于区域示意和选馆参考，全部带 accuracyNote，不代表游客入口、检票口、可步行到达位置或实时导航终点。

## 固定馆区

- 上海博物馆：人民大道201号人民广场馆，非东馆。
- 浙江省博物馆：孤山路25号孤山馆区，非之江馆区。
- 南越王博物院：解放北路867号王墓展区，非中山四路王宫。
- 郑州博物馆：文翰街9号文翰街馆，非嵩山路馆。
- 辛亥革命博物院：彭刘杨路258号南院，非武珞路北院。
- 故宫点位是宫城区域内代表点，不能凭该点决定入院方向。

## 被拒绝或待核实的候选

### 上海自然博物馆旧馆坐标已拒绝

Wikidata Q1312291 的 P625 为 31.23354,121.48278，指向旧馆一带。虽然条目图像是新馆，不能据此认为 P625 已同步迁移。最终选择 OSM way/425762388；原始标签同时有 `name=上海自然博物馆`、`addr:street=北京西路`、`addr:housenumber=510` 和 `opening_date=2015`。最终代表点为馆舍轮廓中心 31.23688225,121.4580124。

### 杭州同名公交站已排除

Nominatim 同时返回馆区 relation/19222156 与同名公交站 node/12691357506。最终使用 `tourism=museum` 且原始 relation 标签为浙江省非物质文化遗产馆的馆区实体，未使用公交站位置。

### 成都蜀锦织绣博物馆暂不落点

现有目录及成都青年志愿服务场馆活动页写草堂东路18号：https://cdyouth.cdcyl.org.cn/volunteer/site/project/204094 。OSM 唯一同名节点 node/4130339065 却明示 `addr:housenumber=2号`、`addr:street=草堂东路`；历史国家博物馆名录也曾写2号。无法在本次研究中证明此节点对应当前目录的18号场馆，因此最终不采用该候选坐标，也不把两处地址拼合成同一入口。

可以保留地址卡与选馆功能；地图中应清楚提示坐标待核实，不画虚构点或声称已算出到馆精确距离。

## 完整点位表

| id | 场馆与馆区 | 纬度 | 经度 | 坐标来源 |
|---|---|---:|---:|---|
| beijing | 中国工艺美术馆 · 中国非遗馆 | 40.00238 | 116.39124 | [Wikidata · 中国工艺美术馆 · 中国非遗馆（P625）](https://www.wikidata.org/wiki/Q10873736) |
| hangzhou | 浙江省非物质文化遗产馆 | 30.1621241 | 120.0993934 | [OpenStreetMap · 浙江省非物质文化遗产馆馆舍POI](https://www.openstreetmap.org/relation/19222156) |
| nanjing | 南京云锦博物馆 | 32.0385 | 118.73961 | [Wikidata · 南京云锦博物馆（P625）](https://www.wikidata.org/wiki/Q10906649) |
| chengdu | 成都蜀锦织绣博物馆 | 待核实 | 待核实 | [成都青年志愿服务 · 场馆活动地点](https://cdyouth.cdcyl.org.cn/volunteer/site/project/204094) |
| guangzhou | 粤剧艺术博物馆 | 23.1181587 | 113.23276665 | [OpenStreetMap · 粤剧艺术博物馆馆舍范围](https://www.openstreetmap.org/way/965382977) |
| xian | 陕西历史博物馆 | 34.22504804 | 108.95063301 | [Wikidata · 陕西历史博物馆（P625）](https://www.wikidata.org/wiki/Q1151210) |
| shanghai | 上海博物馆 · 人民广场馆 | 31.230278 | 121.470556 | [Wikidata · 上海博物馆 · 人民广场馆（P625）](https://www.wikidata.org/wiki/Q1051293) |
| suzhou | 苏州博物馆 | 31.32514 | 120.62354 | [Wikidata · 苏州博物馆（P625）](https://www.wikidata.org/wiki/Q998042) |
| wuhan | 湖北省博物馆 | 30.56388889 | 114.35888889 | [Wikidata · 湖北省博物馆（P625）](https://www.wikidata.org/wiki/Q4391403) |
| zhengzhou | 河南博物院 | 34.788889 | 113.666111 | [Wikidata · 河南博物院（P625）](https://www.wikidata.org/wiki/Q857752) |
| changsha | 湖南博物院 | 28.21526 | 112.98784 | [Wikidata · 湖南博物院（P625）](https://www.wikidata.org/wiki/Q5942029) |
| palace | 故宫博物院 | 39.91555556 | 116.39083333 | [Wikidata · 故宫博物院（P625）](https://www.wikidata.org/wiki/Q2047427) |
| national-china | 中国国家博物馆 | 39.90361111 | 116.395 | [Wikidata · 中国国家博物馆（P625）](https://www.wikidata.org/wiki/Q1074318) |
| zhejiang-history | 浙江省博物馆 · 孤山馆区 | 30.25347222 | 120.13861111 | [Wikidata · 浙江省博物馆 · 孤山馆区（P625）](https://www.wikidata.org/wiki/Q1278762) |
| national-silk | 中国丝绸博物馆 | 30.225 | 120.14722222 | [Wikidata · 中国丝绸博物馆（P625）](https://www.wikidata.org/wiki/Q569019) |
| nanjing-museum | 南京博物院 | 32.0425 | 118.81944444 | [Wikidata · 南京博物院（P625）](https://www.wikidata.org/wiki/Q1815891) |
| six-dynasties | 六朝博物馆 | 32.0448 | 118.79428 | [Wikidata · 六朝博物馆（P625）](https://www.wikidata.org/wiki/Q67931941) |
| chengdu-museum | 成都博物馆 | 30.65973 | 104.0612 | [Wikidata · 成都博物馆（P625）](https://www.wikidata.org/wiki/Q55696247) |
| sichuan-museum | 四川博物院 | 30.663075 | 104.03154167 | [Wikidata · 四川博物院（P625）](https://www.wikidata.org/wiki/Q10924774) |
| guangdong-museum | 广东省博物馆 | 23.11722222 | 113.32138889 | [Wikidata · 广东省博物馆（P625）](https://www.wikidata.org/wiki/Q5613636) |
| nanyue | 南越王博物院 · 王墓展区 | 23.14027778 | 113.25555556 | [Wikidata · 南越王博物院 · 王墓展区（P625）](https://www.wikidata.org/wiki/Q1507198) |
| xian-museum | 西安博物院 | 34.239 | 108.936 | [Wikidata · 西安博物院（P625）](https://www.wikidata.org/wiki/Q15928831) |
| beilin | 西安碑林博物馆 | 34.255 | 108.94833333 | [Wikidata · 西安碑林博物馆（P625）](https://www.wikidata.org/wiki/Q10519071) |
| shanghai-history | 上海市历史博物馆 | 31.23267 | 121.46663 | [Wikidata · 上海市历史博物馆（P625）](https://www.wikidata.org/wiki/Q779273) |
| shanghai-nature | 上海自然博物馆 | 31.23688225 | 121.4580124 | [OpenStreetMap · 上海自然博物馆馆舍范围](https://www.openstreetmap.org/way/425762388) |
| suzhou-silk | 苏州丝绸博物馆 | 31.32541667 | 120.61416667 | [Wikidata · 苏州丝绸博物馆（P625）](https://www.wikidata.org/wiki/Q4806827) |
| suzhou-garden | 苏州园林博物馆 | 31.32544145 | 120.62577435 | [OpenStreetMap · 苏州园林博物馆馆舍范围](https://www.openstreetmap.org/way/542534200) |
| wuhan-museum | 武汉博物馆 | 30.6138079 | 114.25097695 | [OpenStreetMap · 武汉博物馆馆舍范围](https://www.openstreetmap.org/way/369445342) |
| xinhai | 辛亥革命博物院 · 南院 | 30.53972222 | 114.30027778 | [Wikidata · 辛亥革命博物院 · 南院（P625）](https://www.wikidata.org/wiki/Q30946741) |
| zhengzhou-museum | 郑州博物馆 · 文翰街馆 | 34.74075556 | 113.54068333 | [Wikidata · 郑州博物馆 · 文翰街馆（P625）](https://www.wikidata.org/wiki/Q15935528) |
| shangdu | 郑州商都遗址博物院 | 34.7475745 | 113.6806525 | [OpenStreetMap · 郑州商都遗址博物院馆舍POI](https://www.openstreetmap.org/way/1341987750) |
| changsha-museum | 长沙博物馆 | 28.248679 | 112.986445 | [Wikidata · 长沙博物馆（P625）](https://www.wikidata.org/wiki/Q28837838) |
| changsha-slips | 长沙简牍博物馆 | 28.1883 | 112.9776 | [Wikidata · 长沙简牍博物馆（P625）](https://www.wikidata.org/wiki/Q28824296) |

## 实际验证

`python scripts/collect_museum_locations.py` 已通过：33个ID与目录一致；32点逐一与保存的源数据相等；经纬度为有限数字、坐标系WGS84；成都条目不含伪造 lat/lng。
Node 已实际 require CommonJS 并在 vm 中作为浏览器全局加载 UMD，两种方式都得到33条记录、32可用/1待核实。
保存的证据包括 Wikidata entity JSON、Wikipedia 到 Wikidata 的实体解析、Nominatim museum 实体结果，以及对应 OSM 原始 XML。
未修改主应用、后端、其他资产或目标状态。
