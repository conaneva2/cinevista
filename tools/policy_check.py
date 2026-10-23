#!/usr/bin/env python3
"""Checks the repository's explicit policy files and immutable upstream anchors."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=('README.md','LICENSE','CONTRIBUTING.md','SECURITY.md','PROJECT_STATUS.md','CHANGELOG.md','TODO.md','docs/README.md','docs/USER_GUIDE.md','docs/DOCUMENTATION.md','docs/GITEE.md','config/documentation.json','.gitee/ISSUE_TEMPLATE.zh-CN.md','.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md','config/modules.json','config/toolchain.lock.json','third_party/upstreams.lock.json','.github/pull_request_template.md','.github/workflows/ci.yml','docs/01_REUSE_AUDIT.md','docs/02_ARCHITECTURE.md','docs/03_ENVIRONMENT.md','docs/04_WORKFLOW.md','docs/05_TESTING.md')
def validate(root):
    errors=[]
    for name in REQUIRED:
        if not (root/name).is_file():errors.append('missing '+name)
    upstream=root/'third_party/upstreams.lock.json'
    if upstream.exists():
        for row in json.loads(upstream.read_text())['upstreams']:
            if row['decision'] in ('adopt','adapt','reference') and row.get('commit') is not None and not re.fullmatch('[0-9a-f]{40}',row['commit']):errors.append('unpinned upstream '+row['id'])
            if row.get('included_code') and (not row.get('license_file') or not (root/row['license_file']).is_file()):errors.append('included code missing license '+row['id'])
            if row.get('vendored') and not row.get('sha256_manifest'):errors.append('vendored code missing byte-level manifest '+row['id'])
    for p in (root/'.github/workflows').glob('*.yml'):
        text=p.read_text()
        for ownerrepo,ref in re.findall(r'uses:\s*([\w-]+/[\w.-]+)@([^\s#]+)',text):
            if not re.fullmatch('[0-9a-f]{40}',ref):errors.append(p.name+': action not pinned '+ownerrepo)
        if re.search(r'^\s*pull_request_target\s*:',text,re.M):errors.append(p.name+': untrusted PR elevated workflow forbidden')
        if 'continue-on-error: true' in text:errors.append(p.name+': must not hide failing checks')
        if re.search(r'\$\{\{\s*github\.event\.(?:issue|pull_request).*\}\}',text):errors.append(p.name+': avoid event interpolation in workflow')
    ignored={'build','.git','.local','history','__pycache__'}
    for p in root.rglob('*'):
        if not p.is_file() or ignored.intersection(p.relative_to(root).parts):continue
        if p.suffix.lower() in ('.jks','.keystore','.p12','.pk8','.ttf','.otf'):errors.append('private key/font must not ship: '+str(p.relative_to(root)))
    return errors
if __name__=='__main__':
    errors=validate(ROOT)
    for e in errors:print('FAIL',e)
    print(('FAIL' if errors else 'PASS')+' project policy; separate release/device gates still apply.')
    raise SystemExit(bool(errors))
