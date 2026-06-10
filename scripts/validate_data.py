#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Type

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import ValidationError

from semivc.models import Company, Investor, Paper, Patent, Researcher, Transaction
from scripts.common import (
    COMPANY_DIR,
    INVESTOR_DIR,
    METADATA_DIR,
    RESEARCH_DIR,
    TRANSACTION_DIR,
    category_map,
    company_files,
    load_yaml,
    parse_iso_date,
)


def datasets() -> Iterable[Tuple[str, Path, Type[Any]]]:
    for path in company_files():
        yield "company", path, Company
    yield "paper", RESEARCH_DIR / "papers.yaml", Paper
    yield "patent", RESEARCH_DIR / "patents.yaml", Patent
    yield "researcher", RESEARCH_DIR / "researchers.yaml", Researcher
    for path in sorted(INVESTOR_DIR.glob("*investors.yaml")):
        yield "investor", path, Investor
    yield "transaction", TRANSACTION_DIR / "ma_transactions.yaml", Transaction


def is_placeholder(record: Dict[str, Any]) -> bool:
    notes = str(record.get("data_quality", {}).get("notes") or "").lower()
    return "placeholder" in notes or "example" in notes


def validate_repository() -> List[str]:
    errors: List[str] = []
    categories = set(category_map())
    seen: Dict[str, List[str]] = {}
    company_names: List[str] = []

    for kind, path, model in datasets():
        records = load_yaml(path, [])
        if not isinstance(records, list):
            errors.append(f"{path}: top-level value must be a list")
            continue
        id_field = f"{kind}_id"
        for index, record in enumerate(records):
            location = f"{path}:{index + 1}"
            try:
                model.model_validate(record)
            except ValidationError as exc:
                errors.append(f"{location}: {exc}")
                continue
            record_id = record[id_field]
            seen.setdefault(id_field, []).append(record_id)
            if kind == "company":
                company_names.append(record["name"].strip().lower())
                referenced = {record["primary_category"], *record.get("secondary_categories", [])}
            else:
                referenced = set(record.get("research_category", record.get("related_categories", [])))
                if kind == "transaction":
                    referenced = set(record.get("target_categories", []))
            unknown = referenced - categories
            if unknown:
                errors.append(f"{location}: unknown categories {sorted(unknown)}")
            if kind in {"company", "paper", "patent", "researcher", "investor", "transaction"}:
                if not record.get("sources") and not is_placeholder(record):
                    errors.append(f"{location}: requires at least one source or explicit placeholder note")

    for id_field, values in seen.items():
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            errors.append(f"Duplicate {id_field} values: {duplicates}")
    duplicate_names = [name for name, count in Counter(company_names).items() if count > 1]
    if duplicate_names:
        errors.append(f"Duplicate company names: {duplicate_names}")

    refresh = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    expected_sections = set(categories) | {"research_papers", "patents", "ma_transactions", "vc_investors"}
    missing = expected_sections - set(refresh)
    if missing:
        errors.append(f"Missing refresh metadata: {sorted(missing)}")
    for section, metadata in refresh.items():
        path = Path(metadata.get("file_path", ""))
        if not metadata.get("last_refreshed"):
            errors.append(f"Refresh section {section} has no last_refreshed")
        else:
            try:
                parse_iso_date(metadata["last_refreshed"])
            except ValueError:
                errors.append(f"Refresh section {section} has invalid ISO date")
        if not path.parts:
            errors.append(f"Refresh section {section} has no file_path")
        elif not (Path(__file__).resolve().parents[1] / path).exists():
            errors.append(f"Refresh section {section} points to missing file {path}")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
