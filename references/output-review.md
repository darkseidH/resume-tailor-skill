# Final Application Review

## Factual Review

Compare every CV claim, title, date, qualification and skill to the evidence ledger. Check the source excerpt actually supports the wording, level of ownership, and result. A passing ledger check verifies references only; it cannot detect exaggeration or mistranslation. Recheck uncertain facts after edits, and mark unresolved gaps honestly in the match report.

Check the quantification review is complete: each proposed metric is supported and accepted, rejected, or explicitly deferred/omitted. Verify calculations against their inputs, timeframe, attribution, and units; ensure approximate values remain labeled in both languages and in the PDF. Unresolved proposals cannot enter the CV. Approval to use a metric does not imply permission to persist it in the canonical profile.

## Content Completeness

Before delivery, compare the CV with the full profile inventory and tailoring decisions:

- A concise, supported target-role headline appears beneath the name without changing historical employment titles, followed by a specific professional summary explaining the profile.
- Every main role has a consistent title/company/confirmed-location/date header and enough distinct bullets to explain the work. Apply the 3–6 bullet target only where evidence supports it. Confirm chronology and ongoing status.
- Bullets explain action, context, tools, and a supported result or deliverable. Verify every metric and ownership claim; qualitative outcomes must also be supported.
- Compare each main role and substantive project against the profile inventory. Restore important context lost through keyword filtering or excessive shortening. Resolve sparse evidence through clarification, not padding.
- Languages or Langues contains every confirmed spoken language with accurate levels, including languages absent from the offer. Record any explicit user-requested omission; do not infer proficiency or CEFR levels.
- Professional projects appear within the corresponding employer/role’s experience highlights, with no duplicate project entry. Academic, personal, and open-source projects retain explicit provenance in their separate section. Clarify unresolved professional-project associations before finalizing placement.

Verify these items in both YAML and the rendered PDF’s extracted text and page images.

## Document Review

Run `uv run --locked python scripts/review_pdf.py path/to/cv.pdf --output path/to/new-review-dir` from the skill directory to extract text and generate page images. Open every image with the available image-viewing tool. Check clipping, overlap, margins, line breaks, section hierarchy, degree labels, dates, and pagination. Preserve readable typography rather than shrinking everything to one page. Verify the [page metadata rule](rendering.md#page-metadata) on every page: no last-updated note or footer name/page count.

Read extracted text for missing content, accented characters, dates, duplicated or garbled tokens, and reading order. Compare substantive content with the YAML. A single-page synthetic example does not validate a multi-page real CV: review every page for each application.

### Page Balance

Inspect adjacent pages together before passing visual review. A large unused lower area on an earlier page, especially page one, needs adjustment when substantive content on the next page could fit there. Distinguish avoidable gaps from normal margins and whitespace on the final page.

First check forced page breaks and section/entry grouping. Try moving a complete short section, such as an academic project or education, into the available space; choose the order for the actual CV rather than enforcing one universal section order. Keep role chronology, employer-linked projects, heading/content associations and the user's requested order intact. Adjust spacing only where readability is preserved. Retain substantive content and readable font sizes instead of deleting material, adding filler or forcing one page.

Rerender into a fresh revision and inspect every page again: filling page one must not introduce clipping, stranded headings or awkward splits elsewhere. Recheck extracted text and evidence references after reordering. Record the layout adjustment and any unavoidable gap in verification.md; pass visual review only after avoidable large gaps are resolved.

## Evidence on page one

From the match report, choose up to three consequential requirements rated strong. Prioritize mandatory criteria and direct contributions. Record the requirement ID, fact ID, first visible page and section, and actual printed phrase in the tailoring record. For a requirement about demonstrated work, find the contribution itself. If it is buried, consider reordering highlights or clarifying an already supported summary. Preserve chronology, provenance, substantive roles, and readable layout. If strong evidence belongs on a later page, record the reason. Review every changed page and its extracted text in the new revision.

## English and French consistency

When delivering both languages, record the exact revision IDs in verification.md. Compare the two versions against shared source facts for employers, dates, credentials, ownership, environments, quantities, units, timeframe, and qualifiers. Check material omissions. Allow idiomatic wording and ordering that preserve meaning. Resolve and record discrepancies before delivering the pair. Rerender an edited version, repeat its affected checks, and compare the resulting pair again. A single-language delivery uses the regular review.

## Delivery Record

On an explicitly resumed legacy application, retain its recorded artifact layout and deliver the reviewed PDF/YAML from their original revision paths. The new company/role allocation and publish helper apply to new-layout applications only; do not migrate or relocate retained legacy outputs.

Write supporting/verification.md with commands and actual results, the PDF and YAML revision reviewed, page count, images inspected, factual findings, and unresolved limitations. Mark each check passed, failed, or unavailable. After a content or design change, rerender into a new directory and repeat affected checks.

Inspect every image and the extracted text. Set `visual_review` and `text_review` in `review/review.json` to passed only when those checks pass, and record actual findings in `review_notes`. Keep the renderer's PDF and YAML hashes. Deliver the normalized `render/cv.yaml`.

For a new-layout revision, capture the factual review inputs before comparing claims to their sources.

```powershell
rtk proxy uv run --locked python scripts/application_artifacts.py factual-review "APPLICATION" "REVISION"
```

Inspect the normalized YAML and each supporting snapshot. After verifying every claim, supply the printed inputs path and describe the actual factual findings.

```powershell
rtk proxy uv run --locked python scripts/application_artifacts.py factual-review "APPLICATION" "REVISION" --inputs "PRINTED_INPUTS_JSON" --approve "FACTUAL_FINDINGS"
```

A source-only correction requires a new factual review attempt. Retain earlier attempts and reuse visual and text findings only when their reviewed PDF, YAML, page images and extracted text remain valid. Check the review artifacts again if their identity is uncertain. New-layout reviews created before factual input capture require this review before another publication. A manually edited status cannot satisfy factual sign-off.

Run `rtk proxy uv run --locked python scripts/application_artifacts.py publish APPLICATION APPLICATION/supporting/revisions/en-v1 en` (or the corresponding fr revision). This checks review status, PDF/YAML identity, review artifact identity, factual approval, and evidence coverage, then copies the reviewed PDF to the role folder without overwriting older PDFs. It does not independently establish semantic truth or visual quality. A failed or unavailable required check leaves the PDF under supporting/ and must not be presented as final.

Deliver links to each finished resume-en.pdf/resume-fr.pdf (or numbered revision) and its supporting/revisions/.../render/cv.yaml, with match findings, gaps/actions and tailoring explanation. Only final PDFs and supporting/ belong directly in the role folder. Explain that deleting supporting/ removes editable files, evidence and resume state while keeping finished PDFs readable. The agent never deletes it automatically. Report incomplete checks plainly. A real application still requires the user's review before submission, which remains outside scope.
