"""Check claim coverage and source excerpts; semantic review remains manual."""

import argparse
import json
from pathlib import Path

import yaml


def leaves(value, pointer="/cv"):
    if isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from leaves(child, f"{pointer}/{escaped}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, f"{pointer}/{index}")
    elif value is not None and value != "":
        yield pointer


def check(cv_path: Path, ledger_path: Path) -> list[str]:
    cv = yaml.safe_load(cv_path.read_text(encoding="utf-8"))
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if not isinstance(cv, dict) or not isinstance(cv.get("cv"), dict):
        return ["Expected cv mapping"]
    if not isinstance(ledger, dict) or any(not isinstance(ledger.get(k), dict) for k in ("sources", "facts", "claims")):
        return ["Expected sources, facts, and claims mappings"]
    expected = set(leaves(cv["cv"]))
    claims = ledger["claims"]
    errors = [f"Unmapped claim: {p}" for p in sorted(expected - claims.keys())]
    errors.extend(f"Stale claim pointer: {p}" for p in sorted(claims.keys() - expected))
    root = ledger_path.parent.resolve()
    for pointer, fact_ids in claims.items():
        if not isinstance(fact_ids, list) or not fact_ids:
            errors.append(f"No fact references: {pointer}")
            continue
        for fact_id in fact_ids:
            if not isinstance(fact_id, str):
                errors.append(f"Invalid fact ID: {pointer}")
                continue
            fact = ledger["facts"].get(fact_id)
            if not isinstance(fact, dict) or fact.get("status") != "supported":
                errors.append(f"Fact {fact_id} is not supported: {pointer}")
                continue
            source = ledger["sources"].get(fact.get("source"))
            quote = fact.get("quote")
            if not isinstance(source, str) or not isinstance(quote, str) or not quote.strip():
                errors.append(f"Missing source or excerpt: {fact_id}")
                continue
            path = (root / source).resolve()
            if not path.is_relative_to(root):
                errors.append(f"Source outside application directory: {fact_id}")
            elif not path.is_file():
                errors.append(f"Missing snapshot: {fact_id}")
            elif quote not in path.read_text(encoding="utf-8"):
                errors.append(f"Source excerpt not found: {fact_id}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cv", type=Path)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        errors = check(args.cv, args.ledger)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
        parser.exit(1, f"Evidence check failed: {error}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Evidence references pass. Manually review semantic support before delivery.")


if __name__ == "__main__":
    main()
