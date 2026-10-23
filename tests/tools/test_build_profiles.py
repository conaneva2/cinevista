"""Synthetic host fixtures do not approve any production native library."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from build_profiles import validate_archive, validate_sources
from run_evidence import write_evidence
from unittest.mock import patch

class BuildProfileTests(unittest.TestCase):
    def profile(self, data):
        return {'id':'native-fixture', 'native_libraries':[{'path':'lib/armeabi/libfixture.so',
            'sha256':hashlib.sha256(data).hexdigest(), 'source_commit':'a'*40,
            'license':'MIT', 'review':'tests/fixtures/review.md'}], 'source_exceptions':[]}
    def test_pure_java_rejects_native(self):
        with self.assertRaises(ValueError):validate_archive({'lib/armeabi/libx.so':b'x'}, {'native_libraries':[]})
    def test_exact_reviewed_library_allowed(self):
        data=b'fixture only';validate_archive({'lib/armeabi/libfixture.so':data},self.profile(data))
    def test_wrong_hash_abi_missing_extra_rejected(self):
        p=self.profile(b'fixture')
        for files in ({}, {'lib/armeabi/libfixture.so':b'changed'}, {'lib/arm64-v8a/libfixture.so':b'fixture'}, {'lib/armeabi/libfixture.so':b'fixture','lib/armeabi/extra.so':b'x'}):
            with self.assertRaises(ValueError):validate_archive(files,p)
    def test_unreviewed_origin_rejected(self):
        p=self.profile(b'f');p['native_libraries'][0]['source_commit']='main'
        with self.assertRaises(ValueError):validate_archive({'lib/armeabi/libfixture.so':b'f'},p)
    def test_source_exception_exact_path_hash_symbols(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);f=r/'sony/src/Native.java';f.parent.mkdir(parents=True);f.write_text('Backup_sync_all')
            p={'source_exceptions':[]}
            with self.assertRaises(ValueError):validate_sources(r,[f],p)
            p['source_exceptions']=[{'path':'sony/src/Native.java','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'symbols':['Backup_sync_all'],'source_commit':'a'*40,'license':'MIT','review':'review.md'}]
            validate_sources(r,[f],p)
            f.write_text('Backup_sync_all Backup_write')
            with self.assertRaises(ValueError):validate_sources(r,[f],p)
    def test_evidence_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict('os.environ',{'CINEVISTA_RUN_DIR':tmp}):
            write_evidence('report.txt','first')
            with self.assertRaises(FileExistsError):write_evidence('report.txt','replacement')
            self.assertEqual((Path(tmp)/'report.txt').read_text(),'first')
