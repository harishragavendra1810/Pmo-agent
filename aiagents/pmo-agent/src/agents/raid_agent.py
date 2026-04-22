"""RAID Agent - generates RAID logs."""
import logging
from typing import Dict, Any
from src.models.pmo_models import RAIDLog, RAIDItem
from src.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class RAIDAgent:
    """RAID Agent - identifies Risks, Assumptions, Issues, Dependencies."""
    
    def __init__(self):
        """Initialize RAID Agent."""
        self.openai_service = OpenAIService()
    
    async def generate_raid_log(self, project_id: str, project_name: str, project_context: str, plan: Dict[str, Any]) -> RAIDLog:
        """
        Generate RAID log.
        
        Args:
            project_id: Project identifier
            project_name: Project name
            project_context: Overall project context
            plan: Project plan
            
        Returns:
            RAIDLog object
        """
        try:
            raid_data = await self.openai_service.generate_raid_log(project_context, plan)
            
            # Convert items to RAIDItem objects
            items = []
            for item_data in raid_data.get('items', []):
                item = RAIDItem(
                    title=item_data.get('title'),
                    category=item_data.get('category'),
                    description=item_data.get('description'),
                    severity=item_data.get('severity', 'MEDIUM'),
                    mitigation_plan=item_data.get('mitigation_plan'),
                    owner=item_data.get('owner')
                )
                items.append(item)
            
            # Create RAIDLog object
            raid_log = RAIDLog(
                project_id=project_id,
                project_name=project_name,
                items=items
            )
            
            logger.info(f"RAID log generated with {len(items)} items")
            return raid_log
            
        except Exception as e:
            logger.error(f"Error generating RAID log: {str(e)}")
            raise
    
    def categorize_items(self, raid_log: RAIDLog) -> Dict[str, list]:
        """
        Categorize RAID items.
        
        Args:
            raid_log: RAID log
            
        Returns:
            Items organized by category
        """
        categorized = {
            "RISK": [],
            "ASSUMPTION": [],
            "ISSUE": [],
            "DEPENDENCY": []
        }
        
        for item in raid_log.items:
            if item.category in categorized:
                categorized[item.category].append(item)
        
        return categorized
    
    async def validate_raid_log(self, raid_log: RAIDLog) -> Dict[str, Any]:
        """
        Validate RAID log.
        
        Args:
            raid_log: RAID log to validate
            
        Returns:
            Validation result
        """
        issues = []
        
        if not raid_log.project_name:
            issues.append("Project name is required")
        if not raid_log.items:
            issues.append("RAID log should contain at least one item")
        
        # Validate individual items
        for item in raid_log.items:
            if not item.title:
                issues.append(f"RAID item missing title")
            if item.category not in ['RISK', 'ASSUMPTION', 'ISSUE', 'DEPENDENCY']:
                issues.append(f"Invalid RAID category: {item.category}")
            if item.severity not in ['HIGH', 'MEDIUM', 'LOW']:
                issues.append(f"Invalid severity level: {item.severity}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "item_count": len(raid_log.items)
        }
    
    def get_high_priority_items(self, raid_log: RAIDLog) -> list:
        """
        Get high priority RAID items.
        
        Args:
            raid_log: RAID log
            
        Returns:
            List of high priority items
        """
        return [item for item in raid_log.items if item.severity == "HIGH"]
