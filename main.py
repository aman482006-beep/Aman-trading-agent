"""Run one of the repository's deterministic agent_lab demonstrations."""
from __future__ import annotations

import argparse
import runpy


DEMO_MODULES = {
    "portfolio": "agent_lab.portfolio_guardian.demo",
    "research": "agent_lab.research_copilot.demo",
    "earnings": "agent_lab.earnings_intelligence.demo",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a deterministic Agentic Finance Research Lab demonstration."
    )
    parser.add_argument(
        "demo",
        nargs="?",
        choices=tuple(DEMO_MODULES),
        default="portfolio",
        help="Demonstration to run (default: portfolio).",
    )
    args = parser.parse_args()
    runpy.run_module(DEMO_MODULES[args.demo], run_name="__main__")


if __name__ == "__main__":
    main()
