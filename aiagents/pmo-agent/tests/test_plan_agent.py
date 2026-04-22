"""Tests for Plan Agent."""
import pytest
from src.agents.plan_agent import PlanAgent
from src.models.pmo_models import ProjectPlan, PlannedTask


@pytest.mark.asyncio
async def test_plan_agent_initialization():
    """Test Plan Agent initializes correctly."""
    agent = PlanAgent()
    assert agent is not None
    assert agent.openai_service is not None


@pytest.mark.asyncio
async def test_plan_agent_validation():
    """Test project plan validation."""
    agent = PlanAgent()
    
    tasks = [
        PlannedTask(
            name="Design",
            description="Design phase",
            duration_days=5,
            estimated_effort_hours=40
        ),
        PlannedTask(
            name="Development",
            description="Development phase",
            duration_days=10,
            estimated_effort_hours=80
        )
    ]
    
    plan = ProjectPlan(
        project_id="PROJ-001",
        project_name="Test Project",
        scope_document="Test scope",
        total_duration_days=15,
        total_effort_hours=120,
        tasks=tasks
    )
    
    result = await agent.validate_plan(plan)
    assert result["valid"] is True
    assert result["task_count"] == 2
    assert result["duration_days"] == 15
