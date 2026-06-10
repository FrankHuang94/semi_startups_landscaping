#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.common import ROOT


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    run([sys.executable, "scripts/generate_schemas.py"])
    run([sys.executable, "scripts/validate_data.py"])
    run([sys.executable, "-m", "pytest"])
    run([sys.executable, "scripts/generate_docs.py"])
    run([sys.executable, "scripts/generate_watchlists.py"])
    run([sys.executable, "scripts/export_to_csv.py"])
    run([sys.executable, "scripts/export_to_sqlite.py"])
    print("Full build completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
