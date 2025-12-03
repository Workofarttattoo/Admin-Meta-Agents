from __future__ import annotations

import pytest

from admin_meta_agents.agents import MetaAgent, Tool, ToolExecutionResult
from admin_meta_agents.state import AdminOpsState


def test_meta_agent_executes_registered_tool() -> None:
    state = AdminOpsState(available_resources=3)

    def _handler(local_state: AdminOpsState, increment: int) -> int:
        local_state.available_resources += increment
        return local_state.available_resources

    agent = MetaAgent("Tester", tools=[Tool("bump", "", _handler)])
    result = agent.execute(state, "bump", 2)

    assert isinstance(result, ToolExecutionResult)
    assert result.success is True
    assert result.output == 5
    assert state.available_resources == 5


def test_meta_agent_handles_unknown_action() -> None:
    agent = MetaAgent("Tester")
    result = agent.execute(AdminOpsState(), "unknown")
    assert result.success is False
    assert isinstance(result.error, KeyError)


def test_meta_agent_prevents_duplicate_tools() -> None:
    agent = MetaAgent("Tester")
    tool = Tool("action", "", lambda s: None)
    agent.register_tool(tool)
    with pytest.raises(ValueError):
        agent.register_tool(tool)
