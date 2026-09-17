/* Exact integer-grid rules. Shared by the offline page and Node verification. */
(function (root) {
  'use strict';
  const I = [1,0,0,0,1,0,0,0,1];
  const add = (a,b) => a.map((v,i) => v+b[i]);
  const sub = (a,b) => a.map((v,i) => v-b[i]);
  const mul = (a,s) => a.map(v => v*s);
  const dot = (a,b) => a.reduce((s,v,i) => s+v*b[i],0);
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const act = (r,v) => [0,1,2].map(i => dot(r.slice(i*3,i*3+3),v));
  const product = (a,b) => a.map((_,i) => [0,1,2].reduce((s,k) => s+a[3*Math.floor(i/3)+k]*b[k*3+i%3],0));
  const transpose = r => [0,3,6,1,4,7,2,5,8].map(i => r[i]);
  const eq = (a,b) => a.every((v,i) => v===b[i]);
  const key = v => v.join(',');
  const poseKey = p => key(p.t)+'/'+key(p.r);
  const rotations = [];
  const axes = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
  for (const x of axes) for (const y of axes) if (!dot(x,y)) {
    const z = cross(x,y); rotations.push([x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]]);
  }
  const cubes = [];
  for (const x of [-1,1]) for (const y of [-1,1]) for (const z of [-1,1])
    if (x!==1 || y!==1 || z!==1) cubes.push([x,y,z]);
  const clone = value => JSON.parse(JSON.stringify(value));

  function create(data) {
    const faces = data.faces;
    const group = data.group.map(([t,r]) => ({t,r}));
    const placedFaces = p => faces.map(f => ({...f, c:add(act(p.r,f.center_times_2),mul(p.t,2)),
      n:act(p.r,f.normal), u:act(p.r,f.arrow)}));
    const placedCubes = p => cubes.map(c => add(act(p.r,c),mul(p.t,2)));
    function exposed(tiles) {
      const map = new Map();
      tiles.forEach((p,tile) => placedFaces(p).forEach(f => {
        const k=key(f.c); const previous=map.get(k);
        map.set(k,previous ? {internal:true} : {...f,tile,ref:`${tile}:${f.id}`});
      }));
      return [...map.values()].filter(f => !f.internal);
    }
    function handshake(a,b) {
      const patterns = a.motif==='A' ? b.motif==='A' : (a.motif==='B' ? b.motif==='C' : b.motif==='B');
      const expected = a.motif==='A' ? cross(a.n,a.u) : mul(a.u,-1);
      return {patterns, expected, arrow:eq(expected,b.u), ok:patterns && eq(expected,b.u)};
    }
    function check(tiles,p) {
      if (!p) return {ok:false, contacts:[],overlap:[],reason:'面を選んでください'};
      const occupied = new Set(tiles.flatMap(placedCubes).map(key));
      const overlap = placedCubes(p).filter(c => occupied.has(key(c)));
      const boundary = new Map(exposed(tiles).map(f => [key(f.c),f]));
      const contacts = placedFaces(p).flatMap(b => {
        const a=boundary.get(key(b.c));
        return a && eq(a.n,mul(b.n,-1)) ? [{a,b,...handshake(a,b)}] : [];
      });
      const bad=contacts.filter(c => !c.ok);
      return {ok:!overlap.length && contacts.length>0 && !bad.length, contacts,overlap,
        reason:overlap.length ? 'ブロックの内部が重なっています' : !contacts.length ? '面を選んでください'
          : bad.length ? `${contacts.length}面中 ${bad.length}面が不適合` : `接触${contacts.length}面すべて適合`};
    }
    function candidates(tiles,ref,all=false) {
      const a=exposed(tiles).find(f => f.ref===ref);
      if (!a) return [];
      const results=new Map();
      for (const f of faces) for (const r of rotations) {
        if (!eq(act(r,f.normal),mul(a.n,-1))) continue;
        const t=mul(sub(a.c,act(r,f.center_times_2)),0.5);
        if (!t.every(Number.isInteger)) continue;
        const p={t,r}; const b=placedFaces(p)[f.id];
        if (!all && !handshake(a,b).patterns) continue;
        results.set(poseKey(p),{p,face:f.id,motif:f.motif,result:check(tiles,p)});
      }
      // Geometric placement help only: never prune the 14 locally fitting dead ends.
      return [...results.values()].sort((a,b) => Number(!!a.result.overlap.length)-Number(!!b.result.overlap.length) || a.face-b.face || poseKey(a.p).localeCompare(poseKey(b.p)));
    }
    function rotateAt(tiles,p,ref,sign) {
      const a=exposed(tiles).find(f => f.ref===ref);
      if (!a || !p) return p;
      const n=a.n;
      const q=[0,1,2].flatMap(i => [0,1,2].map(j => {
        const e=[0,0,0];e[j]=1;return n[i]*n[j]+sign*cross(n,e)[i];
      }));
      const pivot=mul(a.c,0.5);
      return {t:add(pivot,act(q,sub(p.t,pivot))),r:product(q,p.r)};
    }
    function parent(tiles) {
      if (tiles.length!==8) return null;
      const actual=new Set(tiles.map(poseKey));
      for (const center of tiles) {
        const children=group.map(p => ({t:add(center.t,act(center.r,p.t)),r:product(center.r,p.r)}));
        if (children.every(p => actual.has(poseKey(p)))) return clone(center);
      }
      return null;
    }
    const goalFor = anchor => group.map(p => ({t:add(anchor.t,act(anchor.r,p.t)),r:product(anchor.r,p.r)}));
    const onGoal = (tiles,anchor) => {
      const goal=new Set(goalFor(anchor).map(poseKey)); return tiles.every(p => goal.has(poseKey(p)));
    };
    function nextHint(tiles,anchor) {
      if (!onGoal(tiles,anchor)) return null;
      const present=new Set(tiles.map(poseKey));
      for (const p of goalFor(anchor)) if (!present.has(poseKey(p))) {
        const result=check(tiles,p);
        if (result.ok) return {p:clone(p),ref:result.contacts[0].a.ref};
      }
      return null;
    }
    return {faces,group,placedFaces,placedCubes,exposed,handshake,check,candidates,rotateAt,parent,goalFor,onGoal,nextHint};
  }

  class History {
    constructor(state) {this.entries=[{state:clone(state),label:'開始'}];this.index=0;}
    get state() {return this.entries[this.index].state;}
    get canUndo() {return this.index>0;}
    get canRedo() {return this.index<this.entries.length-1;}
    commit(label,state) {
      this.entries.splice(this.index+1);this.entries.push({state:clone(state),label});this.index++;
    }
    adjust(state) {
      const item=this.entries[this.index];
      if (!this.canRedo && ['開始','部品の追加','候補の調整'].includes(item.label)) item.state=clone(state);
      else this.commit('候補の調整',state);
    }
    undo() {if(this.canUndo)this.index--;}
    redo() {if(this.canRedo)this.index++;}
  }
  const api={I,add,sub,mul,dot,cross,act,product,transpose,eq,key,poseKey,rotations,cubes,clone,create,History};
  if (typeof module!=='undefined' && module.exports) module.exports=api;
  else root.ChairEngine=api;
})(typeof globalThis!=='undefined' ? globalThis : this);
