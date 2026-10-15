# Artifact Storage Verification

Date: 2026-10-14. Scope: SPEC-artifact-storage.md, tasks AS1–AS7.

## Observed Results

- Baseline: 21 tests passed before changes. Current suite: 35 tests passed,
  including real Windows junction rejection, with no skips when run elevated.
- Allocation: readable company/role roots, repeated application numbering,
  sanitized-label collision separation, reserved Windows names, invalid labels,
  original-label/root records, and fresh language revisions passed regression tests.
- Resume: original job bytes retained; legacy root-level job.md remains in place;
  deleting supporting reports missing state without recreating it.
- Delivery guard: pending/failed/unavailable review, stale PDF/YAML hashes,
  mismatched revision language, missing evidence/PDF, and failed copying do not
  expose a finished PDF. Numbered deliveries preserve earlier bytes.
- Fresh real renders: English-only, French-only, and bilingual applications
  produced four one-page PDFs under `.local/artifact-storage-e2e-3/`.
- All four page images and their extracted text were inspected. No clipping,
  overlap, broken accents, top note, footer, or missing substantive fixture content
  was observed. Role/title/date fields, languages, staging-only contribution, and
  academic provenance match the fictional profile and simulated answers.
- Evidence coverage passed for each language revision. Factual comparison was
  performed against `fixtures/profile.md` and `fixtures/answers.md`; this verifies
  fictional wording, not real employment or an actual candidate's background.
- Final PDFs were delivered through the actual publish CLI and matched the
  reviewed bytes. Role directories contain requested PDFs plus supporting only.
- A disposable copy's supporting folder was deleted after resolved-path checks.
  Both bilingual PDFs remained byte-identical and readable; the canonical
  fictional source hash stayed unchanged. No personal files were used or deleted.

## Failures Preserved and Repairs

- Default uv cache writes were denied in the sandbox. Verification used
  `uv --cache-dir .uv-cache run --locked ...` without changing dependencies.
- Git index writes, real Typst rendering, and Windows junction creation required
  elevated execution. Authorized elevated runs succeeded.
- `.local/artifact-storage-e2e-1/` retains the failed sandbox render and its log.
- `.local/artifact-storage-e2e-2/` exposed an existing fixture mismatch: page notes
  and footers were enabled despite the skill's existing rule. Both YAML fixtures
  now contain the documented false settings, with a regression check. Fresh
  renders in e2e-3 passed. No CV claim wording or RenderCV integration was changed.

## Reproduction

Run the commands in [acceptance.md](acceptance.md) with an unused private output
directory. Use `--languages en`, `--languages fr`, or the default bilingual mode.
Run the full unittest suite elevated on Windows if junction creation is denied:

```powershell
rtk proxy uv --cache-dir .uv-cache run --locked python -m unittest discover -s tests -v
```

Review every page, extracted text and claim before setting review fields to
passed. `review_pdf.py` creates hashes and pending statuses; it never approves
factual or visual review automatically. The publish helper rechecks evidence
coverage and exact content identity; review_notes records the actual assessment.

## Limits

These are curated fixture mechanics and a same-agent scenario walkthrough, not
an independent agent behavior evaluation. All rendered fixtures are one page;
multi-page real applications still require every-page review. Final human review,
global installation, and historical real-user acceptance remain separate.
Context7 tools were unavailable; the fixture correction reused the existing
documented page rule and was verified with pinned RenderCV 2.8. No library/API
integration change was needed. CodeGraph was uninitialized and the user selected
continuation without indexing.

## Distribution

- Built `.local/dist/resume-tailor-artifact-storage-v1.zip` using the existing
  packaging allowlist; no packaging implementation change was needed.
- All 27 archived resources match current source bytes. The new storage helper
  is included; private outputs, plans, tests, evaluations and caches are excluded.
- Extracted to `.local/artifact-storage-package-1/extracted/resume-tailor-skill/`.
  The system skill validator returned `Skill is valid!`.
- Executed the extracted allocation, revision, evidence, render, review and publish
  CLIs using the pinned project interpreter. English/French each rendered one page;
  both images and extracted texts were inspected and claims checked against the
  same fictional inputs before approval was recorded.
- Packaged final PDFs matched their reviewed bytes. A disposable supporting
  deletion check again retained readable, unchanged PDFs and the canonical source.
- Global installation and real-user acceptance were not performed or claimed.
