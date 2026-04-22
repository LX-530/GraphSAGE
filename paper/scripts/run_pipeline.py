#!/usr/bin/env python3
"""Run the daily paper pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCOUT = ROOT / "scripts" / "stealth_scout.py"
GRAPH = ROOT / "generate_agent_graph.py"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the pre-scan report and graph generation.")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--download-limit", type=int, default=0)
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, str(SCOUT), "--limit", str(args.limit), "--download-limit", str(args.download_limit)],
        check=True,
        cwd=ROOT,
    )
    subprocess.run([sys.executable, str(GRAPH)], check=True, cwd=ROOT)
    print("Pipeline finished.")


if __name__ == "__main__":
    main()
