"""Tests for CR Agent."""
import pytest
from src.agents.cr_agent import CRAgent
from src.models.pmo_models import ChangeRequest


@pytest.mark.asyncio
async def test_cr_agent_initialization():
    """Test CR Agent initializes correctly."""
    agent = CRAgent()
    assert agent is not None
    assert agent.openai_service is not None


@pytest.mark.asyncio
async def test_cr_agent_validate():
    """Test CR validation."""
    agent = CRAgent()
    
    valid_cr = ChangeRequest(
        title="Add Feature X",
        description="Client requested feature X",
        scope_impact="Adds 2 modules",
        timeline_impact="5 days delay",
        priority="HIGH"
    )
    
    result = await agent.validate_cr(valid_cr)
    assert result["valid"] is True
    assert len(result["issues"]) == 0


@pytest.mark.asyncio
async def test_cr_agent_validation_failure():
    """Test CR validation with missing fields."""
    agent = CRAgent()
    
    invalid_cr = ChangeRequest(
        title="",
        description="",
        scope_impact="",
        timeline_impact="",
        priority="INVALID"
    )
    
    result = await agent.validate_cr(invalid_cr)
    assert result["valid"] is False
    assert len(result["issues"]) > 0
