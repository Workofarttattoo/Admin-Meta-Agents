"""Base classes for the Admin Meta-Agents framework."""

import logging
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class Tool:
    """Base class for agent tools.

    Tools encapsulate specific functionality that agents can use to perform actions.
    """

    def __init__(self, name: str, function: Callable, description: str = ""):
        """Initialize a Tool.

        Args:
            name: Unique identifier for the tool
            function: Callable that implements the tool's functionality
            description: Human-readable description of what the tool does
        """
        self.name = name
        self.function = function
        self.description = description
        self.execution_count = 0
        self.last_executed = None

    def execute(self, *args, **kwargs) -> Any:
        """Execute the tool's function.

        Args:
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function execution
        """
        try:
            self.execution_count += 1
            self.last_executed = datetime.now()
            logger.info(f"Executing tool: {self.name}")
            result = self.function(*args, **kwargs)
            logger.info(f"Tool {self.name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            raise

    def __repr__(self) -> str:
        return f"Tool(name='{self.name}', executions={self.execution_count})"


class Agent:
    """Base class for all agents in the system.

    Agents are autonomous entities that can execute workflows using tools.
    """

    def __init__(
        self,
        name: str,
        tools: Optional[List[str]] = None,
        workflow: Optional[List[Dict[str, str]]] = None,
        description: str = ""
    ):
        """Initialize an Agent.

        Args:
            name: Unique identifier for the agent
            tools: List of tool names the agent can use
            workflow: List of workflow steps (action + tool mappings)
            description: Human-readable description of the agent's purpose
        """
        self.name = name
        self.tools = tools or []
        self.workflow = workflow or []
        self.description = description
        self.tool_instances: Dict[str, Tool] = {}
        self.state = "initialized"
        self.execution_history: List[Dict[str, Any]] = []

        logger.info(f"Agent '{self.name}' initialized with {len(self.tools)} tools")

    def register_tool(self, tool: Tool) -> None:
        """Register a tool instance for this agent.

        Args:
            tool: Tool instance to register
        """
        self.tool_instances[tool.name] = tool
        logger.debug(f"Tool '{tool.name}' registered to agent '{self.name}'")

    def execute_action(self, action: str, tool_name: str, *args, **kwargs) -> Any:
        """Execute a specific action using a tool.

        Args:
            action: Name of the action to perform
            tool_name: Name of the tool to use
            *args: Positional arguments for the tool
            **kwargs: Keyword arguments for the tool

        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tool_instances:
            error_msg = f"Tool '{tool_name}' not registered for agent '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)

        tool = self.tool_instances[tool_name]
        logger.info(f"Agent '{self.name}' executing action '{action}' with tool '{tool_name}'")

        result = tool.execute(*args, **kwargs)

        # Record execution
        self.execution_history.append({
            "timestamp": datetime.now(),
            "action": action,
            "tool": tool_name,
            "result": str(result)[:100]  # Truncate for logging
        })

        return result

    def execute_workflow(self, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Execute the agent's complete workflow.

        Args:
            context: Optional context data for the workflow

        Returns:
            List of results from each workflow step
        """
        if not self.workflow:
            logger.warning(f"Agent '{self.name}' has no workflow defined")
            return []

        self.state = "running"
        logger.info(f"Agent '{self.name}' starting workflow with {len(self.workflow)} steps")

        results = []
        context = context or {}

        try:
            for step in self.workflow:
                action = step.get("action")
                tool_name = step.get("tool")

                if not action or not tool_name:
                    logger.warning(f"Invalid workflow step: {step}")
                    continue

                # Execute with context
                result = self.execute_action(action, tool_name, context=context)
                results.append(result)

                # Update context with result
                context[action] = result

            self.state = "completed"
            logger.info(f"Agent '{self.name}' completed workflow successfully")

        except Exception as e:
            self.state = "error"
            logger.error(f"Agent '{self.name}' workflow failed: {e}")
            raise

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the agent.

        Returns:
            Dictionary containing agent status information
        """
        return {
            "name": self.name,
            "state": self.state,
            "tools_available": len(self.tool_instances),
            "workflow_steps": len(self.workflow),
            "executions": len(self.execution_history)
        }

    def __repr__(self) -> str:
        return f"Agent(name='{self.name}', state='{self.state}', tools={len(self.tool_instances)})"


class MetaAgent(Agent):
    """Meta-agent for coordinating and managing other agents.

    MetaAgents have additional capabilities for managing subordinate agents.
    """

    def __init__(self, name: str, tools: Optional[Dict[str, Callable]] = None, description: str = ""):
        """Initialize a MetaAgent.

        Args:
            name: Unique identifier for the meta-agent
            tools: Dictionary mapping action names to functions
            description: Human-readable description
        """
        super().__init__(name, list(tools.keys()) if tools else [], description=description)
        self.managed_agents: List[Agent] = []

        # Register tools from dictionary
        if tools:
            for tool_name, tool_func in tools.items():
                tool = Tool(tool_name, tool_func)
                self.register_tool(tool)

    def execute(self, action: str, *args, **kwargs) -> Any:
        """Execute an action directly by name.

        Args:
            action: Name of the action/tool to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of the execution
        """
        if action not in self.tool_instances:
            return f"Action '{action}' not supported by {self.name}."

        return self.tool_instances[action].execute(*args, **kwargs)

    def register_agent(self, agent: Agent) -> None:
        """Register an agent for this meta-agent to manage.

        Args:
            agent: Agent instance to manage
        """
        self.managed_agents.append(agent)
        logger.info(f"Agent '{agent.name}' registered to meta-agent '{self.name}'")

    def get_managed_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all managed agents.

        Returns:
            List of status dictionaries for each managed agent
        """
        return [agent.get_status() for agent in self.managed_agents]
