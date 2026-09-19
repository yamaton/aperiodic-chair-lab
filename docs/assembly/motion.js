/* Display-only rigid motion; intermediate poses never enter the grid rules/history. */
(function(root){
  'use strict';
  const E=typeof module!=='undefined'&&module.exports?require('./engine.js'):root.ChairEngine;
  const {add,sub,mul,act,dot,clone}=E;
  const mix=(a,b,t)=>add(mul(a,1-t),mul(b,t));
  // Unit quaternion, scalar first. The largest component is stable at half turns.
  function quaternion(r){
    const terms=[1+r[0]+r[4]+r[8],1+r[0]-r[4]-r[8],1-r[0]+r[4]-r[8],1-r[0]-r[4]+r[8]];
    const i=terms.indexOf(Math.max(...terms)),s=2*Math.sqrt(Math.max(0,terms[i]));
    return [()=>[s/4,(r[7]-r[5])/s,(r[2]-r[6])/s,(r[3]-r[1])/s],
      ()=>[(r[7]-r[5])/s,s/4,(r[1]+r[3])/s,(r[2]+r[6])/s],
      ()=>[(r[2]-r[6])/s,(r[1]+r[3])/s,s/4,(r[5]+r[7])/s],
      ()=>[(r[3]-r[1])/s,(r[2]+r[6])/s,(r[5]+r[7])/s,s/4]][i]();
  }
  function rotation(a,b,t){
    let q=quaternion(a),p=quaternion(b),d=dot(q,p);
    if(d<0){p=mul(p,-1);d=-d;}
    if(d>.9995)q=mix(q,p,t);
    else {const angle=Math.acos(Math.min(1,d));q=add(mul(q,Math.sin((1-t)*angle)/Math.sin(angle)),mul(p,Math.sin(t*angle)/Math.sin(angle)));}
    const [w,x,y,z]=mul(q,1/Math.sqrt(dot(q,q)));
    return [1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w),2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w),2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)];
  }
  // Cube centers are +/- 1/2; removing the (+,+,+) cube shifts their centroid.
  const center=[-1/14,-1/14,-1/14];
  const worldCenter=p=>add(p.t,act(p.r,center));
  function transition(from,to,normal){
    const segments=[];let p=clone(from);
    const push=(phase,end,duration)=>{segments.push({phase,from:p,to:end,duration});p=end;};
    if(normal)push('separate',{t:add(p.t,mul(normal,1.5)),r:p.r},200);
    if(p.r.some((v,i)=>Math.abs(v-to.r[i])>1e-9)){
      push('rotate',{t:sub(worldCenter(p),act(to.r,center)),r:to.r},360);
    }
    if(p.t.some((v,i)=>Math.abs(v-to.t[i])>1e-9))push('approach',clone(to),300);
    return {segments,to:clone(to),duration:segments.reduce((n,s)=>n+s.duration,0)};
  }
  function sample(motion,elapsed){
    for(const s of motion.segments){
      if(elapsed<s.duration){
        const t=Math.max(0,elapsed/s.duration),ease=t*t*(3-2*t);
        const r=s.phase==='rotate'?rotation(s.from.r,s.to.r,ease):s.from.r;
        const c=mix(worldCenter(s.from),worldCenter(s.to),ease);
        return {phase:s.phase,pose:{r,t:sub(c,act(r,center))}};
      }
      elapsed-=s.duration;
    }
    return {phase:'',pose:clone(motion.to)};
  }
  const api={transition,sample};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.ChairMotion=api;
})(typeof globalThis!=='undefined'?globalThis:this);
