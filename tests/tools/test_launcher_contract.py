"""Packed resource regressions: use real aapt, never camera communication."""
import base64
import os
from pathlib import Path
import subprocess
import sys
import struct
import tempfile
import unittest
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from launcher_contract import inspect_launcher, _manifest_icons, _icon_paths

SDK = Path(os.environ.get('ANDROID_SDK_ROOT', '/missing-sdk'))
AAPT = SDK / 'build-tools/30.0.3/aapt'
JAR = Path(os.environ.get('CINEVISTA_ANDROID10_JAR', str(SDK / 'platforms/android-10/android.jar')))
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')

@unittest.skipUnless(AAPT.is_file() and JAR.is_file(), 'real SDK required for packed-resource integration tests')
class LauncherContractTests(unittest.TestCase):
    def package(self, icon=PNG, variant=None, component='', app_attrs='', activity_attrs=''):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name); res = root / 'res'; (res / 'drawable').mkdir(parents=True)
        ext = 'xml' if isinstance(icon, str) else 'png'
        p = res / 'drawable' / ('icon.' + ext)
        p.write_bytes(icon.encode() if isinstance(icon, str) else icon)
        if variant:
            (res / 'drawable-land').mkdir()
            (res / 'drawable-land/icon.xml').write_text(variant)
        manifest = root / 'AndroidManifest.xml'
        manifest.write_text(f'''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.cinevista.fixture"><uses-sdk android:minSdkVersion="10"/><application android:icon="@drawable/icon" {app_attrs}><activity android:name=".Main" {activity_attrs}><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity>{component}</application></manifest>''')
        apk = root / 'fixture.ap_'
        subprocess.run([str(AAPT), 'package', '-f', '-M', str(manifest), '-S', str(res), '-I', str(JAR), '-F', str(apk)], check=True, capture_output=True)
        return apk

    def test_plain_bitmap_passes(self):
        self.assertEqual(inspect_launcher(self.package(), AAPT)['icon_paths'], ['res/drawable/icon.png'])

    def test_layer_list_rejected(self):
        with self.assertRaisesRegex(ValueError, 'plain PNG'):
            inspect_launcher(self.package('<layer-list xmlns:android="http://schemas.android.com/apk/res/android"><item android:drawable="@android:color/black"/></layer-list>'), AAPT)

    def test_landscape_variant_rejected(self):
        with self.assertRaisesRegex(ValueError, 'plain PNG'):
            inspect_launcher(self.package(variant='<shape xmlns:android="http://schemas.android.com/apk/res/android"/>'), AAPT)

    def test_component_whitelist(self):
        for node in ('service', 'receiver', 'provider', 'activity-alias'):
            extra = 'android:authorities="org.cinevista.fixture"' if node == 'provider' else ''
            with self.subTest(node=node), self.assertRaisesRegex(ValueError, 'component'):
                inspect_launcher(self.package(component=f'<{node} android:name=".Extra" {extra}/>'), AAPT)

    def test_persistent_and_custom_process_rejected(self):
        for attrs in ('android:persistent="true"', 'android:process=":worker"'):
            with self.subTest(attrs=attrs), self.assertRaises(ValueError):
                inspect_launcher(self.package(app_attrs=attrs), AAPT)
        with self.assertRaises(ValueError):
            inspect_launcher(self.package(activity_attrs='android:process=":worker"'), AAPT)

    def test_activity_icon_cannot_bypass_app_icon(self):
        with self.assertRaisesRegex(ValueError, 'missing|unsupported'):
            inspect_launcher(self.package(activity_attrs='android:icon="@android:drawable/ic_delete"'), AAPT)

    def test_corrupted_png_rejected(self):
        apk = self.package()
        with zipfile.ZipFile(apk) as z: entries = {n:z.read(n) for n in z.namelist()}
        entries['res/drawable/icon.png'] = b'not a png'
        with zipfile.ZipFile(apk, 'w') as z:
            for n, data in entries.items(): z.writestr(n, data)
        with self.assertRaises(ValueError): inspect_launcher(apk, AAPT)

    def test_resource_alias_rejected_by_conservative_policy(self):
        with self.assertRaises(ValueError):
            inspect_launcher(self.package(activity_attrs='android:icon="@android:color/black"'), AAPT)

    def test_renamed_compiled_nine_patch_rejected(self):
        apk = self.package()
        with zipfile.ZipFile(apk) as z: entries = {n:z.read(n) for n in z.namelist()}
        png = entries['res/drawable/icon.png']
        chunk = b'npTc' + bytes(32)
        entries['res/drawable/icon.png'] = png[:-12] + struct.pack('>I',32) + chunk + struct.pack('>I',zlib.crc32(chunk)) + png[-12:]
        with zipfile.ZipFile(apk, 'w') as z:
            for n, data in entries.items(): z.writestr(n, data)
        with self.assertRaisesRegex(ValueError, 'NinePatch'): inspect_launcher(apk, AAPT)


class DumpFailClosedTests(unittest.TestCase):
    def test_empty_or_unknown_manifest_rejected(self):
        for text in ('', 'unsupported dump format'):
            with self.assertRaises(ValueError): _manifest_icons(text)

    def test_missing_or_reference_value_rejected(self):
        for text in ('', 'resource 0x7f020001 org.cinevista.fixture:drawable/icon: t=0x01 d=0x7f020002'):
            with self.assertRaises(ValueError): _icon_paths(text, [0x7f020001])
