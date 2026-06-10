#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semivc.models import Company, Investor, Paper, Patent, Transaction
from scripts.common import METADATA_DIR, ROOT, dump_yaml, load_yaml, section_path, today


ID_FIELDS = {
    "research_papers": "paper_id",
    "patents": "patent_id",
    "ma_transactions": "transaction_id",
    "vc_investors": "investor_id",
}

MODELS = {
    "research_papers": Paper,
    "patents": Patent,
    "ma_transactions": Transaction,
    "vc_investors": Investor,
}


def record_id_field(section: str) -> str:
    return ID_FIELDS.get(section, "company_id")


def load_operation(path: str | None) -> Dict[str, Any]:
    if not path:
        return {}
    value = load_yaml(Path(path), {})
    if not isinstance(value, dict):
        raise SystemExit("Operation file must contain a YAML mapping")
    return value


def apply_operations(
    records: List[Dict[str, Any]], section: str, operation: Dict[str, Any]
) -> tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
    id_field = record_id_field(section)
    by_id = {record[id_field]: record for record in records}
    changes = {"added": [], "updated": [], "removed": [], "archived": []}

    for record in operation.get("add", []):
        record_id = record[id_field]
        if record_id in by_id:
            raise SystemExit(f"Cannot add duplicate {id_field}: {record_id}")
        by_id[record_id] = record
        changes["added"].append(record_id)

    for record in operation.get("update", []):
        record_id = record[id_field]
        if record_id not in by_id:
            raise SystemExit(f"Cannot update missing {id_field}: {record_id}")
        by_id[record_id] = record
        changes["updated"].append(record_id)

    for record_id in operation.get("remove", []):
        if record_id not in by_id:
            raise SystemExit(f"Cannot remove missing {id_field}: {record_id}")
        del by_id[record_id]
        changes["removed"].append(record_id)

    for record_id in operation.get("archive", []):
        if section in ID_FIELDS:
            raise SystemExit("Archive is currently supported for company sections only")
        if record_id not in by_id:
            raise SystemExit(f"Cannot archive missing {id_field}: {record_id}")
        by_id[record_id]["status"] = "shutdown"
        by_id[record_id].setdefault("data_quality", {})["last_company_update"] = today()
        changes["archived"].append(record_id)

    return list(by_id.values()), changes


def validate_candidate_records(section: str, records: List[Dict[str, Any]]) -> None:
    model = MODELS.get(section, Company)
    for record in records:
        validated = model.model_validate(record)
        if model is Company and validated.primary_category != section:
            raise SystemExit(
                f"Company {validated.company_id} primary_category must match section {section}"
            )


def update_refresh_log(
    section: str, mode: str, changes: Dict[str, List[str]], summary: str | None
) -> None:
    path = METADATA_DIR / "section_refresh_log.yaml"
    log = load_yaml(path, {"sections": {}})
    record = log["sections"][section]
    record["last_refreshed"] = today()
    record["refresh_scope"] = mode
    record["refresh_summary"] = summary or "Section refreshed through refresh_section.py."
    record["major_changes"] = [
        f"{name}: {', '.join(values)}" for name, values in changes.items() if values
    ]
    prefix = {
        "research_papers": ("papers_added", "papers_updated"),
        "patents": ("patents_added", "patents_updated"),
        "ma_transactions": ("transactions_added", "transactions_updated"),
        "vc_investors": ("investors_added", "investors_updated"),
    }.get(section, ("companies_added", "companies_updated"))
    record[prefix[0]] = changes["added"]
    record[prefix[1]] = changes["updated"]
    if section not in ID_FIELDS:
        record["companies_removed"] = changes["removed"]
    dump_yaml(path, log)


def append_changelog(section: str, mode: str, changes: Dict[str, List[str]], summary: str | None) -> None:
    path = ROOT / "CHANGELOG.md"
    detail = "; ".join(f"{key}: {', '.join(value)}" for key, value in changes.items() if value)
    line = f"- `{section}` ({mode}): {summary or 'metadata refresh'}"
    if detail:
        line += f" [{detail}]"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {today()}\n\n{line}\n")


def run_pipeline() -> None:
    for script in ("validate_data.py", "generate_docs.py", "generate_watchlists.py",
                   "export_to_csv.py", "export_to_sqlite.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=True, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh one independently managed database section.")
    parser.add_argument("--section", required=True)
    parser.add_argument("--mode", required=True, choices=["full", "partial", "targeted", "source_check_only"])
    parser.add_argument("--operations", help="YAML file with add/update/remove/archive lists")
    parser.add_argument("--summary")
    parser.add_argument("--list", action="store_true", help="Show current record IDs and exit")
    args = parser.parse_args()

    data_path = section_path(args.section)
    records = load_yaml(data_path, [])
    id_field = record_id_field(args.section)
    print(f"{args.section}: {len(records)} current records")
    for record in records:
        print(f"- {record.get(id_field)}: {record.get('name') or record.get('title') or record.get('target_company')}")
    if args.list:
        return 0

    updated, changes = apply_operations(records, args.section, load_operation(args.operations))
    validate_candidate_records(args.section, updated)
    dump_yaml(data_path, updated)
    update_refresh_log(args.section, args.mode, changes, args.summary)
    append_changelog(args.section, args.mode, changes, args.summary)
    run_pipeline()
    print(f"Refreshed {args.section} and rebuilt derived outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
