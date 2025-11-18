"""Out-of-the-box tooling and workflows showcasing the meta-agent system."""

from __future__ import annotations

from typing import Dict, Tuple

from .agents import MetaAgent, build_tools
from .state import AdminOpsState
from .workflow import Workflow, WorkflowStep


def _oversight_tools() -> Dict[str, callable]:
    def monitor_system(state: AdminOpsState) -> str:
        """Capture a snapshot of the system health."""

        metric = float(state.active_agents) / max(1, state.allocated_resources or 1)
        state.record_metric("utilisation", min(metric, 1.0))
        return f"Health snapshot stored with utilisation={state.performance_metrics['utilisation']:.2f}"

    def identify_needs(state: AdminOpsState) -> str:
        """Analyse task queue and determine resource shortfall."""

        tasks_waiting = len(state.pending_tasks)
        if tasks_waiting > state.available_resources:
            state.log_incident("Resource shortfall detected")
        return f"Queued tasks={tasks_waiting}, available_resources={state.available_resources}"

    def coordinate_actions(state: AdminOpsState) -> str:
        """Coordinate communication between departments."""

        summary = {
            "active_agents": state.active_agents,
            "pending_tasks": len(state.pending_tasks),
            "incidents": len(state.incidents),
        }
        return f"Coordination summary: {summary}"

    return {
        "monitor_system": monitor_system,
        "identify_needs": identify_needs,
        "coordinate_actions": coordinate_actions,
    }


def _resource_tools() -> Dict[str, callable]:
    def allocate_resources(state: AdminOpsState, units: int = 1) -> str:
        """Allocate resources for incoming workloads."""

        if units > state.available_resources:
            state.log_incident("Allocation request exceeds availability")
            raise ValueError("Not enough resources available")
        state.available_resources -= units
        state.allocated_resources += units
        return f"Allocated {units} unit(s)"

    def deallocate_resources(state: AdminOpsState, units: int = 1) -> str:
        """Return unused resources to the pool."""

        state.available_resources += units
        state.allocated_resources = max(0, state.allocated_resources - units)
        return f"Deallocated {units} unit(s)"

    def usage_report(state: AdminOpsState) -> str:
        """Produce a human-readable usage report."""

        return (
            "Usage report: "
            f"allocated={state.allocated_resources}, "
            f"available={state.available_resources}, "
            f"active_agents={state.active_agents}"
        )

    return {
        "allocate_resources": allocate_resources,
        "deallocate_resources": deallocate_resources,
        "usage_report": usage_report,
    }


def _scheduler_tools() -> Dict[str, callable]:
    def assign_tasks(state: AdminOpsState, count: int = 1) -> str:
        """Assign tasks to active agents."""

        assigned = 0
        while state.pending_tasks and assigned < count:
            task = state.pending_tasks[0]
            state.assign_task(task)
            assigned += 1
        return f"Assigned {assigned} task(s)"

    def priority_update(state: AdminOpsState, priority: str) -> str:
        """Record a priority update for downstream teams."""

        state.record_metric("priority", len(priority))
        return f"Priority level updated to '{priority}'"

    def balance_workload(state: AdminOpsState) -> str:
        """Balance agent workload by spinning up additional capacity if needed."""

        if len(state.pending_tasks) > state.active_agents:
            try:
                state.spin_up_agent()
            except ValueError as exc:
                state.log_incident(str(exc))
                return "Failed to balance workload"
            return "Additional agent provisioned"
        return "Workload already balanced"

    return {
        "assign_tasks": assign_tasks,
        "priority_update": priority_update,
        "balance_workload": balance_workload,
    }


def _monitor_tools() -> Dict[str, callable]:
    def evaluate_performance(state: AdminOpsState) -> str:
        """Evaluate recent performance metrics."""

        utilisation = state.performance_metrics.get("utilisation", 0.0)
        if utilisation > 0.8:
            state.log_incident("High utilisation detected")
        return f"Evaluated utilisation={utilisation:.2f}"

    def identify_bottlenecks(state: AdminOpsState) -> str:
        """Identify potential bottlenecks in the workflow."""

        if len(state.pending_tasks) > state.active_agents * 2:
            state.log_incident("Bottleneck: insufficient active agents")
        return "Bottleneck analysis complete"

    def generate_metrics(state: AdminOpsState) -> str:
        """Generate a metrics bundle for dashboards."""

        return f"Metrics generated: {dict(state.performance_metrics)}"

    return {
        "evaluate_performance": evaluate_performance,
        "identify_bottlenecks": identify_bottlenecks,
        "generate_metrics": generate_metrics,
    }


def _lifecycle_tools() -> Dict[str, callable]:
    def spin_up_agent(state: AdminOpsState, resources_required: int = 1) -> str:
        """Provision a new agent instance."""

        state.spin_up_agent(resources_required)
        return f"Agent spun up using {resources_required} resource unit(s)"

    def spin_down_agent(state: AdminOpsState, resources_reclaimed: int = 1) -> str:
        """Decommission an existing agent instance."""

        state.spin_down_agent(resources_reclaimed)
        return f"Agent spun down, reclaimed {resources_reclaimed} unit(s)"

    def reclaim_resources(state: AdminOpsState) -> str:
        """Reclaim unused resources from collapsed agents."""

        reclaimed = max(0, state.allocated_resources - state.active_agents)
        state.available_resources += reclaimed
        state.allocated_resources -= reclaimed
        return f"Reclaimed {reclaimed} resource unit(s)"

    return {
        "spin_up_agent": spin_up_agent,
        "spin_down_agent": spin_down_agent,
        "reclaim_resources": reclaim_resources,
    }


def build_default_agents() -> Tuple[AdminOpsState, Dict[str, MetaAgent]]:
    """Construct the canonical agents and initial state used in demos."""

    state = AdminOpsState(
        available_resources=5,
        allocated_resources=0,
        active_agents=2,
        pending_tasks=["triage incident", "generate report", "update dashboard"],
    )

    agent_specs = {
        "Oversight Coordinator": _oversight_tools(),
        "Resource Manager": _resource_tools(),
        "Task Scheduler": _scheduler_tools(),
        "Performance Monitor": _monitor_tools(),
        "Lifecycle Manager": _lifecycle_tools(),
    }

    agents: Dict[str, MetaAgent] = {}
    for agent_name, tools in agent_specs.items():
        agents[agent_name] = MetaAgent(agent_name, build_tools(tools))

    return state, agents


def build_default_workflow(state: AdminOpsState, agents: Dict[str, MetaAgent]) -> Workflow:
    """Assemble a workflow that coordinates the default agents."""

    workflow = Workflow(state)
    workflow.add_step(WorkflowStep(agents["Oversight Coordinator"], "monitor_system"))
    workflow.add_step(WorkflowStep(agents["Oversight Coordinator"], "identify_needs"))
    workflow.add_step(WorkflowStep(agents["Resource Manager"], "allocate_resources", args=(2,)))
    workflow.add_step(WorkflowStep(agents["Lifecycle Manager"], "spin_up_agent", args=(1,)))
    workflow.add_step(WorkflowStep(agents["Task Scheduler"], "assign_tasks", args=(2,)))
    workflow.add_step(WorkflowStep(agents["Task Scheduler"], "balance_workload"))
    workflow.add_step(WorkflowStep(agents["Performance Monitor"], "evaluate_performance"))
    workflow.add_step(WorkflowStep(agents["Performance Monitor"], "identify_bottlenecks"))
    workflow.add_step(WorkflowStep(agents["Resource Manager"], "usage_report"))
    workflow.add_step(WorkflowStep(agents["Lifecycle Manager"], "reclaim_resources"))
    workflow.add_step(WorkflowStep(agents["Performance Monitor"], "generate_metrics"))
    return workflow


def run_default_workflow() -> str:
    """Execute the default workflow and return a printable summary."""

    state, agents = build_default_agents()
    workflow = build_default_workflow(state, agents)
    result = workflow.run()
    return result.render_summary()
