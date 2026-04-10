"""Tests for built-in example agents and workflows."""

from __future__ import annotations

from admin_meta_agents.examples import (
    build_default_agents,
    build_default_workflow,
    run_default_workflow,
)


def test_build_default_agents_returns_five_agents() -> None:
    state, agents = build_default_agents()
    assert len(agents) == 5
    expected = {
        "Oversight Coordinator",
        "Resource Manager",
        "Task Scheduler",
        "Performance Monitor",
        "Lifecycle Manager",
    }
    assert set(agents.keys()) == expected


def test_build_default_agents_initial_state() -> None:
    state, _ = build_default_agents()
    assert state.available_resources == 5
    assert state.active_agents == 2
    assert len(state.pending_tasks) == 3


def test_run_default_workflow_returns_string() -> None:
    summary = run_default_workflow()
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "OK" in summary


def test_all_default_tools_callable() -> None:
    _, agents = build_default_agents()
    for name, agent in agents.items():
        for tool_name, tool in agent.tools.items():
            assert callable(tool), f"{name}.{tool_name} is not callable"
