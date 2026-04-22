"""OpenAI service for PMO Agent."""
import json
import logging
from typing import Optional, List, Dict, Any
from openai import OpenAI
from src.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured. Some features will be unavailable.")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_change_request(self, sow: str, current_content: str) -> Dict[str, Any]:
        """
        Generate change request based on SOW and current content.
        
        Args:
            sow: Original scope of work document
            current_content: Current meeting/email content
            
        Returns:
            Change request object
        """
        if not self.client:
            # Mock response for testing without API key
            logger.info("Using mock CR response (no API key configured)")
            return {
                "title": "Sample Change Request",
                "description": "This is a mock change request for testing",
                "scope_impact": "Adds sample scope",
                "cost_impact": 5000,
                "timeline_impact": "Add 5 days",
                "priority": "MEDIUM"
            }
        
        prompt = f"""
        Analyze the following Scope of Work (SOW) and current project discussion content.
        Identify any changes or new requirements not in the original SOW.
        
        Original SOW:
        {sow}
        
        Current Content (Meeting/Email):
        {current_content}
        
        Please generate a Change Request with the following fields in JSON format:
        - title: Brief title of the change
        - description: Detailed description of the change
        - scope_impact: How this affects project scope
        - cost_impact: Estimated cost impact (if quantifiable)
        - timeline_impact: How this affects timeline
        - priority: HIGH, MEDIUM, or LOW
        
        If no significant changes are found, indicate that in the response.
        Return only valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content
            # Extract JSON from response
            cr_data = json.loads(response_text)
            logger.info(f"Generated CR: {cr_data['title']}")
            return cr_data
            
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from OpenAI")
            raise
        except Exception as e:
            logger.error(f"Error generating change request: {str(e)}")
            raise
    
    async def generate_project_plan(self, sow: str, meeting_notes: str) -> Dict[str, Any]:
        """
        Generate project plan from SOW and meeting notes.
        
        Args:
            sow: Scope of work document
            meeting_notes: Kick-off meeting notes
            
        Returns:
            Project plan object
        """
        if not self.client:
            # Mock response for testing
            logger.info("Using mock project plan response (no API key configured)")
            return {
                "total_duration_days": 20,
                "total_effort_hours": 160,
                "tasks": [
                    {
                        "name": "Design Phase",
                        "description": "System design and architecture",
                        "duration_days": 5,
                        "estimated_effort_hours": 40,
                        "dependencies": []
                    },
                    {
                        "name": "Development",
                        "description": "Core development work",
                        "duration_days": 10,
                        "estimated_effort_hours": 80,
                        "dependencies": [0]
                    },
                    {
                        "name": "Testing",
                        "description": "QA and testing",
                        "duration_days": 5,
                        "estimated_effort_hours": 40,
                        "dependencies": [1]
                    }
                ],
                "risks": ["Resource availability", "Integration complexity"]
            }
        
        prompt = f"""
        Create a detailed project plan based on the SOW and meeting notes.
        
        Scope of Work:
        {sow}
        
        Meeting Notes:
        {meeting_notes}
        
        Generate a project plan in JSON format with:
        - total_duration_days: Total project duration
        - tasks: Array of tasks with:
          - name: Task name
          - description: Task description
          - duration_days: Duration for this task
          - estimated_effort_hours: Effort estimate
          - dependencies: Array of dependent task IDs
          - assigned_to: Empty (to be assigned)
        
        Include realistic timelines and effort estimates.
        Return only valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            plan_data = json.loads(response_text)
            logger.info(f"Generated project plan with {len(plan_data.get('tasks', []))} tasks")
            return plan_data
            
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from OpenAI")
            raise
        except Exception as e:
            logger.error(f"Error generating project plan: {str(e)}")
            raise
    
    async def generate_raid_log(self, project_context: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate RAID log based on project context and plan.
        
        Args:
            project_context: Overall project context
            plan: Project plan object
            
        Returns:
            RAID log object
        """
        if not self.client:
            # Mock response for testing
            logger.info("Using mock RAID log response (no API key configured)")
            return {
                "items": [
                    {
                        "title": "Resource Availability",
                        "category": "RISK",
                        "description": "Key team members may not be available",
                        "severity": "HIGH",
                        "mitigation_plan": "Cross-train backup resources"
                    },
                    {
                        "title": "API Integration",
                        "category": "DEPENDENCY",
                        "description": "Depends on third-party API availability",
                        "severity": "MEDIUM",
                        "mitigation_plan": "Implement fallback mechanism"
                    },
                    {
                        "title": "Fixed Budget",
                        "category": "ASSUMPTION",
                        "description": "Assuming budget will remain constant",
                        "severity": "MEDIUM",
                        "mitigation_plan": "Build buffer into estimates"
                    }
                ]
            }
        
        prompt = f"""
        Identify Risks, Assumptions, Issues, and Dependencies for this project.
        
        Project Context:
        {project_context}
        
        Project Plan Summary:
        {json.dumps(plan, indent=2)}
        
        Generate a RAID log in JSON format with:
        - items: Array of RAID items with:
          - title: Brief title
          - category: RISK, ASSUMPTION, ISSUE, or DEPENDENCY
          - description: Detailed description
          - severity: HIGH, MEDIUM, or LOW
          - mitigation_plan: How to mitigate (for risks)
          - owner: Empty (to be assigned)
        
        Focus on realistic project risks and dependencies.
        Return only valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            raid_data = json.loads(response_text)
            logger.info(f"Generated RAID log with {len(raid_data.get('items', []))} items")
            return raid_data
            
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from OpenAI")
            raise
        except Exception as e:
            logger.error(f"Error generating RAID log: {str(e)}")
            raise
