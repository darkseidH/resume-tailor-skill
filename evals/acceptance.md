# Acceptance and Reproduction

## Deterministic Checks

Run from the repository root with the pinned Python environment:

```powershell
rtk proxy uv run --locked python -m unittest discover -s tests -v
rtk proxy uv run --locked python evals/run_synthetic.py .local/synthetic-new
rtk proxy uv run --locked python scripts/check_evidence.py .local/synthetic-new/english/cv.yaml .local/synthetic-new/english/evidence.json
rtk proxy uv run --locked python scripts/check_evidence.py .local/synthetic-new/french/cv.yaml .local/synthetic-new/french/evidence.json
rtk proxy uv run --locked python scripts/render_cv.py .local/synthetic-new/english/cv.yaml .local/synthetic-new/english/render-v1
rtk proxy uv run --locked python scripts/render_cv.py .local/synthetic-new/french/cv.yaml .local/synthetic-new/french/render-v1
rtk proxy uv run --locked python scripts/review_pdf.py .local/synthetic-new/english/render-v1/cv.pdf --output .local/synthetic-new/english/review-v1
rtk proxy uv run --locked python scripts/review_pdf.py .local/synthetic-new/french/render-v1/cv.pdf --output .local/synthetic-new/french/review-v1
```

Use a new root on each run. Inspect both languages' images and extracted text. The curated fixture application is reproducible mechanical verification, not an independent AI behavioral evaluation.

## Current Remediation Checks

The synthetic runner uses reviewed per-language claim snapshots in fixtures/*-claims.json. Section order does not determine evidence; changed or unmapped content fails until its evidence is reviewed. Unit regressions cover section reordering, summaries, changed wording, timeout diagnostics, malformed PDFs, and review overwrite protection.

Use fixtures/multi-role-profile.md as raw input for a fresh behavioral application. Keep simulated user decisions and generated artifacts in a new private evaluation workspace. Exercise role chronology, internship/employment distinctions, overlapping freelance work, all confirmed languages, summary depth, metric correction/rejection/skip/resume, and separate profile persistence decisions. Inspect every page of both languages and retain actual results.

## Behavioral Walkthroughs

Run the scenarios in onboarding.md, job-analysis.md, tailoring.md, profile-updates.md and job-intake.md. Record actual observations, especially failure paths. An independent evaluator should receive the skill and raw synthetic inputs without expected answers when such evaluation is available.

## Real User Acceptance

- [x] Mapped user sources are read and uncertainties surfaced.
- [x] Actual supplied job URL is fetched and retained without title/source mismatch.
- [ ] Material ownership, chronology, proficiency and contact details are confirmed.
- [ ] The user reviews the match analysis and selects language/template.
- [ ] A truthful CV is rendered and factually, visually and textually reviewed.
- [ ] Only explicitly approved canonical profile edits are applied.
- [ ] The user reviews the resulting application.

Human-dependent items must remain pending until they actually occur. Implementation completion is separate from the final real-application acceptance.
