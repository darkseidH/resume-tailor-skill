import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import package


class PackageTests(unittest.TestCase):
    def test_private_and_unrelated_files_are_excluded(self):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            root = Path(tmp) / "resume-tailor-skill"
            root.mkdir()
            (root / "SKILL.md").write_text("synthetic skill", encoding="utf-8")
            for name in ("pyproject.toml", "uv.lock", ".python-version", "requirements.txt"):
                (root / name).write_text("synthetic config", encoding="utf-8")
            (root / ".local").mkdir()
            (root / ".local" / "candidate.md").write_text("private", encoding="utf-8")
            (root / "unrelated.md").write_text("private", encoding="utf-8")
            target = Path(tmp) / "skill.zip"
            package(root, target)
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(set(archive.namelist()), {
                    "resume-tailor-skill/SKILL.md",
                    "resume-tailor-skill/pyproject.toml",
                    "resume-tailor-skill/uv.lock",
                    "resume-tailor-skill/.python-version",
                })
            with self.assertRaises(FileExistsError):
                package(root, target)


if __name__ == "__main__":
    unittest.main()
