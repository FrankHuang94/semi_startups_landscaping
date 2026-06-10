#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semivc.models import Company, Investor, Paper, Patent, RefreshLog, Researcher, Transaction
from scripts.common import ROOT


MODELS = {
    "company.schema.json": Company,
    "paper.schema.json": Paper,
    "patent.schema.json": Patent,
    "researcher.schema.json": Researcher,
    "investor.schema.json": Investor,
    "transaction.schema.json": Transaction,
    "refresh_log.schema.json": RefreshLog,
}


def main() -> int:
    target = ROOT / "schemas"
    target.mkdir(parents=True, exist_ok=True)
    for filename, model in MODELS.items():
        schema = model.model_json_schema()
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        (target / filename).write_text(
            json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(f"JSON schemas written to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
