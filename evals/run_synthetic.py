"""Create reproducible fictional application records; not an independent AI eval."""

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_evidence import leaves


def build(output: Path):
    fixtures = Path(__file__).parent / "fixtures"
    output.mkdir(parents=True, exist_ok=False)
    for language in ("english", "french"):
        application = output / language
        sources = application / "sources"
        sources.mkdir(parents=True)
        for name in ("profile.md", "answers.md", "job.md"):
            shutil.copyfile(fixtures / name, sources / name)
        shutil.copyfile(fixtures / f"{language}.yaml", application / "cv.yaml")
        shutil.copyfile(fixtures / "job.md", application / "job.md")
        shutil.copyfile(fixtures / "answers.md", application / "answers.md")
        excerpts = {
            "identity": ("profile", "My name is Alex Example. I live in Casablanca. My email is alex@example.com."),
            "target": ("job", "Fictional Backend Developer Offer"),
            "role": ("profile", "I worked at Example Systems as a Developer from January 2024 through June 2025. I implemented a PostgreSQL stock lookup endpoint as part of a three-person team. I used Python and SQL for this work."),
            "deployment": ("answers", "I deployed it to staging. Another developer handled production deployment."),
            "education": ("profile", "I completed a Bachelor in Computer Science at Example University from September 2020 through June 2023. The French wording for this fictional qualification is Licence en informatique."),
            "project": ("profile", "I built SQL reports for an academic inventory dataset as part of an academic reporting project."),
            "languages": ("profile", "I am fluent in French and have professional working proficiency in English.")
        }
        facts = {key: {"status": "supported", "source": source, "quote": quote} for key, (source, quote) in excerpts.items()}
        cv = yaml.safe_load((application / "cv.yaml").read_text(encoding="utf-8"))
        expected = json.loads((fixtures / f"{language}-claims.json").read_text(encoding="utf-8"))
        if set(leaves(cv["cv"])) != expected.keys():
            raise ValueError(f"Unmapped or stale fixture claims: {language}")
        claims = {}
        for pointer, claim in expected.items():
            value = cv
            for token in pointer.strip("/").split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                value = value[int(token)] if isinstance(value, list) else value[token]
            if value != claim["value"]:
                raise ValueError(f"Fixture claim changed: {pointer}; review its evidence")
            claims[pointer] = claim["facts"]
        ledger = {"sources": {s: f"sources/{s}.md" for s in ("profile", "answers", "job")}, "facts": facts, "claims": claims}
        (application / "evidence.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
        (application / "match.md").write_text("# Synthetic match review\n\nPython, SQL, PostgreSQL and API component development: strong (profile, role). Reporting: partial (academic project). French: strong (languages). Docker: initially unknown, then confirmed gap (answer-docker). Production deployment: initially unknown, then staging-only evidence (answer-deployment). Canadian authorization: confirmed mismatch (profile eligibility).\n\nApply to roles supporting sponsorship; learn Docker for future opportunities. No new qualification is added to the CV.\n", encoding="utf-8")
        (application / "tailoring.md").write_text("# Synthetic tailoring decisions\n\nPrioritized backend endpoint contribution and SQL. Headline describes the target role, not a past employment title. Preserved team context, staging-only deployment, academic provenance, languages and full synthetic history. Omitted Docker and unmeasured metrics. French credential wording is explicitly supported by the fictional source. These are curated fixture outputs, not independent model results.\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    print(build(parser.parse_args().output))
