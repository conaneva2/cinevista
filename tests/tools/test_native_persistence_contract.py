"""Repository contract checks; no camera calls, emulated success, or hardware claims."""
import json
from pathlib import Path
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from evidence_contract import policy_errors, gate_errors
ROOT = Path(__file__).resolve().parents[2]

class NativePersistenceContractTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((ROOT / 'config/native-color-policy.json').read_text())
        self.gates = json.loads((ROOT / 'config/release-gates.json').read_text())
    def test_primary_requires_native_persistence(self):
        self.assertEqual(self.p['primary_delivery'], 'native-persistent')
    def test_realtime_sample_preview_not_removed(self):
        self.assertTrue(self.p['realtime_sample_preview_required'])
    def test_no_autostart_substitute(self):
        self.assertFalse(self.p['boot_autostart_substitute_allowed'])
        self.assertFalse(self.p['app_reapply_counts_as_persistence'])
    def test_current_implementation_not_misrepresented(self):
        self.assertEqual(policy_errors(ROOT,self.p),[])
    def test_software_and_runtime_transform_not_persistent(self):
        bs = {x['id']: x for x in self.p['backends']}
        self.assertEqual(bs['software-lut']['role'], 'secondary')
        self.assertEqual(bs['software-lut']['persists_after_native_reboot'], 'unsupported-without-app')
        self.assertIn(bs['sony-runtime-matrix-gamma']['persists_after_native_reboot'], ('unknown','verified','failed','unsupported'))
    def test_native_release_gates_remain_required_and_consistent(self):
        gs = {x['id']: x for x in self.gates['required']}
        for k in ('native-color-exit-retention', 'native-color-powercycle-without-app', 'native-color-scoped-restore', 'native-preview-model-validation'):
            self.assertIn(k,gs)
            if gs[k]['state']=='verified':self.assertEqual(gate_errors(ROOT,gs[k]),[])
    def test_previous_backend_decision_superseded(self):
        old = (ROOT / 'docs/adr/0010-realtime-software-look-primary.md').read_text()
        self.assertIn('ADR0011', old.splitlines()[0])
    def test_restricted_sources_not_included(self):
        rows = json.loads((ROOT / 'third_party/upstreams.lock.json').read_text())['upstreams']
        row = next(x for x in rows if x['id'] == 'film-studio-a7r2')
        self.assertFalse(row['included_code'])
        self.assertFalse(row['vendored'])
        self.assertIn('Noncommercial', row['license'])
    def test_studio_retains_honest_software_scope(self):
        template = (ROOT / 'studio/grading/template.html').read_text()
        self.assertIn('不能让相机在退出幕野、重启后原生拍照时自动生效', template)
        if not self.p['native_publish_implemented']:self.assertIn('发布器尚未完成', template)
    def test_no_lossless_conversion_claim(self):
        self.assertFalse(self.p['arbitrary_lut_lossless_native_conversion_claim_allowed'])

if __name__ == '__main__': unittest.main()
