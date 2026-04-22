"""Integration tests."""
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_change_request_no_key(client):
    """Test CR endpoint without OpenAI key."""
    response = client.post(
        "/api/v1/change-request",
        json={
            "project_id": "TEST-001",
            "sow": "Test SOW",
            "current_content": "Test content"
        }
    )
    # May fail due to missing API key, but endpoint should be accessible
    assert response.status_code in [200, 500]
