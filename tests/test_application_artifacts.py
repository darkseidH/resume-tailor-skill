import json
import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.application_artifacts import allocate, resume, revision, publish


class ApplicationArtifactTests(unittest.TestCase):
    def setUp(self):
        Path('.local/test-temp').mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir='.local/test-temp')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name).resolve() / 'outputs'

    def test_company_roles_and_repeat_applications_are_separate(self):
        first = allocate(self.output, 'Example Company', 'Data Analyst')
        second = allocate(self.output, 'Example Company', 'Data Analyst')
        other = allocate(self.output, 'Example Company', 'BI Developer')
        self.assertEqual(first, self.output / 'Example Company/Data Analyst')
        self.assertEqual(second.name, 'Data Analyst-2')
        self.assertEqual(other.parent, first.parent)
        record = json.loads((first / 'supporting/application.json').read_text(encoding='utf-8'))
        self.assertEqual(record['company'], 'Example Company')
        self.assertEqual(record['root'], str(first))

    def test_windows_names_and_collisions_do_not_merge_companies(self):
        first = allocate(self.output, 'Example:Co', 'CON. ')
        second = allocate(self.output, 'Example?Co', 'Data/Analyst')
        self.assertNotEqual(first.parent, second.parent)
        self.assertEqual(first.name, '_CON')
        self.assertEqual(second.name, 'Data-Analyst')
        for part in first.relative_to(self.output).parts:
            self.assertFalse(any(c in part for c in '<>:"/\\|?*'))

    def test_invalid_labels_fail_without_creating_outputs(self):
        for label in ('', '   ', '.', '..', '../outside', 'C:\\outside'):
            with self.subTest(label=label), self.assertRaises(ValueError):
                allocate(self.output, label, 'Role')
        self.assertFalse(self.output.exists())

    def test_resume_preserves_records_and_missing_state_is_reported(self):
        root = allocate(self.output, 'Company', 'Role')
        job = root / 'supporting/job.md'
        job.write_text('Original offer', encoding='utf-8')
        self.assertEqual(resume(root), root)
        self.assertEqual(job.read_text(encoding='utf-8'), 'Original offer')
        shutil.rmtree(root / 'supporting')
        with self.assertRaisesRegex(ValueError, 'supporting'):
            resume(root)
        self.assertFalse((root / 'supporting').exists())

    def test_legacy_resume_does_not_migrate(self):
        legacy = self.output / 'legacy-id'
        legacy.mkdir(parents=True)
        (legacy / 'job.md').write_text('Old offer', encoding='utf-8')
        self.assertEqual(resume(legacy), legacy)
        self.assertFalse((legacy / 'supporting').exists())

    def test_revisions_are_language_specific_and_fresh(self):
        root = allocate(self.output, 'Company', 'Role')
        first = revision(root, 'en')
        (first / 'cv.yaml').write_text('retained', encoding='utf-8')
        self.assertEqual(revision(root, 'en').name, 'en-v2')
        self.assertEqual(revision(root, 'fr').name, 'fr-v1')
        self.assertEqual((first / 'cv.yaml').read_text(encoding='utf-8'), 'retained')
        with self.assertRaises(ValueError):
            revision(root, '../en')

    def test_redirected_output_is_rejected(self):
        outside = Path(self.temp.name).resolve() / 'outside'
        outside.mkdir()
        self.output.mkdir()
        link = self.output / 'Company'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            if os.name != 'nt':
                raise
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        with self.assertRaises(ValueError):
            allocate(self.output, 'Company', 'Role')
        self.assertEqual(list(outside.iterdir()), [])

    def reviewed_revision(self):
        root = allocate(self.output, 'Company', 'Role')
        rev = revision(root, 'en')
        render = rev / 'render'
        render.mkdir()
        (render / 'cv.pdf').write_bytes(b'%PDF-1.7\nfictional test bytes')
        (render / 'cv.yaml').write_text('cv: {name: Alex}', encoding='utf-8')
        (rev / 'source.md').write_text('My name is Alex.', encoding='utf-8')
        ledger = {'sources': {'s': 'source.md'}, 'facts': {'f': {'status': 'supported', 'source': 's', 'quote': 'My name is Alex.'}}, 'claims': {'/cv/name': ['f']}}
        (rev / 'evidence.json').write_text(json.dumps(ledger), encoding='utf-8')
        review = rev / 'review'
        review.mkdir()
        record = {'pdf': str(render / 'cv.pdf'), 'pdf_sha256': hashlib.sha256((render / 'cv.pdf').read_bytes()).hexdigest(), 'yaml_sha256': hashlib.sha256((render / 'cv.yaml').read_bytes()).hexdigest(), 'pages': 1, 'text_extracted': True, 'visual_review': 'passed', 'factual_review': 'passed', 'text_review': 'passed', 'review_notes': 'Simulated reviewer approval for unit testing only.'}
        (review / 'extracted.txt').write_text('Alex', encoding='utf-8')
        (review / 'page-1.png').write_bytes(b'unit-test-image')
        (review / 'review.json').write_text(json.dumps(record), encoding='utf-8')
        return root, rev, record

    def test_publication_preserves_bytes_revisions_and_survives_cleanup(self):
        root, rev, _ = self.reviewed_revision()
        original = (rev / 'render/cv.pdf').read_bytes()
        first = publish(root, rev, 'en')
        second = publish(root, rev, 'en')
        self.assertEqual(first.name, 'resume-en.pdf')
        self.assertEqual(second.name, 'resume-en-v2.pdf')
        shutil.rmtree(root / 'supporting')
        self.assertEqual(first.read_bytes(), original)
        self.assertEqual(second.read_bytes(), original)

    def test_incomplete_or_stale_review_never_publishes(self):
        root, rev, record = self.reviewed_revision()
        for field, value in [('visual_review', 'pending'), ('factual_review', 'failed'), ('text_review', 'unavailable'), ('text_extracted', False), ('pdf_sha256', 'stale'), ('yaml_sha256', 'stale'), ('pdf', str(root / 'other.pdf')), ('pages', 0), ('review_notes', '')]:
            with self.subTest(field=field):
                changed = {**record, field: value}
                (rev / 'review/review.json').write_text(json.dumps(changed), encoding='utf-8')
                with self.assertRaises(ValueError):
                    publish(root, rev, 'en')
                self.assertFalse((root / 'resume-en.pdf').exists())

    def test_failed_render_wrong_language_and_missing_evidence_never_publish(self):
        root, rev, _ = self.reviewed_revision()
        with self.assertRaises(ValueError):
            publish(root, rev, 'fr')
        (rev / 'evidence.json').unlink()
        with self.assertRaises(OSError):
            publish(root, rev, 'en')
        (rev / 'render/cv.pdf').unlink()
        with self.assertRaises(OSError):
            publish(root, rev, 'en')
        self.assertFalse((root / 'resume-en.pdf').exists())

    def test_copy_failure_leaves_no_partial_finished_pdf(self):
        root, rev, _ = self.reviewed_revision()
        with patch('scripts.application_artifacts.shutil.copyfileobj', side_effect=OSError('Disk full')):
            with self.assertRaisesRegex(OSError, 'Disk full'):
                publish(root, rev, 'en')
        self.assertFalse((root / 'resume-en.pdf').exists())
