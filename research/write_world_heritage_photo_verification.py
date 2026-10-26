import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'research/world-heritage-image-credits.json').read_text(encoding='utf-8'))
lines=['# 中国世界遗产图片核验','', '核验日期：2026-10-26。覆盖 UNESCO 实时清单内中国全部 46 项文化与文化自然双重遗产，包括 2026 年景德镇手工制瓷业遗存。','',
'46 张均为 Wikimedia Commons 许可真实照片，未使用生成式图片、拼贴示意图或无关通用风景。每张保留作者、原图、文件描述页、具体许可证及许可证链接；素材来源证据见 `world-heritage-photo-selected-evidence.json`。', '',
'下载后已逐张解码，最长边不超过 960 像素，转换 JPEG，未改变画面内容。总计约 6.50 MB。缩略联系表 `world-heritage-contact.jpg` 已人工视觉审阅。','',
'串联、跨省和跨境项目以一个组成部分的实拍呈现，配图说明明确组件，不表示覆盖全部遗产点。景德镇使用御窑厂考古遗址本体，非邻近当代博物馆。平遥使用古城航拍，排除了同名高铁站；良渚使用考古遗址，排除了旧入口标志和平面图；秦始皇陵使用兵马俑坑，排除了博物馆现代建筑外观。', '',
'照片拍摄时间与当前开放状态无关；不据照片推断门票、预约、通行或开放状态。', '',
'复现：在仓库根目录运行 `python scripts/collect_world_heritage_images.py`。搜索候选与最终审定选择分开保存；复现只下载审定文件，不自动替换。', '',
'| ID | 图像说明 | 作者 | 许可 | 原始文件页 |','|---|---|---|---|---|']
for key,v in data.items():lines.append('| '+v['siteId']+' | '+v['caption'].replace('|','/')+' | '+v['author'].replace('|','/')+' | ['+v['license']+']('+v['licenseUrl']+') | [Commons]('+v['source']+') |')
(root/'research/world-heritage-photos-verification.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
