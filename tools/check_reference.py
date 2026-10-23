#!/usr/bin/env python3
"""Compare the Java geometry against the retained v0.1 Python oracle."""
import pathlib, sys, random, subprocess, json, math
from run_evidence import write_evidence, run_dir
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference'))
from geometry_reference import plan_frame
from dataclasses import asdict
r=random.Random(260918); rows=[]; expected=[]
for i in range(3000):
    w=r.randint(256,10000); h=r.randint(256,8000); s=r.uniform(1,2)
    a=None if i%5==0 else r.uniform(1.5,3.7); ox=r.uniform(-1,1); oy=r.uniform(-1,1)
    policy='expanded' if i%3==0 else 'compact'; cap=None if i%2==0 else r.randint(200,8000)
    expected.append(asdict(plan_frame(w,h,s,a,ox,oy,policy,cap,1)))
    rows.append(f'{w} {h} {s} {a if a is not None else "auto"} {ox} {oy} {policy} {cap if cap is not None else "none"}')
p=subprocess.run(['java','-cp',str(ROOT/'build/host/classes'),'org.cinevista.tests.PlanOracle'],input='\n'.join(rows)+'\n',text=True,capture_output=True,check=True)
actual=[json.loads(x) for x in p.stdout.splitlines()]
assert len(actual)==len(expected)
def compare(a,b,path=''):
    if isinstance(a,dict):
        assert set(a)==set(b),(path,set(a)^set(b))
        for k in a: compare(a[k],b[k],path+'/'+k)
    elif isinstance(a,(int,float)):
        assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),(path,a,b)
    else: assert a==b,(path,a,b)
for a,b in zip(actual,expected): compare(a,b)
text='PASS 3000 deterministic Java/Python differential geometry cases.\nNo camera, display, JPEG or SDK behavior inferred.\n'
write_evidence('reference-parity.txt',text);print(text,end='')
