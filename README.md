# Admin Meta-Agents

An orchestration framework for coordinating administrative meta-agents through tool-based workflows. Each agent owns a set of **tools** (callable capabilities) and a **workflow** chains agents together to execute multi-step operations against a shared state.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Workflow                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │  Step 1   │──▶│  Step 2   │──▶│  Step N   │──▶ Result   │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│       │               │               │                     │
│       ▼               ▼               ▼                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │  Agent   │    │  Agent   │    │  Agent   │                │
│  │  + Tools │    │  + Tools │    │  + Tools │                │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│       │               │               │                     │
│       └───────────────┼───────────────┘                     │
│                       ▼                                     │
│              ┌────────────────┐                              │
│              │ AdminOpsState  │                              │
│              │ (shared state) │                              │
│              └────────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Description |
|---|---|
| `AdminOpsState` | Shared mutable state — resources, agents, tasks, metrics, incidents |
| `Tool` | A named callable capability with a description |
| `MetaAgent` | An agent that owns and executes registered tools |
| `Workflow` | An ordered sequence of steps that coordinates agents |
| `WorkflowStep` | A single step binding an agent to an action |
| `WorkflowResult` | Execution summary with per-step success/failure |

### Built-in Agents

| Agent | Tools | Purpose |
|---|---|---|
| Oversight Coordinator | `monitor_system`, `identify_needs`, `coordinate_actions` | System health monitoring and coordination |
| Resource Manager | `allocate_resources`, `usage_report` | Resource allocation and reporting |
| Task Scheduler | `assign_tasks`, `priority_update`, `balance_workload` | Task queue management and load balancing |
| Performance Monitor | `evaluate_performance`, `identify_bottlenecks`, `generate_metrics` | Performance analysis and metrics |
| Lifecycle Manager | `spin_up_agent`, `spin_down_agent`, `reclaim_resources` | Agent provisioning and teardown |

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for containerised deployment)

### Local Development

```bash
# Clone the repository
git clone https://github.com/Workofarttattoo/Admin-Meta-Agents.git
cd Admin-Meta-Agents

# Install with dev dependencies
pip install -e ".[dev]"

# Run the default workflow
python main.py

# Run tests
make test

# Lint and type-check
make lint
make typecheck
```

### Docker

```bash
# Copy and configure environment
cp .env.example .env

# Build and run
make build
make up

# View logs
make logs

# Stop
make down
```

## Usage

### Run the Default Workflow

```python
from admin_meta_agents.examples import run_default_workflow

summary = run_default_workflow()
print(summary)
```

### Build Custom Agents

```python
from admin_meta_agents import AdminOpsState, MetaAgent, Tool, Workflow, WorkflowStep

# Define a custom tool
def my_tool(state: AdminOpsState) -> str:
    state.record_metric("custom_metric", 42.0)
    return "Custom tool executed"

# Create an agent with the tool
agent = MetaAgent("Custom Agent", tools=[
    Tool(name="my_tool", description="A custom tool", handler=my_tool),
])

# Execute directly
result = agent.execute(AdminOpsState(available_resources=5), "my_tool")
print(result.output)  # "Custom tool executed"
```

### Build Custom Workflows

```python
from admin_meta_agents import AdminOpsState, Workflow, WorkflowStep
from admin_meta_agents.examples import build_default_agents

state, agents = build_default_agents()

workflow = Workflow(state)
workflow.add_step(WorkflowStep(agents["Oversight Coordinator"], "monitor_system"))
workflow.add_step(WorkflowStep(agents["Task Scheduler"], "assign_tasks", args=(3,)))
workflow.add_step(WorkflowStep(agents["Performance Monitor"], "generate_metrics"))

result = workflow.run()
print(result.render_summary())
print(f"All steps passed: {result.successful}")
```

## API Reference

### `AdminOpsState`

Shared state container tracking resources, agents, tasks, and metrics.

| Field | Type | Description |
|---|---|---|
| `available_resources` | `int` | Free resource units |
| `allocated_resources` | `int` | Reserved resource units |
| `active_agents` | `int` | Currently running agents |
| `pending_tasks` | `Deque[str]` | Task queue |
| `performance_metrics` | `Dict[str, float]` | Named metrics |
| `incidents` | `List[str]` | Incident log |

**Methods:** `add_task()`, `assign_task()`, `spin_up_agent()`, `spin_down_agent()`, `log_incident()`, `record_metric()`

### `MetaAgent`

| Method | Description |
|---|---|
| `register_tool(tool)` | Register a new tool |
| `execute(state, action, *args, **kwargs)` | Execute a named tool against state |
| `tools` | Property returning registered tools dict |

### `Workflow`

| Method | Description |
|---|---|
| `add_step(step)` | Append a workflow step |
| `run()` | Execute all steps sequentially, returns `WorkflowResult` |
| `steps` | Property returning step list |

### `WorkflowResult`

| Field / Property | Description |
|---|---|
| `steps` | List of executed steps |
| `results` | List of `ToolExecutionResult` per step |
| `successful` | `True` if every step succeeded |
| `render_summary()` | Human-readable execution summary |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `MAX_RESOURCES` | `10` | Maximum resource pool size |
| `ENABLE_AUTO_SCALING` | `false` | Auto-scale agents on demand |
| `ENABLE_INCIDENT_ALERTS` | `false` | Send alerts on incidents |
| `WEBHOOK_URL` | — | External event webhook |
| `API_KEY` | — | API authentication key |
| `DATABASE_URL` | — | Database connection string |

## Development

```bash
make help          # Show all available commands
make install       # Install with dev dependencies
make test          # Run tests with coverage
make lint          # Lint with ruff
make typecheck     # Type-check with mypy
make format        # Auto-format code
make clean         # Remove build artifacts
```

### Deployment

```bash
# Standard deploy
./scripts/deploy.sh

# Deploy to staging
./scripts/deploy.sh staging

# Dry-run (preview only)
DRY_RUN=1 ./scripts/deploy.sh
```

## Project Structure

```
Admin-Meta-Agents/
├── admin_meta_agents/       # Core package
│   ├── __init__.py          # Public API exports
│   ├── agents.py            # MetaAgent, Tool, ToolExecutionResult
│   ├── state.py             # AdminOpsState
│   ├── workflow.py          # Workflow, WorkflowStep, WorkflowResult
│   └── examples.py          # Built-in agents and demo workflow
├── tests/                   # Test suite
│   ├── conftest.py
│   ├── test_agents.py
│   ├── test_state.py
│   └── test_workflow.py
├── examples/                # Legacy agent prototypes (reference only)
│   └── legacy/
├── scripts/
│   └── deploy.sh            # Build, test, and deploy script
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── .env.example
└── README.md
```

## License

MIT — see [LICENSE](LICENSE) for details.
