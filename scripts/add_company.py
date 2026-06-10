#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semivc.models import Company
from scripts.common import dump_yaml, load_yaml, section_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a validated company record from a YAML file.")
    parser.add_argument("--section", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    source = load_yaml(__import__("pathlib").Path(args.input))
    company = Company.model_validate(source).model_dump(mode="json")
    if company["primary_category"] != args.section:
        raise SystemExit("primary_category must match --section")
    path = section_path(args.section)
    records = load_yaml(path, [])
    if any(item["company_id"] == company["company_id"] for item in records):
        raise SystemExit(f"Duplicate company_id: {company['company_id']}")
    records.append(company)
    dump_yaml(path, records)
    print(f"Added {company['name']} to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
