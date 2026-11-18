"""Package only distributable skill resources, excluding private workspaces."""

import argparse
import zipfile
from pathlib import Path, PureWindowsPath


RESOURCES = (
    ".python-version",
    "agents/openai.yaml",
    "pyproject.toml",
    "README.md",
    "references/data-contracts.md",
    "references/job-analysis.md",
    "references/job-intake.md",
    "references/onboarding.md",
    "references/output-review.md",
    "references/profile-updates.md",
    "references/quantification.md",
    "references/rendering.md",
    "references/tailoring.md",
    "scripts/application_artifacts.py",
    "scripts/check_evidence.py",
    "scripts/package_skill.py",
    "scripts/render_cv.py",
    "scripts/review_pdf.py",
    "SKILL.md",
    "templates/evidence.json",
    "templates/job-record.md",
    "templates/match-report.md",
    "templates/profile-map.md",
    "templates/profile-summary.md",
    "templates/profile-update.md",
    "templates/tailoring-decisions.md",
    "uv.lock",
)


def package(root: Path, target: Path):
    root = root.resolve()
    files = []
    for name in RESOURCES:
        relative = Path(name)
        if relative.is_absolute() or PureWindowsPath(name).anchor or ".." in relative.parts:
            raise ValueError(f"Invalid resource path: {name}")
        path = root
        for part in relative.parts:
            path /= part
            if path.is_symlink() or path.is_junction():
                raise ValueError(f"Linked skill resource: {path}")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or invalid skill resource: {path}")
        files.append(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, Path("resume-tailor-skill") / path.relative_to(root))
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        print(package(Path(__file__).resolve().parents[1], args.target))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")


if __name__ == "__main__":
    main()
