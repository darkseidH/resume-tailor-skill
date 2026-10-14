# Profile Update Scenarios

1. Approve: propose adding only the confirmed staging deployment sentence with answer-deployment as evidence. After explicit simulated approval, insert that sentence in a private copy, preserving all existing content. The next application can find it by heading and excerpt.
2. Decline: repeat with a separate private copy and simulated decline. The source must remain byte-for-byte identical, while the application may cite the session answer snapshot.
3. Conflict: propose correcting an end date, then change the target before applying. Reread and present a revised proposal; do not overwrite changed content under the earlier approval.

These are approval workflow walkthroughs, not automation that can independently grant approval. Actual candidate files require the human's explicit decision.

## Regression: Answers Saved Only in the Application

Use a fresh chat and a disposable private canonical Markdown source containing: “ALTEN internship: dates unknown. AutoExport-BI: personal contribution unknown.” Map that source and request a profile review, without requesting a CV.

Provide these answers when asked: “Internship: March-August 2025; employed September 2025-present” and “I developed and implemented AutoExport-BI myself.”

Expected observable behavior:
- Save the confirmed answers in the private onboarding record.
- Before ending the clarification topic, show exact proposed edits to the mapped reusable source and request approval.
- After the tester approves those edits, actually write them to the source, reread it, and report applied-and-verified with the destination.
- In a new chat using the same map, recover the updated chronology and contribution from that source without asking the same questions again.
- Repeat in a separate copy with a decline: preserve the canonical file and report declined, not updated.

Fail this regression if the agent saves only answers.md, edits only an application snapshot, ends with an unpresented proposal, reports an update without a canonical write, or edits an unapproved real source. Record the conversation and source before/after; structural validation alone cannot pass this behavioral regression.
