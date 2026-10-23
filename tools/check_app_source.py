#!/usr/bin/env python3
import pathlib, subprocess, tempfile, re, json, xml.etree.ElementTree as ET
from run_evidence import write_evidence, run_dir
ROOT=pathlib.Path(__file__).resolve().parents[1]
sources=[p for folder in ('core/src','io/src','camera-api/src','sony/src','app/src') for p in (ROOT/folder).rglob('*.java')]
with tempfile.TemporaryDirectory(prefix='cv-syntax-') as tmp:
    subprocess.run(['javac','-d',tmp,str(ROOT/'tools/SyntaxCheck.java')],check=True)
    result=subprocess.run(['java','-cp',tmp,'SyntaxCheck',*[str(p) for p in sources]],text=True,capture_output=True,check=True)
ns='{http://schemas.android.com/apk/res/android}'
m=ET.parse(ROOT/'app/AndroidManifest.xml').getroot()
assert m.find('uses-sdk').get(ns+'minSdkVersion')=='10'
assert m.find('uses-sdk').get(ns+'targetSdkVersion')=='10'
permissions=[x.get(ns+'name') for x in m.findall('uses-permission')]
assert set(permissions)=={'android.permission.CAMERA','android.permission.WRITE_EXTERNAL_STORAGE'}
all_code='\n'.join(p.read_text() for p in sources)
for p in sources:
    text=p.read_text()
    assert not re.search(r'^\s*package\s+(com\.sony|android\.)',text,re.M),p
    assert not re.search(r'import\s+(android\.view\.TextureView|android\.hardware\.camera2|androidx\.)',text),p
from build_profiles import load, validate_sources
validate_sources(ROOT, sources, load(ROOT))
text=result.stdout+'PASS manifest/source guardrails (limited checks, not Android API compatibility proof).\n'
write_evidence('android-source-checks.txt',text);print(text,end='')
