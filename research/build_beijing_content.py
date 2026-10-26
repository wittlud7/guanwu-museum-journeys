"""Rebuild the browser catalogue from the reviewed source JSON without network access."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/'research/beijing-museums-content.json').read_text(encoding='utf8'))
assert len(data['museums'])==47
(root/'dist/beijing-museums.js').write_text('(function(root){\n"use strict";\nconst data='+json.dumps(data,ensure_ascii=False,indent=2)+';\nif(typeof module!=="undefined"&&module.exports)module.exports=data;else root.GUANWU_BEIJING_MUSEUMS=data;\n})(typeof globalThis!=="undefined"?globalThis:this);\n',encoding='utf8')
print('Built 47 museums from reviewed content JSON')
