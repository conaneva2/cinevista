"""Check official aapt output, keeping declared vs implied permissions distinct."""
import hashlib
import re
import xml.etree.ElementTree as ET
NS='{http://schemas.android.com/apk/res/android}'
PERMISSIONS={'android.permission.CAMERA','android.permission.WRITE_EXTERNAL_STORAGE'}

def validate_badging(text, manifest):
    declared={e.get(NS+'name') for e in manifest.findall('uses-permission')}
    if declared != PERMISSIONS:raise ValueError('unexpected declared permissions')
    if "sdkVersion:'10'" not in text or "targetSdkVersion:'10'" not in text:
        raise ValueError('APK SDK mismatch')
    for field,value in [('name',manifest.get('package')),('versionCode',manifest.get(NS+'versionCode')),('versionName',manifest.get(NS+'versionName'))]:
        if field+"='"+value+"'" not in text.splitlines()[0]:raise ValueError('APK identity mismatch')
    permissions=set(re.findall(r"^uses-permission: name='([^']+)'",text,re.M))
    implied=set(re.findall(r"^uses-implied-permission: name='([^']+)'",text,re.M))
    allowed_implied={'android.permission.READ_EXTERNAL_STORAGE'}
    if implied - allowed_implied:raise ValueError('unexpected implied permission')
    if implied and "uses-implied-permission: name='android.permission.READ_EXTERNAL_STORAGE' reason='requested WRITE_EXTERNAL_STORAGE'" not in text:
        raise ValueError('unexpected read-storage implication')
    if permissions != declared | implied:raise ValueError('APK permission mismatch')
    return {'declared':sorted(declared),'implied_by_aapt':sorted(implied)}

def source_hashes(root):
    files=[root/'app/AndroidManifest.xml',root/'config/modules.json',root/'config/build-profiles.json']
    for folder in ('core/src','io/src','camera-api/src','sony/src','app/src'):
        files.extend((root/folder).rglob('*.java'))
    files.extend(p for p in (root/'app/res').rglob('*') if p.is_file())
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
