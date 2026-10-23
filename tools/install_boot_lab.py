#!/usr/bin/env python3
"""Reproduce bounded installation/startup control paths on the host only.

Requires already-extracted, hash-pinned local firmware sources and original APK.
No camera discovery, driver creation, USB, ADB, sockets or firmware modifications.
Run: source .local/env.sh; .local/connection/venv/bin/python tools/install_boot_lab.py
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from unittest.mock import patch

from compat_lab.inputs import load, digest, verify_inputs
from compat_lab.environment import Environment, INSTALL, SSBOOT
from compat_lab.vm import JavaFault, PowerCut, Unsupported, Obj
from launcher_contract import sdk_aapt, _run, _manifest_icons

ROOT = Path(__file__).resolve().parents[1]


def apk_icon(config):
    apk = ROOT / config['apk']; aapt = sdk_aapt()
    manifest = _run(aapt, 'dump', 'xmltree', apk, 'AndroidManifest.xml')
    ids = _manifest_icons(manifest)
    if len(ids) != 1: raise Unsupported('fixture requires exactly one app icon')
    # Explicitly reject Activity icon override; this fixture follows app fallback.
    element = None
    for line in manifest.splitlines():
        m = re.match(r'\s*E: (\S+) ', line)
        if m: element = m[1]
        if 'android:icon(' in line and element != 'application':
            raise Unsupported('fixture does not support component icon override')
    resource = _run(aapt, 'dump', '--values', 'resources', apk)
    paths = set()
    lines = resource.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'\s*resource 0x%08x ' % ids[0], line):
            match = re.fullmatch(r'\s*\(string(?:8|16)\) "([^"]+)"', lines[i + 1])
            if not match: raise Unsupported('unsupported resource alias')
            paths.add(match[1])
    if len(paths) != 1: raise Unsupported('ambiguous icon configuration')
    path = paths.pop()
    xml = _run(aapt, 'dump', 'xmltree', apk, path)
    root = re.search(r'^\s*E: ([\w-]+) ', xml, re.M)
    if root is None: raise Unsupported('missing XML root')
    return {'apk_sha256': digest(apk), 'icon_id': ids[0], 'icon_path': path, 'xml_root': root[1],
            'manifest': manifest, 'icon_xml': xml, 'activity_icon': 'inherited application icon',
            'aapt': str(aapt), 'aapt_sha256': digest(aapt)}


def installer_scenarios(config):
    # Import only a pinned local Python library. No cli/driver constructors.
    sys.path.insert(0, str(ROOT / config['pmca_root']))
    from pmca import installer
    from pmca.usb.sony import RequestMessage
    def request(endpoint, body):
        return RequestMessage(installer._buildRequest(endpoint, 'application/json', json.dumps(body).encode('ascii')))
    def progress(percent):
        return request('/task/progress', {'status': 1, 'status text': 'Installing', 'percent': percent, 'total size': (ROOT/config['apk']).stat().st_size})
    class FakeCamera:
        def __init__(self, messages): self.messages = iter(messages); self.events = []
        def emptyBuffer(self): self.events.append('emptyBuffer')
        def sendInit(self): self.events.append('sendInit')
        def sendRequest(self, data):
            self.events.append('synthetic_task_start')
            return b'REST/1.0 200 OK\r\n\r\n{"resultCode":0,"message":"fixture"}'
        def receive(self):
            item = next(self.messages)
            if isinstance(item, Exception): raise item
            return item
        def sendEnd(self): self.events.append('sendEnd')
    scenarios = []
    for name, messages, expected in (
        ('transport_interruption_before_progress', [OSError('injected receive failure')], 'OSError'),
        ('transport_interruption_after_100', [progress(100), OSError('injected receive failure')], 'OSError'),
        ('transport_success_complete', [progress(100), request('/task/complete', {'resultCode':0,'message':'fixture'})], 0),
        ('transport_failure_complete', [progress(100), request('/task/complete', {'resultCode':1,'message':'fixture'})], 1)):
        fake = FakeCamera(messages); percentages = []
        try:
            result = installer.install(fake, 'offline.invalid', 0, b'synthetic xpd, no APK transfer', lambda s: percentages.append(s.percent))
            actual = result.code
        except OSError: actual = 'OSError'
        if actual != expected or fake.events.count('sendEnd') != (0 if expected == 'OSError' else 1):
            raise AssertionError('installer scenario mismatch: ' + name)
        scenarios.append({'name':name, 'scope':'real PMCA control loop; synthetic transport only; no APK installation',
                          'expected':expected, 'actual':actual, 'passed':True, 'progress':percentages, 'events':fake.events})
    return scenarios


def run_lab(config, output):
    methods, hierarchy = load(ROOT, config)
    icon = apk_icon(config)
    (output/'apk-manifest.txt').write_text(icon.pop('manifest'))
    (output/'apk-icon.xmltree.txt').write_text(icon.pop('icon_xml'))
    rows = []
    def scenario(name, action, state=None, fault=None, expected=None, check=None, png=False):
        env = Environment(methods, hierarchy, state, fault, 'png_control' if png else icon['xml_root'], icon['icon_id'])
        before = env.snapshot(); actual = None
        try:
            returned = action(env)
            actual = 'return'
            if isinstance(returned, Obj): returned = {'type': returned.kind}
        except JavaFault as exc: actual = exc.kind; returned = str(exc)
        except PowerCut as exc: actual = 'injected_power_cut'; returned = str(exc)
        passed = actual == (expected or 'return') and (check is None or bool(check(env)))
        row = {'name':name, 'scope':'restricted firmware-method replay with explicit adapters', 'fault':fault,
               'expected':expected or 'return', 'actual':actual, 'return':returned, 'passed':passed,
               'state_before':before, 'state_after':env.snapshot(), 'events':env.events,
               'external_adapters':sorted(env.adapters), 'trace_file':name+'.trace.json', 'instructions':len(env.vm.trace),
               'held_monitor_count':sum(env.vm.monitors.values())}
        (output/row['trace_file']).write_text(json.dumps(env.vm.trace, ensure_ascii=False, indent=2)+'\n')
        (output/(name+'.snapshot.json')).write_text(json.dumps(env.snapshot(),indent=2)+'\n')
        rows.append(row)
        if not passed: raise AssertionError('scenario failed: ' + name)
        return env.snapshot()
    # The original compiled APK supplies its resource ID and XML root. The class
    # dispatch and cast are executed from the selected firmware methods.
    for n in (1, 2):
        scenario('original_icon_fresh_process_'+str(n), lambda e:e.icon(),
                 expected='Ljava/lang/ClassCastException;',
                 check=lambda e: any(t['offset']=='bc' and 'java_fault' in t for t in e.vm.trace))
    scenario('bitmap_type_control', lambda e:e.icon(), png=True)
    created = scenario('install_stamp_create', lambda e:e.stamp(), check=lambda e:INSTALL in e.state['files'])
    scenario('install_stamp_existing', lambda e:e.stamp(), state=created,
             check=lambda e:not any(x['event']=='file_create' for x in e.events))
    scenario('install_stamp_io_failure', lambda e:e.stamp(), fault='create_io',
             check=lambda e:INSTALL not in e.state['files'] and any(x.get('message')=='createInstallStamp failed' for x in e.events))
    incomplete = dict(created, incomplete=['org.cinevista.probe'], temporary=['synthetic-vmdl.tmp'])
    def count(env, event): return sum(x['event']==event for x in env.events)
    def sync_result(env): return next((x['value'] for x in env.events if x['event']=='sync_return'), None)
    scenario('resume_other_mode', lambda e:e.resume(7), state=incomplete,
             check=lambda e:count(e,'settings_read_stub')==0 and INSTALL in e.state['files'])
    scenario('resume8_incomplete_cleanup', lambda e:e.resume(), state=incomplete,
             check=lambda e:count(e,'cleanup_failed_package_stub')==1 and INSTALL not in e.state['files'] and sync_result(e)==1)
    no_marker = dict(incomplete, files=[])
    scenario('resume8_without_marker', lambda e:e.resume(), state=no_marker,
             check=lambda e:count(e,'cleanup_failed_package_stub')==0 and e.state['incomplete']==['org.cinevista.probe'])
    scenario('resume8_scan_returns_false', lambda e:e.resume(), state=incomplete, fault='scan_false',
             check=lambda e:sync_result(e)==0 and INSTALL not in e.state['files'])
    scenario('resume8_missing_directory', lambda e:e.resume(), state=dict(incomplete, dirs=['/data/app']),
             check=lambda e:sync_result(e)==0 and INSTALL not in e.state['files'])
    retained = scenario('resume8_marker_delete_false', lambda e:e.resume(), state=incomplete, fault='delete_false',
             check=lambda e:sync_result(e)==1 and INSTALL in e.state['files'])
    scenario('resume8_after_delete_failure_restart', lambda e:e.resume(), state=retained,
             check=lambda e:count(e,'cleanup_temporary_stub')==1 and INSTALL not in e.state['files'])
    cut = scenario('resume8_power_cut_before_delete', lambda e:e.resume(), state=incomplete, fault='cut_before_delete',
                   expected='injected_power_cut', check=lambda e:INSTALL in e.state['files'])
    # Reload the written snapshot, not the in-memory objects or monitor state.
    cut = json.loads((output/'resume8_power_cut_before_delete.snapshot.json').read_text())
    scenario('resume8_after_power_cut_restart', lambda e:e.resume(), state=cut,
             check=lambda e:count(e,'cleanup_temporary_stub')==1 and INSTALL not in e.state['files'])
    for fault in ('read_io', 'write_io'):
        scenario('resume8_'+fault, lambda e:e.resume(), state=incomplete, fault=fault,
                 expected='Ljava/io/IOException;', check=lambda e:INSTALL in e.state['files'] and sum(e.vm.monitors.values())==0)
    scenario('resume8_binder_remote_failure', lambda e:e.resume(), state=incomplete, fault='binder_remote',
             check=lambda e:count(e,'settings_read_stub')==0 and INSTALL in e.state['files'])
    scenario('resume8_firmware_marker', lambda e:e.resume(), state=dict(created, files=[SSBOOT]),
             check=lambda e: any(x.get('path')=='/system/app' and x.get('parse_flags')==65 for x in e.events) and SSBOOT not in e.state['files'])
    scenario('sync_default_paths', lambda e:e.sync(e.pm, 0), state=created,
             check=lambda e:sync_result(e)==1 and count(e,'scan_directory_stub')==2)
    rows.extend(installer_scenarios(config))
    verify_inputs(ROOT, config)
    return {'schema':'cinevista.install-boot-lab-result/1', 'created_utc':datetime.now(timezone.utc).isoformat(),
            'device_access':False, 'full_android_boot':False, 'original_apk_executed':False,
            'python':sys.version, 'input_hashes_verified_before_and_after':True,
            'implementation_sha256':{str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__).resolve(), *sorted((ROOT/'tools/compat_lab').glob('*.py'))]},
            'source_lock_sha256':digest(ROOT/'config/install-boot-lab.lock.json'), 'apk':icon,
            'boundary':'Selected smali control flow only. External File/Settings/scanner/Binder/graphics services are host adapters. PMCA gets fake transport. No claim of physical bootloop reproduction.',
            'unsupported':'Added-package broadcast/thread branch, actual APK scan/install, child drawable inflation, native backup, scheduler, power/SSB and recovery are not modelled; unknown calls stop.',
            'scenario_count':len(rows), 'passed':all(x['passed'] for x in rows), 'scenarios':rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = args.output or ROOT/'.local/compat-lab'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = output.resolve()
    if not output.is_relative_to((ROOT/'.local/compat-lab').resolve()):
        parser.error('output must be inside .local/compat-lab')
    output.mkdir(parents=True, exist_ok=False)
    config = json.loads((ROOT/'config/install-boot-lab.lock.json').read_text())
    # Network attempt is a hard lab failure, not a simulated firmware exception.
    try:
        with patch('socket.socket', side_effect=Unsupported('network forbidden')):
            report = run_lab(config, output)
    except Exception as exc:
        (output/'failure.json').write_text(json.dumps({'passed':False,'exception':type(exc).__name__,'detail':str(exc)},indent=2)+'\n')
        raise
    (output/'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'output':str(output),'scenarios':report['scenario_count'],'passed':report['passed'],
                      'full_android_boot':False,'device_access':False},ensure_ascii=False))


if __name__ == '__main__': main()
