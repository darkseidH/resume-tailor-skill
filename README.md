# Resume Tailoring AI Skill

An agent skill for building a professional profile from Markdown notes, analyzing job fit, clarifying missing facts, and producing truthful English or French CVs through RenderCV 2.8.

## Use

Invoke the skill with the paths to your profile notes, then supply a pasted job offer or posting URL. The agent builds a usable profile, clarifies material uncertainties, reviews the match, and confirms language/template before selecting content. It then presents evidence-backed metric proposals for your validation before generating the CV. Accept, correct, reject, or explicitly skip proposed metrics; approximate values stay labeled, and an unmeasured contribution can remain qualitative. Profile updates require approval of the exact proposed edits.

Confirmed answers are saved in the private application/onboarding record. When they add reusable background facts, the agent presents exact edits to your mapped profile at the end of the clarification topic. After approval, it writes and verifies those edits immediately. The final summary distinguishes applied profile updates from declined or pending proposals; saving answers alone does not count as updating your profile.

Tailored CVs include a supported target-role headline, a specific professional summary, and every confirmed spoken language, including those absent from the offer. Experience uses title-first headers and reverse chronological roles, with substantive action/context/result bullets and enough readable space to explain the background. Professional projects belong under their corresponding work experience; separate project sections preserve academic, personal, or open-source provenance.

You do not need to create a job.md file. The agent creates it for each application from your offer. If the URL cannot be read, it asks for pasted text, a supplied job file, or your description of the role; it waits for your input and records missing details honestly. Files in evals/fixtures/ are for explicit testing only and are never fallback job offers for real applications.

Example: “Use $resume-tailor-skill with my profile map at `.local/profile-map.md`. Analyze this job offer, clarify uncertainties, and tailor a French CV.”

## Install

Extract the distribution's `resume-tailor-skill` directory into your agent's skills directory. For Codex, the default personal location is `~/.codex/skills/resume-tailor-skill`. The package includes SKILL.md, references, templates, helper scripts, metadata and pinned dependencies. Install into the chosen location deliberately; the build process does not modify your global skill collection.

Set up Python 3.12+ and dependencies inside the extracted skill directory:

```powershell
rtk proxy uv sync --locked
```

Dependencies are declared in `pyproject.toml` and resolved in `uv.lock`; `.python-version` selects Python 3.12. Use `uv add` or `uv remove` to change dependencies and `uv run --locked` to run helpers. See the [official uv project guide](https://docs.astral.sh/uv/guides/projects/). If RTK is unavailable in another environment, use the command following `rtk proxy` directly. Run commands from the installed skill directory; candidate sources and outputs can live in a separate private workspace. Relative map paths resolve against the map, not the skill installation.

## Private Data

Start from templates/profile-map.md and map existing narrative notes. Suggested local locations are `.local/profile/` and `.local/applications/`; these are ignored by Git and excluded from the package. Git exclusion does not encrypt data or grant permission to upload it. Use only fictional data in distributable examples.

Keep alternate local workspaces under `.local-*/` (for example, `.local-test/`); these are also ignored. Source, tests, fictional fixtures, and the dependency lockfile belong in Git. Local environments, caches, generated packages, and candidate application records do not.

## Verification Commands

From the repository root:

```powershell
rtk proxy uv run --locked python -m unittest discover -s tests -v
rtk proxy uv run --locked python scripts/check_evidence.py APPLICATION/cv.yaml APPLICATION/evidence.json
rtk proxy uv run --locked python scripts/render_cv.py APPLICATION/cv.yaml APPLICATION/render-v1
rtk proxy uv run --locked python scripts/review_pdf.py APPLICATION/render-v1/cv.pdf --output APPLICATION/review-v1
rtk proxy uv run --locked python scripts/package_skill.py .local/dist/resume-tailor-skill.zip
```

Application rendering and review directories must be new. Inspect every page image and extracted text; review semantic support for each claim manually. The evidence checker verifies coverage and source excerpts, not the truth or adequacy of the wording. Tests and evaluation fixtures live in the development repository and are excluded from installation packages.

See evals/acceptance.md and evals/results.md for scenarios, observed verification, and pending real-user acceptance. Windows Codex may need approved elevated execution for Typst rendering. A failed render is recorded as failure, never as a successful final CV.

## Boundaries

The initial renderer supports built-in templates without photos. The skill performs qualitative job analysis; it does not guarantee ATS ranking or interviews. Job discovery, submitting applications, outreach, LinkedIn editing and multi-user/web interfaces are outside scope.
