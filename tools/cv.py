#!/usr/bin/env python3
"""Small orchestration entrypoint; delegates compilation/packaging to existing tools."""
from pathlib import Path
import subprocess,sys,argparse
from run_evidence import run_dir
ROOT=Path(__file__).resolve().parents[1]
def run(*args):
    print('+',*args,flush=True)
    subprocess.run(list(args),cwd=ROOT,check=True)
def script(name,*args):run(sys.executable,str(ROOT/'tools'/name),*args)
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['doctor','check','host-test','source-check','android','release-check']);p.add_argument('--android',action='store_true');a=p.parse_args()
    print('Evidence:', run_dir(), flush=True)
    if a.command=='doctor':script('doctor.py',*(['--android'] if a.android else []))
    elif a.command=='check':
        script('architecture_check.py');script('policy_check.py');script('docs_check.py');run('node','--test','studio/tests/look-core.test.js','studio/grading/tests/grade-core.test.js');run(sys.executable,'-m','unittest','discover','-s','tests/tools','-v')
        script('build_host.py');script('check_reference.py');script('check_app_source.py');run(sys.executable,'-m','unittest','discover','-s','reference','-v')
    elif a.command=='host-test':script('build_host.py');script('check_reference.py')
    elif a.command=='source-check':script('check_app_source.py')
    elif a.command=='android':script('doctor.py','--android');script('build_android.py')
    elif a.command=='release-check':script('release_check.py')
if __name__=='__main__':
    try:main()
    except subprocess.CalledProcessError as e:sys.exit(e.returncode)
