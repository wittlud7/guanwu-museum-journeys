(function(root){
"use strict";
const data={
  "beijing": {
    "coordinateSystem": "WGS84",
    "label": "中国工艺美术馆 · 中国非遗馆",
    "address": "北京市朝阳区湖景东路16号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 40.00238,
    "lng": 116.39124,
    "source": {
      "title": "Wikidata · 中国工艺美术馆 · 中国非遗馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10873736"
    }
  },
  "hangzhou": {
    "coordinateSystem": "WGS84",
    "label": "浙江省非物质文化遗产馆",
    "address": "杭州市西湖区江涵路300号之江文化中心",
    "accuracyNote": "OpenStreetMap对应博物馆建筑/馆区POI的参考点（Nominatim提供代表点），不是入口或导航终点。已区分同名公交站与博物馆实体。",
    "lat": 30.1621241,
    "lng": 120.0993934,
    "source": {
      "title": "OpenStreetMap · 浙江省非物质文化遗产馆馆舍POI",
      "url": "https://www.openstreetmap.org/relation/19222156"
    }
  },
  "nanjing": {
    "coordinateSystem": "WGS84",
    "label": "南京云锦博物馆",
    "address": "南京市建邺区茶亭东街240号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 32.0385,
    "lng": 118.73961,
    "source": {
      "title": "Wikidata · 南京云锦博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10906649"
    }
  },
  "chengdu": {
    "coordinateSystem": "WGS84",
    "label": "成都蜀锦织绣博物馆",
    "address": "成都市青羊区草堂东路18号",
    "accuracyNote": "地址存在未解决冲突：当前目录与志愿服务来源写草堂东路18号；唯一同名OSM馆点标为草堂东路2号，可能为旧址。未证实馆区一致，暂不提供经纬度；请按中文地址向馆方核实。",
    "unavailable": true,
    "source": {
      "title": "成都青年志愿服务 · 场馆活动地点",
      "url": "https://cdyouth.cdcyl.org.cn/volunteer/site/project/204094"
    }
  },
  "guangzhou": {
    "coordinateSystem": "WGS84",
    "label": "粤剧艺术博物馆",
    "address": "广州市荔湾区恩宁路127号",
    "accuracyNote": "按OpenStreetMap对应馆舍轮廓的经纬范围中心生成的区域参考点；不是实测游客入口、检票口或实时导航终点。",
    "lat": 23.1181587,
    "lng": 113.23276665,
    "source": {
      "title": "OpenStreetMap · 粤剧艺术博物馆馆舍范围",
      "url": "https://www.openstreetmap.org/way/965382977"
    }
  },
  "xian": {
    "coordinateSystem": "WGS84",
    "label": "陕西历史博物馆",
    "address": "西安市雁塔区小寨东路91号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 34.22504804,
    "lng": 108.95063301,
    "source": {
      "title": "Wikidata · 陕西历史博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1151210"
    }
  },
  "shanghai": {
    "coordinateSystem": "WGS84",
    "label": "上海博物馆 · 人民广场馆",
    "address": "上海市黄浦区人民大道201号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。固定为人民广场馆，非浦东东馆。",
    "lat": 31.230278,
    "lng": 121.470556,
    "source": {
      "title": "Wikidata · 上海博物馆 · 人民广场馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1051293"
    }
  },
  "suzhou": {
    "coordinateSystem": "WGS84",
    "label": "苏州博物馆",
    "address": "苏州市姑苏区东北街204号（本馆）",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 31.32514,
    "lng": 120.62354,
    "source": {
      "title": "Wikidata · 苏州博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q998042"
    }
  },
  "wuhan": {
    "coordinateSystem": "WGS84",
    "label": "湖北省博物馆",
    "address": "武汉市武昌区东湖路160号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 30.56388889,
    "lng": 114.35888889,
    "source": {
      "title": "Wikidata · 湖北省博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4391403"
    }
  },
  "zhengzhou": {
    "coordinateSystem": "WGS84",
    "label": "河南博物院",
    "address": "郑州市金水区农业路8号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 34.788889,
    "lng": 113.666111,
    "source": {
      "title": "Wikidata · 河南博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q857752"
    }
  },
  "changsha": {
    "coordinateSystem": "WGS84",
    "label": "湖南博物院",
    "address": "长沙市开福区东风路50号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 28.21526,
    "lng": 112.98784,
    "source": {
      "title": "Wikidata · 湖南博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q5942029"
    }
  },
  "palace": {
    "coordinateSystem": "WGS84",
    "label": "故宫博物院",
    "address": "北京市东城区景山前街4号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。故宫点位在宫城区域内，不能用于判断入院方向。",
    "lat": 39.91555556,
    "lng": 116.39083333,
    "source": {
      "title": "Wikidata · 故宫博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q2047427"
    }
  },
  "national-china": {
    "coordinateSystem": "WGS84",
    "label": "中国国家博物馆",
    "address": "北京市东城区东长安街16号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 39.90361111,
    "lng": 116.395,
    "source": {
      "title": "Wikidata · 中国国家博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q1074318"
    }
  },
  "zhejiang-history": {
    "coordinateSystem": "WGS84",
    "label": "浙江省博物馆 · 孤山馆区",
    "address": "杭州市西湖区孤山路25号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。固定为孤山馆区，非之江馆区。",
    "lat": 30.25347222,
    "lng": 120.13861111,
    "source": {
      "title": "Wikidata · 浙江省博物馆 · 孤山馆区（P625）",
      "url": "https://www.wikidata.org/wiki/Q1278762"
    }
  },
  "national-silk": {
    "coordinateSystem": "WGS84",
    "label": "中国丝绸博物馆",
    "address": "杭州市玉皇山路73-1号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 30.225,
    "lng": 120.14722222,
    "source": {
      "title": "Wikidata · 中国丝绸博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q569019"
    }
  },
  "nanjing-museum": {
    "coordinateSystem": "WGS84",
    "label": "南京博物院",
    "address": "南京市玄武区中山东路321号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 32.0425,
    "lng": 118.81944444,
    "source": {
      "title": "Wikidata · 南京博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q1815891"
    }
  },
  "six-dynasties": {
    "coordinateSystem": "WGS84",
    "label": "六朝博物馆",
    "address": "南京市玄武区长江路302号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 32.0448,
    "lng": 118.79428,
    "source": {
      "title": "Wikidata · 六朝博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q67931941"
    }
  },
  "chengdu-museum": {
    "coordinateSystem": "WGS84",
    "label": "成都博物馆",
    "address": "成都市青羊区小河街1号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 30.65973,
    "lng": 104.0612,
    "source": {
      "title": "Wikidata · 成都博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q55696247"
    }
  },
  "sichuan-museum": {
    "coordinateSystem": "WGS84",
    "label": "四川博物院",
    "address": "成都市青羊区浣花南路251号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 30.663075,
    "lng": 104.03154167,
    "source": {
      "title": "Wikidata · 四川博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q10924774"
    }
  },
  "guangdong-museum": {
    "coordinateSystem": "WGS84",
    "label": "广东省博物馆",
    "address": "广州市天河区珠江新城珠江东路2号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 23.11722222,
    "lng": 113.32138889,
    "source": {
      "title": "Wikidata · 广东省博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q5613636"
    }
  },
  "nanyue": {
    "coordinateSystem": "WGS84",
    "label": "南越王博物院 · 王墓展区",
    "address": "广州市解放北路867号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。固定为解放北路王墓展区，非中山四路王宫展区。",
    "lat": 23.14027778,
    "lng": 113.25555556,
    "source": {
      "title": "Wikidata · 南越王博物院 · 王墓展区（P625）",
      "url": "https://www.wikidata.org/wiki/Q1507198"
    }
  },
  "xian-museum": {
    "coordinateSystem": "WGS84",
    "label": "西安博物院",
    "address": "西安市碑林区友谊西路72号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 34.239,
    "lng": 108.936,
    "source": {
      "title": "Wikidata · 西安博物院（P625）",
      "url": "https://www.wikidata.org/wiki/Q15928831"
    }
  },
  "beilin": {
    "coordinateSystem": "WGS84",
    "label": "西安碑林博物馆",
    "address": "西安市碑林区三学街15号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 34.255,
    "lng": 108.94833333,
    "source": {
      "title": "Wikidata · 西安碑林博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q10519071"
    }
  },
  "shanghai-history": {
    "coordinateSystem": "WGS84",
    "label": "上海市历史博物馆",
    "address": "上海市黄浦区南京西路325号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 31.23267,
    "lng": 121.46663,
    "source": {
      "title": "Wikidata · 上海市历史博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q779273"
    }
  },
  "shanghai-nature": {
    "coordinateSystem": "WGS84",
    "label": "上海自然博物馆",
    "address": "上海市静安区北京西路510号",
    "accuracyNote": "按OpenStreetMap对应馆舍轮廓的经纬范围中心生成的区域参考点；不是实测游客入口、检票口或实时导航终点。",
    "lat": 31.23688225,
    "lng": 121.4580124,
    "source": {
      "title": "OpenStreetMap · 上海自然博物馆馆舍范围",
      "url": "https://www.openstreetmap.org/way/425762388"
    }
  },
  "suzhou-silk": {
    "coordinateSystem": "WGS84",
    "label": "苏州丝绸博物馆",
    "address": "苏州市姑苏区人民路2001号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 31.32541667,
    "lng": 120.61416667,
    "source": {
      "title": "Wikidata · 苏州丝绸博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q4806827"
    }
  },
  "suzhou-garden": {
    "coordinateSystem": "WGS84",
    "label": "苏州园林博物馆",
    "address": "苏州市姑苏区东北街202号",
    "accuracyNote": "按OpenStreetMap对应馆舍轮廓的经纬范围中心生成的区域参考点；不是实测游客入口、检票口或实时导航终点。",
    "lat": 31.32544145,
    "lng": 120.62577435,
    "source": {
      "title": "OpenStreetMap · 苏州园林博物馆馆舍范围",
      "url": "https://www.openstreetmap.org/way/542534200"
    }
  },
  "wuhan-museum": {
    "coordinateSystem": "WGS84",
    "label": "武汉博物馆",
    "address": "武汉市江汉区青年路373号",
    "accuracyNote": "按OpenStreetMap对应馆舍轮廓的经纬范围中心生成的区域参考点；不是实测游客入口、检票口或实时导航终点。",
    "lat": 30.6138079,
    "lng": 114.25097695,
    "source": {
      "title": "OpenStreetMap · 武汉博物馆馆舍范围",
      "url": "https://www.openstreetmap.org/way/369445342"
    }
  },
  "xinhai": {
    "coordinateSystem": "WGS84",
    "label": "辛亥革命博物院 · 南院",
    "address": "武汉市武昌区彭刘杨路258号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。固定为彭刘杨路南院，非武珞路北院。",
    "lat": 30.53972222,
    "lng": 114.30027778,
    "source": {
      "title": "Wikidata · 辛亥革命博物院 · 南院（P625）",
      "url": "https://www.wikidata.org/wiki/Q30946741"
    }
  },
  "zhengzhou-museum": {
    "coordinateSystem": "WGS84",
    "label": "郑州博物馆 · 文翰街馆",
    "address": "郑州市中原区文翰街9号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。固定为文翰街馆，非嵩山路馆。",
    "lat": 34.74075556,
    "lng": 113.54068333,
    "source": {
      "title": "Wikidata · 郑州博物馆 · 文翰街馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q15935528"
    }
  },
  "shangdu": {
    "coordinateSystem": "WGS84",
    "label": "郑州商都遗址博物院",
    "address": "郑州市管城回族区东大街366号",
    "accuracyNote": "OpenStreetMap对应博物馆馆区POI的参考点（Nominatim提供代表点），不是入口、检票口或实时导航终点。",
    "lat": 34.7475745,
    "lng": 113.6806525,
    "source": {
      "title": "OpenStreetMap · 郑州商都遗址博物院馆舍POI",
      "url": "https://www.openstreetmap.org/way/1341987750"
    }
  },
  "changsha-museum": {
    "coordinateSystem": "WGS84",
    "label": "长沙博物馆",
    "address": "长沙市开福区新河三角洲滨江文化园内",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 28.248679,
    "lng": 112.986445,
    "source": {
      "title": "Wikidata · 长沙博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q28837838"
    }
  },
  "changsha-slips": {
    "coordinateSystem": "WGS84",
    "label": "长沙简牍博物馆",
    "address": "长沙市天心区白沙路92号",
    "accuracyNote": "Wikidata P625的场馆区域参考点；精度与实际位置以源记录为限，不代表游客入口、检票口或实时导航终点。",
    "lat": 28.1883,
    "lng": 112.9776,
    "source": {
      "title": "Wikidata · 长沙简牍博物馆（P625）",
      "url": "https://www.wikidata.org/wiki/Q28824296"
    }
  }
};
if(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_LOCATIONS=data;
})(typeof window!=="undefined"?window:globalThis);
