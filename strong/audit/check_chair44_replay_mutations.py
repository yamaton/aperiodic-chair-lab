from pathlib import Path
import argparse,gzip,hashlib,json,subprocess,sys,tempfile,time
parser=argparse.ArgumentParser(description='Check three corruption controls for the independent Chair44 companion replay.')
parser.add_argument('--release-root',required=True,type=Path)
parser.add_argument('--checker',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
args=parser.parse_args()
root=args.release_root.resolve()
script=args.checker.resolve()
base=Path('verify/packets/r44_unrestricted_alignment')
paths=[Path('solid/r44_solid.json'),base/'input/candidate_certificate.json',base/'input/companion_collision_certificate.json',Path('certificates/candidate_certificate.json'),Path('certificates/companion_collision_certificate.json'),base/'input/r44_solid.json',base/'results/collision_core_witnesses.jsonl.gz']
results=[]
for mutation,expected in [('omit_partner','export omitted an unpruned partner'),('alter_intersection','claimed carrier intersection incorrect'),('duplicate_partner','invalid/duplicate listed partner')]:
 with tempfile.TemporaryDirectory(prefix='chair44-replay-mutation-') as tmp:
  local=Path(tmp)
  for p in paths:
   dest=local/p;dest.parent.mkdir(parents=True,exist_ok=True)
   if p.suffix!='.gz': dest.symlink_to(root/p)
  with gzip.open(root/paths[-1],'rt') as source,gzip.open(local/paths[-1],'wt') as target:
   record=json.loads(source.readline())
   if mutation=='omit_partner':record['overlaps'].pop()
   if mutation=='alter_intersection':record['overlaps'][0][4][0]+=1
   if mutation=='duplicate_partner':record['overlaps'].append(record['overlaps'][0])
   target.write(json.dumps(record)+'\n')
   for line in source:target.write(line)
  start=time.monotonic()
  run=subprocess.run([sys.executable,str(script),'--release-root',str(local),'--output',str(local/'output.json')],text=True,capture_output=True)
  if run.returncode==0 or expected not in run.stderr:
   raise ValueError((mutation,run.returncode,run.stdout,run.stderr))
  results.append({'mutation':mutation,'detected':True,'expected_error':expected,'seconds':time.monotonic()-start})
output={'status':'PASS','scope':'Three corrupted copies of the collision-box stream must be rejected by the independent checker. Release data remains untouched.','checker_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'controls':results}
args.output.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
