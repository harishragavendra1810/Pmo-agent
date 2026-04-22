"""Test configuration."""
import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Get test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_sow():
    """Sample scope of work."""
    return """
    PROJECT: Website Redesign
    SCOPE:
    - Redesign homepage
    - Implement responsive design
    - Migrate to new CMS
    - Performance optimization
    
    TIMELINE: 8 weeks
    BUDGET: $50,000
    TEAM: 3 developers, 1 designer
    """


@pytest.fixture
def sample_meeting_transcript():
    """Sample meeting transcript."""
    return """
    Meeting: Project Kick-off
    Attendees: Client, PM, Tech Lead
    
    Client: We want to add real-time notifications
    Tech Lead: That wasn't in scope originally
    Client: Yes, but it's critical for user engagement
    PM: We'll need to assess impact
    
    Action items:
    - Assess notification feature impact
    - Update timeline accordingly
    """
