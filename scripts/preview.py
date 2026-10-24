"""Static local preview with byte ranges, matching audio behavior on Sites hosting."""
import argparse,re,http.server,os
from functools import partial
from pathlib import Path
class Handler(http.server.SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes')
  super().end_headers()
 def send_head(self):
  self.remaining=None
  target=self.translate_path(self.path)
  header=self.headers.get('Range')
  if not header or not os.path.isfile(target):return super().send_head()
  size=os.path.getsize(target);match=re.fullmatch(r'bytes=(\d+)-(\d*)',header)
  if not match:
   self.send_error(416,'Unsupported byte range');return None
  start=int(match[1]);end=min(int(match[2] or size-1),size-1)
  if start>=size or start>end:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
  file=open(target,'rb');file.seek(start);self.remaining=end-start+1
  self.send_response(206);self.send_header('Content-Type',self.guess_type(target));self.send_header('Content-Length',str(self.remaining));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.end_headers();return file
 def copyfile(self,source,outputfile):
  if self.remaining is None:return super().copyfile(source,outputfile)
  while self.remaining>0:
   chunk=source.read(min(self.remaining,65536))
   if not chunk:break
   outputfile.write(chunk);self.remaining-=len(chunk)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=4173);args=p.parse_args()
 directory=Path(__file__).resolve().parents[1]/'dist'
 server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(directory)))
 print(f'Local: http://localhost:{args.port}',flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
