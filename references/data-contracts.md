# Profile and Application Data Contracts

## Profile Map

The map records a private workspace, source files with stable IDs and coverage, and optional language/template preferences. A source can cover several areas. Resolve relative paths against the map's directory; do not silently search unrelated directories for personal information.

The suggested local layout is `.local/profile-map.md`, `.local/profile/`, and `.local/applications/`. These paths are ignored by this repository. A user may instead map an external private directory. Check the destination before writing; `.gitignore` prevents ordinary Git inclusion, not disclosure by other means. Templates contain fictional examples only.

## Evidence Record

Each extracted fact has:

| Field | Meaning |
|---|---|
| Fact ID | Stable identifier, such as `fact-api-component` |
| Statement | Narrow assertion supported by the cited material |
| Context | Role/project and professional, academic, or personal provenance |
| Ownership | Confirmed contribution; otherwise unknown |
| Status | `supported`, `unconfirmed`, or `conflicting` |
| Evidence | Source ID, path, heading, and short identifying excerpt; line numbers are optional |
| Confirmation | User's explicit answer when needed, with a session/answer ID |

`supported` means an explicit source statement or unambiguous user confirmation supports the assertion; it is not independent employment verification. `unconfirmed` means the assertion cannot yet be made. `conflicting` retains every incompatible source and the question needed to resolve it. A missing statement never proves the candidate lacks a skill.

Assign identifiers once and retain them when wording changes. When a source changes, relocate its heading/excerpt and recheck support before reusing the fact. If evidence cannot be located, mark it unconfirmed. Keep facts narrower than their evidence: implementing an endpoint does not establish deploying a service, leading a team, or owning the entire system.

## Session Answers and Profile Updates

Record each confirmed answer in the private application record with an answer ID, question, the user's answer, and supported fact IDs. For profile-only onboarding, use a private onboarding record under the mapped workspace. Saving these answers preserves session evidence; it does not update the reusable profile.

Compare new facts with the mapped canonical sources. For additions or corrections, prepare and present the exact source edit at the current clarification topic's profile-update checkpoint. Once approved, write the canonical edit and verify it immediately. An answer already represented accurately in the source needs no duplicate edit; record that comparison result instead. Every new reusable fact must end as applied-and-verified, declined, deferred/pending, or already-present, never silently stop at application-only storage.

Before a canonical update, present the target path and section, existing wording, proposed wording, and supporting answer. Apply only the approved change. Declining persistence leaves the source unchanged and does not invalidate confirmed facts for the current application. Preserve unresolved conflicts rather than choosing a convenient version.

## Application Record Contract

Allocate `<mapped-output>/<company>/<role>/` during intake with `scripts/application_artifacts.py allocate`. Names are readable Windows-safe labels, not supplied paths. Different labels that sanitize alike and repeated applications receive unused numbered folders; company directories are reused only when their recorded original company matches. Ask for missing labels. Record the absolute application root and labels in `supporting/application.json`.

Reuse this root throughout analysis, quantification, tailoring, and delivery. Only reviewed final PDFs (`resume-en.pdf`, `resume-fr.pdf`, then unused `-v2` names) and `supporting/` belong directly in the role folder. All other artifacts live inside supporting. Save shared job.md, answers.md, match.md, tailoring.md, verification.md and approval records there. Keep each language revision's cv.yaml, evidence.json and sources/ together in `supporting/revisions/en-v1/` or `fr-v1/`; render/ and review/ also live inside that revision. Each ledger's source paths remain relative to its own directory.

Generate only requested languages. Allocate a fresh revision with `scripts/application_artifacts.py revision ROOT en` (or fr). Retain prior revisions and final PDFs. On explicit resume, load the recorded root, original job snapshot, answers and decisions; do not allocate a replacement. Legacy root-level job.md applications retain their original layout. If supporting is missing, report the loss and recover required inputs before continuing; do not infer saved answers or review results from a PDF.

Deletion of supporting is a user action, never automatic. It removes editable YAML, evidence and resume state but leaves delivered PDFs readable. Keep canonical profile sources outside supporting. Keep:

- Original job text, source URL when supplied, retrieval date for URLs, and completeness notes.
- Requirements with IDs, required/preferred status, and evidence-based assessments.
- Fact references and a snapshot of the evidence used, preserving the background at generation time.
- Clarification answers and any separately approved profile changes.
- Match report, gaps, practical suggestions, and tailoring decisions.
- Editable RenderCV YAML, final PDF, and recorded factual, visual, and extracted-text checks.

Requirement assessments are `strong`, `partial`, `unknown`, or `confirmed gap`. These describe job fit, separately from evidence status. An unmentioned skill is unknown until clarified; a confirmed gap requires an explicit answer or confirmed facts establishing a mismatch. Weak points describe application risks and must cite their evidence.

## Fictional Evidence Walkthrough

Source `experience-notes`, heading `Inventory API`, says: "As part of a team of three, I implemented the stock lookup endpoint using PostgreSQL."

- `fact-stock-endpoint`: implemented the stock lookup endpoint using PostgreSQL; professional team project; ownership limited to the stated endpoint; supported by that excerpt.
- Service deployment: unknown. Ask whether the candidate deployed it and which deployment tasks they handled.
- Sole ownership of the API: unsupported. Retain team context; ask before expanding the contribution.
- User answer `answer-01`: "I deployed the service to our staging server, but another developer deployed production."
- A new fact can support staging deployment with `answer-01`; production deployment remains outside the candidate's confirmed contribution.
- Propose adding the staging detail to the mapped source. Save it only after approval. Without approval, use it only within the current application/session.

This walkthrough checks the contract's source traceability and ownership boundaries; it is not an independent behavioral evaluation of the skill.
