"""Exact reviewed exceptions. Empty production allowlists retain Java probe policy.
Not an ELF/linker audit: native loading and firmware qualification remain T05.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
ROOT = Path(__file__).resolve().parents[1]
WRITE_SYMBOLS = ('Backup_write', 'Backup_sync_all')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def reviewed(row):
    if not re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')):
        raise ValueError('missing pinned SHA256')
    if not re.fullmatch('[0-9a-f]{40}', row.get('source_commit', '')) or not row.get('license') or not row.get('review'):
        raise ValueError('missing source/license/review')

def load(root=ROOT):
    config = json.loads((root/'config/build-profiles.json').read_text())
    profile = config['profiles'][config['active']]
    for row in profile['native_libraries'] + profile['source_exceptions']:
        reviewed(row)
        review = (root/row['review']).resolve()
        if not review.is_relative_to(root.resolve()) or not review.is_file() or not review.stat().st_size:
            raise ValueError('missing local review')
    return profile

def validate_archive(files, profile):
    rows = profile['native_libraries']
    expected = {}
    for row in rows:
        reviewed(row)
        path = row['path'];parts = PurePosixPath(path).parts
        if len(parts) != 3 or parts[0] != 'lib' or parts[1] not in ('armeabi', 'armeabi-v7a') or not re.fullmatch(r'lib[\w-]+\.so', parts[2]):
            raise ValueError('unapproved native ABI/path')
        if path in expected:raise ValueError('duplicate native entry')
        expected[path] = row['sha256']
    actual = {p:digest(b) for p,b in files.items() if p.startswith('lib/')}
    if actual != expected:
        raise ValueError('native archive differs from exact reviewed allowlist')

def validate_sources(root, sources, profile):
    exceptions = {x['path']:x for x in profile['source_exceptions']}
    for p in sources:
        used = {s for s in WRITE_SYMBOLS if s in p.read_text()}
        if not used:continue
        row = exceptions.get(p.relative_to(root).as_posix())
        if not row:raise ValueError('unapproved Backup source: '+str(p))
        reviewed(row)
        if not row['path'].startswith('sony/src/') or digest(p.read_bytes()) != row['sha256'] or used != set(row['symbols']):
            raise ValueError('Backup source exception mismatch')
