#!/usr/bin/env python3
"""Build the desktop reference and tests. No downloads and no Android stubs."""
import pathlib, shutil, subprocess, sys, os
from run_evidence import write_evidence, run_dir
ROOT=pathlib.Path(__file__).resolve().parents[1]
BUILD=ROOT/'build'/'host'; CLASSES=BUILD/'classes'
def main():
    for command in ('javac','java','jar'):
        if not shutil.which(command): raise SystemExit(f'{command} is required (JDK 17 or 21 recommended)')
    if BUILD.exists(): shutil.rmtree(BUILD)
    CLASSES.mkdir(parents=True)
    import json
    modules=json.loads((ROOT/'config/modules.json').read_text())
    compiled={}
    for name in modules['host_order']:
        spec=modules['modules'][name]
        out=BUILD/'modules'/name;out.mkdir(parents=True)
        sources=sorted((ROOT/spec['src']).rglob('*.java'))
        args=BUILD/(name+'-sources.txt')
        args.write_text('\n'.join('"'+str(p)+'"' for p in sources),encoding='utf-8')
        command=['javac','--release','8','-encoding','UTF-8','-Xlint:all','-d',str(out)]
        deps=[str(compiled[d]) for d in spec['deps']]
        if deps: command+=['-classpath',os.pathsep.join(deps)]
        subprocess.run(command+['@'+str(args)],check=True)
        compiled[name]=out
        shutil.copytree(out,CLASSES,dirs_exist_ok=True)
    subprocess.run(['jar','cfe',str(BUILD/'cinevista-reference.jar'),'org.cinevista.host.Main','-C',str(CLASSES),'.'],check=True)
    env=dict(os.environ); env['JAVA_TOOL_OPTIONS']='-Djava.awt.headless=true'
    result=subprocess.run(['java','-Xmx512m','-cp',str(CLASSES),'org.cinevista.tests.AllTests'],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    write_evidence('java-host-tests.txt',result.stdout); print(result.stdout,end='')
    if result.returncode: raise SystemExit(result.returncode)
    print('Desktop JAR built; Android APK not built by this script.')
if __name__=='__main__': main()
