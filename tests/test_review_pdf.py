import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

from scripts.review_pdf import review


class PdfReviewTests(unittest.TestCase):
    def setUp(self):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=".local/test-temp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_malformed_pdf_cli_fails_without_traceback(self):
        for contents in (b"not a PDF", b"%PDF-1.7\ntruncated"):
            with self.subTest(contents=contents):
                source = self.root / "broken.pdf"
                source.write_bytes(contents)
                result = subprocess.run(
                    [sys.executable, "scripts/review_pdf.py", str(source), "--output", str(self.root / "bad-review")],
                    capture_output=True, text=True, encoding="utf-8",
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("PDF review failed:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse((self.root / "bad-review").exists())

    def test_valid_pages_extract_and_existing_review_is_preserved(self):
        source = self.root / "valid.pdf"
        with pymupdf.open() as document:
            for title in ("First experience", "Earlier experience"):
                page = document.new_page()
                page.insert_text((72, 72), title)
            document.save(source)
        output = self.root / "review"
        result = review(source, output)
        self.assertEqual(result["pages"], 2)
        self.assertEqual(result["visual_review"], "pending")
        self.assertEqual(result["factual_review"], "pending")
        self.assertTrue((output / "page-1.png").is_file())
        self.assertTrue((output / "page-2.png").is_file())
        self.assertIn("Earlier experience", (output / "extracted.txt").read_text(encoding="utf-8"))
        before = (output / "review.json").read_bytes()
        with self.assertRaises(FileExistsError):
            review(source, output)
        self.assertEqual((output / "review.json").read_bytes(), before)

    def test_blank_page_is_rejected(self):
        source = self.root / "blank.pdf"
        with pymupdf.open() as document:
            document.new_page()
            document.save(source)
        with self.assertRaisesRegex(ValueError, "empty or non-extractable"):
            review(source, self.root / "review")


if __name__ == "__main__":
    unittest.main()
