#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import (
    INVESTOR_DIR,
    METADATA_DIR,
    RESEARCH_DIR,
    ROOT,
    TRANSACTION_DIR,
    all_companies,
    all_investors,
    category_map,
    load_yaml,
    markdown_table,
    ranked_companies,
    score_value,
)

DOCS = ROOT / "docs"


def write(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def company_rows(companies: List[Dict[str, Any]]) -> List[List[Any]]:
    rows = []
    for company in companies:
        funding = company.get("funding_profile", {})
        rows.append([
            company["name"],
            company.get("vc_investment_view", {}).get("investment_stage_fit"),
            ", ".join(filter(None, company.get("hq", {}).values())),
            company.get("one_line_summary"),
            funding.get("total_raised_usd_m"),
            funding.get("key_investors"),
            company.get("strategic_scoring", {}).get("overall_vc_priority"),
            company.get("data_quality", {}).get("last_company_update"),
        ])
    return rows


def generate_category_pages() -> None:
    categories = category_map()
    refresh = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    companies_by_category = defaultdict(list)
    for company in ranked_companies(all_companies()):
        companies_by_category[company["primary_category"]].append(company)
    diligence = load_yaml(ROOT / "data" / "market_maps" / "technical_diligence_framework.yaml", {})
    questions = diligence.get("default_questions", [])
    for category_id, category in categories.items():
        companies = companies_by_category[category_id]
        meta = refresh[category_id]
        profiles = []
        sources = []
        for company in companies:
            profiles.append(
                f"### {company['name']}\n\n"
                f"**Summary:** {company.get('investor_summary') or 'Research required.'}\n\n"
                f"**Differentiation:** {company.get('technical_profile', {}).get('technical_differentiation') or 'Research required.'}\n\n"
                f"**Key diligence:** {', '.join(company.get('vc_investment_view', {}).get('key_diligence_questions', [])) or 'Not yet recorded.'}"
            )
            sources.extend(company.get("sources", []))
        body = f"""Last refreshed: {meta['last_refreshed']}  
Refresh scope: {meta['refresh_scope']}  
Number of companies: {len(companies)}

## VC Summary

{category.get('vc_summary')}

## Market Map

{markdown_table(
    ["Company", "Stage", "HQ", "Product", "Funding USDm", "Key Investors", "VC Priority", "Last Updated"],
    company_rows(companies),
)}

## Top Watchlist Names

{chr(10).join(f"{index}. {company['name']}" for index, company in enumerate(companies[:10], 1)) or "No scored companies yet."}

## Company Profiles

{chr(10).join(profiles) or "No companies recorded yet."}

## Diligence Questions

{chr(10).join(f"- {question}" for question in questions)}

## Key Sources

{chr(10).join(f"- [{source.get('title')}]({source.get('url')})" for source in sources if source.get('url')) or "No sources recorded yet."}

## Refresh Notes

{meta.get('refresh_summary') or "Initial repository scaffold; category research is pending."}
"""
        write(DOCS / "category_landscape" / f"{category_id}.md", category["display_name"], body)


def generate_dashboard() -> None:
    companies = ranked_companies(all_companies())
    refresh = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    stale = load_yaml(METADATA_DIR / "stale_sections.yaml", {"stale_sections": []})["stale_sections"]
    category_scores = defaultdict(list)
    for company in companies:
        average, count = score_value(company)
        if count:
            category_scores[company["primary_category"]].append(average)
    category_rows = sorted(
        ((category, round(sum(values) / len(values), 2), len(values))
         for category, values in category_scores.items()),
        key=lambda row: row[1],
        reverse=True,
    )
    write(
        DOCS / "vc_dashboard.md",
        "VC Dashboard",
        f"""## Top Companies by VC Priority

{markdown_table(
    ["Company", "Category", "Priority", "Average Score"],
    [[c["name"], c["primary_category"], c.get("strategic_scoring", {}).get("overall_vc_priority"),
      f"{score_value(c)[0]:.2f}" if score_value(c)[1] else "Unscored"] for c in companies[:25]],
)}

## Highest-Scoring Categories

{markdown_table(["Category", "Average Score", "Scored Companies"], category_rows)}

## Stale Categories Needing Refresh

{chr(10).join(f"- {item}" for item in stale) or "No sections are currently flagged stale."}

## Active Diligence

{chr(10).join(f"- {c['name']}" for c in companies if c.get('strategic_scoring', {}).get('overall_vc_priority') == 'active_diligence') or "None."}

## Recent Changes

See [CHANGELOG](../CHANGELOG.md) and [refresh status](refresh_status.md).

## Research and Patent Signals

- [Research radar](research_radar.md)
- [Patent radar](patent_radar.md)
- [Founder radar](founder_radar.md)
""",
    )


def generate_research_docs() -> None:
    papers = load_yaml(RESEARCH_DIR / "papers.yaml", [])
    patents = load_yaml(RESEARCH_DIR / "patents.yaml", [])
    researchers = load_yaml(RESEARCH_DIR / "researchers.yaml", [])
    labs = load_yaml(RESEARCH_DIR / "labs_and_universities.yaml", [])
    themes = load_yaml(RESEARCH_DIR / "emerging_research_themes.yaml", [])
    papers = sorted(papers, key=lambda x: x.get("commercialization_potential", {}).get("score") or 0, reverse=True)
    patents = sorted(patents, key=lambda x: x.get("commercialization_signal", {}).get("score") or 0, reverse=True)
    researchers = sorted(researchers, key=lambda x: x.get("commercialization_signal", {}).get("score") or 0, reverse=True)
    write(
        DOCS / "research_radar.md", "Research Radar",
        f"""## Top Papers by Commercialization Potential

{markdown_table(
    ["Paper", "Venue", "Categories", "Score", "Investor Relevance"],
    [[p.get("title"), p.get("venue"), p.get("research_category"),
      p.get("commercialization_potential", {}).get("score"), p.get("investor_relevance")] for p in papers],
)}

## Emerging Technology Themes

{markdown_table(["Theme", "Categories", "Maturity", "Investor Relevance"],
                [[t.get("name"), t.get("categories"), t.get("maturity"), t.get("investor_relevance")] for t in themes])}

## Leading Researchers

{markdown_table(["Researcher", "Affiliation", "Areas", "Commercialization Score"],
                [[r.get("name"), r.get("current_affiliation"), r.get("research_areas"),
                  r.get("commercialization_signal", {}).get("score")] for r in researchers])}

## Labs Producing Relevant Work

{markdown_table(["Lab", "Institution", "Focus Areas", "Startup Signals"],
                [[l.get("name"), l.get("institution"), l.get("focus_areas"), l.get("startup_signals")] for l in labs])}

## Startup Formation Signals

See [hot research opportunities](views/hot_research_to_startup_opportunities.md).
""",
    )
    assignees = Counter(p.get("assignee") for p in patents if p.get("assignee"))
    write(
        DOCS / "patent_radar.md", "Patent Radar",
        f"""## Patents by Commercialization Signal

{markdown_table(
    ["Patent", "Assignee", "Categories", "Score", "Investor Relevance"],
    [[p.get("title"), p.get("assignee"), p.get("research_category"),
      p.get("commercialization_signal", {}).get("score"), p.get("investor_relevance")] for p in patents],
)}

## High-Signal Assignees

{markdown_table(["Assignee", "Patent Count"], assignees.most_common())}

## Inventors and Patent Clusters

Use `technology_tags`, `related_researchers`, and `related_papers` in the source YAML to build clusters.

## Patent White Spaces

Record identified white spaces in `data/research/emerging_research_themes.yaml`; do not infer freedom to operate from this database.
""",
    )
    write(
        DOCS / "founder_radar.md", "Founder Radar",
        f"""## Researchers with High Commercialization Signal

{markdown_table(
    ["Researcher", "Affiliation", "Score", "Evidence", "Possible Startup Angle"],
    [[r.get("name"), r.get("current_affiliation"), r.get("commercialization_signal", {}).get("score"),
      r.get("commercialization_signal", {}).get("evidence"), r.get("possible_startup_angle")] for r in researchers],
)}

## Suggested Monitoring Priority

Prioritize repeated top-tier publication, meaningful patent activity, open-source adoption, industry collaboration, and evidence of customer discovery. Verify all outreach and employment restrictions separately.
""",
    )


def generate_market_docs() -> None:
    transactions = load_yaml(TRANSACTION_DIR / "ma_transactions.yaml", [])
    investors = all_investors()
    write(
        DOCS / "ma_exit_landscape.md", "M&A and Exit Landscape",
        f"""## Transactions

{markdown_table(
    ["Target", "Acquirer", "Categories", "Status", "Value USDm", "Strategic Rationale", "VC Read-Through"],
    [[t.get("target_company"), t.get("acquirer"), t.get("target_categories"), t.get("transaction_status"),
      t.get("transaction_value_usd_m"), t.get("strategic_rationale"), t.get("exit_readthrough_for_vc")]
     for t in transactions],
)}

## Strategic Acquirers

See [strategic acquirer watchlist](views/strategic_acquirer_watchlist.md).
""",
    )
    write(
        DOCS / "investor_landscape.md", "Investor Landscape",
        f"""## Active Investors

{markdown_table(
    ["Investor", "Type", "Preferred Stage", "Relevant Partners", "Portfolio", "Sourcing Score"],
    [[i.get("name"), i.get("investor_type"), i.get("preferred_stage"), i.get("relevant_partners"),
      i.get("relevant_portfolio_companies"), i.get("relevance_for_deal_sourcing", {}).get("score")]
     for i in investors],
)}

## Co-Investor Network

The structured network is maintained in `data/investors/co_investor_network.yaml`.
""",
    )


def generate_refresh_docs() -> None:
    refresh = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    write(
        DOCS / "refresh_status.md", "Refresh Status",
        markdown_table(
            ["Section", "Last Refreshed", "Scope", "Owner", "Next Refresh"],
            [[value.get("display_name"), value.get("last_refreshed"), value.get("refresh_scope"),
              value.get("refreshed_by"), value.get("next_refresh_recommendation")]
             for value in refresh.values()],
        ),
    )
    write(
        DOCS / "views" / "stale_sections_need_refresh.md", "Stale Sections Needing Refresh",
        "See the generated [refresh status](../refresh_status.md) and `data/metadata/stale_sections.yaml`.",
    )


def generate_index() -> None:
    write(
        DOCS / "index.md", "Semiconductor VC Landscape",
        """This documentation is generated from the YAML source-of-truth database.

- [VC dashboard](vc_dashboard.md)
- [Company landscape](company_landscape.md)
- [Research radar](research_radar.md)
- [Patent radar](patent_radar.md)
- [Founder radar](founder_radar.md)
- [M&A and exit landscape](ma_exit_landscape.md)
- [Investor landscape](investor_landscape.md)
- [Refresh status](refresh_status.md)
""",
    )
    categories = category_map()
    write(
        DOCS / "company_landscape.md", "Company Landscape",
        "\n".join(
            f"- [{item['display_name']}](category_landscape/{category_id}.md)"
            for category_id, item in categories.items()
        ),
    )


def generate_docs() -> None:
    generate_category_pages()
    generate_dashboard()
    generate_research_docs()
    generate_market_docs()
    generate_refresh_docs()
    generate_index()


def main() -> int:
    generate_docs()
    print(f"Documentation written to {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
