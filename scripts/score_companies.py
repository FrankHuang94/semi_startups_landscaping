#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import all_companies, ranked_companies, score_value


def score_report() -> dict:
    companies = ranked_companies(all_companies())
    buckets = {
        "top_vc_watchlist": companies[:25],
        "high_conviction": [],
        "active_diligence": [],
        "monitor": [],
        "pass": [],
        "high_risk_high_upside": [],
        "technical_strength_commercial_gap": [],
        "traction_without_clear_moat": [],
        "missing_diligence": [],
    }
    for company in companies:
        scoring = company.get("strategic_scoring", {})
        priority = scoring.get("overall_vc_priority")
        if priority in buckets:
            buckets[priority].append(company)
        technical = scoring.get("technical_differentiation")
        customer = scoring.get("customer_pull")
        capital = scoring.get("capital_efficiency")
        if technical and technical >= 4 and (customer or 0) <= 2:
            buckets["technical_strength_commercial_gap"].append(company)
        if customer and customer >= 4 and (technical or 0) <= 2:
            buckets["traction_without_clear_moat"].append(company)
        if technical and technical >= 4 and capital and capital <= 2:
            buckets["high_risk_high_upside"].append(company)
        if score_value(company)[1] < 6 or company.get("data_quality", {}).get("missing_fields"):
            buckets["missing_diligence"].append(company)
    return buckets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = score_report()
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        for name, records in report.items():
            print(f"{name}: {len(records)}")
            for company in records[:25]:
                average, count = score_value(company)
                print(f"  - {company['name']} ({average:.2f}, {count} scored dimensions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
