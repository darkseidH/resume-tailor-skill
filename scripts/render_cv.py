"""Render a self-contained CV into a new directory, preserving diagnostics."""

import argparse
import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import yaml


def render(source: Path, output: Path) -> Path:
    source, output = source.resolve(), output.resolve()
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cv"), dict):
        raise ValueError("Expected a YAML mapping with a cv mapping")
    if not isinstance(data["cv"].get("name"), str) or not data["cv"]["name"].strip():
        raise ValueError("A confirmed candidate name is required")
    if "design" in data and not isinstance(data["design"], dict):
        raise ValueError("Expected design to be a mapping")
    if data["cv"].get("photo"):
        raise ValueError("Photo assets are unsupported by this initial self-contained renderer")
    if data.get("design", {}).get("theme", "classic") not in {
        "classic", "harvard", "engineeringresumes", "engineeringclassic", "sb2nov", "moderncv"
    }:
        raise ValueError("Use a supported built-in RenderCV 2.8 theme")
    if version("rendercv") != "2.8":
        raise RuntimeError("Install the pinned RenderCV 2.8 dependencies")
    output.mkdir(parents=True, exist_ok=False)
    # Avoid input-controlled output paths and command settings. All formats stay here.
    data["settings"] = {}
    local_source = output / "cv.yaml"
    local_source.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    command = [sys.executable, "-m", "rendercv", "render", str(local_source)]
    for kind, filename in [("pdf", "cv.pdf"), ("typst", "cv.typ"), ("markdown", "cv.md"), ("html", "cv.html"), ("png", "cv.png")]:
        command.extend([f"--{kind}-path", str(output / filename)])
    scratch = output / ".tmp"
    scratch.mkdir()
    environment = {**os.environ, "TEMP": str(scratch), "TMP": str(scratch), "TMPDIR": str(scratch), "PYTHONUTF8": "1"}
    try:
        result = subprocess.run(command, cwd=output, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", timeout=120)
    except subprocess.TimeoutExpired as error:
        captured = error.stdout or ""
        if isinstance(captured, bytes):
            captured = captured.decode("utf-8", errors="replace")
        (output / "render.log").write_text(f"{captured}\nRenderCV timed out after {error.timeout} seconds.\n", encoding="utf-8")
        raise
    (output / "render.log").write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"RenderCV failed ({result.returncode}): {result.stdout}")
    pdf = output / "cv.pdf"
    if not pdf.exists() or not pdf.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("RenderCV returned without a valid PDF header")
    return pdf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, help="Must not exist; use a new revision directory")
    args = parser.parse_args()
    try:
        print(render(args.source, args.output))
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, yaml.YAMLError) as error:
        parser.exit(1, f"Rendering failed: {error}\n")


if __name__ == "__main__":
    main()
