#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import (
    METADATA_DIR,
    RESEARCH_DIR,
    ROOT,
    TRANSACTION_DIR,
    all_companies,
    all_investors,
    category_map,
    load_yaml,
    score_value,
)

DB_PATH = ROOT / "exports" / "semiconductor_vc_landscape.sqlite"


def text(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float)):
        return value
    return json.dumps(value, sort_keys=True, default=str)


def source_rows(parent_type: str, parent_id: str, sources: List[Dict[str, Any]]) -> Iterable[tuple]:
    for source in sources:
        yield (
            source.get("source_id"), parent_type, parent_id, source.get("title"),
            source.get("url"), source.get("publisher"), source.get("date_published"),
            source.get("date_accessed"), source.get("source_type"), source.get("reliability"),
            source.get("notes"),
        )


def export_database(path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE categories (category_id TEXT PRIMARY KEY, display_name TEXT, description TEXT);
        CREATE TABLE companies (
          company_id TEXT PRIMARY KEY, name TEXT NOT NULL, status TEXT, website TEXT,
          hq_json TEXT, founded_year INTEGER, primary_category TEXT, summary TEXT,
          vc_priority TEXT, average_score REAL, raw_json TEXT
        );
        CREATE TABLE products (
          id INTEGER PRIMARY KEY, company_id TEXT, product_name TEXT, product_type TEXT,
          product_status TEXT, raw_json TEXT
        );
        CREATE TABLE funding (
          company_id TEXT PRIMARY KEY, total_raised_usd_m REAL, latest_round TEXT,
          latest_round_date TEXT, latest_round_amount_usd_m REAL, valuation_usd_m REAL,
          key_investors_json TEXT
        );
        CREATE TABLE founders (
          id INTEGER PRIMARY KEY, company_id TEXT, name TEXT, role TEXT, background TEXT,
          prior_company_or_lab TEXT, technical_relevance TEXT
        );
        CREATE TABLE investors (
          investor_id TEXT PRIMARY KEY, name TEXT, investor_type TEXT, website TEXT, raw_json TEXT
        );
        CREATE TABLE investor_portfolios (
          id INTEGER PRIMARY KEY, investor_id TEXT, company_id TEXT, company_name TEXT,
          category_json TEXT, investment_stage TEXT, investment_date TEXT
        );
        CREATE TABLE transactions (
          transaction_id TEXT PRIMARY KEY, target_company TEXT, target_company_id TEXT,
          acquirer TEXT, announcement_date TEXT, transaction_status TEXT,
          transaction_value_usd_m REAL, raw_json TEXT
        );
        CREATE TABLE papers (paper_id TEXT PRIMARY KEY, title TEXT, venue TEXT, publication_date TEXT, raw_json TEXT);
        CREATE TABLE patents (patent_id TEXT PRIMARY KEY, title TEXT, patent_number TEXT, assignee TEXT, filing_date TEXT, raw_json TEXT);
        CREATE TABLE researchers (researcher_id TEXT PRIMARY KEY, name TEXT, current_affiliation TEXT, raw_json TEXT);
        CREATE TABLE sources (
          id INTEGER PRIMARY KEY, source_id TEXT, parent_type TEXT, parent_id TEXT, title TEXT,
          url TEXT, publisher TEXT, date_published TEXT, date_accessed TEXT, source_type TEXT,
          reliability TEXT, notes TEXT
        );
        CREATE TABLE refresh_log (
          section_id TEXT PRIMARY KEY, display_name TEXT, file_path TEXT, last_refreshed TEXT,
          refreshed_by TEXT, refresh_scope TEXT, raw_json TEXT
        );
        CREATE TABLE scores (
          company_id TEXT PRIMARY KEY, market_size INTEGER, timing INTEGER,
          technical_differentiation INTEGER, founder_quality INTEGER, customer_pull INTEGER,
          business_model_quality INTEGER, capital_efficiency INTEGER, competitive_intensity INTEGER,
          exit_potential INTEGER, strategic_scarcity INTEGER, overall_vc_priority TEXT,
          average_score REAL
        );
        """
    )
    for category_id, category in category_map().items():
        connection.execute(
            "INSERT INTO categories VALUES (?, ?, ?)",
            (category_id, category.get("display_name"), category.get("description")),
        )
    for company in all_companies():
        average, count = score_value(company)
        scores = company.get("strategic_scoring", {})
        connection.execute(
            "INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                company["company_id"], company["name"], company["status"], company.get("website"),
                text(company.get("hq")), company.get("founded_year"), company["primary_category"],
                company.get("one_line_summary"), scores.get("overall_vc_priority"),
                average if count else None, text(company),
            ),
        )
        for product in company.get("product_profile", {}).get("products", []):
            connection.execute(
                "INSERT INTO products (company_id, product_name, product_type, product_status, raw_json) VALUES (?, ?, ?, ?, ?)",
                (company["company_id"], product.get("product_name"), product.get("product_type"),
                 product.get("product_status"), text(product)),
            )
        funding = company.get("funding_profile", {})
        connection.execute(
            "INSERT INTO funding VALUES (?, ?, ?, ?, ?, ?, ?)",
            (company["company_id"], funding.get("total_raised_usd_m"), funding.get("latest_round"),
             funding.get("latest_round_date"), funding.get("latest_round_amount_usd_m"),
             funding.get("disclosed_valuation_usd_m"), text(funding.get("key_investors", []))),
        )
        for founder in company.get("team_profile", {}).get("founders", []):
            connection.execute(
                "INSERT INTO founders (company_id, name, role, background, prior_company_or_lab, technical_relevance) VALUES (?, ?, ?, ?, ?, ?)",
                (company["company_id"], founder.get("name"), founder.get("role"), founder.get("background"),
                 founder.get("prior_company_or_lab"), founder.get("technical_relevance")),
            )
        connection.execute(
            "INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (company["company_id"], scores.get("market_size"), scores.get("timing"),
             scores.get("technical_differentiation"), scores.get("founder_quality"),
             scores.get("customer_pull"), scores.get("business_model_quality"),
             scores.get("capital_efficiency"), scores.get("competitive_intensity"),
             scores.get("exit_potential"), scores.get("strategic_scarcity"),
             scores.get("overall_vc_priority"), average if count else None),
        )
        connection.executemany(
            "INSERT INTO sources (source_id, parent_type, parent_id, title, url, publisher, date_published, date_accessed, source_type, reliability, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            source_rows("company", company["company_id"], company.get("sources", [])),
        )
    for investor in all_investors():
        connection.execute(
            "INSERT INTO investors VALUES (?, ?, ?, ?, ?)",
            (investor["investor_id"], investor.get("name"), investor["investor_type"],
             investor.get("website"), text(investor)),
        )
        for portfolio in investor.get("relevant_portfolio_companies", []):
            connection.execute(
                "INSERT INTO investor_portfolios (investor_id, company_id, company_name, category_json, investment_stage, investment_date) VALUES (?, ?, ?, ?, ?, ?)",
                (investor["investor_id"], portfolio.get("company_id"), portfolio.get("company_name"),
                 text(portfolio.get("category", [])), portfolio.get("investment_stage"),
                 portfolio.get("estimated_investment_date")),
            )
        connection.executemany(
            "INSERT INTO sources (source_id, parent_type, parent_id, title, url, publisher, date_published, date_accessed, source_type, reliability, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            source_rows("investor", investor["investor_id"], investor.get("sources", [])),
        )
    collection_specs = [
        ("transactions", TRANSACTION_DIR / "ma_transactions.yaml", "transaction_id",
         "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
         lambda r: (r["transaction_id"], r.get("target_company"), r.get("target_company_id"),
                    r.get("acquirer"), r.get("announcement_date"), r.get("transaction_status"),
                    r.get("transaction_value_usd_m"), text(r))),
        ("papers", RESEARCH_DIR / "papers.yaml", "paper_id",
         "INSERT INTO papers VALUES (?, ?, ?, ?, ?)",
         lambda r: (r["paper_id"], r.get("title"), r.get("venue"), r.get("publication_date"), text(r))),
        ("patents", RESEARCH_DIR / "patents.yaml", "patent_id",
         "INSERT INTO patents VALUES (?, ?, ?, ?, ?, ?)",
         lambda r: (r["patent_id"], r.get("title"), r.get("patent_number"), r.get("assignee"),
                    r.get("filing_date"), text(r))),
        ("researchers", RESEARCH_DIR / "researchers.yaml", "researcher_id",
         "INSERT INTO researchers VALUES (?, ?, ?, ?)",
         lambda r: (r["researcher_id"], r.get("name"), r.get("current_affiliation"), text(r))),
    ]
    for parent_type, source_path, id_field, statement, mapper in collection_specs:
        for record in load_yaml(source_path, []):
            connection.execute(statement, mapper(record))
            connection.executemany(
                "INSERT INTO sources (source_id, parent_type, parent_id, title, url, publisher, date_published, date_accessed, source_type, reliability, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                source_rows(parent_type, record[id_field], record.get("sources", [])),
            )
    refresh = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    for section_id, record in refresh.items():
        connection.execute(
            "INSERT INTO refresh_log VALUES (?, ?, ?, ?, ?, ?, ?)",
            (section_id, record.get("display_name"), record.get("file_path"),
             record.get("last_refreshed"), record.get("refreshed_by"),
             record.get("refresh_scope"), text(record)),
        )
    connection.commit()
    connection.close()


def main() -> int:
    export_database()
    print(f"SQLite export written to {DB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
