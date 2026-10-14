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

## Delivery Record

Write verification.md with commands and actual results, the PDF and YAML revision reviewed, page count, images inspected, factual findings, and unresolved limitations. Mark each check passed, failed, or unavailable. After a content or design change, rerender into a new directory and repeat affected checks.

Deliver the PDF and editable YAML together with the match analysis, gaps/actions and tailoring explanation. Report incomplete checks plainly; do not label an unreviewed artifact final. A real application still requires the user's review before submission, which remains outside scope.
