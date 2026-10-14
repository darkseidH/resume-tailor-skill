import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_evidence import check


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=".local/test-temp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cv = self.root / "cv.yaml"
        self.cv.write_text("cv: {name: Alex}", encoding="utf-8")
        (self.root / "source.md").write_text("My name is Alex.", encoding="utf-8")
        self.ledger = {"sources": {"s": "source.md"}, "facts": {"f": {"status": "supported", "source": "s", "quote": "My name is Alex."}}, "claims": {"/cv/name": ["f"]}}

    def run_check(self):
        path = self.root / "evidence.json"
        path.write_text(json.dumps(self.ledger), encoding="utf-8")
        return check(self.cv, path)

    def test_supported_reference_passes(self):
        self.assertEqual(self.run_check(), [])

    def test_unmapped_claim_fails(self):
        self.ledger["claims"] = {}
        self.assertTrue(any("Unmapped" in e for e in self.run_check()))

    def test_unknown_fact_cannot_support_a_claim(self):
        self.ledger["facts"]["f"]["status"] = "unconfirmed"
        self.assertTrue(any("not supported" in e for e in self.run_check()))

    def test_changed_quote_fails(self):
        self.ledger["facts"]["f"]["quote"] = "My name is Jordan."
        self.assertTrue(any("excerpt" in e for e in self.run_check()))

    def test_snapshot_cannot_escape_record_directory(self):
        self.ledger["sources"]["s"] = "../outside.md"
        self.assertTrue(any("outside" in e for e in self.run_check()))

    def test_stale_claim_pointer_fails(self):
        self.ledger["claims"]["/cv/old"] = ["f"]
        self.assertTrue(any("Stale" in e for e in self.run_check()))


if __name__ == "__main__":
    unittest.main()
