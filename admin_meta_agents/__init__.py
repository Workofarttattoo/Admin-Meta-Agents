"""Admin Meta-Agents Framework - Hierarchical multi-agent coordination system."""

import logging
from typing import Dict, Any

from .base import Agent, MetaAgent, Tool
from .meta_agents import (
    OversightCoordinator,
    ResourceManager,
    TaskScheduler,
    PerformanceMonitor,
    LifecycleManager,
    create_meta_agent_system,
    execute_coordination_workflow
)
from . import agents

__version__ = "0.1.0"
__author__ = "Admin Meta-Agents Team"

__all__ = [
    # Base classes
    "Agent",
    "MetaAgent",
    "Tool",
    # Meta-agents
    "OversightCoordinator",
    "ResourceManager",
    "TaskScheduler",
    "PerformanceMonitor",
    "LifecycleManager",
    "create_meta_agent_system",
    "execute_coordination_workflow",
    # Submodules
    "agents",
]


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the framework.

    Args:
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_version() -> str:
    """Get the current version of the framework.

    Returns:
        Version string
    """
    return __version__
