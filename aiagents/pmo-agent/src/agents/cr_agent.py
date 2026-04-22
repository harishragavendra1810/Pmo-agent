"""Change Request Agent."""
import logging
from typing import Dict, Any, Optional
from src.models.pmo_models import ChangeRequest
from src.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class CRAgent:
    """Change Request Agent - generates CRs based on scope changes."""
    
    def __init__(self):
        """Initialize CR Agent."""
        self.openai_service = OpenAIService()
        self.cr_template = {
            "title": "",
            "description": "",
            "scope_impact": "",
            "cost_impact": None,
            "timeline_impact": "",
            "priority": "MEDIUM"
        }
    
    async def generate_cr(self, sow: str, new_content: str) -> Optional[ChangeRequest]:
        """
        Generate change request from SOW and new content.
        
        Args:
            sow: Original scope of work
            new_content: New meeting/email content
            
        Returns:
            ChangeRequest object or None if no changes detected
        """
        try:
            cr_data = await self.openai_service.generate_change_request(sow, new_content)
            
            # Check if changes were found
            if 'no_changes' in str(cr_data).lower():
                logger.info("No significant changes detected")
                return None
            
            # Create ChangeRequest object
            cr = ChangeRequest(
                title=cr_data.get('title'),
                description=cr_data.get('description'),
                scope_impact=cr_data.get('scope_impact'),
                cost_impact=cr_data.get('cost_impact'),
                timeline_impact=cr_data.get('timeline_impact'),
                priority=cr_data.get('priority', 'MEDIUM')
            )
            
            logger.info(f"CR generated: {cr.title}")
            return cr
            
        except Exception as e:
            logger.error(f"Error in CR generation: {str(e)}")
            raise
    
    async def validate_cr(self, cr: ChangeRequest) -> Dict[str, Any]:
        """
        Validate change request.
        
        Args:
            cr: Change request to validate
            
        Returns:
            Validation result
        """
        issues = []
        
        if not cr.title:
            issues.append("CR title is required")
        if not cr.description:
            issues.append("CR description is required")
        if cr.priority not in ['HIGH', 'MEDIUM', 'LOW']:
            issues.append(f"Invalid priority: {cr.priority}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    async def estimate_cr_impact(self, cr: ChangeRequest) -> Dict[str, Any]:
        """
        Estimate impact of change request.
        
        Args:
            cr: Change request
            
        Returns:
            Impact estimation
        """
        # This would be enhanced with more sophisticated estimation
        return {
            "scope_complexity": "HIGH" if "complex" in cr.scope_impact.lower() else "MEDIUM",
            "timeline_risk": "HIGH" if "delay" in cr.timeline_impact.lower() else "MEDIUM",
            "cost_risk": "HIGH" if cr.cost_impact and cr.cost_impact > 10000 else "MEDIUM",
            "recommendation": "Block" if cr.priority == "HIGH" else "Review"
        }
