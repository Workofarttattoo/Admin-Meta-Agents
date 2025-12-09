#!/usr/bin/env python3
"""Main entry point for the Admin Meta-Agents framework."""

import logging
import argparse
from admin_meta_agents import setup_logging
from admin_meta_agents.meta_agents import create_meta_agent_system, execute_coordination_workflow
from admin_meta_agents.agents import (
    create_crisis_response_system,
    create_healthcare_policy_system,
    create_economic_policy_system,
    execute_crisis_response,
    execute_healthcare_policy_lifecycle,
    execute_economic_policy_cycle
)


logger = logging.getLogger(__name__)


def run_meta_agent_demo():
    """Run a demonstration of the meta-agent system."""
    logger.info("="*60)
    logger.info("RUNNING META-AGENT COORDINATION DEMO")
    logger.info("="*60)

    meta_agents = create_meta_agent_system()
    execute_coordination_workflow(meta_agents)

    # Display status
    print("\n" + "="*60)
    print("META-AGENT STATUS REPORT")
    print("="*60)
    for name, agent in meta_agents.items():
        status = agent.get_status()
        print(f"\n{status['name']}:")
        print(f"  State: {status['state']}")
        print(f"  Tools Available: {status['tools_available']}")
        print(f"  Executions: {status['executions']}")


def run_crisis_response_demo():
    """Run a demonstration of crisis response."""
    logger.info("="*60)
    logger.info("RUNNING CRISIS RESPONSE DEMO")
    logger.info("="*60)

    agents = create_crisis_response_system()
    results = execute_crisis_response(agents)

    print("\n" + "="*60)
    print("CRISIS RESPONSE RESULTS")
    print("="*60)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")


def run_healthcare_policy_demo():
    """Run a demonstration of healthcare policy lifecycle."""
    logger.info("="*60)
    logger.info("RUNNING HEALTHCARE POLICY DEMO")
    logger.info("="*60)

    agents = create_healthcare_policy_system()
    results = execute_healthcare_policy_lifecycle(agents)

    print("\n" + "="*60)
    print("HEALTHCARE POLICY RESULTS")
    print("="*60)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")


def run_economic_policy_demo():
    """Run a demonstration of economic policy cycle."""
    logger.info("="*60)
    logger.info("RUNNING ECONOMIC POLICY DEMO")
    logger.info("="*60)

    agents = create_economic_policy_system()
    results = execute_economic_policy_cycle(agents)

    print("\n" + "="*60)
    print("ECONOMIC POLICY RESULTS")
    print("="*60)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Admin Meta-Agents Framework - Hierarchical agent coordination system"
    )
    parser.add_argument(
        "--mode",
        choices=["meta", "crisis", "healthcare", "economic", "all"],
        default="all",
        help="Demonstration mode to run (default: all)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)

    logger.info("Admin Meta-Agents Framework Starting...")

    try:
        if args.mode == "all":
            run_meta_agent_demo()
            print("\n")
            run_crisis_response_demo()
            print("\n")
            run_healthcare_policy_demo()
            print("\n")
            run_economic_policy_demo()
        elif args.mode == "meta":
            run_meta_agent_demo()
        elif args.mode == "crisis":
            run_crisis_response_demo()
        elif args.mode == "healthcare":
            run_healthcare_policy_demo()
        elif args.mode == "economic":
            run_economic_policy_demo()

        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("="*60)

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
