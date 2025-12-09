#!/usr/bin/env python3
"""Basic usage example of the Admin Meta-Agents framework."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_meta_agents import setup_logging, OversightCoordinator, ResourceManager


def main():
    """Demonstrate basic usage of meta-agents."""
    setup_logging()

    print("="*60)
    print("BASIC USAGE EXAMPLE")
    print("="*60)

    # Create meta-agents
    print("\nCreating meta-agents...")
    oversight = OversightCoordinator()
    resources = ResourceManager()

    # Execute individual actions
    print("\nExecuting oversight coordinator actions:")
    result = oversight.execute("monitor_system")
    print(f"  {result}")

    result = oversight.execute("identify_needs")
    print(f"  {result}")

    print("\nExecuting resource manager actions:")
    result = resources.execute("allocate_resources")
    print(f"  {result}")

    result = resources.execute("usage_report")
    print(f"  {result}")

    # Display status
    print("\n" + "="*60)
    print("AGENT STATUS")
    print("="*60)
    print(f"\n{oversight.name}:")
    print(f"  Tools: {len(oversight.tool_instances)}")
    print(f"  Executions: {sum(t.execution_count for t in oversight.tool_instances.values())}")

    print(f"\n{resources.name}:")
    print(f"  Tools: {len(resources.tool_instances)}")
    print(f"  Executions: {sum(t.execution_count for t in resources.tool_instances.values())}")


if __name__ == "__main__":
    main()
