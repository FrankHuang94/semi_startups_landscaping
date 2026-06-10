#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import (
    RESEARCH_DIR,
    ROOT,
    TRANSACTION_DIR,
    all_companies,
    all_investors,
    load_yaml,
    score_value,
)

EXPORTS = ROOT / "exports"


def scalar(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, default=str)
    return value


def write_csv(path: Path, records: List[Dict[str, Any]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for record in records:
            writer.writerow({field: scalar(record.get(field)) for field in fields})


def export_all() -> None:
    companies = []
    for company in all_companies():
        average, count = score_value(company)
        companies.append(
            {
                **company,
                "hq": company.get("hq"),
                "vc_priority": company.get("strategic_scoring", {}).get("overall_vc_priority"),
                "average_score": round(average, 2) if count else None,
                "last_verified": company.get("data_quality", {}).get("last_verified"),
            }
        )
    write_csv(
        EXPORTS / "companies.csv",
        companies,
        [
            "company_id", "name", "status", "website", "hq", "founded_year", "primary_category",
            "secondary_categories", "technology_tags", "one_line_summary", "vc_priority",
            "average_score", "last_verified",
        ],
    )
    write_csv(
        EXPORTS / "investors.csv",
        all_investors(),
        ["investor_id", "name", "investor_type", "website", "hq", "preferred_stage",
         "semiconductor_thesis", "ai_infrastructure_thesis", "relevant_partners",
         "relevant_portfolio_companies", "co_investors", "notable_exits"],
    )
    specs = [
        ("ma_transactions.csv", TRANSACTION_DIR / "ma_transactions.yaml",
         ["transaction_id", "target_company", "target_company_id", "acquirer", "acquirer_type",
          "target_categories", "announcement_date", "close_date", "transaction_status",
          "transaction_value_usd_m", "consideration_type", "strategic_rationale"]),
        ("papers.csv", RESEARCH_DIR / "papers.yaml",
         ["paper_id", "title", "authors", "institution_affiliations", "venue", "publication_year",
          "publication_date", "url", "arxiv_url", "doi", "research_category", "technology_tags",
          "investor_relevance", "commercialization_potential"]),
        ("patents.csv", RESEARCH_DIR / "patents.yaml",
         ["patent_id", "title", "patent_number", "application_number", "jurisdiction", "filing_date",
          "publication_date", "grant_date", "assignee", "inventors", "research_category",
          "technology_tags", "investor_relevance", "commercialization_signal"]),
        ("researchers.csv", RESEARCH_DIR / "researchers.yaml",
         ["researcher_id", "name", "current_affiliation", "prior_affiliations", "location",
          "research_areas", "related_categories", "notable_papers", "notable_patents",
          "possible_startup_angle", "commercialization_signal", "investor_notes"]),
    ]
    for filename, source, fields in specs:
        write_csv(EXPORTS / filename, load_yaml(source, []), fields)


def main() -> int:
    export_all()
    print(f"CSV exports written to {EXPORTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
