"""Command line entry point for running the default admin meta-agent workflow."""

from __future__ import annotations

import logging

from admin_meta_agents.examples import run_default_workflow


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def main() -> None:
    configure_logging()
    summary = run_default_workflow()
    print("=== Admin Meta-Agent Workflow Summary ===")
    print(summary)


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
