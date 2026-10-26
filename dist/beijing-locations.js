(function(root){
"use strict";
const data={
  "bj-capital": {
    "coordinateSystem": "WGS84",
    "label": "首都博物馆",
    "checked": "2026-10-25",
    "lat": 39.905,
    "lng": 116.336,
    "sourcePrecisionDegrees": 2.777777777777778e-05,
    "source": {
      "title": "Wikidata · 首都博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1189666"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-grand-canal": {
    "coordinateSystem": "WGS84",
    "label": "北京大运河博物馆",
    "checked": "2026-10-25",
    "lat": 39.8795,
    "lng": 116.7108,
    "sourcePrecisionDegrees": 0.0001,
    "source": {
      "title": "Wikidata · 北京大运河博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q105718642"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-art": {
    "coordinateSystem": "WGS84",
    "label": "中国美术馆",
    "checked": "2026-10-25",
    "lat": 39.92382,
    "lng": 116.40275,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 中国美术馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q233705"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-geology": {
    "coordinateSystem": "WGS84",
    "label": "中国地质博物馆",
    "checked": "2026-10-25",
    "lat": 39.92194444,
    "lng": 116.36527778,
    "sourcePrecisionDegrees": 0.00027777777777778,
    "source": {
      "title": "Wikidata · 中国地质博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q585544"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-agriculture": {
    "coordinateSystem": "WGS84",
    "label": "中国农业博物馆",
    "checked": "2026-10-25",
    "lat": 39.9391895,
    "lng": 116.4589809,
    "source": {
      "title": "OpenStreetMap · 全国农业展览馆;中国农业博物馆",
      "url": "https://www.openstreetmap.org/way/129187924"
    },
    "accuracyNote": "全国农业展览馆与中国农业博物馆同址园区参考点；Wikidata 两个冲突候选已弃用。OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-paleozoo": {
    "coordinateSystem": "WGS84",
    "label": "中国古动物馆",
    "checked": "2026-10-25",
    "lat": 39.93625,
    "lng": 116.32777778,
    "sourcePrecisionDegrees": 2.777777777778e-05,
    "source": {
      "title": "Wikidata · 中国古动物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q846592"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-science": {
    "coordinateSystem": "WGS84",
    "label": "中国科学技术馆",
    "checked": "2026-10-25",
    "lat": 40.005,
    "lng": 116.39244,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 中国科学技术馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1074292"
    },
    "accuracyNote": "已排除北三环北京科学中心旧馆点，选择奥林匹克公园现馆。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-military": {
    "coordinateSystem": "WGS84",
    "label": "中国人民革命军事博物馆",
    "checked": "2026-10-25",
    "lat": 39.90766944,
    "lng": 116.31772222,
    "sourcePrecisionDegrees": 2.77777777778e-06,
    "source": {
      "title": "Wikidata · 中国人民革命军事博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1789184"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-planetarium": {
    "coordinateSystem": "WGS84",
    "label": "北京天文馆",
    "checked": "2026-10-25",
    "lat": 39.9362,
    "lng": 116.3304,
    "sourcePrecisionDegrees": 0.0001,
    "source": {
      "title": "Wikidata · 北京天文馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4348118"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-nature": {
    "coordinateSystem": "WGS84",
    "label": "国家自然博物馆",
    "checked": "2026-10-25",
    "lat": 39.88165,
    "lng": 116.39365,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 国家自然博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q846583"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-bells": {
    "coordinateSystem": "WGS84",
    "label": "大钟寺古钟博物馆",
    "checked": "2026-10-25",
    "lat": 39.9680185,
    "lng": 116.3317352,
    "source": {
      "title": "OpenStreetMap · 大钟寺古钟博物馆",
      "url": "https://www.openstreetmap.org/way/1303228717"
    },
    "accuracyNote": "OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-wanshou": {
    "coordinateSystem": "WGS84",
    "label": "北京艺术博物馆",
    "checked": "2026-10-25",
    "lat": 39.945282,
    "lng": 116.305226,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 北京艺术博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q2063448"
    },
    "accuracyNote": "万寿寺内的北京艺术博物馆馆区；不是未来建设中的同名新美术馆。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-architecture": {
    "coordinateSystem": "WGS84",
    "label": "北京古代建筑博物馆",
    "checked": "2026-10-25",
    "lat": 39.87684703676186,
    "lng": 116.38622786863257,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 北京古代建筑博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q341718"
    },
    "accuracyNote": "先农坛馆区参考点；不代表太岁殿入口。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-stone": {
    "coordinateSystem": "WGS84",
    "label": "北京石刻艺术博物馆",
    "checked": "2026-10-25",
    "lat": 39.944166666667,
    "lng": 116.32416666667,
    "sourcePrecisionDegrees": 0.00027777777777778,
    "source": {
      "title": "Wikidata · 北京石刻艺术博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1208573"
    },
    "accuracyNote": "真觉寺馆区参考点；不代表金刚宝座塔或游客入口。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-luxun": {
    "coordinateSystem": "WGS84",
    "label": "北京鲁迅博物馆",
    "checked": "2026-10-25",
    "lat": 39.92445,
    "lng": 116.35234,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 北京鲁迅博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4881160"
    },
    "accuracyNote": "阜成门宫门口鲁迅馆区参考点；非新街口八道湾旧居。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-xubeihong": {
    "coordinateSystem": "WGS84",
    "label": "徐悲鸿纪念馆",
    "checked": "2026-10-25",
    "lat": 39.944929,
    "lng": 116.371478,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 徐悲鸿纪念馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q11070647"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-guomoruo": {
    "coordinateSystem": "WGS84",
    "label": "郭沫若纪念馆",
    "checked": "2026-10-25",
    "lat": 39.933212,
    "lng": 116.3832,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 郭沫若纪念馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4165193"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-meilanfang": {
    "coordinateSystem": "WGS84",
    "label": "梅兰芳纪念馆",
    "checked": "2026-10-25",
    "lat": 39.93416944444444,
    "lng": 116.37317777777778,
    "sourcePrecisionDegrees": 2.777777777777778e-06,
    "source": {
      "title": "Wikidata · 梅兰芳纪念馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4165212"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-laoshe": {
    "coordinateSystem": "WGS84",
    "label": "老舍纪念馆",
    "checked": "2026-10-25",
    "lat": 39.918643,
    "lng": 116.408362,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 老舍纪念馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10902396"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-red-chamber": {
    "coordinateSystem": "WGS84",
    "label": "北京红楼文化艺术博物馆",
    "checked": "2026-10-25",
    "lat": 39.8703006,
    "lng": 116.3500796,
    "source": {
      "title": "OpenStreetMap · 北京大观园",
      "url": "https://www.openstreetmap.org/way/24825443"
    },
    "accuracyNote": "博物馆所在北京大观园园区的参考点，非单独展厅位置。OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-folk": {
    "coordinateSystem": "WGS84",
    "label": "北京民俗博物馆",
    "checked": "2026-10-25",
    "lat": 39.923611111111,
    "lng": 116.43777777778,
    "sourcePrecisionDegrees": 0.00027777777777778,
    "source": {
      "title": "Wikidata · 北京民俗博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q814721"
    },
    "accuracyNote": "东岳庙馆区参考点。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-opera": {
    "coordinateSystem": "WGS84",
    "label": "北京戏曲博物馆",
    "checked": "2026-10-25",
    "lat": 39.888833,
    "lng": 116.384083,
    "sourcePrecisionDegrees": 0.011707634675972,
    "source": {
      "title": "Wikidata · 北京戏曲博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q24131484"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-gongwang": {
    "coordinateSystem": "WGS84",
    "label": "恭王府博物馆",
    "checked": "2026-10-25",
    "lat": 39.936636,
    "lng": 116.379862,
    "sourcePrecisionDegrees": 2.77778e-05,
    "source": {
      "title": "Wikidata · 恭王府博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q2666344"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-guozijian": {
    "coordinateSystem": "WGS84",
    "label": "孔庙和国子监博物馆",
    "checked": "2026-10-25",
    "lat": 39.94522,
    "lng": 116.40762,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 孔庙和国子监博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q28417597"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-guanfu": {
    "coordinateSystem": "WGS84",
    "label": "观复博物馆",
    "checked": "2026-10-25",
    "lat": 40.00594,
    "lng": 116.52816,
    "sourcePrecisionDegrees": 0.011728013016104,
    "source": {
      "title": "Wikidata · 观复博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q15310035"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-poly": {
    "coordinateSystem": "WGS84",
    "label": "保利艺术博物馆",
    "checked": "2026-10-25",
    "lat": 39.9332369,
    "lng": 116.429438,
    "sourcePrecisionDegrees": 2.77778e-07,
    "source": {
      "title": "Wikidata · 保利艺术博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q18651572"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-zitan": {
    "coordinateSystem": "WGS84",
    "label": "中国紫檀博物馆",
    "checked": "2026-10-25",
    "lat": 39.908812,
    "lng": 116.520312,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 中国紫檀博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q126373489"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-garden": {
    "coordinateSystem": "WGS84",
    "label": "中国园林博物馆",
    "checked": "2026-10-25",
    "lat": 39.879603,
    "lng": 116.1764225,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 中国园林博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q18651344"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-film": {
    "coordinateSystem": "WGS84",
    "label": "中国电影博物馆",
    "checked": "2026-10-25",
    "lat": 39.9951,
    "lng": 116.51493055555555,
    "sourcePrecisionDegrees": 2.777777777777778e-06,
    "source": {
      "title": "Wikidata · 中国电影博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q5099799"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-railway": {
    "coordinateSystem": "WGS84",
    "label": "中国铁道博物馆东郊展馆",
    "checked": "2026-10-25",
    "lat": 39.9963,
    "lng": 116.5103,
    "sourcePrecisionDegrees": 2.77777777778e-06,
    "source": {
      "title": "Wikidata · 中国铁道博物馆东郊展馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1074280"
    },
    "accuracyNote": "酒仙桥北路东郊展馆参考点；非正阳门展馆。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-auto": {
    "coordinateSystem": "WGS84",
    "label": "北京汽车博物馆",
    "checked": "2026-10-25",
    "lat": 39.82752,
    "lng": 116.29617,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 北京汽车博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q16928682"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-beihang": {
    "coordinateSystem": "WGS84",
    "label": "北京航空航天博物馆",
    "checked": "2026-10-25",
    "lat": 39.98082,
    "lng": 116.3445,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 北京航空航天博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10902402"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-civil-aviation": {
    "coordinateSystem": "WGS84",
    "label": "民航博物馆",
    "checked": "2026-10-25",
    "lat": 40.01677,
    "lng": 116.53225,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 民航博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q65171962"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-printing": {
    "coordinateSystem": "WGS84",
    "label": "中国印刷博物馆",
    "checked": "2026-10-25",
    "lat": 39.7419,
    "lng": 116.325,
    "sourcePrecisionDegrees": 0.011682632842124,
    "source": {
      "title": "Wikidata · 中国印刷博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q9384146"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-women": {
    "coordinateSystem": "WGS84",
    "label": "中国妇女儿童博物馆",
    "checked": "2026-10-25",
    "lat": 39.90909,
    "lng": 116.41729,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 中国妇女儿童博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4306266"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-overseas": {
    "coordinateSystem": "WGS84",
    "label": "中国华侨历史博物馆",
    "checked": "2026-10-25",
    "lat": 39.941542,
    "lng": 116.418885,
    "sourcePrecisionDegrees": 1e-07,
    "source": {
      "title": "Wikidata · 中国华侨历史博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q28418208"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-customs": {
    "coordinateSystem": "WGS84",
    "label": "中国海关博物馆",
    "checked": "2026-10-25",
    "lat": 39.905687,
    "lng": 116.426505,
    "sourcePrecisionDegrees": 1e-07,
    "source": {
      "title": "Wikidata · 中国海关博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q19851717"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-coins": {
    "coordinateSystem": "WGS84",
    "label": "中国钱币博物馆",
    "checked": "2026-10-25",
    "lat": 39.90075,
    "lng": 116.38875,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 中国钱币博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10874154"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-ethnic": {
    "coordinateSystem": "WGS84",
    "label": "民族文化宫博物馆",
    "checked": "2026-10-25",
    "lat": 39.90683,
    "lng": 116.36266,
    "sourcePrecisionDegrees": 1e-05,
    "source": {
      "title": "Wikidata · 民族文化宫博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1791802"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-literature": {
    "coordinateSystem": "WGS84",
    "label": "中国现代文学馆",
    "checked": "2026-10-25",
    "lat": 39.98291,
    "lng": 116.42378,
    "sourcePrecisionDegrees": 1e-06,
    "source": {
      "title": "Wikidata · 中国现代文学馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10873917"
    },
    "accuracyNote": "Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-tsinghua": {
    "coordinateSystem": "WGS84",
    "label": "清华大学艺术博物馆",
    "checked": "2026-10-25",
    "lat": 39.999822,
    "lng": 116.335609,
    "sourcePrecisionDegrees": 0.011726642630902,
    "source": {
      "title": "Wikidata · 清华大学艺术博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q28412420"
    },
    "accuracyNote": "Wikidata 原始精度约 0.0117°，仅作馆区示意；不代表校门或游客入口。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-archaeology": {
    "coordinateSystem": "WGS84",
    "label": "中国考古博物馆",
    "checked": "2026-10-25",
    "lat": 39.9976929,
    "lng": 116.3925689,
    "source": {
      "title": "OpenStreetMap · 中国考古博物馆",
      "url": "https://www.openstreetmap.org/way/610079824"
    },
    "accuracyNote": "OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-zhoukoudian": {
    "coordinateSystem": "WGS84",
    "label": "周口店北京人遗址博物馆",
    "checked": "2026-10-25",
    "lat": 39.6863399,
    "lng": 115.9309486,
    "source": {
      "title": "OpenStreetMap · 周口店北京人遗址博物馆",
      "url": "https://www.openstreetmap.org/way/1090515798"
    },
    "accuracyNote": "独立博物馆馆舍参考点，非猿人洞或世界遗产遗址总点。OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-yunju": {
    "coordinateSystem": "WGS84",
    "label": "北京房山云居寺石经博物馆",
    "checked": "2026-10-25",
    "lat": 39.60805556,
    "lng": 115.76777778,
    "sourcePrecisionDegrees": 0.00027777777777778,
    "source": {
      "title": "Wikidata · 北京房山云居寺石经博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1528443"
    },
    "accuracyNote": "云居寺馆区参考点；石经陈列及具体入口须另查馆方导览。Wikidata P625 场馆区域参考点，源记录精度有限，不代表游客入口、检票口或实时导航终点。"
  },
  "bj-dabaotai": {
    "coordinateSystem": "WGS84",
    "label": "北京大葆台遗址博物馆",
    "checked": "2026-10-25",
    "lat": 39.8044893,
    "lng": 116.2913995,
    "source": {
      "title": "OpenStreetMap · 大葆台遗址博物馆",
      "url": "https://www.openstreetmap.org/way/1012672989"
    },
    "accuracyNote": "大葆台遗址博物馆馆区参考点；不是旧版粗精度汉墓坐标。OpenStreetMap 对应馆舍/馆区 POI 的 Nominatim 代表点，不代表入口或实时导航终点。"
  },
  "bj-yongding": {
    "coordinateSystem": "WGS84",
    "label": "永定河文化博物馆",
    "checked": "2026-10-25",
    "unavailable": true,
    "accuracyNote": "尚未取得可核验的场馆 WGS84 点位，先按中文馆址查询；不使用河流或门头沟区中心点代替。"
  },
  "bj-haidian": {
    "coordinateSystem": "WGS84",
    "label": "海淀区博物馆",
    "checked": "2026-10-25",
    "unavailable": true,
    "accuracyNote": "三山五园文化艺术中心新馆尚无可靠公开 WGS84 点位；已拒绝旧海淀馆坐标，先按最新中文馆址查询。"
  }
};
if(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_BEIJING_LOCATIONS=data;
})(typeof window!=="undefined"?window:globalThis);
