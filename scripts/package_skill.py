"""Package only distributable skill resources, excluding private workspaces."""

import argparse
import zipfile
from pathlib import Path


def package(root: Path, target: Path):
    root = root.resolve()
    files = [root / "SKILL.md"]
    files += [root / name for name in ("README.md", "pyproject.toml", "uv.lock", ".python-version") if (root / name).is_file()]
    for directory in ("agents", "references", "templates", "scripts"):
        folder = root / directory
        if folder.exists():
            if folder.is_symlink():
                raise ValueError(f"Symlink resource directory: {folder}")
            files.extend(p for p in folder.rglob("*") if p.is_file() and not any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(root).parts) and p.suffix in {".md", ".json", ".yaml", ".py", ".txt"})
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Resource outside skill directory: {path}")
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
