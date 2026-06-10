from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COMPANY_DIR = DATA / "companies"
RESEARCH_DIR = DATA / "research"
INVESTOR_DIR = DATA / "investors"
TRANSACTION_DIR = DATA / "transactions"
METADATA_DIR = DATA / "metadata"


def load_yaml(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return default if value is None else value


def dump_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(value, handle, sort_keys=False, allow_unicode=False, width=100)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def company_files() -> List[Path]:
    return sorted(COMPANY_DIR.glob("*.yaml"))


def all_companies() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in company_files():
        records.extend(load_yaml(path, []))
    return records


def all_investors() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in sorted(INVESTOR_DIR.glob("*investors.yaml")):
        records.extend(load_yaml(path, []))
    return records


def records_for_section(section: str) -> List[Dict[str, Any]]:
    value = load_yaml(section_path(section), [])
    if not isinstance(value, list):
        raise ValueError(f"Section {section} must contain a YAML list")
    return value


def category_map() -> Dict[str, Dict[str, Any]]:
    taxonomy = load_yaml(DATA / "market_maps" / "category_taxonomy.yaml", {})
    return {item["id"]: item for item in taxonomy.get("categories", [])}


def section_path(section: str) -> Path:
    log = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})
    record = log["sections"].get(section)
    if not record:
        raise KeyError(f"Unknown section: {section}")
    return ROOT / record["file_path"]


def today() -> str:
    return date.today().isoformat()


def parse_iso_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def markdown_table(headers: List[str], rows: Iterable[Iterable[Any]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(_cell(value) for value in row) + " |")
    return "\n".join([header, divider, *body])


def _cell(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def score_value(company: Dict[str, Any]) -> Tuple[float, int]:
    scores = company.get("strategic_scoring", {})
    numeric = [
        value
        for key, value in scores.items()
        if key != "overall_vc_priority" and isinstance(value, (int, float))
    ]
    return (sum(numeric) / len(numeric), len(numeric)) if numeric else (0.0, 0)


PRIORITY_RANK = {
    "high_conviction": 5,
    "active_diligence": 4,
    "watchlist": 3,
    "monitor": 2,
    "pass": 1,
    None: 0,
}


def ranked_companies(companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        companies,
        key=lambda company: (
            PRIORITY_RANK.get(company.get("strategic_scoring", {}).get("overall_vc_priority"), 0),
            score_value(company)[0],
        ),
        reverse=True,
    )
