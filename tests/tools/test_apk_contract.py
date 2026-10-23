import unittest
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from apk_contract import validate_badging, source_hashes
class ApkContractTests(unittest.TestCase):
    def setUp(self):
        self.text=(ROOT/'tests/fixtures/v0.6/api10-build-badging.txt').read_text()
        self.manifest=ET.fromstring('''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.cinevista.probe" android:versionCode="4" android:versionName="0.4-probe"><uses-permission android:name="android.permission.CAMERA"/><uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/></manifest>''')
    def test_api10_storage_implication_is_explicit(self):
        self.assertEqual(validate_badging(self.text,self.manifest)['implied_by_aapt'],['android.permission.READ_EXTERNAL_STORAGE'])
    def test_internet_or_unexplained_permission_rejected(self):
        for text in (self.text+"\nuses-permission: name='android.permission.INTERNET'\n",self.text.replace('uses-implied-permission:','hidden-implication:')):
            with self.assertRaises(ValueError):validate_badging(text,self.manifest)
    def test_version_sdk_mismatch_rejected(self):
        for text in (self.text.replace("versionCode='4'","versionCode='5'"),self.text.replace("sdkVersion:'10'","sdkVersion:'16'")):
            with self.assertRaises(ValueError):validate_badging(text,self.manifest)
    def test_input_hashes_cover_all_compiled_modules(self):
        inputs=source_hashes(ROOT)
        for prefix in ('core/src/','io/src/','camera-api/src/','sony/src/','app/src/'):
            self.assertTrue(any(p.startswith(prefix) for p in inputs))
        self.assertFalse(any(p.startswith('build/') for p in inputs))
