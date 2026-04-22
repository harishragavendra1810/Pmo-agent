"""Sample data for testing."""

SAMPLE_SOW = """
PROJECT: Enterprise Dashboard
VERSION: 1.0
DATE: 2024-01-15

EXECUTIVE SUMMARY
The Enterprise Dashboard project aims to create a centralized platform for real-time business analytics and monitoring.

SCOPE OF WORK
1. Frontend Development
   - React-based UI
   - Real-time data visualization
   - User authentication
   - Role-based access control

2. Backend Development
   - RESTful API
   - Database design
   - Integration with data sources
   - Performance optimization

3. Infrastructure
   - Cloud deployment (AWS)
   - CI/CD pipeline
   - Monitoring and logging

TIMELINE
- Month 1: Architecture & Design
- Month 2: Core Development
- Month 3: Testing & Deployment

BUDGET: $150,000
TEAM: 5 developers, 1 architect, 1 QA engineer

DELIVERABLES
- Working dashboard application
- API documentation
- Deployment guide
- User manual
"""

SAMPLE_MEETING_TRANSCRIPT = """
MEETING: Project Kick-off Meeting
DATE: 2024-01-20
ATTENDEES: Project Manager, Tech Lead, Client, Architect

PM: Welcome everyone. Let's discuss the Enterprise Dashboard project.

Client: Thanks for having us. Before we start, we need to add real-time notifications. Users need alerts when metrics exceed thresholds.

Tech Lead: That's a significant addition. Wasn't in the original scope.

Client: Yes, but our users have been requesting it. It's critical for our operations.

Architect: We'd need to implement a WebSocket layer and notification service. Adds complexity.

PM: Let me document this. We'll need to assess impact - timeline and cost.

Tech Lead: Also, we need to support data export to Excel and PDF. Users want to generate reports.

PM: Adding to the list. Any other changes?

Client: The dashboard needs to support multi-tenancy. Each client needs isolated data.

Architect: That requires architecture changes from the beginning.

PM: I'll create change requests for all of these. Let's reconvene in 2 days with impact analysis.

ACTION ITEMS:
- PM: Assess impact of notifications, export features, and multi-tenancy
- Tech Lead: Provide effort estimates for each change
- Client: Prioritize which features are must-have vs nice-to-have
"""

SAMPLE_KICKOFF_NOTES = """
ENTERPRISE DASHBOARD - INITIAL KICKOFF NOTES

Date: 2024-01-15
Attendees: PM, Architect, Client Lead

OBJECTIVES
- Deliver real-time business analytics platform
- Support 100+ concurrent users
- 99.9% uptime SLA
- Support 3 different data sources

ROLES & RESPONSIBILITIES
- PM: Project coordination and stakeholder management
- Architect: Technical design and infrastructure
- Tech Lead: Development team leadership
- QA Lead: Quality assurance and testing

HIGH-LEVEL PLAN
Phase 1 (Weeks 1-2): Requirements and Architecture Design
Phase 2 (Weeks 3-6): Core Development
Phase 3 (Weeks 7-8): Testing and Optimization
Phase 4 (Week 9): Deployment and Launch

KEY RISKS IDENTIFIED
1. Data integration complexity
2. Real-time performance requirements
3. Third-party API dependencies
4. Resource availability

ASSUMPTIONS
- Team members available full-time
- Client can provide product owner
- Third-party APIs remain stable
- Cloud infrastructure costs predictable
"""

SAMPLE_CR_CONTENT = SAMPLE_MEETING_TRANSCRIPT

__all__ = [
    'SAMPLE_SOW',
    'SAMPLE_MEETING_TRANSCRIPT',
    'SAMPLE_KICKOFF_NOTES',
    'SAMPLE_CR_CONTENT'
]
