#!/usr/bin/env python3
"""Local environment inventory; does not install, change security, connect USB or record camera IDs."""
from __future__ import annotations
import argparse,ctypes.util,json,os,platform,shutil,subprocess
from pathlib import Path

def run(cmd: list[str]) -> dict:
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
        return {'exit_code':p.returncode,'output':(p.stdout+'\n'+p.stderr).strip()[:4000]}
    except (OSError,subprocess.TimeoutExpired) as e:
        return {'exit_code':None,'error':type(e).__name__}

def inspect() -> dict:
    r={'schema':1,'host':{'os':platform.system(),'machine':platform.machine(),'python':platform.python_version()},
       'scope':'environment only; no USB calls, no package installation, no OS setting changes',
       'host_confirmed_by_user':'Apple Silicon MacBook Pro / macOS 27',
       'macos27_usb_verified':False,'apk_built_by_this_tool':False}
    if platform.system()=='Darwin':r['host']['sw_vers']=run(['/usr/bin/sw_vers','-productVersion'])
    sdk=Path(os.environ.get('ANDROID_SDK_ROOT',os.environ.get('ANDROID_HOME',str(Path.home()/'Library/Android/sdk'))))
    bt=sdk/'build-tools'/'30.0.3'
    paths={'android10.jar':Path(os.environ.get('CINEVISTA_ANDROID10_JAR',str(sdk/'platforms/android-10/android.jar'))),
           'android28.jar':sdk/'platforms/android-28/android.jar','aapt':bt/'aapt','zipalign':bt/'zipalign',
           'd8.jar':bt/'lib/d8.jar','apksigner':bt/'apksigner'}
    r['sdk']={}
    for key,path in paths.items():
        r['sdk'][key]={'present':path.is_file()}
        if path.is_file() and key in ('aapt','zipalign') and shutil.which('file'):
            info=run(['file','-b',str(path)]);r['sdk'][key]['binary_type']=info
    r['commands']={}
    for command,arg in [('java','-version'),('javac','-version'),('git','--version'),('node','--version')]:
        found=shutil.which(command)
        r['commands'][command]=run([found,arg]) if found else {'present':False}
    r['libusb']={'discoverable':bool(ctypes.util.find_library('usb-1.0')),
                 'homebrew_arm64_file':Path('/opt/homebrew/opt/libusb/lib/libusb-1.0.dylib').is_file()}
    r['next']='Check actual SDK executables on the Mac; then PMCA info via MTP. This report is not a USB compatibility result.'
    return r

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
    text=json.dumps(inspect(),ensure_ascii=False,indent=2)+'\n'
    print(text,end='')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f:f.write(text)
    return 0
if __name__=='__main__':raise SystemExit(main())
