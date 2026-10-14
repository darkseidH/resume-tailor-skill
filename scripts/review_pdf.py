"""Extract PDF text and page images into a fresh review directory."""

import argparse
import json
from pathlib import Path

import pymupdf
from pypdf import PdfReader
from pypdf.errors import PyPdfError


def review(pdf: Path, output: Path):
    reader = PdfReader(pdf)
    texts = [page.extract_text() or "" for page in reader.pages]
    if not texts or any(not text.strip() for text in texts):
        raise ValueError("PDF has an empty or non-extractable page")
    output.mkdir(parents=True, exist_ok=False)
    (output / "extracted.txt").write_text("\n\n".join(texts), encoding="utf-8")
    with pymupdf.open(pdf) as document:
        for index, page in enumerate(document):
            page.get_pixmap(dpi=120).save(output / f"page-{index + 1}.png")
    result = {"pdf": str(pdf.resolve()), "pages": len(texts), "text_extracted": True, "visual_review": "pending", "factual_review": "pending"}
    (output / "review.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(review(args.pdf, args.output)))
    except (OSError, ValueError, PyPdfError, pymupdf.FileDataError) as error:
        parser.exit(1, f"PDF review failed: {error}\n")


if __name__ == "__main__":
    main()
