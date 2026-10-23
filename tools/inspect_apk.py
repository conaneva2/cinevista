#!/usr/bin/env python3
"""Inspect actual DEX class definitions, not string literals of Sony reflection names."""
import struct,zipfile,sys,json,pathlib

from build_profiles import load, validate_archive

def inspect(path):
    from launcher_contract import inspect_launcher
    launcher = inspect_launcher(path)
    with zipfile.ZipFile(path) as z:
        assert 'AndroidManifest.xml' in z.namelist(),'missing manifest'
        assert 'classes.dex' in z.namelist(),'missing DEX'
        assert len(z.namelist()) == len(set(z.namelist())), 'duplicate ZIP entries'
        validate_archive({x:z.read(x) for x in z.namelist() if x.startswith('lib/')}, load())
        d=z.read('classes.dex')
        assert d[:8]==b'dex\n035\0','unexpected DEX version for API 10'
        def u(p): return struct.unpack_from('<I',d,p)[0]
        so,to=u(60),u(68); count,off=u(96),u(100)
        def string(index):
            p=u(so+index*4)
            while d[p]&128:p+=1
            p+=1
            return d[p:d.index(0,p)].decode('utf-8')
        classes=[]
        for i in range(count):
            typ=u(off+i*32);desc=string(u(to+typ*4));classes.append(desc)
        assert classes and all(x.startswith(('Lorg/cinevista/core/','Lorg/cinevista/io/','Lorg/cinevista/camera/','Lorg/cinevista/sony/','Lorg/cinevista/probe/')) for x in classes),classes
        return {'dex_version':'035','defined_classes':classes,'sony_implementation_classes_packaged':False,'device_execution_verified':False,'launcher_contract':launcher}
if __name__=='__main__': print(json.dumps(inspect(sys.argv[1]),indent=2))
