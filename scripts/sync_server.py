"""Keep the original static atlas as the source; build its server separately."""
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
script="const a=require('./dist/heritage-data.js'),b=require('./dist/expansion-data.js'),c=require('./dist/city-museums.js'),d=require('./dist/beijing-museums.js'),q=require('./dist/inquiries-data.js');process.stdout.write(JSON.stringify({museums:[...a.museums,...b.museums,...c.museums,...d.museums],crafts:a.crafts,artifacts:b.artifacts,inquiries:q}))"
catalog=json.loads(subprocess.check_output(['node','-e',script],cwd=root,encoding='utf-8'))
(root/'server-app/lib/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
manifest=json.loads((root/'.openai/hosting.json').read_text(encoding='utf-8'));manifest.pop('static',None)
(root/'server-app/.openai/hosting.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(f"Server catalog: {len(catalog['museums'])} museums, {len(catalog['artifacts'])} artifacts")
