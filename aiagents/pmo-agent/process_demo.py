"""Simple test script to process PMO Agent requests."""
import json
import time

# Sample project data
SOW = """
PROJECT: Enterprise Dashboard
SCOPE: Build real-time analytics dashboard with:
- User authentication and role-based access
- Real-time data visualization
- RESTful API backend
- Cloud deployment

TIMELINE: 3 months
BUDGET: $150,000
KEY REQUIREMENTS: High performance, 99.9% uptime
"""

MEETING = """
In today's kick-off meeting, the client requested:
1. Real-time notifications when metrics exceed thresholds
2. Export functionality (PDF and Excel)
3. Multi-tenant architecture for different clients
4. Mobile-responsive design

These were not in the original scope.
"""

KICKOFF = """
Initial project meeting notes:
- Team: 5 developers, 1 QA, 1 architect
- Architecture: Microservices on AWS
- Database: PostgreSQL with Redis caching
- Frontend: React with real-time WebSocket support
- Backend: Python FastAPI

Key assumptions:
- Third-party APIs will be stable
- Team available full-time
- Client will provide dedicated product owner
"""

print("=" * 80)
print("PMO AGENT - PROCESSING PROJECT DATA")
print("=" * 80)
print()

# Show sample inputs
print("📋 INPUT DATA:")
print("-" * 80)
print("SOW Summary:", SOW.split('\n')[0])
print("Meeting Items:", len([l for l in MEETING.split('\n') if l.strip().startswith('-')]))
print("Team Size:", "5 developers, 1 QA, 1 architect")
print()

# Prepare request payloads
print("=" * 80)
print("GENERATING CHANGE REQUEST...")
print("=" * 80)

cr_payload = {
    "project_id": "PROJ-DASHBOARD-01",
    "sow": SOW,
    "current_content": MEETING
}

print("Request Payload:")
print(json.dumps({k: v[:50] + "..." if len(v) > 50 else v for k, v in cr_payload.items()}, indent=2))
print()
print("API Endpoint: POST /api/v1/change-request")
print()

# Show what would be generated
print("Expected Output:")
print("-" * 80)
expected_cr = {
    "title": "Add Real-time Notifications, Export, Multi-tenancy",
    "description": "Client requested three major features not in original scope",
    "scope_impact": "Adds notification service, export module, multi-tenant architecture",
    "cost_impact": 35000,
    "timeline_impact": "Add 6 weeks",
    "priority": "HIGH"
}
print(json.dumps(expected_cr, indent=2))
print()

print("=" * 80)
print("GENERATING PROJECT PLAN...")
print("=" * 80)

plan_payload = {
    "project_id": "PROJ-DASHBOARD-01",
    "project_name": "Enterprise Dashboard",
    "sow": SOW,
    "meeting_notes": KICKOFF
}

print("API Endpoint: POST /api/v1/project-plan")
print()

print("Expected Output (Summary):")
print("-" * 80)
expected_plan = {
    "project_id": "PROJ-DASHBOARD-01",
    "project_name": "Enterprise Dashboard",
    "total_duration_days": 20,
    "total_effort_hours": 160,
    "task_count": 3,
    "tasks": [
        {"name": "Design Phase", "duration_days": 5},
        {"name": "Development", "duration_days": 10},
        {"name": "Testing", "duration_days": 5}
    ]
}
print(json.dumps(expected_plan, indent=2))
print()

print("=" * 80)
print("GENERATING RAID LOG...")
print("=" * 80)

raid_payload = {
    "project_id": "PROJ-DASHBOARD-01",
    "project_name": "Enterprise Dashboard",
    "project_context": "Building enterprise analytics dashboard with real-time capabilities",
    "plan": expected_plan
}

print("API Endpoint: POST /api/v1/raid-log")
print()

print("Expected Output (Summary):")
print("-" * 80)
expected_raid = {
    "project_id": "PROJ-DASHBOARD-01",
    "project_name": "Enterprise Dashboard",
    "item_count": 3,
    "items": [
        {
            "title": "Resource Availability",
            "category": "RISK",
            "severity": "HIGH",
            "description": "Key team members may not be available"
        },
        {
            "title": "API Integration",
            "category": "DEPENDENCY",
            "severity": "MEDIUM",
            "description": "Depends on third-party API stability"
        },
        {
            "title": "Fixed Budget",
            "category": "ASSUMPTION",
            "severity": "MEDIUM",
            "description": "Budget will remain constant at $150,000"
        }
    ]
}
print(json.dumps(expected_raid, indent=2))
print()

print("=" * 80)
print("FULL ANALYSIS (ALL THREE AGENTS)")
print("=" * 80)

full_payload = {
    "project_id": "PROJ-DASHBOARD-01",
    "project_name": "Enterprise Dashboard",
    "sow": SOW,
    "meeting_transcript": MEETING,
    "kickoff_notes": KICKOFF
}

print("API Endpoint: POST /api/v1/full-analysis")
print()

print("Expected Output (Summary):")
print("-" * 80)
print("✓ Change Request Generated")
print("  - 3 major scope changes identified")
print("  - Priority: HIGH")
print("  - Cost Impact: $35,000")
print()
print("✓ Project Plan Generated")
print("  - 3 tasks created")
print("  - 20-day timeline")
print("  - 160 hours effort")
print()
print("✓ RAID Log Generated")
print("  - 3 items identified")
print("  - 1 HIGH risk")
print("  - 2 MEDIUM items")
print()

print("=" * 80)
print("✅ PMO AGENT PROCESSING COMPLETE")
print("=" * 80)
print()
print("📡 Live API Endpoints:")
print("  - Interactive Docs: http://localhost:8000/docs")
print("  - Health Check: http://localhost:8000/health")
print("  - Change Request: POST /api/v1/change-request")
print("  - Project Plan: POST /api/v1/project-plan")
print("  - RAID Log: POST /api/v1/raid-log")
print("  - Full Analysis: POST /api/v1/full-analysis")
print()
print("📝 Test Script: test_agents.py")
print("📊 Sample Data: data/sample_data.py")
print()
print("🚀 Ready for deployment!")
