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

    def revision_path(self, language):
        code = {"english": "en", "french": "fr"}[language]
        return self.output / "Fictional Employer/Backend Developer/supporting/revisions" / f"{code}-v1"

    def test_only_requested_languages_share_one_application(self):
        for languages in (("en",), ("fr",), ("en", "fr")):
            with self.subTest(languages=languages):
                output = self.output / "-".join(languages)
                build(output, languages)
                root = output / "Fictional Employer/Backend Developer"
                self.assertEqual([p.name for p in root.iterdir()], ["supporting"])
                supporting = root / "supporting"
                self.assertEqual({p.name for p in (supporting / "revisions").iterdir()}, {f"{lang}-v1" for lang in languages})
                self.assertTrue((supporting / "job.md").is_file())
                for lang in languages:
                    revision = supporting / "revisions" / f"{lang}-v1"
                    self.assertEqual(check(revision / "cv.yaml", revision / "evidence.json"), [])

    def test_existing_synthetic_output_is_preserved(self):
        build(self.output)
        with self.assertRaises(FileExistsError):
            build(self.output)

    def test_fixtures_follow_existing_page_metadata_rule(self):
        build(self.output)
        for language in ('english', 'french'):
            data = yaml.safe_load((self.revision_path(language) / 'cv.yaml').read_text(encoding='utf-8'))
            self.assertIs(data['design']['page'].get('show_top_note'), False)
            self.assertIs(data['design']['page'].get('show_footer'), False)

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
            ledger = json.loads((self.revision_path(language) / "evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(ledger["claims"][f"/cv/sections/{section}/0/label"], ["languages"])
            self.assertEqual(check(self.revision_path(language) / "cv.yaml", self.revision_path(language) / "evidence.json"), [])

    def test_documented_direct_script_runs(self):
        result = subprocess.run(
            [sys.executable, "evals/run_synthetic.py", str(self.output)],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(check(self.revision_path("english") / "cv.yaml", self.revision_path("english") / "evidence.json"), [])

    def test_summary_has_profile_evidence(self):
        build(self.output)
        for language, section in [("english", "Summary"), ("french", "Profil")]:
            data = yaml.safe_load((self.revision_path(language) / "cv.yaml").read_text(encoding="utf-8"))
            self.assertTrue(data["cv"]["sections"][section])
            ledger = json.loads((self.revision_path(language) / "evidence.json").read_text(encoding="utf-8"))
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
