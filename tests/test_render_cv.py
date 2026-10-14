import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.render_cv import render


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Path(".local/test-temp").mkdir(parents=True, exist_ok=True)

    def test_timeout_preserves_available_diagnostics(self):
        for captured in ("render started", b"render started\xff", None):
            with self.subTest(captured=captured):
                with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
                    source = Path(tmp) / "cv.yaml"
                    source.write_text("cv: {name: Example}", encoding="utf-8")
                    output = Path(tmp) / "output"
                    failure = subprocess.TimeoutExpired(["rendercv"], 120, output=captured)
                    with patch("scripts.render_cv.subprocess.run", side_effect=failure):
                        with self.assertRaises(subprocess.TimeoutExpired):
                            render(source, output)
                    log = (output / "render.log").read_text(encoding="utf-8")
                    self.assertIn("timed out", log)
                    if captured:
                        self.assertIn("render started", log)
                    self.assertFalse((output / "cv.pdf").exists())

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            source = Path(tmp) / "cv.yaml"
            source.write_text("cv: {name: Example}", encoding="utf-8")
            output = Path(tmp) / "output"
            output.mkdir()
            (output / "cv.pdf").write_bytes(b"old")
            with self.assertRaises(FileExistsError):
                render(source, output)
            self.assertEqual((output / "cv.pdf").read_bytes(), b"old")

    def test_failed_renderer_is_reported_without_success(self):
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            source = Path(tmp) / "cv.yaml"
            source.write_text("cv: {name: Example}", encoding="utf-8")
            with patch("scripts.render_cv.subprocess.run", return_value=subprocess.CompletedProcess([], 1, "bad YAML")):
                with self.assertRaisesRegex(RuntimeError, "bad YAML"):
                    render(source, Path(tmp) / "output")

    def test_zero_exit_without_pdf_is_a_failure(self):
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            source = Path(tmp) / "cv.yaml"
            source.write_text("cv: {name: Example}", encoding="utf-8")
            with patch("scripts.render_cv.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "")):
                with self.assertRaisesRegex(RuntimeError, "PDF"):
                    render(source, Path(tmp) / "output")

    def test_missing_identity_is_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            source = Path(tmp) / "cv.yaml"
            source.write_text("cv: {}", encoding="utf-8")
            output = Path(tmp) / "output"
            with self.assertRaisesRegex(ValueError, "name"):
                render(source, output)
            self.assertFalse(output.exists())

    def test_malformed_design_has_a_useful_error(self):
        with tempfile.TemporaryDirectory(dir=".local/test-temp") as tmp:
            source = Path(tmp) / "cv.yaml"
            source.write_text("cv: {name: Example}\ndesign: []", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "design"):
                render(source, Path(tmp) / "output")


if __name__ == "__main__":
    unittest.main()
