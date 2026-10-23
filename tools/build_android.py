#!/usr/bin/env python3
"""Requires real Android SDK API 10 + build-tools 30.0.3. No fabricated SDK stubs.
Host build evidence is recorded per run; device behavior is independently gated.
"""
import os,sys,pathlib,subprocess,shutil,zipfile,json,hashlib,re
import xml.etree.ElementTree as ET
from run_evidence import write_evidence, run_dir
ROOT=pathlib.Path(__file__).resolve().parents[1]
BUILD=ROOT/'build/android'/run_dir().name
def main():
    from architecture_check import validate
    errors=validate(ROOT)
    if errors: raise SystemExit("Architecture check failed: " + "; ".join(errors))
    from build_profiles import load, validate_sources
    sources=[p for folder in ('core/src','io/src','camera-api/src','sony/src','app/src') for p in (ROOT/folder).rglob('*.java')]
    validate_sources(ROOT, sources, load(ROOT))
    manifest=ET.parse(ROOT/'app/AndroidManifest.xml').getroot()
    ns='{http://schemas.android.com/apk/res/android}'
    version=manifest.get(ns+'versionName');code=manifest.get(ns+'versionCode')
    if not re.fullmatch(r'[0-9]+\.[0-9]+-probe',version):raise ValueError('unsupported probe version name')
    sdk_text=os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME')
    sdk=pathlib.Path(sdk_text) if sdk_text else None
    bt=sdk/'build-tools/30.0.3' if sdk else None
    aj=pathlib.Path(os.environ['CINEVISTA_ANDROID10_JAR']) if os.environ.get('CINEVISTA_ANDROID10_JAR') else (sdk/'platforms/android-10/android.jar' if sdk else None)
    win=os.name=='nt';suffix='.exe' if win else ''
    paths={'android_api10_jar':aj}
    for tool in ('aapt','zipalign','apksigner'):
        ext=('.bat' if tool in ('d8','apksigner') else suffix) if win else ''
        paths[tool]=bt/(tool+ext) if bt else None
    paths['d8_jar']=bt/'lib/d8.jar' if bt else None
    missing=[k for k,v in paths.items() if v is None or not v.is_file()]
    for command in ('javac','java','jar','keytool'):
        if not shutil.which(command):missing.append(command)
    if missing:
        report={'apk_built':False,'reason':'required SDK components unavailable','missing':missing,
                'next':'Provide real API 10 android.jar and Android build-tools 30.0.3; rerun this script. Do not substitute handmade stubs.'}
        write_evidence('android-build-status.json',json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2));return 2
    if BUILD.exists():raise SystemExit('Refusing to overwrite an existing Android build run')
    for folder in ('classes','generated','dex'):(BUILD/folder).mkdir(parents=True)
    def run(args): print('+',' '.join(map(str,args)),flush=True);subprocess.run([str(x) for x in args],check=True)
    run([paths['aapt'],'package','-f','-m','-M',ROOT/'app/AndroidManifest.xml','-S',ROOT/'app/res','-I',aj,'-J',BUILD/'generated','-F',BUILD/'resources.ap_'])
    from launcher_contract import inspect_launcher
    # Refuse incompatible packaged resources before compilation or signing.
    write_evidence('launcher-preflight.json',json.dumps(inspect_launcher(BUILD/'resources.ap_',paths['aapt']),indent=2)+'\n')
    modules=json.loads((ROOT/'config/modules.json').read_text())
    compiled={}
    for name in modules['android_order']:
        spec=modules['modules'][name]
        out=BUILD/'modules'/name;out.mkdir(parents=True)
        sources=sorted((ROOT/spec['src']).rglob('*.java'))
        if name=='app': sources+=sorted((BUILD/'generated').rglob('*.java'))
        src=BUILD/(name+'-sources.txt');src.write_text('\n'.join('"'+str(p)+'"' for p in sources))
        args=['javac','-encoding','UTF-8','-source','8','-target','8','-bootclasspath',aj,'-d',out]
        deps=[str(compiled[d]) for d in spec['deps']]
        if deps: args+=['-classpath',os.pathsep.join(deps)]
        run(args+['@'+str(src)])
        compiled[name]=out
        shutil.copytree(out,BUILD/'classes',dirs_exist_ok=True)
    run(['jar','cf',BUILD/'classes.jar','-C',BUILD/'classes','.'])
    run(['java','-cp',paths['d8_jar'],'com.android.tools.r8.D8','--min-api','10','--lib',aj,'--output',BUILD/'dex',BUILD/'classes.jar'])
    shutil.copyfile(BUILD/'resources.ap_',BUILD/'unsigned.apk')
    with zipfile.ZipFile(BUILD/'unsigned.apk','a',compression=zipfile.ZIP_DEFLATED) as z:z.write(BUILD/'dex/classes.dex','classes.dex')
    run([paths['zipalign'],'-f','4',BUILD/'unsigned.apk',BUILD/'aligned.apk'])
    local=ROOT/'.local';local.mkdir(exist_ok=True);key=local/'cinevista-debug.jks'
    # An explicitly non-production signing identity, generated LOCALLY; never committed.
    if not key.exists():
        run(['keytool','-genkeypair','-keystore',key,'-storetype','JKS','-storepass','android','-keypass','android',
             '-alias','androiddebugkey','-keyalg','RSA','-keysize','2048','-validity','3650','-dname','CN=CineVista Local Debug,O=Development,C=XX'])
    apk=BUILD/('CineVista-Probe-'+version.removesuffix('-probe')+'-debug.apk')
    run([paths['apksigner'],'sign','--ks',key,'--ks-pass','pass:android','--key-pass','pass:android','--ks-key-alias','androiddebugkey',
         '--min-sdk-version','10','--v1-signing-enabled','true','--v2-signing-enabled','false','--v3-signing-enabled','false','--v4-signing-enabled','false','--out',apk,BUILD/'aligned.apk'])
    key.chmod(0o600)
    run([paths['zipalign'],'-c','-v','4',apk])
    signature=subprocess.run([str(paths['apksigner']),'verify','--verbose','--min-sdk-version','10','--max-sdk-version','10','--print-certs',str(apk)],check=True,text=True,capture_output=True)
    write_evidence('apk-signature.txt',signature.stdout)
    badging=subprocess.run([str(paths['aapt']),'dump','badging',str(apk)],check=True,text=True,capture_output=True)
    write_evidence('apk-badging.txt',badging.stdout)
    assert 'Verified using v1 scheme (JAR signing): true' in signature.stdout
    from apk_contract import validate_badging, source_hashes
    permissions=validate_badging(badging.stdout,manifest)
    from inspect_apk import inspect
    input_hashes=source_hashes(ROOT)
    write_evidence('android-source-inputs.json',json.dumps(input_hashes,indent=2)+'\n')
    report=inspect(apk);report.update(apk_built=True,permissions=permissions,apk_path=str(apk.relative_to(ROOT)),version_name=version,version_code=int(code),build_profile=load(ROOT)['id'],sha256=hashlib.sha256(apk.read_bytes()).hexdigest(),apk_name=apk.name,
        sdk_jar_sha256=hashlib.sha256(aj.read_bytes()).hexdigest(),toolchain='build-tools 30.0.3; API 10 android.jar',
        device_execution_verified=False)
    write_evidence('android-build-status.json',json.dumps(report,indent=2)+'\n');print(apk)
    return 0
if __name__=='__main__':sys.exit(main())
