#!/usr/bin/env python3
"""Validate JSON Schema contracts and YAML/CFF syntax."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    try:
        schema = json.loads((ROOT / "catalog/schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "catalog/resources.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(catalog, schema, format_checker=jsonschema.FormatChecker())
    except Exception as exc:  # validation output needs the exact parser error
        errors.append(f"catalog schema validation: {exc}")

    for path in sorted([*ROOT.rglob("*.yml"), *ROOT.rglob("*.yaml"), ROOT / "CITATION.cff"]):
        if not path.is_file():
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")

    if errors:
        print("STRUCTURED FILE VALIDATION FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("STRUCTURED FILE VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
