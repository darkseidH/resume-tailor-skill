import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from evals.run_synthetic import build
from scripts.check_evidence import check


class SyntheticTests(unittest.TestCase):
    def setUp(self):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=".local/test-temp")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "application"

    def test_reordered_sections_keep_their_evidence(self):
        original_copy = shutil.copyfile

        def reorder(source, target):
            result = original_copy(source, target)
            if Path(target).name == "cv.yaml":
                data = yaml.safe_load(Path(target).read_text(encoding="utf-8"))
                data["cv"]["sections"] = dict(reversed(list(data["cv"]["sections"].items())))
                Path(target).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            return result

        with patch("evals.run_synthetic.shutil.copyfile", side_effect=reorder):
            build(self.output)
        for language, section in [("english", "Languages"), ("french", "Langues")]:
            ledger = json.loads((self.output / language / "evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(ledger["claims"][f"/cv/sections/{section}/0/label"], ["languages"])
            self.assertEqual(check(self.output / language / "cv.yaml", self.output / language / "evidence.json"), [])

    def test_documented_direct_script_runs(self):
        result = subprocess.run(
            [sys.executable, "evals/run_synthetic.py", str(self.output)],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(check(self.output / "english/cv.yaml", self.output / "english/evidence.json"), [])

    def test_summary_has_profile_evidence(self):
        build(self.output)
        for language, section in [("english", "Summary"), ("french", "Profil")]:
            data = yaml.safe_load((self.output / language / "cv.yaml").read_text(encoding="utf-8"))
            self.assertTrue(data["cv"]["sections"][section])
            ledger = json.loads((self.output / language / "evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(ledger["claims"][f"/cv/sections/{section}/0"], ["role"])

    def test_unmapped_content_fails_instead_of_receiving_a_fact(self):
        original_copy = shutil.copyfile

        def add_unknown(source, target):
            result = original_copy(source, target)
            if Path(target).name == "cv.yaml":
                data = yaml.safe_load(Path(target).read_text(encoding="utf-8"))
                data["cv"]["sections"]["Unreviewed"] = ["Unsupported qualification"]
                Path(target).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            return result

        with patch("evals.run_synthetic.shutil.copyfile", side_effect=add_unknown):
            with self.assertRaisesRegex(ValueError, "Unmapped or stale"):
                build(self.output)

    def test_changed_claim_is_not_given_old_evidence(self):
        original_copy = shutil.copyfile

        def exaggerate(source, target):
            result = original_copy(source, target)
            if Path(target).name == "cv.yaml":
                data = yaml.safe_load(Path(target).read_text(encoding="utf-8"))
                data["cv"]["headline"] = "Senior Architect"
                Path(target).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            return result

        with patch("evals.run_synthetic.shutil.copyfile", side_effect=exaggerate):
            with self.assertRaisesRegex(ValueError, "Fixture claim changed"):
                build(self.output)


if __name__ == "__main__":
    unittest.main()
