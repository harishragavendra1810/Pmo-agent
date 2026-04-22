"""Pydantic models for PMO Agent."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChangeRequest(BaseModel):
    """Change Request model."""
    id: Optional[str] = None
    title: str
    description: str
    scope_impact: str
    cost_impact: Optional[float] = None
    timeline_impact: str
    priority: str  # HIGH, MEDIUM, LOW
    requested_by: Optional[str] = None
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.now)
    jira_ticket: Optional[str] = None


class PlannedTask(BaseModel):
    """Task in project plan."""
    id: Optional[str] = None
    name: str
    description: str
    duration_days: int
    estimated_effort_hours: float
    dependencies: List[str] = []
    assigned_to: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "NOT_STARTED"


class ProjectPlan(BaseModel):
    """Project Plan model."""
    project_id: str
    project_name: str
    scope_document: str
    total_duration_days: int
    total_effort_hours: float
    tasks: List[PlannedTask]
    risks: List[str] = []
    resources: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)


class RAIDItem(BaseModel):
    """RAID (Risks, Assumptions, Issues, Dependencies) item."""
    id: Optional[str] = None
    title: str
    category: str  # RISK, ASSUMPTION, ISSUE, DEPENDENCY
    description: str
    severity: str  # HIGH, MEDIUM, LOW
    owner: Optional[str] = None
    mitigation_plan: Optional[str] = None
    status: str = "OPEN"
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[str] = None


class RAIDLog(BaseModel):
    """RAID Log model."""
    project_id: str
    project_name: str
    items: List[RAIDItem]
    created_at: datetime = Field(default_factory=datetime.now)


class ProcessedInput(BaseModel):
    """Processed input from various sources."""
    source_type: str  # MEETING, SOW, EMAIL, KICKOFF, REPOSITORY
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class PMOAgentResponse(BaseModel):
    """Response from PMO Agent."""
    status: str  # SUCCESS, ERROR
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
