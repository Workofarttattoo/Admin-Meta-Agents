from __future__ import annotations

from admin_meta_agents.examples import build_default_agents, build_default_workflow


def test_default_workflow_runs_successfully() -> None:
    state, agents = build_default_agents()
    workflow = build_default_workflow(state, agents)
    result = workflow.run()

    assert result.successful is True
    assert len(result.steps) == len(result.results)
    assert state.active_agents >= 2  # Lifecycle manager may add more agents


def test_workflow_summary_contains_agent_names() -> None:
    state, agents = build_default_agents()
    workflow = build_default_workflow(state, agents)
    summary = workflow.run().render_summary()

    assert "Oversight Coordinator" in summary
    assert "Resource Manager" in summary
