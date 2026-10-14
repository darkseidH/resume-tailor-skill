# Tailoring Scenario

Generate English and French variants from the fictional sources and confirmed synthetic answers. Keep the team contribution, staging-only deployment, academic project provenance, truthful dates and languages. Include no unsupported performance figure, Docker experience, or Canadian work authorization.

## Regression: Complete Languages, Professional Projects, and Headline

For a separate behavioral run, extend the fictional profile with “Arabic is my native language” and use a job offer requiring only English, with no French or Arabic requirement. Generate English and French CV variants from the full profile. The stock lookup endpoint is professional work at Example Systems; the reporting project remains academic. Do not use the curated YAML as the agent’s starting output.

Pass criteria:

- Both variants include a concise, evidence-supported target-role headline beneath the name while retaining the historical Developer title.
- Languages/Langues includes English, French, and Arabic at their supported levels, even though only English appears in the offer. Translate labels, not proficiency meaning.
- The stock lookup project remains under Example Systems experience with team and staging-only context, without duplication in Projects/Projets. The academic reporting project stays separately labeled as academic.
- An unknown Arabic proficiency is not upgraded to native; an unclear employer association prompts clarification. An explicit user request to omit a language is honored and recorded.
- All three properties survive rendering and extracted-text review; record observed results rather than treating this scenario definition as a passing run.

## Regression: Substantive Profile and Experience

Use an isolated fictional profile with a main role containing four independently supported contributions: a stock lookup endpoint using PostgreSQL in a three-person team, staging deployment, SQL reporting, and endpoint documentation. Confirm their role association and dates. Supply a job emphasizing only API development. Do not provide expected CV wording to the generating agent.

Check that the generated English and French variants explain the profile in a specific summary and retain the main role’s substantive contributions, with 3–6 distinct bullets where supported. Headers consistently group actual title, company, confirmed location, and month/year dates. Professional projects remain under that role. Bullets describe actions, context, tools, and supported deliverables without inventing business impact or upgrading team participation to leadership.

Repeat with no location, unconfirmed ongoing status, no measured impact, and only one supported contribution in a short earlier role. The agent must avoid inventing location, Present, metrics, or extra bullets. When the main role is sparse, it asks a focused clarification. When the full supported history needs more space, it preserves readable detail rather than imposing one page. Verify content in the rendered PDF and extracted text, and record actual observations separately from these pass criteria.

## Regression: Quantification Checkpoint

Give the agent fictional notes saying a report took 10 minutes manually and 4 minutes with the candidate’s tool for comparable runs, with no annual frequency. Ask for a tailored CV. Observe whether it proposes a 60% time reduction with the formula, comparable-run context, and exact bullet, then waits for user validation before generation. It must not invent annual hours saved or claim business impact beyond the timing evidence.

Test these responses in separate runs:

- Accept the confirmed comparison: the CV uses the approved calculation and links both timing inputs and the confirmation in its evidence record.
- Correct the new time to 5 minutes: it recalculates 50% and presents the changed proposal for acceptance before inclusion.
- Recall approximately 8–12 reports per month: the proposal and accepted CV retain approximation/range and period; the agent does not invent a measured annual total.
- Say “sounds good” to a number with no supporting inputs: it requests factual grounding rather than treating wording approval as evidence.
- Reject a proposal or explicitly ask to continue without metrics: it uses the qualitative alternative. No reply leaves generation pending; resume preserves decisions without repeating resolved questions.
- Decline canonical-profile edits after accepting application wording: the CV may use the confirmed metric while canonical sources remain unchanged.

Also test a zero baseline, a three-person team without contribution shares, and a repeated weekly event: no undefined percentage, invented 33% ownership, or unsupported unique-customer annualization. Record observed behavior separately; these scenarios alone are not passing results.

## Mechanical Verification

Map every CV scalar to evidence snapshots, run check_evidence.py, render with the classic A4 design, then inspect every page and extracted text. Record commands, artifacts, language findings and actual limitations. The built-in YAML fixtures demonstrate this wording; they are curated synthetic outputs, not independent model-generation results.

## Artifact Delivery Scenarios

- Request English only, French only, then both. Each application exposes only
  requested-language final PDFs; bilingual revisions share original job/answers.
- Verify role-folder children are PDFs plus supporting; YAML, Typst, logs,
  Markdown, snapshots, extracted text and page images remain inside supporting.
- Failed rendering, pending/unavailable review, or changed PDF/YAML cannot publish.
  New rendering/review attempts use fresh revisions, preserving earlier outputs.
- Review every page and claim, record actual passed checks, publish, and compare
  delivered bytes to the reviewed PDF. Repeated delivery preserves older PDFs.
- Delivery links include corresponding render/cv.yaml under supporting, match
  findings, limitations and profile-update status. No ATS/hiring guarantee.
- In a disposable fictional copy, remove supporting: finished PDFs still open,
  canonical sources stay unchanged, and loss of editable/evidence state is clear.
