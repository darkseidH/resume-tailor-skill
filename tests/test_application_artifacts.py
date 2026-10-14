import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.application_artifacts import allocate, resume, revision


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
        except OSError as error:
            self.skipTest(f'Directory symlinks unavailable: {error}')
        with self.assertRaises(ValueError):
            allocate(self.output, 'Company', 'Role')
        self.assertEqual(list(outside.iterdir()), [])
