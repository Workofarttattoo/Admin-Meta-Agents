from __future__ import annotations

import pytest

from admin_meta_agents.agents import MetaAgent, Tool, ToolExecutionResult, build_tools
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


def test_build_tools_with_docstrings() -> None:
    def handler_one(state: AdminOpsState) -> str:
        """First tool description."""
        return "one"

    def handler_two(state: AdminOpsState) -> str:
        """Second tool description."""
        return "two"

    tool_map = {"one": handler_one, "two": handler_two}
    tools = list(build_tools(tool_map))

    assert len(tools) == 2
    assert tools[0].name == "one"
    assert tools[0].description == "First tool description."
    assert tools[0].handler == handler_one

    assert tools[1].name == "two"
    assert tools[1].description == "Second tool description."
    assert tools[1].handler == handler_two


def test_build_tools_without_docstrings() -> None:
    def handler_no_doc(state: AdminOpsState) -> str:
        return "no doc"

    tool_map = {"no_doc": handler_no_doc}
    tools = list(build_tools(tool_map))

    assert len(tools) == 1
    assert tools[0].name == "no_doc"
    assert tools[0].description == "Handler for no_doc"
    assert tools[0].handler == handler_no_doc


def test_build_tools_empty_map() -> None:
    tools = list(build_tools({}))
    assert len(tools) == 0
