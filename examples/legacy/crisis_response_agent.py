# Crisis Coordinator Agent
crisis_coordinator = Agent(
    name="Crisis Coordinator",
    tools=[
        "data_feed_monitor",
        "situation_assessment_request",
        "resource_allocation_request",
        "communication_plan_request",
        "recovery_plan_request"
    ],
    workflow=[
        {"action": "monitor_data_feeds", "tool": "data_feed_monitor"},
        {"action": "assess_situation", "tool": "situation_assessment_request"},
        {"action": "allocate_resources", "tool": "resource_allocation_request"},
        {"action": "develop_communication_plan", "tool": "communication_plan_request"},
        {"action": "create_recovery_plan", "tool": "recovery_plan_request"}
    ]
)

# Situation Assessment Agent
situation_assessment = Agent(
    name="Situation Assessment",
    tools=["data_analysis", "impact_assessment"],
    workflow=[
        {"action": "analyze_data", "tool": "data_analysis"},
        {"action": "assess_impact", "tool": "impact_assessment"}
    ]
)

# Resource Allocation Agent
resource_allocation = Agent(
    name="Resource Allocation",
    tools=["resource_identification", "deployment_planning"],
    workflow=[
        {"action": "identify_resources", "tool": "resource_identification"},
        {"action": "plan_deployment", "tool": "deployment_planning"}
    ]
)

# Communication Agent
communication = Agent(
    name="Communication",
    tools=["stakeholder_identification", "message_crafting"],
    workflow=[
        {"action": "identify_stakeholders", "tool": "stakeholder_identification"},
        {"action": "craft_messages", "tool": "message_crafting"}
    ]
)

# Recovery Planning Agent
recovery_planning = Agent(
    name="Recovery Planning",
    tools=["short_term_planning", "long_term_planning"],
    workflow=[
        {"action": "create_short_term_plan", "tool": "short_term_planning"},
        {"action": "create_long_term_plan", "tool": "long_term_planning"}
    ]
)
