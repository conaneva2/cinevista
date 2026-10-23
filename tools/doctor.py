#!/usr/bin/env python3
"""Read-only environment report. Missing SDK is a nonzero result in --android mode."""
import os,sys,platform,json,shutil,subprocess,hashlib,argparse
from pathlib import Path
from run_evidence import write_evidence, run_dir
ROOT=Path(__file__).resolve().parents[1]
def inspect():
    sdk=os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME')
    base=Path(sdk) if sdk else None; bt=base/'build-tools/30.0.3' if base else None
    jar=Path(os.environ['CINEVISTA_ANDROID10_JAR']) if os.environ.get('CINEVISTA_ANDROID10_JAR') else (base/'platforms/android-10/android.jar' if base else None)
    paths={'android_api10_jar':jar}
    for t in ('aapt','zipalign','apksigner'):
        ext=('.bat' if t in ('d8','apksigner') else '.exe') if os.name=='nt' else ''
        paths[t]=bt/(t+ext) if bt else None
    paths['d8_jar']=bt/'lib/d8.jar' if bt else None
    tools={}
    for t in ('java','javac','jar','keytool','git'):
        path=shutil.which(t);tools[t]={'present':bool(path)}
        if path and t in ('java','javac','git'):
            p=subprocess.run([path,'--version' if t=='git' else '-version'],capture_output=True,text=True)
            tools[t]['present']=p.returncode==0
            tools[t]['exit_code']=p.returncode
            tools[t]['version']=(p.stdout or p.stderr).splitlines()[:2]
    missing=[k for k,p in paths.items() if p is None or not p.is_file()]
    missing += [t for t in ('java','javac','jar','keytool') if not tools[t]['present']]
    artifacts={k:{'present':bool(p and p.is_file()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p and p.is_file() else None} for k,p in paths.items()}
    return {'schema_version':1,'os':platform.system(),'arch':platform.machine(),'python':platform.python_version(),'tools':tools,'sdk':artifacts,'missing_android':missing,'android_ready':not missing,'apk_built':False,'device_tested':False,'note':'Readiness only; presence/hash does not prove provenance, compiler success or device behavior.'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--android',action='store_true');a=ap.parse_args()
    report=inspect();(ROOT/'evidence').mkdir(exist_ok=True)
    write_evidence('environment-v0.4.json',json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return 2 if a.android and not report['android_ready'] else 0
if __name__=='__main__':sys.exit(main())
