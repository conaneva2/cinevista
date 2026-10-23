#!/usr/bin/env python3
"""Project-specific boundary checks, not a Java parser or complete API verifier.
Separate javac module compilations complement these cheap source checks.
"""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]

def validate(root: Path) -> list[str]:
    errors=[]
    cfg=json.loads((root/'config/modules.json').read_text())
    modules=cfg['modules']; classes={}; sources=[]
    for name,spec in modules.items():
        for p in (root/spec['src']).rglob('*.java'):
            text=p.read_text(encoding='utf-8')
            m=re.search(r'\bpackage\s+([\w.]+)\s*;',text)
            if not m: errors.append(f'{p.relative_to(root)}: missing package');continue
            fqn=m.group(1)+'.'+p.stem
            if fqn in classes: errors.append(f'duplicate type: {fqn}')
            classes[fqn]=name;sources.append((name,p,text,m.group(1)))
    visiting=set();done=set()
    def visit(name):
        if name in visiting:errors.append('module dependency cycle: '+name);return
        if name in done:return
        visiting.add(name)
        for dep in modules[name]['deps']:
            if dep not in modules:errors.append('unknown module dependency: '+dep)
            else:visit(dep)
        visiting.remove(name);done.add(name)
    for name in modules:visit(name)
    for name,spec in modules.items():
        if spec['kind'] not in ('desktop','test'):
            for dep in spec['deps']:
                if dep in modules and modules[dep]['kind'] in ('desktop','test'):
                    errors.append(name+': production dependency on desktop/test module '+dep)
    for key in ('android_order','host_order'):
        seen=set()
        for name in cfg[key]:
            if name not in modules or name in seen:
                errors.append(key+': unknown/duplicate module '+name);continue
            if set(modules[name]['deps'])-seen:errors.append(key+': dependency not built before '+name)
            seen.add(name)
    compositions=set(cfg.get('composition_roots',[]))
    for name,p,text,pkg in sources:
        rel=p.relative_to(root).as_posix()
        clean=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
        imports=re.findall(r'\bimport\s+(?:static\s+)?([\w.*]+)\s*;',clean)
        allowed=set(modules[name]['deps'])|{name}
        for imp in imports:
            targets={owner for fqn,owner in classes.items() if fqn==imp or (imp.endswith('.*') and fqn.rsplit('.',1)[0]==imp[:-2])}
            if targets-allowed:errors.append(f'{rel}: forbidden dependency {imp} -> {sorted(targets-allowed)}')
        for reference in re.findall(r'\borg\.cinevista\.[\w.$]+',clean):
            for fqn,owner in classes.items():
                if (reference==fqn or reference.startswith(fqn+'.')) and owner not in allowed:
                    errors.append(rel+': forbidden qualified dependency '+reference)
        if modules[name]['kind']=='portable' and re.search(r'\b(?:android\.|com\.sony\.)',clean):
            errors.append(rel+': portable module depends on platform')
        if name=='core' and re.search(r'\b(?:android\.|com\.sony\.|org\.cinevista\.(?:io|host|sony|camera|probe)\.|java\.(?:io|nio|awt|sql)\.)',clean):
            errors.append(rel+': domain must remain platform/IO independent')
        if name not in ('host','tests'):
            for bad in ('java.awt.','javax.imageio.','java.nio.file.','java.time.','java.util.stream.','androidx.','android.hardware.camera2.'):
                if bad in clean:errors.append(rel+': forbidden device dependency '+bad)
        if 'com.sony.' in text and name!='sony':errors.append(rel+': Sony private API names must stay in sony module')
        if name=='app' and 'org.cinevista.sony.' in text and rel not in compositions:
            errors.append(rel+': backend selection allowed only in composition root')
        if re.search(r'\bpackage\s+(?:android|com\.sony)\.',clean):errors.append(rel+': must not package platform implementation classes')
    from build_profiles import load, validate_sources
    try:
        validate_sources(root,[p for name,p,text,pkg in sources if name not in ('host','tests')],load(root))
    except (ValueError,KeyError,OSError) as exc:
        errors.append('reviewed build profile: '+str(exc))
    return errors

if __name__=='__main__':
    errors=validate(ROOT)
    for e in errors:print('FAIL',e)
    print(('FAIL' if errors else 'PASS')+' module boundaries (source checks; not full API compatibility).')
    raise SystemExit(bool(errors))
