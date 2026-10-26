# 北京新增 47 馆地图参考点核查

核查日期：2026-10-25。交付 `dist/beijing-locations.js`，UMD 为 `window.GUANWU_BEIJING_LOCATIONS` / CommonJS `module.exports`。只含新增 `bj-*` ID，原有 3 个北京馆点位不改动。

47 个 ID 完整覆盖，其中 45 个为有原始证据的 WGS84 参考点，2 个显式 `unavailable:true` 且没有 lat/lng。它们用于馆区位置示意与选馆，不是入馆门、步行到达点或预约凭证，也不代表开放状态。

## 原始证据与复核

- 39 个点读取自 Wikidata P625，保存在 `beijing-locations-wikidata.json`。排除 deprecated，要求地球 Q2，保存原始 precision。P625 规范明确只支持地球 WGS84：https://www.wikidata.org/wiki/Property:P625 。候选由北京周边 90 公里博物馆查询获取，保留 `beijing-locations-wikidata-query.json`；不能把候选自动当作已核验结果。
- 6 个点读取自 OpenStreetMap：大钟寺、北京大观园、周口店博物馆、中国考古博物馆、中国农业博物馆、大葆台遗址博物馆。Nominatim 结果保存在 `beijing-locations-nominatim*.json`，相应 OSM way 的 `/full` 原始 XML 分别保存为 `beijing-locations-osm-bj-*.xml`。逐一检查实体 ID 和原始 name 标签；点位为 Nominatim 提供的馆舍或园区代表点，不是自行输入的 GCJ-02 / BD-09 数字。
- `beijing-locations-build.py` 是明确的审核清单和重建校验脚本；运行 `python research/beijing-locations-build.py` 会核验对应原始 P625/OSM、47 个 ID 及 45 个坐标。独占的 `beijing-locations-catalog.json` 是审核时固定的 ID/馆名快照，不读取其他流程可能修改的内容种子或照片查询文件。`beijing-locations-reviewed.json` 保存最终审核结果。
- 地图展示保留 © OpenStreetMap contributors 归属。OSM 证据为 ODbL；Wikidata 结构化数据为 CC0。不抓取或缓存地图瓦片。

## 分馆和新旧馆排除

- 中国科学技术馆 P625 同时有 40.005,116.39244 与 39.96856,116.386315。后者 qualifiers 写明“北京科学中心”，是北三环旧馆；明确选择奥林匹克公园现馆点。
- 中国农业博物馆 P625 两个坐标冲突，未直接选精度更高者；采用 OSM 同时标记“全国农业展览馆;中国农业博物馆”、门牌东三环北路 16 号的园区实体。
- 北京艺术博物馆以万寿寺馆区为参考，拒绝搜索命中的“2029 年计划开馆”同名新美术馆条目。
- 北京古代建筑博物馆以先农坛馆区为参考，北京石刻艺术博物馆以真觉寺馆区为参考，北京民俗博物馆以东岳庙馆区为参考。每条 accuracyNote 明确为馆区，不把寺庙中心冒充入口。
- 北京红楼文化艺术博物馆使用其所在北京大观园园区的 OSM 参考点，明确不是独立展厅点。
- 北京鲁迅博物馆采用阜成门宫门口馆区；中国铁道博物馆采用东郊展馆，均不混用其他馆区。
- 周口店采用名称明确的独立博物馆馆舍，不采用猿人洞、遗址入口或世界遗产总坐标。
- 大葆台采用“大葆台遗址博物馆”的 OSM 馆区对象，不用旧 Wikidata 约 0.01° 粗精度汉墓点。
- 清华大学艺术博物馆 P625 原始 precision 约 0.0117°；虽然坐标小数位多，仍在 accuracyNote 提醒仅作馆区示意，不能用于校门导航。
- 云居寺使用寺院馆区参考点，具体石经展厅与入园方向需另查馆方导览。
- 中国航空博物馆原址闭馆，不纳入新增列表；替换为学院路 37 号的北京航空航天博物馆 `bj-beihang`。

## 无坐标馆

- `bj-haidian`：海淀区博物馆现馆为海淀公园路 6 号三山五园文化艺术中心。旧 P625 Q10902252 位于中关村大街旧馆，拒绝使用；Nominatim 模糊查询还返回军博、地铁站、国家典籍博物馆，均已拒绝。
- `bj-yongding`：永定河文化博物馆未取得可核验的 WGS84 场馆实体。不能以永定河河流中心、门头沟区中心或同区其他博物馆代替。保留按中文馆址查询导航。

## 最终内容目录馆址对照

已读取最终 `dist/beijing-museums.js`，将全部 47 个馆名、馆址与点位源所指机构及固定馆区逐项对照；45 个参考点没有发现跨馆区冲突，2 个不可靠点仍保持无坐标。结果保存于 `beijing-locations-campus-audit.json`，可执行 `node research/beijing-locations-audit.cjs` 复核目录之后是否发生馆址变化。这个检查验证固定馆区关系，不能验证门口通行性、实时开闭馆或道路导航。

- 北京天文馆目录已改用西直门外大街 138 号和正确官方资料；初始旅游资料页混入“卢沟桥城内街 101 号”和航天馆公交，已通知内容流程拒绝，不作为地图或最终介绍依据。
- 保利艺术博物馆固定为朝阳门北大街 1 号新保利大厦，不把旧保利大厦当作现馆。
- 恭王府前海西街馆址和柳荫街入口均属于同一馆区；P625 参考点不替代入口信息，具体进馆方向以馆方预约导览为准。
- 海淀公园路 6 号三山五园新馆仍明确无坐标；永定河目录当前使用门头沟路 8 号，旧旅游页写增产路，点位未因此猜测补齐。

下表所有点均为参考点；最终小数值完整保存在 JS 与审核 JSON 中。

| ID | 场馆 | 来源 |
|---|---|---|
| bj-capital | 首都博物馆 | [Wikidata · 首都博物馆（P625）](https://www.wikidata.org/wiki/Q1189666) |
| bj-grand-canal | 北京大运河博物馆 | [Wikidata · 北京大运河博物馆（P625）](https://www.wikidata.org/wiki/Q105718642) |
| bj-art | 中国美术馆 | [Wikidata · 中国美术馆（P625）](https://www.wikidata.org/wiki/Q233705) |
| bj-geology | 中国地质博物馆 | [Wikidata · 中国地质博物馆（P625）](https://www.wikidata.org/wiki/Q585544) |
| bj-agriculture | 中国农业博物馆 | [OpenStreetMap · 全国农业展览馆;中国农业博物馆](https://www.openstreetmap.org/way/129187924) |
| bj-paleozoo | 中国古动物馆 | [Wikidata · 中国古动物馆（P625）](https://www.wikidata.org/wiki/Q846592) |
| bj-science | 中国科学技术馆 | [Wikidata · 中国科学技术馆（P625）](https://www.wikidata.org/wiki/Q1074292) |
| bj-military | 中国人民革命军事博物馆 | [Wikidata · 中国人民革命军事博物馆（P625）](https://www.wikidata.org/wiki/Q1789184) |
| bj-planetarium | 北京天文馆 | [Wikidata · 北京天文馆（P625）](https://www.wikidata.org/wiki/Q4348118) |
| bj-nature | 国家自然博物馆 | [Wikidata · 国家自然博物馆（P625）](https://www.wikidata.org/wiki/Q846583) |
| bj-bells | 大钟寺古钟博物馆 | [OpenStreetMap · 大钟寺古钟博物馆](https://www.openstreetmap.org/way/1303228717) |
| bj-wanshou | 北京艺术博物馆 | [Wikidata · 北京艺术博物馆（P625）](https://www.wikidata.org/wiki/Q2063448) |
| bj-architecture | 北京古代建筑博物馆 | [Wikidata · 北京古代建筑博物馆（P625）](https://www.wikidata.org/wiki/Q341718) |
| bj-stone | 北京石刻艺术博物馆 | [Wikidata · 北京石刻艺术博物馆（P625）](https://www.wikidata.org/wiki/Q1208573) |
| bj-luxun | 北京鲁迅博物馆 | [Wikidata · 北京鲁迅博物馆（P625）](https://www.wikidata.org/wiki/Q4881160) |
| bj-xubeihong | 徐悲鸿纪念馆 | [Wikidata · 徐悲鸿纪念馆（P625）](https://www.wikidata.org/wiki/Q11070647) |
| bj-guomoruo | 郭沫若纪念馆 | [Wikidata · 郭沫若纪念馆（P625）](https://www.wikidata.org/wiki/Q4165193) |
| bj-meilanfang | 梅兰芳纪念馆 | [Wikidata · 梅兰芳纪念馆（P625）](https://www.wikidata.org/wiki/Q4165212) |
| bj-laoshe | 老舍纪念馆 | [Wikidata · 老舍纪念馆（P625）](https://www.wikidata.org/wiki/Q10902396) |
| bj-red-chamber | 北京红楼文化艺术博物馆 | [OpenStreetMap · 北京大观园](https://www.openstreetmap.org/way/24825443) |
| bj-folk | 北京民俗博物馆 | [Wikidata · 北京民俗博物馆（P625）](https://www.wikidata.org/wiki/Q814721) |
| bj-opera | 北京戏曲博物馆 | [Wikidata · 北京戏曲博物馆（P625）](https://www.wikidata.org/wiki/Q24131484) |
| bj-gongwang | 恭王府博物馆 | [Wikidata · 恭王府博物馆（P625）](https://www.wikidata.org/wiki/Q2666344) |
| bj-guozijian | 孔庙和国子监博物馆 | [Wikidata · 孔庙和国子监博物馆（P625）](https://www.wikidata.org/wiki/Q28417597) |
| bj-guanfu | 观复博物馆 | [Wikidata · 观复博物馆（P625）](https://www.wikidata.org/wiki/Q15310035) |
| bj-poly | 保利艺术博物馆 | [Wikidata · 保利艺术博物馆（P625）](https://www.wikidata.org/wiki/Q18651572) |
| bj-zitan | 中国紫檀博物馆 | [Wikidata · 中国紫檀博物馆（P625）](https://www.wikidata.org/wiki/Q126373489) |
| bj-garden | 中国园林博物馆 | [Wikidata · 中国园林博物馆（P625）](https://www.wikidata.org/wiki/Q18651344) |
| bj-film | 中国电影博物馆 | [Wikidata · 中国电影博物馆（P625）](https://www.wikidata.org/wiki/Q5099799) |
| bj-railway | 中国铁道博物馆东郊展馆 | [Wikidata · 中国铁道博物馆东郊展馆（P625）](https://www.wikidata.org/wiki/Q1074280) |
| bj-auto | 北京汽车博物馆 | [Wikidata · 北京汽车博物馆（P625）](https://www.wikidata.org/wiki/Q16928682) |
| bj-beihang | 北京航空航天博物馆 | [Wikidata · 北京航空航天博物馆（P625）](https://www.wikidata.org/wiki/Q10902402) |
| bj-civil-aviation | 民航博物馆 | [Wikidata · 民航博物馆（P625）](https://www.wikidata.org/wiki/Q65171962) |
| bj-printing | 中国印刷博物馆 | [Wikidata · 中国印刷博物馆（P625）](https://www.wikidata.org/wiki/Q9384146) |
| bj-women | 中国妇女儿童博物馆 | [Wikidata · 中国妇女儿童博物馆（P625）](https://www.wikidata.org/wiki/Q4306266) |
| bj-overseas | 中国华侨历史博物馆 | [Wikidata · 中国华侨历史博物馆（P625）](https://www.wikidata.org/wiki/Q28418208) |
| bj-customs | 中国海关博物馆 | [Wikidata · 中国海关博物馆（P625）](https://www.wikidata.org/wiki/Q19851717) |
| bj-coins | 中国钱币博物馆 | [Wikidata · 中国钱币博物馆（P625）](https://www.wikidata.org/wiki/Q10874154) |
| bj-ethnic | 民族文化宫博物馆 | [Wikidata · 民族文化宫博物馆（P625）](https://www.wikidata.org/wiki/Q1791802) |
| bj-literature | 中国现代文学馆 | [Wikidata · 中国现代文学馆（P625）](https://www.wikidata.org/wiki/Q10873917) |
| bj-tsinghua | 清华大学艺术博物馆 | [Wikidata · 清华大学艺术博物馆（P625）](https://www.wikidata.org/wiki/Q28412420) |
| bj-archaeology | 中国考古博物馆 | [OpenStreetMap · 中国考古博物馆](https://www.openstreetmap.org/way/610079824) |
| bj-zhoukoudian | 周口店北京人遗址博物馆 | [OpenStreetMap · 周口店北京人遗址博物馆](https://www.openstreetmap.org/way/1090515798) |
| bj-yunju | 北京房山云居寺石经博物馆 | [Wikidata · 北京房山云居寺石经博物馆（P625）](https://www.wikidata.org/wiki/Q1528443) |
| bj-dabaotai | 北京大葆台遗址博物馆 | [OpenStreetMap · 大葆台遗址博物馆](https://www.openstreetmap.org/way/1012672989) |
| bj-yongding | 永定河文化博物馆 | 待核实 |
| bj-haidian | 海淀区博物馆 | 待核实 |
