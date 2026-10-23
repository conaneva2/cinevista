"""Shared resource and deliberately limited host schematic contracts."""
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import preview_camera_ui as preview


class CameraUiPreviewTests(unittest.TestCase):
    def test_shared_layout_actions_bound_once(self):
        tree = ET.parse(ROOT / preview.LAYOUT).getroot()
        java = (ROOT / 'app/src/org/cinevista/probe/MainActivity.java').read_text()
        ids = [n.attrib[preview.A + 'id'].split('/')[-1]
               for n in tree.iter('Button')]
        self.assertEqual(6, len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        for name in ids:
            self.assertEqual(1, java.count('bind(R.id.' + name + ','))
        self.assertIn('setContentView(R.layout.probe_home)', java)

    def test_schematic_uses_actual_text_and_warns(self):
        html = preview.render(ROOT)
        self.assertIn('读取设备与显示信息', html)
        self.assertIn('不是相机截图', html)
        self.assertIn('不写入固件或持久参数', html)
        self.assertNotIn('https://', html)

    def test_text_escaped(self):
        node = ET.Element('TextView', {preview.A+'text': '<script>alert(1)</script>'})
        self.assertIn('&lt;script&gt;', preview.node_html(node))

    def test_unsupported_view_fails(self):
        with self.assertRaises(ValueError):
            preview.node_html(ET.Element('SurfaceView'))

    def test_resource_reference_not_silently_rendered(self):
        node = ET.Element('TextView', {preview.A+'text': '@string/title'})
        with self.assertRaises(ValueError):
            preview.node_html(node)


class NativeLayoutContracts(unittest.TestCase):
    def test_top_bar_before_isolated_surface(self):
        root = ET.parse(ROOT / 'app/res/layout/probe_viewfinder.xml').getroot()
        self.assertEqual('vertical', root.get(preview.A+'orientation'))
        self.assertEqual('@+id/viewfinder_header', root[0].get(preview.A+'id'))
        stage = root[1]
        self.assertEqual('@+id/viewfinder_stage', stage.get(preview.A+'id'))
        self.assertEqual('true', stage.get(preview.A+'clipChildren'))
        self.assertEqual(1, len(list(root.iter('SurfaceView'))))
        self.assertEqual('SurfaceView', stage[0].tag)
        self.assertEqual(3, len(list(root.iter('Button'))))

    def test_layout_strings_have_chinese_defaults(self):
        strings = {n.get('name'): n.text or '' for n in
                   ET.parse(ROOT/'app/res/values/strings.xml').getroot()}
        for layout in ('probe_home.xml', 'probe_viewfinder.xml'):
            for n in ET.parse(ROOT/'app/res/layout'/layout).getroot().iter():
                ref = n.get(preview.A+'text')
                if ref:
                    self.assertTrue(ref.startswith('@string/'), ref)
                    value = strings[ref.split('/')[-1]]
                    self.assertTrue(any('\u4e00' <= c <= '\u9fff' for c in value), value)

    def test_focus_selector_and_navigation(self):
        selector = ET.parse(ROOT/'app/res/drawable/control_background.xml').getroot()
        self.assertTrue(any(n.get(preview.A+'state_focused') == 'true' for n in selector))
        root = ET.parse(ROOT/'app/res/layout/probe_viewfinder.xml').getroot()
        buttons = list(root.iter('Button'))
        ids = {n.get(preview.A+'id').replace('@+id/', '@id/') for n in buttons}
        for n in buttons:
            self.assertIn(n.get(preview.A+'nextFocusLeft'), ids)
            self.assertIn(n.get(preview.A+'nextFocusRight'), ids)
