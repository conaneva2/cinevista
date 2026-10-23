"""Artificial files test validation behavior only; never device evidence."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from evidence_contract import gate_errors, policy_errors, read_json
ROOT=Path(__file__).resolve().parents[2]

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.files=[self.write('test.apk',b'synthetic apk'),self.write('plan.json',b'synthetic plan')]
        self.binding={'model':'TEST-ONLY','firmware':'fixture','mode':'M','apk_sha256':self.files[0]['sha256'],'plan_sha256':self.files[1]['sha256']}
        self.data={'schema_version':1,'claim':'test-only','result':'passed','kind':'device','scope':'physical-device','binding':self.binding,'reviewer':'synthetic-test','observed_at':'fixture','procedure':'fixture only','artifacts':self.files}
    def write(self,name,data):
        (self.root/name).write_bytes(data);return {'path':name,'sha256':hashlib.sha256(data).hexdigest()}
    def gate(self):
        ref=self.write('report.json',json.dumps(self.data).encode());return {'id':'test-only','state':'verified','binding':self.binding,'evidence':[ref]}
    def test_consistent_fixture_accepted(self):self.assertEqual(gate_errors(self.root,self.gate()),[])
    def test_false_verified_rejected(self):self.assertTrue(gate_errors(self.root,{'id':'x','state':'verified','evidence':[]}))
    def test_empty_tampered_missing_artifact_rejected(self):
        for data in (b'',b'tampered'):
            gate=self.gate();(self.root/'test.apk').write_bytes(data);self.assertTrue(gate_errors(self.root,gate))
    def test_outside_path_and_symlink_rejected(self):
        gate=self.gate()
        for path in ('../outside.json',str(self.root/'report.json')):
            gate['evidence'][0]['path']=path;self.assertTrue(gate_errors(self.root,gate))
        (self.root/'link').symlink_to(ROOT/'PROJECT_STATUS.md');gate['evidence'][0]['path']='link';self.assertTrue(gate_errors(self.root,gate))
    def test_model_firmware_build_plan_mismatch(self):
        for field in ('model','firmware','apk_sha256','plan_sha256'):
            gate=self.gate();gate['binding']=dict(self.binding,**{field:'wrong'});self.assertTrue(gate_errors(self.root,gate))
    def test_host_cannot_certify_hardware(self):
        self.data['scope']='host';self.assertTrue(gate_errors(self.root,self.gate()))
    def test_missing_observation_metadata(self):
        del self.data['reviewer'];self.assertTrue(gate_errors(self.root,self.gate()))
    def test_claim_and_result_mismatch(self):
        self.data['result']='unknown';self.assertTrue(gate_errors(self.root,self.gate()))
    def test_duplicate_json_and_nonfinite_rejected(self):
        for text in ('{"a":1,"a":2}','{"a":NaN}'):
            (self.root/'bad.json').write_text(text)
            with self.assertRaises(ValueError):read_json(self.root/'bad.json')
    def test_implementation_cannot_self_assert(self):
        p=json.loads((ROOT/'config/native-color-policy.json').read_text());p['native_publish_implemented']=True
        self.assertTrue(policy_errors(self.root,p))
    def test_historical_fixture_stays_unknown(self):
        p=json.loads((ROOT/'tests/fixtures/v0.6/native-color-policy.json').read_text())
        self.assertFalse(p['native_publish_implemented']);self.assertFalse(p['native_preview_model_calibrated'])
        self.assertEqual(p['known_native_profiles'],[]);self.assertIsNone(p['target_runtime']['firmware'])
        gs=json.loads((ROOT/'tests/fixtures/v0.6/release-gates.json').read_text())
        self.assertTrue(all(g['state']=='unknown' and g['evidence']==[] for g in gs['required']))
    def test_implemented_can_advance_with_matched_host_evidence(self):
        p=json.loads((ROOT/'config/native-color-policy.json').read_text());p['native_publish_implemented']=True
        source=self.write('source.txt',b'synthetic implementation');binding={'source_sha256':source['sha256']}
        self.data.update(claim='native-publish-implementation',kind='implementation',scope='host',binding=binding,artifacts=[source])
        ref=self.write('implementation.json',json.dumps(self.data).encode())
        p['claims']={'native-publish-implementation':{'report':ref,'binding':binding}}
        self.assertEqual(policy_errors(self.root,p),[])
