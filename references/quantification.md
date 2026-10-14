# Quantification Review Before Generation

Run this checkpoint after job-match review, language/template confirmation, and provisional selection of substantive roles and projects, but before final CV generation/rendering. Review the selected contributions and propose exact bullets in the chosen CV language. Use the full profile and saved answers; do not ask again about metrics already confirmed with the same context. Present useful opportunities even when no business-impact figures are available.

## Discover Defensible Metrics

Look for scope (reports, endpoints, datasets, users, team size), volume (records, tickets, transactions), frequency (daily/weekly/monthly), time (task duration or response time), quality (errors, accuracy, test results), and money (documented budgets or savings). For data/AI work, distinguish evaluation-dataset results from production performance and identify the metric, dataset size, split, and baseline when available. Team size describes context; it does not establish leadership or an equal share of output.

Ask one focused question at a time about the most useful missing input: what was counted, over which period, measured how, and what portion was the candidate’s contribution? Ask for before/after values only when a real comparison exists. Respect confidentiality: a percentage or range can still disclose restricted information. If the user cannot disclose it, retain a safe qualitative description.

## Measured, Calculated, and Approximate Values

- **Measured:** quote the source or explicit answer with units, period, scope, and attribution.
- **Calculated:** show the formula and confirmed inputs. A reduction from 10 to 4 minutes is `(10 - 4) / 10 × 100 = 60%`; confirm that both timings concern comparable work before proposing the claim. A zero baseline cannot support a percentage change.
- **Approximate:** use only a grounded user recollection or an explicit calculation from supported approximate inputs. Preserve “approximately/environ” or a defensible range in the CV; do not silently turn an estimate into an exact result. Use “at least/X+” only when a genuine lower bound is established.

Never choose a plausible number, arbitrarily discount a guess, or infer a contribution percentage from team size. Annualizing a weekly count requires confirmation of active weeks and whether the count measures distinct items or repeated events. Hypothetical extrapolations are proposals, not observed annual results. Do not attach an unmeasured downstream benefit to a measured activity. Every bullet need not contain a number.

## Present and Resolve Proposals

Record proposals in the Quantification Review section of tailoring.md using [the decision template](../templates/tailoring-decisions.md). Give each proposal an ID and show the original contribution, exact proposed bullet, metric type, supporting facts/answers, formula and assumptions, precision, and an honest qualitative alternative. If inputs are absent, propose a question or a clearly marked placeholder in the review notes, never a fabricated numeric bullet.

Show the concrete proposals to the user before generation. Ask them to confirm factual accuracy and accept the wording, correct the inputs, reject the proposal, or explicitly skip quantification. Resolve each proposed metric as accepted, corrected-and-accepted, rejected, or deferred/omitted. Silence remains pending: wait for the response before generating the CV. An explicit request to proceed without unresolved metrics permits qualitative fallbacks. If no useful opportunities exist, explain that finding and complete the checkpoint without manufacturing proposals.

Approval alone does not substantiate an unsupported number. Acceptance must confirm the underlying value/context or a defensible calculation, including approximation. Use only supported and accepted proposals in the CV; retain qualitative wording for rejected or explicitly deferred items. Recalculate and re-present any materially changed value or assumptions. Record decisions and answer IDs, and preserve this state when resuming.

## Evidence and Profile Persistence

Map the final numeric claim to its input facts and confirmation in evidence.json; record derivation and uncertainty in tailoring.md. Keep estimates labeled through translation and PDF review. Newly confirmed reusable metrics also trigger [profile updates](profile-updates.md): approval to use a bullet in this application is separate from approval of exact canonical-profile edits. Apply and verify only those separately approved source changes.
