# Rendering and PDF Review

## Supported Backend

Use RenderCV 2.8 with dependencies declared in pyproject.toml and locked in uv.lock, and the `classic` A4 template initially. The backend produces PDF and page PNGs plus editable YAML and Typst. RenderCV localizes dates with `locale.language`; the agent must translate prose and section titles itself.

Official references checked 2026-10-13:
- https://docs.rendercv.com/user_guide/
- https://docs.rendercv.com/user_guide/cli_reference/
- https://docs.rendercv.com/user_guide/yaml_input_structure/settings/
- https://github.com/rendercv/rendercv/blob/main/pyproject.toml

Context7 was unavailable during implementation. Recheck version-specific documentation through Context7 when changing the integration. The installed RenderCV skill is useful formatting reference material but is not a required dependency: this skill owns evidence, approval, and review rules. Do not copy its entire schema into the entry point.

## Experience Header Configuration

Apply this supported RenderCV 2.8 override in generated cv.yaml so the actual PDF uses title-first role headers, including with a user-selected built-in theme:

```yaml
design:
  templates:
    experience_entry:
      main_column: |-
        **POSITION** | COMPANY
        SUMMARY
        HIGHLIGHTS
      date_and_location_column: |-
        LOCATION
        DATE
```

Populate location only when confirmed; the template omits an absent LOCATION. Dates stay in the adjacent date column. Keep the chosen theme and other design settings; merge these fields rather than replacing the entire design. Use [tailoring](tailoring.md) for chronology and project placement.

Verified against the installed 2.8 schema and actual English/French renders on 2026-10-14. Context7 was unavailable; the official [design reference](https://docs.rendercv.com/user_guide/yaml_input_structure/design/) was used as a fallback and checked against the pinned installation because the live docs also cover newer themes.

## Page Metadata

Keep the CV body and contact header as the visible content. Every generated CV must omit the last-updated note and the entire page footer, including the repeated candidate name and page numbers. Merge these settings into the selected theme:

```yaml
design:
  page:
    show_top_note: false
    show_footer: false
```

Apply this rule in English and French, on every page. Check both page images and extracted text before delivery.

## Setup and Render

From the repository root (prefix shell commands with `rtk` when configured):

```powershell
rtk proxy uv sync --locked
rtk proxy uv run --locked python scripts/render_cv.py path/to/cv.yaml .local/applications/unique-id/render-v1
```

The same uv commands work on Windows and Unix. The helper invokes `python -m rendercv` with its own interpreter, avoiding platform-specific executable wrappers. Output must be a new directory, including retries; it never overwrites a previous revision. It resets input-controlled settings and sets all format paths inside that directory. Unsupported photos and custom themes are rejected in this version. Use quoted strings for free prose and explicit confirmed end dates, since an omitted end date may imply a current role. Preserve source date precision: do not put a year-only value into start_date/end_date if rendering would imply January. For a project known only as 2021, use a supported textual label such as “Academic project (2021)” and omit the month-bearing date fields. If employment month precision is missing and affects chronology, ask rather than inventing it. Check the rendered dates against the source, not only the YAML.

On failure, inspect render.log when available and correct the source; create a new revision directory. A zero process status and a PDF header establish rendering success only. They do not establish factual or visual quality.

## Required Review

Read [output-review.md](output-review.md) before delivery. Inspect every page PNG, extract PDF text, check accents, dates and ownership, and compare against the evidence ledger. Never claim ATS success from a keyword count; text extraction is only a compatibility check, not a hiring prediction.
