"""Governance mutations exercise real failures without touching the working tree."""
from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import docs_check
class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.local','.git','build','runs','__pycache__'))
    def test_current_docs_and_task_view_consistent(self):self.assertEqual(docs_check.validate(self.root),[])
    def test_stale_todo_rejected(self):
        (self.root/'TODO.md').write_text('stale');self.assertTrue(docs_check.validate(self.root))
    def test_missing_manual_rejected(self):
        (self.root/'docs/USER_GUIDE.md').unlink();self.assertTrue(docs_check.validate(self.root))
    def test_bad_task_dependency_rejected(self):
        p=self.root/'handoff/task-board.json';d=json.loads(p.read_text());d['tasks'][0]['depends_on']=['missing'];p.write_text(json.dumps(d))
        self.assertTrue(docs_check.validate(self.root))
    def test_duplicate_task_and_cycle_rejected(self):
        p=self.root/'handoff/task-board.json';d=json.loads(p.read_text());d['tasks'][0]['depends_on']=['T01'];p.write_text(json.dumps(d))
        self.assertTrue(docs_check.validate(self.root));d['tasks'].append(d['tasks'][0]);p.write_text(json.dumps(d));self.assertTrue(docs_check.validate(self.root))
    def test_completed_task_needs_evidence_reference(self):
        p=self.root/'handoff/task-board.json';d=json.loads(p.read_text());d['tasks'][0]['evidence']=[];p.write_text(json.dumps(d));self.assertTrue(docs_check.validate(self.root))
    def test_broken_document_link_rejected(self):
        p=self.root/'docs/USER_GUIDE.md';p.write_text(p.read_text()+'\n[broken](missing.md)\n');self.assertTrue(docs_check.validate(self.root))
