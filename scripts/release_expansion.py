import json,re,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
# This is the actual source project, not a compiled native package.
out=root/'output';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'观物-微信小程序.zip','w',zipfile.ZIP_DEFLATED) as archive:
 for file in (root/'miniprogram').rglob('*'):
  if not file.is_file():continue
  relative=file.relative_to(root/'miniprogram')
  if relative.parts[0]=='assets' or relative.as_posix().startswith('media/suzhou-brick/'):continue
  archive.write(file,relative.as_posix())
print('Native source archive ready.')
