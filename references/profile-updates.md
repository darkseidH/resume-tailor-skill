# Persist Approved Profile Enrichment

Confirmed answers support the current application. Saving them to canonical files is a separate action requiring the user's approval of the proposed edit.

## Required Trigger and Completion

Run this workflow when an answer adds or corrects reusable information such as employment dates, role titles, project ownership, deployment, tools used, education, or proficiency. Do not wait until CV delivery. Store the answer in the private application/onboarding record and compare it with the mapped canonical files. If the fact is already represented correctly, record already-present and avoid duplication. Otherwise queue an exact source edit for the current topic.

At the end of the clarification topic, present the proposed edits together and request approval before changing topics or generating the CV. If the user already approved those exact edits in this session, apply them without asking again. If the user defers or declines, record that decision and proceed with the current application. Silence is pending, not approval.

Saving answers.md, changing a CV, editing an application snapshot, or writing a proposal file does not complete an approved profile update. Completion requires an actual edit to the mapped reusable source, a reread confirming it, and an update record identifying the source and result.

## Apply and Verify

Use [the update proposal](../templates/profile-update.md). Include the mapped source ID, exact path/section, existing text, proposed replacement or insertion, supporting answer ID and quote, and affected facts. Ask approval for that concrete change. A general request to tailor a CV, or to implement this skill, does not approve candidate-profile changes.

After approval, reread the target and check that the reviewed old text still matches. If it changed, present the new proposal rather than replacing newer content. Apply only approved hunks through normal file tools, preserve unrelated content and source IDs, then reread the result. Record the actual change and approval in the private application notes. Save a private before-state when needed to recover an edit; never distribute candidate history with the skill.

If the user declines or does not approve, leave canonical files unchanged and continue using confirmed session answers for this application. If they approve only part, apply that part only. If an answer conflicts with an existing fact, keep both references until the user explicitly resolves it. Never rewrite a conflicting source to erase the conflict without review.

On the next application, reread the updated source and relocate its evidence by heading/excerpt. If the excerpt has changed, revalidate the associated fact rather than silently reusing stale evidence.

## Resume and Report

When resuming an application, read its answer history and update proposals. Reconcile confirmed additions with the canonical sources: apply previously approved edits that are still pending after the before-state check, or present unapproved proposals. Do not ask the user to repeat an answer already recorded unless there is a real conflict.

Before completing profile review, match review or CV delivery, account for every new reusable fact as applied-and-verified, declined, deferred/pending, or already-present. For applied edits, report the actual destination and a concise change summary. If a write fails, mark it failed/pending with the reason; never report the source updated because a proposal or answer was saved.
