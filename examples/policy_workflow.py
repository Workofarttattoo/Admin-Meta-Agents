#!/usr/bin/env python3
"""Example of healthcare and economic policy workflows."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_meta_agents import setup_logging
from admin_meta_agents.agents.healthcare import create_healthcare_policy_system
from admin_meta_agents.agents.economic import create_economic_policy_system


def run_healthcare_example():
    """Demonstrate healthcare policy workflow."""
    print("="*60)
    print("HEALTHCARE POLICY LIFECYCLE")
    print("="*60)

    agents = create_healthcare_policy_system()

    # Execute policy lifecycle phases
    phases = [
        ("Data Analysis", "data_analysis"),
        ("Policy Formulation", "formulation"),
        ("Implementation", "implementation"),
        ("Monitoring", "monitoring"),
        ("Evaluation", "evaluation")
    ]

    for phase_name, agent_key in phases:
        print(f"\n--- {phase_name.upper()} ---")
        results = agents[agent_key].execute_workflow()
        for result in results:
            print(f"  • {result}")


def run_economic_example():
    """Demonstrate economic policy workflow."""
    print("\n" + "="*60)
    print("ECONOMIC POLICY CYCLE")
    print("="*60)

    agents = create_economic_policy_system()

    # Execute policy cycle phases
    phases = [
        ("Economic Analysis", "analysis"),
        ("Policy Development", "development"),
        ("Implementation", "implementation"),
        ("Monitoring", "monitoring"),
        ("Adjustment", "adjustment")
    ]

    for phase_name, agent_key in phases:
        print(f"\n--- {phase_name.upper()} ---")
        results = agents[agent_key].execute_workflow()
        for result in results:
            print(f"  • {result}")


def main():
    """Run both policy workflow examples."""
    setup_logging()

    run_healthcare_example()
    print("\n")
    run_economic_example()

    print("\n" + "="*60)
    print("POLICY WORKFLOWS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
