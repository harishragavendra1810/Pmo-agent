"""Tests for RAID Agent."""
import pytest
from src.agents.raid_agent import RAIDAgent
from src.models.pmo_models import RAIDLog, RAIDItem


@pytest.mark.asyncio
async def test_raid_agent_initialization():
    """Test RAID Agent initializes correctly."""
    agent = RAIDAgent()
    assert agent is not None
    assert agent.openai_service is not None


@pytest.mark.asyncio
async def test_raid_agent_categorization():
    """Test RAID item categorization."""
    agent = RAIDAgent()
    
    items = [
        RAIDItem(
            title="API Delivery Delay",
            category="RISK",
            description="API may be delayed",
            severity="HIGH"
        ),
        RAIDItem(
            title="Budget Constraint",
            category="ASSUMPTION",
            description="Assume budget is fixed",
            severity="MEDIUM"
        ),
        RAIDItem(
            title="Database Dependency",
            category="DEPENDENCY",
            description="Depends on DB team",
            severity="MEDIUM"
        )
    ]
    
    raid_log = RAIDLog(
        project_id="PROJ-001",
        project_name="Test Project",
        items=items
    )
    
    categorized = agent.categorize_items(raid_log)
    assert len(categorized["RISK"]) == 1
    assert len(categorized["ASSUMPTION"]) == 1
    assert len(categorized["DEPENDENCY"]) == 1


@pytest.mark.asyncio
async def test_raid_high_priority_items():
    """Test filtering high priority items."""
    agent = RAIDAgent()
    
    items = [
        RAIDItem(
            title="Critical Risk",
            category="RISK",
            description="Critical issue",
            severity="HIGH"
        ),
        RAIDItem(
            title="Minor Risk",
            category="RISK",
            description="Minor issue",
            severity="LOW"
        )
    ]
    
    raid_log = RAIDLog(
        project_id="PROJ-001",
        project_name="Test Project",
        items=items
    )
    
    high_priority = agent.get_high_priority_items(raid_log)
    assert len(high_priority) == 1
    assert high_priority[0].severity == "HIGH"
