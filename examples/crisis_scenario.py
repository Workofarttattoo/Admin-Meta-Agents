#!/usr/bin/env python3
"""Example of using the crisis response system."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_meta_agents import setup_logging
from admin_meta_agents.agents.crisis import (
    CrisisCoordinator,
    SituationAssessment,
    ResourceAllocation,
    Communication,
    RecoveryPlanning
)


def main():
    """Demonstrate crisis response scenario."""
    setup_logging()

    print("="*60)
    print("CRISIS RESPONSE SCENARIO: Natural Disaster")
    print("="*60)

    # Create crisis response agents
    print("\nInitializing crisis response team...")
    coordinator = CrisisCoordinator()
    assessment = SituationAssessment()
    resources = ResourceAllocation()
    communication = Communication()
    recovery = RecoveryPlanning()

    # Phase 1: Initial Response
    print("\n--- PHASE 1: INITIAL RESPONSE ---")
    print("\nCoordinator monitoring situation:")
    coordinator_results = coordinator.execute_workflow()
    for result in coordinator_results:
        print(f"  • {result}")

    # Phase 2: Situation Assessment
    print("\n--- PHASE 2: SITUATION ASSESSMENT ---")
    print("\nAssessment team analyzing:")
    assessment_results = assessment.execute_workflow()
    for result in assessment_results:
        print(f"  • {result}")

    # Phase 3: Resource Deployment
    print("\n--- PHASE 3: RESOURCE DEPLOYMENT ---")
    print("\nResource team deploying:")
    resource_results = resources.execute_workflow()
    for result in resource_results:
        print(f"  • {result}")

    # Phase 4: Communication
    print("\n--- PHASE 4: STAKEHOLDER COMMUNICATION ---")
    print("\nCommunication team coordinating:")
    comm_results = communication.execute_workflow()
    for result in comm_results:
        print(f"  • {result}")

    # Phase 5: Recovery Planning
    print("\n--- PHASE 5: RECOVERY PLANNING ---")
    print("\nRecovery team planning:")
    recovery_results = recovery.execute_workflow()
    for result in recovery_results:
        print(f"  • {result}")

    # Summary
    print("\n" + "="*60)
    print("CRISIS RESPONSE COMPLETED")
    print("="*60)
    total_actions = (len(coordinator_results) + len(assessment_results) +
                    len(resource_results) + len(comm_results) + len(recovery_results))
    print(f"Total actions executed: {total_actions}")
    print("Status: All phases completed successfully")


if __name__ == "__main__":
    main()
