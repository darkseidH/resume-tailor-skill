# Verification Results

Date: 2026-10-13.

## Implementation and Deterministic Checks

- RenderCV 2.8 and all rendering/review dependencies installed in a project-local .venv. Dependencies are now managed by uv in pyproject.toml and uv.lock, preserving the tested versions. Sandbox DNS blocked the first download; an approved escalated install succeeded.
- Twelve unittest checks passed: prior-output preservation, renderer failures, missing PDF, missing identity, malformed design, complete evidence references, missing claims, unsupported facts, stale pointers, changed excerpts, source containment, and packaging exclusions/overwrite refusal.
- `python -m compileall -q scripts tests evals/run_synthetic.py` passed.
- Codex skill-creator's quick_validate.py passed after PyYAML became available.
- All relative resource links resolve.
- Two complete synthetic application records were created under .local/synthetic-v1; each has original job/answer snapshots, evidence ledger, match analysis, tailoring decisions, YAML, PDF and verification notes.
- Both evidence ledgers passed check_evidence.py. Both PDF variants rendered successfully; each has one page and extractable text.
- Every page was visually inspected. The initial classic degree column split Bachelor/Licence; increasing degree_width to 2cm fixed it. Final variants show no clipping or broken degree labels. Extracted text retains accents, dates, staging-only deployment and academic provenance.
- Windows sandbox denied Typst access even after local scratch isolation. Approved escalated rendering succeeded. The helper preserves failure diagnostics and requires a fresh revision directory for retry.

## Behavioral Evidence

See walkthrough-results.md for self-reviewed onboarding, job classification, unsupported-metric, approval, URL fallback and malicious-content branches. They are worked examples, not independent fresh-context model evaluations.

Private native-tool simulations verified exact approved insertion, no declined change, and detection of a concurrently changed before-state. A first shell attempt used an unavailable hashing cmdlet; a Python byte/hash check replaced it successfully.

## Real Application Check

Live URL intake and candidate clarification were exercised in a private application. Candidate details and original verification notes are retained in the ignored private workspace. Real CV generation, output preferences, and final human acceptance remain pending. No profile upload, outreach, or application submission occurred.

## Package Verification

The prior ZIP .local/dist/resume-tailor-skill-v2.zip contained 24 distributable files and excluded .local, .venv, applications, tests and evals. Its extracted copy passed quick_validate.py and evidence checks. The current uv-based package is .local/dist/resume-tailor-skill-v3.zip, replacing requirements files with pyproject.toml, uv.lock and .python-version. The package uses an allowlist, so private source files and real application records are never included.

## uv Migration (2026-10-13)

- Direct dependencies moved to pyproject.toml; uv generated uv.lock using the previous pins as migration constraints. The project uses Python 3.12 and does not install itself as a Python package.
- Removed requirements.txt and requirements-lock.txt; updated setup, execution and evaluation instructions to uv sync --locked and uv run --locked.
- Offline locked synchronization passed; all twelve tests passed through uv run, including archive inclusion of the uv files and exclusion of legacy requirements files.
- uv lock --check --offline passed. The rebuilt v3 archive contains 25 files, includes the manifest/lock/Python version, excludes requirements and private data, and its extracted skill passes quick_validate.py.
- Commands in this Windows sandbox use `--cache-dir .local/uv-cache` to avoid the restricted default cache. Normal installations can use uv's default cache.
- Context7 was unavailable; official uv project and synchronization documentation was consulted instead: https://docs.astral.sh/uv/guides/projects/ and https://docs.astral.sh/uv/concepts/projects/sync/.

## Profile Persistence Correction (2026-10-14)

The user reported that a real test retained answers only in the application. Inspection found stale data-contract text instructing conversation-only storage and a late workflow position for profile updates. Removed the stale increment language and introduced a checkpoint during onboarding and job-analysis clarification topics: save answers, compare reusable facts with canonical sources, present exact edits, obtain approval, then apply and reread immediately. Report applied-and-verified, already-present, declined, or pending outcomes explicitly; application-only storage does not count as an approved profile update.

Added a fresh-session regression in evals/profile-updates.md for dates and sole project ownership, approval/write verification, reuse in a later session, and decline preservation. This behavioral regression still needs a fresh tester run; structural checks do not prove instruction compliance. The standard skill validator and resource-link checks passed. The v5 ZIP was rebuilt and checked to contain the current instructions while excluding private data and evaluation artifacts. No actual candidate source was edited by this correction.

## Limitations

- Independent agent behavioral evaluation was unavailable.
- Live accessible URL intake was exercised; unavailable and malicious branches were self-reviewed simulations.
- Final user review and approved real canonical edits cannot be marked complete until the user actually supplies the relevant decisions.
- No Git repository exists, so increments are saved without commits. No global skill installation was performed.

## Audit Remediation Verification (2026-10-14)

Implementation was authorized through incremental-implementation. Tasks 9–14 are implemented; behavioral and distribution results below are recorded separately. Existing real-user acceptance remains pending.

- Synthetic evidence is mapped through per-language reviewed scalar snapshots, not section position. A changed value or missing/extra claim fails explicitly. Added supported English/French summary fixtures and title-first experience template configuration.
- Red/green evidence: initial tests reproduced wrong facts after section reversal, missing summary, and silent evidence reuse after a headline change. The repaired tests pass. Direct-script execution is also covered.
- Application stages now reuse one intake root and preserve job/answer/approval records. Output preferences and provisional content selection precede exact metric proposals; accepted claims changed materially require review again.
- Timeout regressions initially reproduced missing render.log with text, bytes, and absent captured output. The helper now preserves diagnostics and re-raises the timeout.
- Invalid/truncated PDF CLI regressions initially produced unhandled parser tracebacks. Expected parser errors now yield a nonzero diagnostic; blank pages and existing review directories still fail safely. A valid two-page PDF produces both page images and pending review metadata.
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`: **21 tests passed**.
- `.venv/Scripts/python.exe -m compileall -q scripts tests evals/run_synthetic.py`: passed.
- The standard skill validator and local reference-link checks passed.
- English and French simple examples rendered under `.local/layout-review-7weyt4v1/`. Both one-page PDFs were visually inspected and extracted text checked: title precedes employer, profile summary is present, no clipping observed.
- Context7 was unavailable. Layout configuration was verified against official RenderCV design documentation and the installed pinned 2.8 schema, then tested in actual renders; dependencies were not changed.
- RTK was unavailable and shell process creation had failed in this environment. Verification used the existing project Python executable through the process runner. No Git repository exists; a private source baseline was saved instead of commits. No real candidate source was edited.

### Fresh-Context Behavioral Application — Observed

A separate application agent used only the raw fictional multi-role profile, its map, and fictional job text under `.local/behavior-review-Dozj2i/`, without expected CV YAML or audit answers. The parent supplied explicitly simulated user decisions at the agent's actual checkpoints.

- The agent paused for profile/match review, then prepared exact English/French quantification proposals before generation.
- A correction from 4 to 5 automated minutes per report superseded 60% with a recalculated 50%; the agent presented both revised bullets and waited for acceptance.
- Application use was accepted while the canonical correction was declined. The mapped fictional source remained byte-for-byte equal to its original snapshot (SHA256 `b40d77b6b0a373af24769d6b2b3e710842e7d754b74aa2321490caa1172c7eb2`).
- Both reviewed revision-2 CVs have **2 pages**, **5 distinct roles**, and **76 scalar evidence pointers**. Parent independently reran evidence checks and confirmed ordering: ongoing BI employment, BI internship, analyst employment, overlapping part-time freelance work, earlier support employment.
- Both variants retain English, French and Arabic; employer work stays under its role, and personal/academic work is separately labeled. The summaries explain the professional profile; the current role and internship each have five substantive bullets.
- The generating agent and parent inspected all four final revision-2 page images. No clipping or overlap was observed; extracted text preserves substantive content and accents, with ordinary line-break hyphenation and icon glyphs noted.
- Rendering exposed a date-precision issue: year-only project dates initially became January. The agent retained that prior render, corrected the new revision to supported years in project headings, and the shared rendering instructions now explicitly prevent invented months.
- Rejected annualized savings and team contribution shares were not added. These are fictional evaluation results, not real-user acceptance or independent employment verification.

Observed artifacts: `applications/example-reporting-bi/en/render-v2/`, `fr/render-v2/`, both `review-v2/` directories, evidence-en-v2.json, evidence-fr-v2.json, answers.md, profile-update.md, and verification.md beneath the private behavioral workspace. Resume/rejection/skip and approved fictional persistence are being exercised in a further revision.

### Resume, Rejection/Skip, and Approved Fictional Persistence — Observed

The same application agent received an explicit simulated revision request to reject q-02 for the new variant, skip time-impact quantification, and separately approve the exact previously reviewed fictional source correction.

- It reused the same application root without repeating resolved intake questions and generated English/French **render-v3** and **review-v3**, two pages per language.
- The qualitative variants omit the 50%/10→5 impact claim while retaining the full five-role history, both projects, and all three languages. Historical q-02 acceptance still applies to the preserved v2, with rejection/skip recorded for v3.
- The newly authorized canonical edit changed only the reviewed 4-minute timing to 5 minutes in the isolated fictional source. It was reread and checked against the before-state; all other text remained unchanged. Before/after snapshots and the override of the earlier decline are recorded.
- New fictional canonical SHA256: `786c832d0cb439712124ca7f3e720ced65891006cd8e3d252a74e85278831421`.
- Prior v2 PDFs/YAML/ledgers have identical before/after hashes in preservation-v3-after.json. English v2 PDF: `3c4cb1cea0cb1fb585697765abed581653d9bdfa03db3e6d9b4da2834ed6ea07`; French v2 PDF: `1a22c2a3e2d9b79a16f9199cd7754647265e598aef5f04d0e89a9b63fa76c5f3`.
- The generating agent inspected all four v3 page images and both extracted texts. Details are in verification-v3.md. No real candidate files or external accounts were touched.

### Supplemental Behavioral Boundaries — Observed

- An added role with unknown dates/ongoing status created a separate pending application branch. The agent asked for dates/current status and generated no CV or canonical edit, rather than inventing Present or silently ordering it.
- Approximate scope: proposed “approximately 8–12 reports per month” / “environ 8 à 12 rapports par mois”, preserved the range and period, and waited for validation. No annual total or unique count was inferred.
- Zero baseline: declined to compute a reduction percentage from 0 to 4 minutes and asked what zero represented and whether the runs were comparable. No timing CV claim was produced.
- Unsupported approval: omitted a liked-but-unsupported 90% savings figure despite wording approval, and proposed a supported qualitative alternative for validation.
- Each isolated branch retained its actual input, response, source context, and pending state beneath the same private behavioral workspace. Pending input in these negative test cases is the expected observed boundary, not unfinished real-user work.

Task 15 behavioral checks are complete for the scoped remediation. Broader model reliability, external factual verification, and the original real-user application acceptance are not established by these runs.

### Current Distribution Verification

Built `.local/dist/resume-tailor-skill-v6.zip` after remediation. It contains **26 distributable files**, including the current quantification reference and repaired helpers. SHA256: `37515275241e72497c3f81d9110f503dfc7709456329348561ae8599d256d6e6`.

Every archived resource was compared byte-for-byte with the current source. Private workspaces, candidate applications, environments, tests and evaluation fixtures are excluded. Previous archives were preserved. The archive was extracted into `.local/distribution-check-v6-65xpqwx2/`; that copy passed the standard skill validator, both fictional evidence checks, both two-page renders, and both PDF text/image extraction runs using the existing pinned project runtime. This checks extracted code, not a newly provisioned environment.

Detailed machine results: `.local/distribution-check-v6-65xpqwx2/verification.json`. The final independent implementation-review agent is now inspecting source, test coverage, the archive, and the extracted render pages. Its outcome will be recorded separately; no clean-review claim is made before it returns.

### Final Independent Review — Complete

A separate fresh-context review agent returned **no actionable findings** and approved shipping the scoped remediation. It independently ran all 21 tests, verified all 26 archive resources against current source and the recorded SHA256, inspected all four packaged page images and complete texts, reran both extracted evidence checks, and reviewed actual approval/persistence records.

Full report: [implementation-review.md](implementation-review.md). Tasks 9–16 are implemented and verified. Original human checkpoint reviews and the real-user application acceptance remain pending; no global installation or fresh dependency provisioning was performed.

## Company and Role Artifact Storage (2026-10-14)

AS1–AS7 completed. See [artifact-storage.md](artifact-storage.md) for actual observations.
35 tests pass (no skips with elevated Windows junction tests). English-only,
French-only and bilingual source applications and both extracted-package languages
were rendered, factually reviewed against fictional sources, visually inspected on
every page, text checked and delivered with identical bytes. Supporting cleanup was
verified on disposable copies only. New archive: `.local/dist/resume-tailor-artifact-storage-v1.zip`,
27 resources matching source, private files excluded, system skill validation passed.
Existing real-user acceptance and human reviews remain pending; no global install.
