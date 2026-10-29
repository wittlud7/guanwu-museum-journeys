// Generated from dist/object-viewer.js; teaching geometry, not a collection scan.
 function mesh(o){const verts=[],norms=[];function triangle(a,b,c,na,nb,nc){verts.push(...a,...b,...c);norms.push(...na,...nb,...nc)}
  function lathe(profile,n=80,xOffset=0,yOffset=0){for(let j=0;j<profile.length-1;j++){const [r0,y0]=profile[j],[r1,y1]=profile[j+1],dr=r1-r0,dy=y1-y0,len=Math.hypot(dr,dy)||1;for(let i=0;i<n;i++){const a=i/n*Math.PI*2,b=(i+1)/n*Math.PI*2;const p=(r,y,t)=>[xOffset+r*Math.cos(t),yOffset+y,r*Math.sin(t)],nm=t=>[dy/len*Math.cos(t),-dr/len,dy/len*Math.sin(t)];triangle(p(r0,y0,a),p(r1,y1,a),p(r1,y1,b),nm(a),nm(a),nm(b));triangle(p(r0,y0,a),p(r1,y1,b),p(r0,y0,b),nm(a),nm(b),nm(b))}}}
  function tube(path,radius,segments=20){for(let j=0;j<path.length-1;j++){const a=path[j],b=path[j+1],dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy)||1;const norm=t=>[-dy/len*Math.cos(t),dx/len*Math.cos(t),Math.sin(t)],p=(c,t)=>{const n=norm(t);return c.map((v,i)=>v+radius*n[i])};for(let i=0;i<segments;i++){const t=i/segments*Math.PI*2,u=(i+1)/segments*Math.PI*2;triangle(p(a,t),p(b,t),p(b,u),norm(t),norm(t),norm(u));triangle(p(a,t),p(b,u),p(a,u),norm(t),norm(u),norm(u))}}}
  if(o.objectType==='茶壶'){
   const facets=o.id==='tea-dpm-227616'?6:80;
   lathe([[0,-.66],[.3,-.66],[.34,-.6],[.6,-.55],[.75,-.32],[.79,.05],[.64,.38],[.37,.53],[.37,.58],[.31,.58],[.31,.48],[.58,.32],[.69,.02],[.63,-.3],[.48,-.46],[0,-.46]],facets);
   lathe([[0,.61],[.1,.61],[.12,.65],[.08,.72],[0,.74]],32);lathe([[0,.57],[.36,.57],[.4,.55],[.42,.58],[.3,.63],[0,.63]],facets);
   const handle=[];for(let i=0;i<=42;i++){const t=-Math.PI*.55+i/42*Math.PI*1.1;handle.push([-.67-.48*Math.cos(t),.01+.49*Math.sin(t),0])}tube(handle,.075);
   tube([[.57,-.21,0],[.82,-.1,0],[1.02,.14,0],[1.16,.38,0],[1.27,.48,0]],.11);
  }else{
   const d=o.fields.dimensions.value||'',h=d.match(/高\s*([\d.]+)/),diam=d.match(/(?:口径|直径)\s*([\d.]+)/),height=h&&diam?Math.min(1.5,Math.max(.45,2*Number(h[1])/Number(diam[1]))):.94;
   const y=-height/2;lathe([[0,y],[.3,y],[.34,y+.06],[.33,y+.14],[.44,y+.19],[.6,y+height*.38],[.8,y+height*.65],[.98,y+height*.95],[1,y+height],[.96,y+height+.012],[.92,y+height*.94],[.74,y+height*.64],[.53,y+height*.36],[.33,y+.23],[0,y+.2]]);
  }return {positions:new Float32Array(verts),normals:new Float32Array(norms)};
 }

module.exports={mesh,shaders:{"VERTEX_SHADER": "attribute vec3 position; attribute vec3 normal; uniform float yaw; uniform float pitch; uniform float zoom; uniform float aspect; varying vec3 N; varying vec3 P; vec3 rotate(vec3 p){p=vec3(cos(yaw)*p.x+sin(yaw)*p.z,p.y,-sin(yaw)*p.x+cos(yaw)*p.z);return vec3(p.x,cos(pitch)*p.y-sin(pitch)*p.z,sin(pitch)*p.y+cos(pitch)*p.z);} void main(){vec3 p=rotate(position)*zoom;N=rotate(normal);P=p;p.z-=4.4;float f=2.4142;gl_Position=vec4(p.x*f/aspect,p.y*f,-1.004*p.z-.2004,-p.z);}", "FRAGMENT_SHADER": "precision mediump float; varying vec3 N; varying vec3 P; uniform vec3 clay; void main(){vec3 n=normalize(N);vec3 light=normalize(vec3(-2.,3.,4.));float d=max(0.,dot(n,light));vec3 eye=normalize(vec3(0.,0.,4.4)-P);float spec=pow(max(0.,dot(n,normalize(light+eye))),48.);vec3 base=clay*(.27+.7*d)+vec3(.38)*spec;float rim=pow(1.-max(0.,dot(n,eye)),3.);gl_FragColor=vec4(base+rim*.055,1.);}"}};
