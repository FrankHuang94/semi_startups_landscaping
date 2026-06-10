#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semivc.models import Company
from scripts.common import company_files, dump_yaml, load_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Replace a company record with validated YAML.")
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    replacement = Company.model_validate(load_yaml(Path(args.input))).model_dump(mode="json")
    if replacement["company_id"] != args.company_id:
        raise SystemExit("Input company_id does not match --company-id")
    for path in company_files():
        records = load_yaml(path, [])
        for index, record in enumerate(records):
            if record["company_id"] == args.company_id:
                if replacement["primary_category"] != path.stem:
                    raise SystemExit("Moving categories must be done as remove plus add")
                records[index] = replacement
                dump_yaml(path, records)
                print(f"Updated {args.company_id} in {path}")
                return 0
    raise SystemExit(f"Company not found: {args.company_id}")


if __name__ == "__main__":
    raise SystemExit(main())
