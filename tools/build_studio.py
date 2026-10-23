#!/usr/bin/env python3
"""Package the offline editor as one HTML file, with hashed inline assets and no network dependencies."""
from pathlib import Path
import hashlib,base64,re,argparse
ROOT=Path(__file__).resolve().parents[1]
def digest(text):return base64.b64encode(hashlib.sha256(text.encode('utf-8')).digest()).decode('ascii')
def build(dest):
    s=ROOT/'studio';css=(s/'studio.css').read_text();script=(s/'look-core.js').read_text()+'\n'+(s/'studio.js').read_text()
    html=(s/'index.html').read_text()
    html=html.replace('<link rel="stylesheet" href="studio.css">','<style>'+css+'</style>')
    html=html.replace('<script src="look-core.js"></script><script src="studio.js"></script>','<script>'+script+'</script>')
    html=html.replace("script-src 'self'; style-src 'self';", "script-src 'sha256-"+digest(script)+"'; style-src 'sha256-"+digest(css)+"';")
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')
    return dest
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'build/studio/CineVista_Studio_0.1.html');a=p.parse_args();print(build(a.output))
