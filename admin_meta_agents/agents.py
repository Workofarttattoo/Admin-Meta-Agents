"""Core agent models used across the admin meta-agent system."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional

from .state import AdminOpsState


logger = logging.getLogger(__name__)


ToolHandler = Callable[[AdminOpsState, Any], Any]


@dataclass(frozen=True)
class Tool:
    """A callable capability that can be executed by a :class:`MetaAgent`."""

    name: str
    description: str
    handler: Callable[[AdminOpsState, Any], Any]

    def __call__(self, state: AdminOpsState, *args: Any, **kwargs: Any) -> Any:
        return self.handler(state, *args, **kwargs)


@dataclass
class ToolExecutionResult:
    """Details from executing a tool."""

    success: bool
    output: Any = None
    error: Optional[Exception] = None

    def __bool__(self) -> bool:  # pragma: no cover - convenience only
        return self.success


class MetaAgent:
    """Agent that can execute named tooling against the shared state."""

    def __init__(self, name: str, tools: Optional[Iterable[Tool]] = None) -> None:
        self.name = name
        self._tools: Dict[str, Tool] = {}
        if tools:
            for tool in tools:
                self.register_tool(tool)

    def register_tool(self, tool: Tool) -> None:
        """Register a new tool that the meta-agent can execute."""

        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered for {self.name}")
        self._tools[tool.name] = tool
        logger.debug("Registered tool '%s' on agent '%s'", tool.name, self.name)

    def execute(
        self, state: AdminOpsState, action: str, *args: Any, **kwargs: Any
    ) -> ToolExecutionResult:
        """Execute a registered tool, capturing any raised exceptions."""

        tool = self._tools.get(action)
        if tool is None:
            error = KeyError(f"Action '{action}' not supported by {self.name}")
            logger.error(str(error))
            return ToolExecutionResult(success=False, error=error)

        logger.info("%s executing action '%s'", self.name, action)
        try:
            output = tool(state, *args, **kwargs)
        except Exception as exc:  # pragma: no cover - logging path
            logger.exception("Error executing action '%s' by agent '%s'", action, self.name)
            return ToolExecutionResult(success=False, error=exc)

        logger.debug(
            "Agent '%s' completed action '%s' with output: %s", self.name, action, output
        )
        return ToolExecutionResult(success=True, output=output)

    @property
    def tools(self) -> Dict[str, Tool]:
        """Expose a copy of registered tools for inspection."""

        return dict(self._tools)


def build_tools(tool_map: Dict[str, Callable[[AdminOpsState], Any]]) -> Iterable[Tool]:
    """Helper to convert a mapping of callables into :class:`Tool` instances."""

    for name, handler in tool_map.items():
        description = getattr(handler, "__doc__", "") or f"Handler for {name}"
        yield Tool(name=name, description=description.strip(), handler=handler)
