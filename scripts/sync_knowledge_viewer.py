"""Share exactly the same procedural geometry and shaders with native canvas."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
web=(root/'dist/object-viewer.js').read_text(encoding='utf-8')
mesh=web[web.index(' function mesh(o)'):web.index(' function mount(route)')]
shaders={kind:re.search(r"shader\(gl\."+kind+r",'([^']+)'\)",web).group(1) for kind in ['VERTEX_SHADER','FRAGMENT_SHADER']}
(root/'miniprogram/knowledge/geometry.js').write_text('// Generated from dist/object-viewer.js; teaching geometry, not a collection scan.\n'+mesh+'\nmodule.exports={mesh,shaders:'+json.dumps(shaders)+'};\n',encoding='utf-8')
print('Shared native study geometry and shaders regenerated.')
