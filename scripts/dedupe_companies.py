#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import all_companies


def main() -> int:
    by_id = defaultdict(list)
    by_name = defaultdict(list)
    for company in all_companies():
        by_id[company["company_id"]].append(company["primary_category"])
        by_name[company["name"].strip().lower()].append(company["company_id"])
    duplicates = False
    for label, mapping in (("ID", by_id), ("name", by_name)):
        for value, locations in mapping.items():
            if len(locations) > 1:
                duplicates = True
                print(f"Duplicate {label} {value}: {locations}")
    if not duplicates:
        print("No duplicate company IDs or normalized names.")
    return int(duplicates)


if __name__ == "__main__":
    raise SystemExit(main())
