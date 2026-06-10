#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import RESEARCH_DIR, ROOT, all_companies, load_yaml, markdown_table, ranked_companies, score_value

VIEWS = ROOT / "docs" / "views"


def company_table(companies: List[Dict[str, Any]]) -> str:
    rows = []
    for company in companies:
        average, count = score_value(company)
        rows.append([
            company["name"], company["primary_category"],
            company.get("vc_investment_view", {}).get("investment_stage_fit"),
            company.get("strategic_scoring", {}).get("overall_vc_priority"),
            f"{average:.2f}" if count else "Unscored",
            company.get("data_quality", {}).get("last_verified"),
        ])
    return markdown_table(["Company", "Category", "Stage Fit", "Priority", "Score", "Verified"], rows)


def write_view(filename: str, title: str, intro: str, body: str) -> None:
    VIEWS.mkdir(parents=True, exist_ok=True)
    (VIEWS / filename).write_text(f"# {title}\n\n{intro}\n\n{body}\n", encoding="utf-8")


def generate_watchlists() -> None:
    companies = ranked_companies(all_companies())
    priority = lambda value: [
        c for c in companies if c.get("strategic_scoring", {}).get("overall_vc_priority") == value
    ]
    write_view("top_vc_watchlist.md", "Top VC Watchlist",
               "Ranked by explicit VC priority and average completed score.", company_table(companies[:25]))
    write_view("active_diligence_pipeline.md", "Active Diligence Pipeline",
               "Companies explicitly marked for active diligence.", company_table(priority("active_diligence")))
    write_view("high_conviction_companies.md", "High Conviction Companies",
               "Companies requiring an explicit high-conviction designation.", company_table(priority("high_conviction")))
    emerging = [
        c for c in companies
        if c.get("status") == "stealth"
        or c.get("vc_investment_view", {}).get("investment_stage_fit") in {"pre_seed", "seed"}
    ]
    write_view("emerging_stealth_or_pre_seed_targets.md", "Emerging Stealth or Pre-Seed Targets",
               "Early sourcing targets; verify all claims before outreach.", company_table(emerging))
    likely_acquirers = [
        c for c in companies if c.get("vc_investment_view", {}).get("likely_acquirers")
    ]
    rows = [
        [c["name"], c["primary_category"], c["vc_investment_view"].get("likely_acquirers"),
         c["vc_investment_view"].get("likely_exit_path")]
        for c in likely_acquirers
    ]
    write_view("strategic_acquirer_watchlist.md", "Strategic Acquirer Watchlist",
               "Potential exit pathways recorded during company diligence.",
               markdown_table(["Company", "Category", "Potential Acquirers", "Exit Paths"], rows))
    papers = load_yaml(RESEARCH_DIR / "papers.yaml", [])
    hot = sorted(
        papers,
        key=lambda paper: paper.get("commercialization_potential", {}).get("score") or 0,
        reverse=True,
    )
    write_view(
        "hot_research_to_startup_opportunities.md", "Hot Research to Startup Opportunities",
        "Research ranked by recorded commercialization potential.",
        markdown_table(
            ["Paper", "Categories", "Score", "Startup Angles"],
            [[p.get("title"), p.get("research_category"),
              p.get("commercialization_potential", {}).get("score"),
              p.get("commercialization_potential", {}).get("possible_startup_angles")] for p in hot],
        ),
    )
    researchers = load_yaml(RESEARCH_DIR / "researchers.yaml", [])
    founders = sorted(
        researchers,
        key=lambda item: item.get("commercialization_signal", {}).get("score") or 0,
        reverse=True,
    )
    write_view(
        "researcher_founder_candidates.md", "Researcher Founder Candidates",
        "Researchers ranked by commercialization signal; not an endorsement.",
        markdown_table(
            ["Researcher", "Affiliation", "Areas", "Score", "Possible Startup Angle"],
            [[r.get("name"), r.get("current_affiliation"), r.get("research_areas"),
              r.get("commercialization_signal", {}).get("score"), r.get("possible_startup_angle")]
             for r in founders],
        ),
    )
    missing = [c for c in companies if not c.get("sources") or c.get("data_quality", {}).get("missing_fields")]
    write_view("companies_missing_sources.md", "Companies Missing Sources",
               "Records needing source or field completion.", company_table(missing))


def main() -> int:
    generate_watchlists()
    print(f"Watchlists written to {VIEWS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
