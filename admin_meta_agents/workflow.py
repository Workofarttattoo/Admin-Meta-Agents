"""Workflow orchestration for coordinating meta-agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Sequence

from .agents import MetaAgent, ToolExecutionResult
from .state import AdminOpsState


@dataclass
class WorkflowStep:
    """Single step in a workflow, referencing an agent and an action."""

    agent: MetaAgent
    action: str
    args: Sequence[Any] = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    description: str | None = None


@dataclass
class WorkflowResult:
    """Summary of a workflow execution."""

    steps: List[WorkflowStep]
    results: List[ToolExecutionResult]

    @property
    def successful(self) -> bool:
        return all(result.success for result in self.results)

    def render_summary(self) -> str:
        lines = []
        for step, result in zip(self.steps, self.results):
            status = "OK" if result.success else f"FAILED: {result.error}"
            lines.append(f"{step.agent.name}::{step.action} -> {status}")
        return "\n".join(lines)


class Workflow:
    """Container for coordinating a set of workflow steps."""

    def __init__(self, state: AdminOpsState, steps: Iterable[WorkflowStep] | None = None) -> None:
        self.state = state
        self._steps: List[WorkflowStep] = list(steps or [])

    def add_step(self, step: WorkflowStep) -> None:
        self._steps.append(step)

    def run(self) -> WorkflowResult:
        results: List[ToolExecutionResult] = []
        for step in self._steps:
            result = step.agent.execute(self.state, step.action, *step.args, **step.kwargs)
            results.append(result)
        return WorkflowResult(steps=list(self._steps), results=results)

    @property
    def steps(self) -> List[WorkflowStep]:
        return list(self._steps)
