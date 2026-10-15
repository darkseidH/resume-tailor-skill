# Spec: Company and Role Artifact Storage

Status: Implemented and verified on 2026-10-14 following user authorization to implement all tasks. Final human review remains pending.

Verification: [artifact-storage.md](evals/artifact-storage.md).

## Objective

Make finished CV PDFs easy to find by company and role. Keep editable YAML and
every supporting artifact in one removable `supporting/` folder. Generate English,
French, or both only as requested by the user.

Confirmed intent: company folders contain role folders; role folders expose the
finished PDFs, while YAML, evidence, drafts, and verification files belong inside
`supporting/`.

## Implementation Defaults

- Use the existing mapped application output directory as the parent. `outputs/`
  is an example name, not a new mandatory location or configuration field.
- Apply the structure to new applications. Leave existing application folders
  untouched; an explicitly resumed older application retains its recorded root.
- Keep revisions and rendering failures inside `supporting/`. Publish a PDF to
  the role folder only after required review passes.
- Preserve existing PDFs. Use a revision suffix for subsequent finished PDFs;
  never silently replace a previously delivered file.
- A separate application to the same company and role gets an unused role folder
  with a numeric suffix. Explicitly resuming an application reuses its root.
- Deleting supporting files is a user action. The agent does not delete them
  automatically or recreate missing evidence by guessing.

## Output Contract

```text
<mapped-output-directory>/
  Example Company/
    Data Analyst/
      resume-en.pdf
      resume-fr.pdf
      supporting/
        job.md
        answers.md
        match.md
        tailoring.md
        verification.md
        revisions/
          en-v1/
            cv.yaml
            evidence.json
            sources/
            render/
            review/
          fr-v1/
            cv.yaml
            evidence.json
            sources/
            render/
            review/
```

This tree illustrates a bilingual application. A single-language request creates
only that language's artifacts. Supporting filenames may follow existing
templates; all non-final artifacts must remain under `supporting/`.

1. Resolve the output directory against the profile map as today, keeping
   personal outputs inside the mapped private destination.
2. Use readable company and role directory names. Sanitize Windows-invalid
   characters, reserved device names, and trailing dots/spaces. Treat supplied
   names as labels, never paths; prevent traversal and writes outside the mapped
   output directory. Do not merge distinct applications after name collisions.
3. Obtain missing company or role labels from the user without inventing them.
   Preserve the actual supplied offer text separately from sanitized labels.
4. Allocate and record one absolute application root during intake. All later
   stages and requested languages reuse that root and original job snapshot.
5. The role folder contains finished PDF files and `supporting/` only. YAML,
   Typst, HTML, Markdown, logs, scratch files, evidence snapshots, answer logs,
   profile-change records, page images, and extracted text stay in `supporting/`.
6. Keep each evidence ledger's snapshots within its parent directory, preserving
   the containment rule enforced by `scripts/check_evidence.py`.
7. Render and review in fresh per-language revision directories. The existing
   renderer can continue generating all its formats together inside `supporting/`.
8. After successful factual, visual, and extracted-text review, copy the reviewed
   PDF to `resume-en.pdf` or `resume-fr.pdf`. The delivered bytes must match the
   reviewed PDF. An unavailable or failed required check leaves the artifact in
   `supporting/`, with its status reported honestly.
9. If the final name exists, retain it and choose an unused numbered name, such
   as `resume-en-v2.pdf`. Do not overwrite either language or an older revision.
10. At delivery, link each finished PDF and its corresponding editable YAML
    under `supporting/`. Report match findings and verification status as today.
11. The user can delete `supporting/` without breaking the finished PDFs. Explain
    briefly that this removes editable sources, evidence, and resume state.
    Canonical profile sources must never be stored inside this removable folder.
12. If supporting files are missing on resume, report what is unavailable and
    request the necessary inputs before rebuilding or claiming prior review.

## Tech Stack

Keep Python 3.12+, standard-library filesystem operations, and the pinned
RenderCV 2.8, PyYAML, pypdf, and PyMuPDF dependencies. No new dependency,
framework, service, or RenderCV integration change is required by this feature.

## Commands

Run from the repository root. These use existing helper interfaces; sample
revision directories must not already exist.

```powershell
rtk proxy uv run --locked python -m unittest discover -s tests -v
rtk proxy uv run --locked python evals/run_synthetic.py .local/synthetic-artifact-storage-new
rtk proxy uv run --locked python scripts/check_evidence.py ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/cv.yaml" ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/evidence.json"
rtk proxy uv run --locked python scripts/render_cv.py ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/cv.yaml" ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/render"
rtk proxy uv run --locked python scripts/review_pdf.py ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/render/cv.pdf" --output ".local/applications/Example Company/Data Analyst/supporting/revisions/en-v1/review"
rtk proxy uv run --locked python scripts/package_skill.py .local/dist/resume-tailor-artifact-storage-new.zip
```

The example application inputs must first be prepared with fictional evidence.
Repeat rendering and review for French. Packaging targets must be unused.
No formatter or linter is configured.

## Project Structure and Affected Contracts

- `SKILL.md`: intake, revision, application-output, and delivery instructions.
- `references/data-contracts.md`, `job-intake.md`, `rendering.md`, and
  `output-review.md`: root allocation, evidence containment, staging, and delivery.
- Other `references/` and `templates/`: update paths that assume job records,
  answers, or reports live directly in the application root.
- `templates/profile-map.md` and `README.md`: mapped destination and examples.
- `scripts/`: reuse evidence, render, review, and package helpers. Add or change
  filesystem logic only where needed to enforce allocation/publication rules.
- `tests/`: focused regression checks for changed filesystem behavior.
- `evals/run_synthetic.py` and `evals/`: fictional layout, walkthrough commands,
  and acceptance scenarios. Historical results remain labeled as historical.
- `tasks/`: implementation planning after this spec is approved.

## Code Style

Preserve existing Python conventions: four spaces, snake_case, `pathlib.Path`,
explicit UTF-8 text operations, validation, and useful CLI errors. Existing
fresh-directory protection is the model:

```python
output.mkdir(parents=True, exist_ok=False)
```

Keep changes focused. Reuse the current helpers rather than redesign rendering,
evidence schemas, or profile approval handling.

## Testing Strategy

Use standard-library `unittest` in `tests/`, without a new coverage threshold.
Test requested language selection, company/role separation, sanitized-name
collisions, traversal rejection, repeated application allocation, explicit resume,
fresh revision directories, and preservation of existing finished PDFs wherever
new executable behavior owns these rules.

Verify that failed or unreviewed rendering cannot publish a final PDF, published
bytes match the reviewed artifact, and removing a temporary fixture's supporting
folder leaves the final PDFs intact. Evidence checks must still resolve local
snapshots and reject escaping paths. Use fictional data only.

Exercise English, French, and bilingual workflow scenarios. Inspect every page
and extracted text of both language fixtures after implementation. Synthetic
fixtures validate mechanics; they do not establish real-candidate truth or prove
that an agent follows every behavioral instruction.

## Boundaries

- Always: preserve privacy, source evidence, canonical-profile approval gates,
  existing validation, fresh render/review directories, and honest review status.
- Ask first: migrating existing applications, replacing retained PDFs, deleting
  supporting files, or changing canonical profiles. Existing exact authorization
  applies without asking again.
- Never: auto-delete evidence, fabricate missing resume state, upload personal
  artifacts, put canonical sources in `supporting/`, or expose drafts as final.

Out of scope: CV content changes, automatic cleanup, existing-output migration,
job discovery, application submission, new language support, and a document UI.

## Success Criteria

- New applications follow company → role → PDFs plus `supporting/`.
- Only requested language PDFs appear in the role folder after successful review.
- Every other generated file is beneath `supporting/`.
- Multiple roles, applications, and revisions remain separate without data loss.
- Editable YAML and evidence stay usable until the user removes them.
- Removing `supporting/` leaves finished PDFs readable and canonical sources intact.
- Instructions, examples, synthetic fixtures, and relevant tests agree on layout.
- Existing render, review, evidence validation, and package privacy checks pass.

## Open Questions

No unresolved implementation questions. Repeat applications use numbered role
folders, final PDF revisions use unused numbered filenames, and existing folders
remain untouched. Final human review and real-candidate acceptance remain separate.
