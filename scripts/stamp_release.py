from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
version='2026102901'
p=root/'dist/index.html';s=p.read_text(encoding='utf-8')
for name in ['object-viewer.js','knowledge-data.js','knowledge-core.js','knowledge.js','knowledge.css','world-heritage-data.js','world-heritage.js','world-heritage.css','voice-packs-data.js','voices.js','beijing-museums.js','beijing-locations.js','vendor/leaflet/leaflet.js','vendor/leaflet/leaflet.css','style.css','heritage.css','heritage-data.js','player.js','heritage-app.js','expansion-data.js','companion.js','companion.css','city-museums.js','inquiries-data.js','experience.js','experience.css','museum-locations.js','route-planner.js','community.js','social-planner.css']:
 s=re.sub(r'(["\'])'+re.escape(name)+r'(?:\?v=\d+)?(["\'])',lambda m:m[1]+name+'?v='+version+m[2],s)
p.write_text(s,encoding='utf-8')
