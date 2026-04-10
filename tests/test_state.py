"""Tests for AdminOpsState."""

from __future__ import annotations

from collections import deque

import pytest

from admin_meta_agents.state import AdminOpsState


def test_initial_defaults() -> None:
    state = AdminOpsState()
    assert state.available_resources == 0
    assert state.allocated_resources == 0
    assert state.active_agents == 0
    assert len(state.pending_tasks) == 0
    assert state.performance_metrics == {}
    assert state.incidents == []


def test_pending_tasks_coerced_to_deque() -> None:
    state = AdminOpsState(pending_tasks=["a", "b"])  # type: ignore[arg-type]
    assert isinstance(state.pending_tasks, deque)
    assert list(state.pending_tasks) == ["a", "b"]


def test_add_and_assign_task() -> None:
    state = AdminOpsState()
    state.add_task("task-1")
    state.add_task("task-2")
    assert list(state.pending_tasks) == ["task-1", "task-2"]

    state.assign_task("task-1")
    assert list(state.pending_tasks) == ["task-2"]


def test_assign_non_head_task() -> None:
    state = AdminOpsState(pending_tasks=deque(["a", "b", "c"]))
    state.assign_task("b")
    assert list(state.pending_tasks) == ["a", "c"]


def test_assign_missing_task_is_noop() -> None:
    state = AdminOpsState(pending_tasks=deque(["a"]))
    state.assign_task("nonexistent")
    assert list(state.pending_tasks) == ["a"]


def test_log_incident() -> None:
    state = AdminOpsState()
    state.log_incident("disk full")
    state.log_incident("network timeout")
    assert state.incidents == ["disk full", "network timeout"]


def test_record_metric() -> None:
    state = AdminOpsState()
    state.record_metric("latency", 1.5)
    state.record_metric("latency", 2.0)
    assert state.performance_metrics["latency"] == 2.0


def test_spin_up_agent() -> None:
    state = AdminOpsState(available_resources=5)
    state.spin_up_agent(2)
    assert state.available_resources == 3
    assert state.allocated_resources == 2
    assert state.active_agents == 1


def test_spin_up_agent_insufficient_resources() -> None:
    state = AdminOpsState(available_resources=0)
    with pytest.raises(ValueError, match="Insufficient resources"):
        state.spin_up_agent(1)


def test_spin_down_agent() -> None:
    state = AdminOpsState(available_resources=2, allocated_resources=3, active_agents=2)
    state.spin_down_agent(1)
    assert state.available_resources == 3
    assert state.allocated_resources == 2
    assert state.active_agents == 1


def test_spin_down_agent_none_active() -> None:
    state = AdminOpsState(active_agents=0)
    with pytest.raises(ValueError, match="No active agents"):
        state.spin_down_agent()


def test_spin_down_clamps_allocated_to_zero() -> None:
    state = AdminOpsState(available_resources=0, allocated_resources=0, active_agents=1)
    state.spin_down_agent(5)
    assert state.allocated_resources == 0
    assert state.available_resources == 5
