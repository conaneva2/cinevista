#!/usr/bin/env python3
"""Build a no-CDN single HTML from separated, reviewed Studio sources."""
import base64, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'studio'/'grading'
core=(S/'grade-core.js').read_text();ui=(S/'ui.js').read_text();css=(S/'style.css').read_text();worker=(S/'render-worker.js').read_text()
def csp_hash(s): return "'sha256-"+base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()+"'"
script=core+'\n'+ui
csp="default-src 'none'; script-src "+csp_hash(script)+"; style-src "+csp_hash(css)+"; img-src blob: data:; worker-src blob:; child-src blob:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
html=(S/'template.html').read_text()
for key,value in {'CSP':csp,'CSS':css,'CORE':core,'WORKER':worker,'UI':ui}.items():html=html.replace('__'+key+'__',value)
(S/'index.html').write_text(html)
(ROOT/'studio'/'index.html').write_text(html)
(ROOT/'studio'/'CineVista_Studio_Realtime_0.2.html').write_text(html)
print('Built Studio Realtime:',len(html.encode()),'bytes')
