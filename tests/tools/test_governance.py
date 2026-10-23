"""Mutation checks show that selected guardrails actually reject invalid changes."""
import unittest,tempfile,shutil,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import architecture_check,policy_check,release_check
class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'repo'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('build','.git','.local','runs','evidence','__pycache__','examples'))
    def tearDown(self):self.tmp.cleanup()
    def inject(self,rel,line):
        p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(line)
    def test_valid_boundaries(self):self.assertEqual([],architecture_check.validate(self.root))
    def test_domain_android_rejected(self):
        self.inject('core/src/org/cinevista/core/Bad.java','package org.cinevista.core; import android.app.Activity; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))
    def test_domain_io_rejected(self):
        self.inject('core/src/org/cinevista/core/Bad.java','package org.cinevista.core; import java.io.File; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))
    def test_private_api_in_ui_rejected(self):
        self.inject('app/src/org/cinevista/probe/Bad.java','package org.cinevista.probe; class Bad { String name="com.sony.scalar.hardware.CameraEx"; }')
        self.assertTrue(architecture_check.validate(self.root))
    def test_desktop_dependency_rejected(self):
        self.inject('sony/src/org/cinevista/sony/Bad.java','package org.cinevista.sony; import javax.imageio.ImageIO; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))
    def test_cycle_rejected(self):
        p=self.root/'config/modules.json';d=json.loads(p.read_text());d['modules']['core']['deps']=['app'];p.write_text(json.dumps(d))
        self.assertTrue(architecture_check.validate(self.root))
    def test_valid_policy(self):self.assertEqual([],policy_check.validate(self.root))
    def test_unpinned_action_rejected(self):
        p=self.root/'.github/workflows/ci.yml';p.write_text(p.read_text().replace('11bd71901bbe5b1630ceea73d27597364c9af683','main'))
        self.assertTrue(policy_check.validate(self.root))
    def test_private_key_rejected(self):
        self.inject('release.jks','not a key');self.assertTrue(policy_check.validate(self.root))
    def test_unsupported_release_blocked(self):self.assertTrue(release_check.blockers(self.root))
    def test_core_sibling_import_rejected(self):
        self.inject('core/src/org/cinevista/core/Bad.java','package org.cinevista.core; import org.cinevista.io.Filesafe; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))
    def test_production_code_cannot_use_modern_api(self):
        self.inject('io/src/org/cinevista/io/Bad.java','package org.cinevista.io; import java.nio.file.Files; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))

class OptionalReleaseTests(unittest.TestCase):
    def test_enabled_optional_is_not_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'config').mkdir()
            for n in ('release-gates.json','native-color-policy.json','toolchain.lock.json'):
                shutil.copyfile(ROOT/'config'/n,root/'config'/n)
            path=root/'config/release-gates.json';d=json.loads(path.read_text())
            d['optional_features'][0]['enabled']=True;path.write_text(json.dumps(d))
            self.assertTrue(any('software-lut-camera-roundtrip' in x for x in release_check.blockers(root)))
    def test_removed_required_gate_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'config').mkdir()
            for n in ('release-gates.json','native-color-policy.json','toolchain.lock.json'):
                shutil.copyfile(ROOT/'config'/n,root/'config'/n)
            path=root/'config/release-gates.json';d=json.loads(path.read_text());d['required'].pop();path.write_text(json.dumps(d))
            self.assertIn('required gate set changed or duplicated',release_check.blockers(root))


class AdditionalBoundaryTests(unittest.TestCase):
    setUp=GovernanceTests.setUp
    tearDown=GovernanceTests.tearDown
    inject=GovernanceTests.inject
    def test_portable_io_android_rejected(self):
        self.inject('io/src/org/cinevista/io/Bad.java','package org.cinevista.io; import android.content.Context; class Bad {}')
        self.assertTrue(architecture_check.validate(self.root))
    def test_qualified_reference_cannot_skip_dependency_graph(self):
        self.inject('sony/src/org/cinevista/sony/Bad.java','package org.cinevista.sony; class Bad { org.cinevista.host.Main forbidden; }')
        self.assertTrue(architecture_check.validate(self.root))
    def test_production_cannot_add_desktop_dependency(self):
        p=self.root/'config/modules.json';d=json.loads(p.read_text());d['modules']['sony']['deps'].append('host');p.write_text(json.dumps(d))
        self.assertTrue(architecture_check.validate(self.root))
    def test_invalid_build_order_rejected(self):
        p=self.root/'config/modules.json';d=json.loads(p.read_text());d['android_order'].reverse();p.write_text(json.dumps(d))
        self.assertTrue(architecture_check.validate(self.root))

if __name__=='__main__':unittest.main()
