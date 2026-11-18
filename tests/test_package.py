import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import RESOURCES, package


class PackageTests(unittest.TestCase):
    def setUp(self):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(dir=".local/test-temp")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve() / "skill"
        self.target = self.root.parent / "skill.zip"
        for name in RESOURCES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fictional resource", encoding="utf-8")

    def test_private_and_unrelated_files_are_excluded(self):
        (self.root / "templates/candidate-notes.md").write_text("fictional private note", encoding="utf-8")
        package(self.root, self.target)
        with zipfile.ZipFile(self.target) as archive:
            self.assertEqual(set(archive.namelist()), {f"resume-tailor-skill/{name}" for name in RESOURCES})
        original = self.target.read_bytes()
        with self.assertRaises(FileExistsError):
            package(self.root, self.target)
        self.assertEqual(self.target.read_bytes(), original)

    def test_missing_listed_resource_creates_no_archive(self):
        (self.root / "SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            package(self.root, self.target)
        self.assertFalse(self.target.exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_in_tree_junction_is_rejected(self):
        folder = self.root / "templates"
        moved = folder.rename(self.root / "other")
        subprocess.run(["cmd", "/c", "mklink", "/J", str(folder), str(moved)], check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "Linked"):
            package(self.root, self.target)
        self.assertFalse(self.target.exists())

    def test_symlink_is_rejected(self):
        path = self.root / "SKILL.md"
        moved = path.rename(self.root / "other.md")
        try:
            path.symlink_to(moved)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error.winerror if os.name == 'nt' else error.errno}")
        with self.assertRaisesRegex(ValueError, "Linked"):
            package(self.root, self.target)
        self.assertFalse(self.target.exists())
