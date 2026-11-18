# Acceptance and Reproduction

## Deterministic Checks

Run from the repository root with the pinned Python environment:

```powershell
rtk proxy uv run --locked python -m unittest discover -s tests -v
rtk proxy uv run --locked python evals/run_synthetic.py .local/synthetic-new
rtk proxy uv run --locked python scripts/check_evidence.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/cv.yaml" ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/evidence.json"
rtk proxy uv run --locked python scripts/check_evidence.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/cv.yaml" ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/evidence.json"
rtk proxy uv run --locked python scripts/render_cv.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/cv.yaml" ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/render"
rtk proxy uv run --locked python scripts/render_cv.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/cv.yaml" ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/render"
rtk proxy uv run --locked python scripts/review_pdf.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/render/cv.pdf" --output ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/en-v1/review"
rtk proxy uv run --locked python scripts/review_pdf.py ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/render/cv.pdf" --output ".local/synthetic-new/Fictional Employer/Backend Developer/supporting/revisions/fr-v1/review"
```

Use a new root on each run. Add `--languages en` or `--languages fr` to the synthetic builder for single-language scenarios; its default creates both under one application. Keep all render/review outputs inside supporting. Follow references/output-review.md to record genuine review decisions and publish PDFs only afterward. See artifact-storage.md for storage-specific observations. Inspect both languages' images and extracted text. The curated fixture application is reproducible mechanical verification, not an independent AI behavioral evaluation.

## Current Remediation Checks

The synthetic runner uses reviewed per-language claim snapshots in fixtures/*-claims.json. Section order does not determine evidence; changed or unmapped content fails until its evidence is reviewed. Unit regressions cover section reordering, summaries, changed wording, timeout diagnostics, malformed PDFs, and review overwrite protection.

Use fixtures/multi-role-profile.md as raw input for a fresh behavioral application. Keep simulated user decisions and generated artifacts in a new private evaluation workspace. Exercise role chronology, internship/employment distinctions, overlapping freelance work, all confirmed languages, summary depth, metric correction/rejection/skip/resume, and separate profile persistence decisions. Inspect every page of both languages and retain actual results.

## Behavioral Walkthroughs

Run the scenarios in onboarding.md, job-analysis.md, tailoring.md, profile-updates.md and job-intake.md. Record actual observations, especially failure paths. An independent evaluator should receive the skill and raw synthetic inputs without expected answers when such evaluation is available.

For page balance, render a multi-page CV with a large lower-page gap followed by substantive content. Follow references/output-review.md#page-balance to adjust grouping or section order, then inspect all pages and extracted text. Pass when avoidable gaps are resolved with complete content, readable typography, intact chronology and no stranded headings or awkward splits. A naturally shorter final page is acceptable. Exercise both English and French; record any language not checked.

## Real User Acceptance

- [x] Mapped user sources are read and uncertainties surfaced.
- [x] Actual supplied job URL is fetched and retained without title/source mismatch.
- [ ] Material ownership, chronology, proficiency and contact details are confirmed.
- [ ] The user reviews the match analysis and selects language/template.
- [ ] A truthful CV is rendered and factually, visually and textually reviewed.
- [ ] Only explicitly approved canonical profile edits are applied.
- [ ] The user reviews the resulting application.

Human-dependent items must remain pending until they actually occur. Implementation completion is separate from the final real-application acceptance.

## Blind tailoring comparison

Use fixtures/comparison-profile.md and exactly one comparison posting per independent session. A test operator answers questions using fixtures/comparison-answers.md. Give generation sessions only the installed skill variant, selected posting, profile and replies actually elicited. Keep this protocol and its expected evidence outside their context. Use a clean workspace and the same model settings and interaction budget throughout. Run baseline and updated skill copies for both jobs, requesting English for backend and both languages for reporting.

For each posting, randomly order the CVs and redact file paths or labels that reveal the skill version. Give the reviewer the offer, source notes and exact answers for each anonymous application. Record page-one evidence, questions asked, omissions, semantic support and preferences or ties before revealing the version labels. Read every page and check the English/French facts. Record version, model, visible evidence and limitations in results.md.

Evaluator only. For backend, look for the personal endpoint contribution with Python, SQL and PostgreSQL, preserving team and staging boundaries. For reporting, look for the Power BI dashboard, SQL source, Excel reconciliation and the audience or use if elicited. An unanswered audience question does not authorize an invented audience. Both roles must preserve chronology, credentials and provenance. An unsupported claim or material bilingual discrepancy fails even when the layout is preferred. Report results per posting and leave comparative improvement unverified when a matched blind run is unavailable.
