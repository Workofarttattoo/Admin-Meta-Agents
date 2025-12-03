"""Domain models representing the operations state tracked by meta-agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AdminOpsState:
    """Container describing the current administrative operations environment.

    The state is intentionally lightweight so it can be serialised or logged for
    audit trails. Meta-agents can mutate this state to keep track of actions
    taken during a workflow.
    """

    available_resources: int = 0
    """Number of resource units (e.g. compute slots, credits) currently free."""

    allocated_resources: int = 0
    """Number of resource units that have been reserved for running agents."""

    active_agents: int = 0
    """How many agents are currently live in the system."""

    pending_tasks: List[str] = field(default_factory=list)
    """Tasks that still need to be assigned to an agent."""

    performance_metrics: Dict[str, float] = field(default_factory=dict)
    """Aggregated metrics that can be updated by monitoring agents."""

    incidents: List[str] = field(default_factory=list)
    """Incident log describing exceptional events raised during a workflow."""

    def log_incident(self, message: str) -> None:
        """Append an incident description to the log."""

        self.incidents.append(message)

    def record_metric(self, metric: str, value: float) -> None:
        """Record or update a performance metric."""

        self.performance_metrics[metric] = value

    def assign_task(self, task: str) -> None:
        """Move a task from the pending queue into active work."""

        if task in self.pending_tasks:
            self.pending_tasks.remove(task)

    def add_task(self, task: str) -> None:
        """Add a new task to the pending queue."""

        self.pending_tasks.append(task)

    def spin_up_agent(self, resources_required: int = 1) -> None:
        """Provision a new agent if enough resources exist."""

        if resources_required > self.available_resources:
            raise ValueError("Insufficient resources to spin up agent")
        self.available_resources -= resources_required
        self.allocated_resources += resources_required
        self.active_agents += 1

    def spin_down_agent(self, resources_reclaimed: int = 1) -> None:
        """Decommission an agent and free its resources."""

        if self.active_agents == 0:
            raise ValueError("No active agents to spin down")
        self.active_agents -= 1
        self.available_resources += resources_reclaimed
        self.allocated_resources = max(0, self.allocated_resources - resources_reclaimed)
