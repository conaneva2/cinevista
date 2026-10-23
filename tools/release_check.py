#!/usr/bin/env python3
"""Validate evidence bindings; host green never authorizes a release."""
import sys
from pathlib import Path
from evidence_contract import read_json, gate_errors, policy_errors
ROOT=Path(__file__).resolve().parents[1]
REQUIRED = {
    'production-package-owner','sdk-build-and-signature','runtime-api-audit',
    'target-model-install','source-file-safety','wide-framing-calibration',
    'anamorphic-content-transform','color-capability-mapping',
    'license-and-assets-review','production-signing-approval',
    'native-color-exit-retention','native-color-powercycle-without-app',
    'native-color-scoped-restore','native-preview-model-validation'
}
def blockers(root):
    try:
        status=read_json(root/'config/release-gates.json')
        errors=[]
        ids=[g['id'] for g in status['required']]
        if set(ids)!=REQUIRED or len(ids)!=len(REQUIRED):errors.append('required gate set changed or duplicated')
        for gate in status['required']:errors.extend(gate_errors(root,gate))
        optional=status['optional_features']
        if len({g['id'] for g in optional})!=len(optional):errors.append('duplicate optional feature')
        for gate in optional:
            if type(gate.get('enabled')) is not bool:errors.append(gate['id']+': explicit enabled boolean required')
            elif gate['enabled']:errors.extend(gate_errors(root,gate))
        errors.extend(policy_errors(root,read_json(root/'config/native-color-policy.json')))
        lock=read_json(root/'config/toolchain.lock.json')
        if not lock.get('qualification_complete'):errors.append('toolchain: not fully qualified/locked')
        return errors
    except (ValueError,KeyError,TypeError,OSError,RecursionError) as exc:
        return ['invalid release contract: '+str(exc)]
if __name__=='__main__':
    errors=blockers(ROOT)
    for e in errors:print('BLOCKED',e)
    print('Release NOT ready.' if errors else 'Machine consistency gates passed; human evidence review still required.')
    sys.exit(2 if errors else 0)
