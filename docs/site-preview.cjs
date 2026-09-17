// A static illustration of two legally joined chairs, drawn from the same model.
const fs=require('node:fs');
const E=require('./assembly/engine.js');
module.exports=()=>{
  const certificate=JSON.parse(fs.readFileSync('strong/audit/motif_grouping_certificate.json'));
  const rules=E.create({faces:certificate.face_table,group:certificate.derived_group});
  const base={t:[0,0,0],r:E.I};
  // Use the demo's contact so both chairs are visible from the landing-page view.
  const joined=rules.goalFor(base).find(p=>{const result=rules.check([base],p);return result.ok&&result.contacts.some(c=>c.a.ref==='0:11');});
  const tiles=[base,joined];
  const view=p=>{const x=Math.cos(.8)*p[0]-Math.sin(.8)*p[1],d=Math.sin(.8)*p[0]+Math.cos(.8)*p[1];return [x,Math.sin(.6)*d-Math.cos(.6)*p[2],Math.cos(.6)*d+Math.sin(.6)*p[2]];};
  const faces=rules.exposed(tiles).filter(f=>view(f.n)[2]>0).map(f=>{
    const center=E.mul(f.c,.5),v=E.cross(f.n,f.u);
    const points=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>view(E.add(center,E.add(E.mul(f.u,a*.5),E.mul(v,b*.5)))));
    return {...f,center,points,depth:view(center)[2]};
  }).sort((a,b)=>a.depth-b.depth);
  const points=faces.flatMap(f=>f.points),lo=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),hi=[0,1].map(i=>Math.max(...points.map(p=>p[i])));
  const scale=Math.min(450/(hi[0]-lo[0]),330/(hi[1]-lo[1]));
  const project=p=>[280+(p[0]-(lo[0]+hi[0])/2)*scale,205+(p[1]-(lo[1]+hi[1])/2)*scale];
  const polygons=faces.map(f=>{
    const p=project(view(f.center)),end=project(view(E.add(f.center,E.mul(f.u,.27)))),dx=end[0]-p[0],dy=end[1]-p[1],n=Math.hypot(dx,dy);
    const fill=f.tile===0?'#84b3a1':'#e6bd77';
    return `<g><polygon points="${f.points.map(p=>project(p).join(',')).join(' ')}" fill="${fill}" stroke="#48675b" stroke-opacity=".55"/><path d="M${p[0]} ${p[1]}L${end[0]} ${end[1]}m${-dx/n*6+dy/n*3} ${-dy/n*6-dx/n*3}L${end[0]} ${end[1]}l${-dx/n*6-dy/n*3} ${-dy/n*6+dx/n*3}" fill="none" stroke="#284e43" stroke-width="2"/><text x="${p[0]-dx*.85}" y="${p[1]-dy*.85+4}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" font-weight="650" fill="#284e43">${f.motif}</text></g>`;
  }).join('');
  return `<svg viewBox="0 0 560 420" aria-hidden="true"><ellipse cx="280" cy="379" rx="190" ry="22" fill="#416955" opacity=".07"/>${polygons}</svg>`;
};
