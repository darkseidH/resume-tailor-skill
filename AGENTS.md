# Repository Guidelines

## Project Structure & Module Organization

This repository packages an evidence-based CV tailoring agent skill using RenderCV 2.8. `SKILL.md` defines the workflow; `references/` contains stage-specific contracts and instructions. Reusable Markdown/JSON templates live in `templates/`, and agent metadata lives in `agents/openai.yaml`.

Python helpers are in `scripts/`; unit tests are in `tests/`. `evals/` contains fictional fixtures, behavioral scenarios, and a synthetic runner. `tasks/` tracks implementation work. Keep candidate notes and generated applications in the mapped private workspace, typically `.local/`.

## Build, Test, and Development Commands

Run from the repository root with Python 3.12+:

- `rtk proxy uv sync --locked` — install pinned dependencies.
- `rtk proxy uv run --locked python -m unittest discover -s tests -v` — run unit tests.
- `rtk proxy uv run --locked python evals/run_synthetic.py .local/synthetic-new` — create synthetic evaluation outputs in a new directory.
- `rtk proxy uv run --locked python scripts/package_skill.py .local/dist/resume-tailor-skill.zip` — build the distributable archive; the target must not exist.

For evidence checking, CV rendering, and PDF review commands, follow `README.md` and `evals/acceptance.md`. Use fresh render/review directories for each revision.

## Coding Style & Naming Conventions

Follow existing Python style: four-space indentation, snake_case functions/modules, PascalCase test classes, and explicit UTF-8 file operations. Use `pathlib.Path` for filesystem paths and preserve input validation and useful CLI errors. Markdown reference filenames use kebab-case. No formatter or linter is configured; keep changes consistent with surrounding files.

## Testing Guidelines

Use standard-library `unittest`, naming files `test_*.py` and methods `test_<behavior>`. Add regression tests for changed validation, overwrite protection, rendering failures, or package exclusions. No numerical coverage threshold is configured. For rendering changes, inspect every page image and extracted text in both English and French; automated evidence coverage does not establish factual truth.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout. Use concise imperative commit subjects describing one focused change. PRs should explain the behavior changed, link relevant issues, list verification results and unavailable checks, and include page images when PDF layout changes.

## Privacy & Agent Boundaries

Use fictional data in committed fixtures and examples. Keep personal sources, outputs, and secrets out of distribution archives. Preserve evidence for every substantive CV claim. Canonical profile edits require approval of the exact proposed changes; follow `references/profile-updates.md`.
