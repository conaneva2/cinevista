"""Host-side evidence consistency, not proof that a claimed experiment happened.
Maintainer review of real observations remains mandatory. No device success fixtures
are installed in production config.
"""
from pathlib import Path
import hashlib
import json
import re

STATES = {'unknown', 'declared', 'probed', 'verified', 'failed', 'unsupported'}

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:raise ValueError('duplicate JSON key')
        result[key] = value
    return result

def read_json(path):
    if path.stat().st_size > 1024 * 1024:raise ValueError('oversized evidence JSON')
    return json.loads(path.read_text(), object_pairs_hook=_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('non-finite JSON')))

def local_file(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError('evidence must be a repository-relative path')
    path = (root/value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file() or path.stat().st_size == 0:
        raise ValueError('missing, empty or escaping evidence file')
    return path

def artifact(root, row):
    if set(row) != {'path', 'sha256'}:raise ValueError('artifact requires path and sha256')
    path = local_file(root, row['path'])
    if not re.fullmatch('[0-9a-f]{64}', row['sha256']) or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('artifact hash mismatch')
    return row['sha256']

def report(root, ref, claim, binding, kind):
    artifact(root, ref)
    data = read_json(local_file(root, ref['path']))
    if data.get('schema_version') != 1 or data.get('claim') != claim or data.get('result') != 'passed' or data.get('kind') != kind:
        raise ValueError('evidence claim/result/kind mismatch')
    if not binding or data.get('binding') != binding:raise ValueError('evidence identity mismatch')
    if not data.get('reviewer') or not data.get('observed_at') or not data.get('procedure'):
        raise ValueError('evidence lacks observation/review metadata')
    artifacts = data.get('artifacts', [])
    if not artifacts:raise ValueError('evidence lacks artifacts')
    hashes = {artifact(root, row) for row in artifacts}
    for field in ('source_sha256',) if kind == 'implementation' else ('apk_sha256', 'plan_sha256'):
        if binding.get(field) not in hashes:raise ValueError('binding has no matching artifact: '+field)
    if kind != 'implementation':
        if not binding.get('model') or not binding.get('firmware') or not binding.get('mode'):
            raise ValueError('device identity/mode incomplete')
        if data.get('scope') != 'physical-device':raise ValueError('host report cannot certify device')
    return data

def gate_errors(root, gate):
    try:
        if gate['state'] not in STATES:raise ValueError('invalid state')
        if gate['state'] != 'verified':return [gate['id']+': '+gate['state']]
        refs = gate.get('evidence', [])
        if not refs:raise ValueError('missing evidence')
        host_gates={'production-package-owner','sdk-build-and-signature','license-and-assets-review','production-signing-approval'}
        kind='implementation' if gate['id'] in host_gates else 'device'
        for ref in refs:report(root, ref, gate['id'], gate.get('binding'), kind)
        return []
    except (ValueError, TypeError, KeyError, OSError, RecursionError) as exc:
        return [str(gate.get('id'))+': invalid evidence: '+str(exc)]

def policy_errors(root, policy):
    errors=[]
    required={}
    if policy['native_publish_implemented']:required['native-publish-implementation']='implementation'
    if policy['native_preview_model_calibrated']:required['native-preview-model-validation']='device'
    runtime=policy['target_runtime']
    if runtime['firmware'] is not None or runtime['sdk_int'] is not None or runtime['external_report_independently_verified']:
        required['target-runtime-read']='device'
    for backend in policy['backends']:
        if backend['persists_after_native_reboot'] == 'verified':required[backend['id']+'-powercycle']='device'
    for claim,kind in required.items():
        try:
            item=policy.get('claims', {})[claim]
            data=report(root,item['report'],claim,item['binding'],kind)
            if kind == 'device' and (item['binding'].get('model') != runtime['model'] or item['binding'].get('firmware') != runtime['firmware']):
                raise ValueError('claim target mismatch')
            if claim == 'target-runtime-read' and (type(runtime['sdk_int']) is not int or runtime['sdk_int'] < 1 or data.get('sdk_int') != runtime['sdk_int']):
                raise ValueError('runtime SDK evidence mismatch')
        except (ValueError,TypeError,KeyError,OSError,RecursionError) as exc:errors.append(claim+': '+str(exc))
    for profile in policy['known_native_profiles']:
        try:
            report(root,profile['report'],'native-profile',profile['binding'],'device')
            if profile['binding']['model'] != runtime['model'] or profile['binding']['firmware'] != runtime['firmware']:
                raise ValueError('profile target mismatch')
        except (ValueError,TypeError,KeyError,OSError,RecursionError) as exc:errors.append('native-profile: '+str(exc))
    return errors
