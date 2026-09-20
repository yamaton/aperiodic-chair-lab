from pathlib import Path
import sys,json,hashlib
from collections import defaultdict
from itertools import product
from fractions import Fraction as Q
import numpy as np
ROOT=Path.cwd(); sys.path.insert(0,str(ROOT/'docs'))
from relocated_cover_mesh import prepare_relocated
from triangular_cover_mesh import prepare_triangular
out=Path('/tmp/aperiodic-rendering-review');out.mkdir(exist_ok=True)
rdir=out/'relocated';rdir.mkdir(exist_ok=True)
report=prepare_relocated(rdir) if not (rdir/'chair.npz').exists() else json.loads((ROOT/'docs/figures/aperiodic-chair-cover-relocated.json').read_text())
print('Relocated preparation passed',report['chair_mesh'],flush=True)
source=json.loads((ROOT/'strong/audit/triangular_v1/candidate.json').read_text())
m=np.load(rdir/'chair.npz');v=m['vertices'];tri=v[m['faces']];kinds=m['kinds']
# Independent carrier boundary face set.
cubes=set(map(tuple,source['coarse_cubes'])); carrier_faces=set()
for c in cubes:
 for ax,sgn in product(range(3),(-1,1)):
  n=tuple(sgn if i==ax else 0 for i in range(3))
  if tuple(c[i]+n[i] for i in range(3)) not in cubes:
   f=tuple(Q(2*c[i]+1+n[i],2) for i in range(3));carrier_faces.add((f,n))
groups=defaultdict(list);ports=[]
for idx,p in enumerate(source['ports']):
 U,V,N=[np.array(p[k]) for k in ('u_axis','v_axis','outward_normal')]
 f=tuple(Q(x)-Q(3*int(u)+int(vv),16) for x,u,vv in zip(p['center'],U,V))
 center=np.array(f,float)-U/4+V*7/32
 rec=dict(index=idx,U=U,V=V,N=N,f=np.array(f,float),p=center,key=p['signed_key'])
 groups[(f,tuple(N))].append(rec);ports.append(rec)
assert set(groups)==carrier_faces
# Clipping independent polygons to verify flat triangles do not enter support.
def clip(poly,a,b):
 def side(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
 result=[]
 for x,y in zip(poly,poly[1:]+poly[:1]):
  sx,sy=side(x),side(y)
  if sx>=-1e-14:result.append(x)
  if (sx>1e-14 and sy<-1e-14) or (sx<-1e-14 and sy>1e-14):result.append(x+(y-x)*sx/(sx-sy))
 return result
def ar(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0
w=3/16;h=1/16;inner=np.array([[-1/4-w,7/32-w],[-1/4+w,7/32-w],[-1/4-w,7/32]])
maxerr=0.; minclear=1.;curved={};at=0
for (face,N),ps in groups.items():
 wedge_centroids=[]
 face_area=0
 for p in ps:
  block=tri[at:at+2451];ks=kinds[at:at+2451];at+=2451
  assert np.count_nonzero(ks)==2304 and np.all(ks[:147]==0)
  planar=np.stack([(block-p['f'])@p['U'],(block-p['f'])@p['V']],axis=-1)
  # Whole projection lies in actual reflection wedge and has the expected area.
  X,Y=planar[...,0],planar[...,1]
  assert np.min(X+.5)>-1e-11 and np.min(Y)>-1e-11 and np.min(-X-Y)>-1e-11
  areas=abs(np.linalg.det(np.stack([planar[:,1]-planar[:,0],planar[:,2]-planar[:,0]],axis=1)))/2
  assert abs(areas.sum()-1/8)<1e-11;face_area+=areas.sum()
  for flat in planar[:147]:
   poly=list(flat)
   for a,b in zip(inner,np.roll(inner,-1,axis=0)):poly=clip(poly,a,b)
   assert ar(poly)<1e-12
  cap=block[147:];d=cap-p['p'];x=(d@p['U']/w+1)/2;y=d@p['V']/w+1;z=d@p['N']
  assert min(x.min(),y.min(),(1-x-y).min())>-1e-10
  maxerr=max(maxerr,float(abs(z-p['key']*h*27*x*y*(1-x-y)).max()))
  edgeclear=np.minimum(.5-abs(X[147:]),.5-abs(Y[147:]))-abs(z)
  minclear=min(minclear,float(edgeclear.min()))
  assert np.all(np.cross(block[:,1]-block[:,0],block[:,2]-block[:,0])@p['N']>0)
  curved[p['index']]=np.unique(cap.reshape(-1,3),axis=0)
  wedge_centroids.append(tuple(np.round((-p['U']+p['V']/2)/3,12)))
 assert len(set(wedge_centroids))==8 and abs(face_area-1)<1e-10
assert at==len(tri) and maxerr<1e-10 and minclear>=5/256-1e-10
print('Independent geometry: 24 true carrier faces; each eight nonoverlapping wedges; projected areas; no flat/cap overlap; cap support and depth; all outward triangles',flush=True)
print('After-export maximum cap coordinate error',maxerr,'minimum vertex curved-zone clearance',minclear,flush=True)
# Shared anchors plus actual mesh vertex coincidence for all internal contacts.
occs=defaultdict(list)
for ci,c in enumerate(source['children']):
 R=np.array(c['matrix']);t=np.array(c['center']);assert round(np.linalg.det(R))==1
 for p in ports:occs[tuple(R@p['p']+t)].append((ci,p,R,t))
contacts=[os for os in occs.values() if len(os)==2];assert len(contacts)==384
assert all(len(os) in (1,2) for os in occs.values())
for left,right in contacts:
 _,a,A,ta=left;_,b,B,tb=right
 assert a['key']==-b['key']
 assert np.array_equal(A@a['U'],B@b['U']) and np.array_equal(A@a['V'],B@b['V']) and np.array_equal(A@a['N'],-B@b['N'])
 va=np.unique(np.round(curved[a['index']]@A.T+ta,10),axis=0)
 vb=np.unique(np.round(curved[b['index']]@B.T+tb,10),axis=0)
 assert np.array_equal(va,vb)
print('All 384 internal contacts coincide as exported cap vertex sets',flush=True)
# Invert both detail display transforms and test actual cap and rim positions.
scene=json.loads((rdir/'scene.json').read_text())
for i,idx in enumerate((40,56)):
 p=ports[idx];chi=int(np.dot(np.cross(p['U'],p['V']),p['N']))
 F=np.column_stack((p['U'],p['V'],p['N']));D=np.diag((1,chi,1));R=D@F.T
 assert np.array_equal(R@R.T,np.eye(3)) and round(np.linalg.det(R))==1
 dm=np.load(rdir/f'detail-{i}.npz');dv=dm['vertices'];dt=dv[dm['faces']];dk=dm['kinds']
 centroid=np.array([-w/3,-2*w/3,0]);local=(dt/scene['detail_magnification'])@D+centroid
 cap=local[dk!=0];x=(cap[...,0]/w+1)/2;y=cap[...,1]/w+1
 assert abs(cap[...,2]-p['key']*h*27*x*y*(1-x-y)).max()<1e-10
 top=local[np.all(abs(local[...,2])<1e-11,axis=1)]
 px=top[...,0]-1/4;py=top[...,1]+7/32
 assert (px>-.5).all() and (py>0).all() and (-px>py).all()
 # Backing entirely below the pocket's peak and top's flat crop.
 assert local[...,2].min() <= -abs(p['key'])*h*1.5+1e-11
print('Both detail meshes invert to actual cubic profiles and 9/8 rims inside true wedges; display rotations det +1',flush=True)
# Orthographic projected bounding rectangles; all geometry must stay in panels.
def project(points,loc,scale=3.65):
 z=np.array(loc,float);z/=np.linalg.norm(z);x=np.cross([0,0,1],z);x/=np.linalg.norm(x);y=np.cross(z,x)
 return np.stack((points@x,points@y),axis=-1)/scale*800+400
for name,points,loc in [('one',v,(6,8,5.4)),('assembly',np.concatenate([v@np.array(c['matrix']).T*.5+np.array(c['center'])*.5 for c in source['children']]),(6,8,5.4)),('detail',np.concatenate([np.load(rdir/f'detail-{i}.npz')['vertices']+np.array([x,0,0]) for i,x in enumerate((-.9,.9))]),(.7,-4.5,4))]:
 pixels=project(points,loc);assert pixels.min()>0 and pixels.max()<800
 print(name,'projected pixel bounds',pixels.min(axis=0).tolist(),pixels.max(axis=0).tolist(),flush=True)
# Provenance, separating original receipt hashes from evolving shared sources.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((ROOT/'docs/figures/aperiodic-chair-cover-relocated.json').read_text())
paths={'source_candidate_sha256':'strong/audit/triangular_v1/candidate.json','dimension_evidence_sha256':'strong/audit/port_dimensions.json','driver_sha256':'docs/render_chair_cover.py','blender_script_sha256':'docs/blender_chair_cover.py','mesh_exporter_sha256':'strong/build_recut_visualization.py','triangular_mesh_exporter_sha256':'docs/triangular_cover_mesh.py','relocated_mesh_exporter_sha256':'docs/relocated_cover_mesh.py','image_sha256':'docs/figures/aperiodic-chair-cover-relocated.png'}
assert all(sha(ROOT/p)==r[k] for k,p in paths.items())
for p in (ROOT/'docs/figures').glob('aperiodic-chair-cover-*.json'):
 if p.with_suffix('.png').exists():assert sha(p.with_suffix('.png'))==json.loads(p.read_text())['image_sha256']
print('All 8 current provenance hashes and all preserved cover image hashes match',flush=True)
tdir=out/'triangular';tdir.mkdir(exist_ok=True);t=prepare_triangular(tdir,3,64)
print('Earlier triangular prepare at 3x/64x passed',t['mesh_triangles'],t['checked_internal_port_pairs'],flush=True)
(out/'review-result.json').write_text(json.dumps({'status':'passed','max_export_coordinate_error':maxerr,'minimum_vertex_zone_clearance':minclear,'generated_report':report},indent=2))
