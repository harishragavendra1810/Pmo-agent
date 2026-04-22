"""Excel integration for PMO Agent."""
import logging
import json
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from src.config import settings

logger = logging.getLogger(__name__)


class ExcelIntegration:
    """Integration for saving outputs to Excel."""
    
    def __init__(self):
        """Initialize Excel integration."""
        self.output_path = Path(settings.excel_output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    async def save_change_request(self, cr_data: Dict[str, Any], project_id: str) -> str:
        """
        Save change request to Excel.
        
        Args:
            cr_data: Change request data
            project_id: Project identifier
            
        Returns:
            File path
        """
        try:
            filename = self.output_path / f"CR_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(cr_data, f, indent=2, default=str)
            
            logger.info(f"Saved CR to: {filename}")
            return str(filename)
            
        except Exception as e:
            logger.error(f"Error saving CR to Excel: {str(e)}")
            raise
    
    async def save_project_plan(self, plan_data: Dict[str, Any], project_id: str) -> str:
        """
        Save project plan to Excel.
        
        Args:
            plan_data: Project plan data
            project_id: Project identifier
            
        Returns:
            File path
        """
        try:
            filename = self.output_path / f"ProjectPlan_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(plan_data, f, indent=2, default=str)
            
            logger.info(f"Saved project plan to: {filename}")
            return str(filename)
            
        except Exception as e:
            logger.error(f"Error saving project plan: {str(e)}")
            raise
    
    async def save_raid_log(self, raid_data: Dict[str, Any], project_id: str) -> str:
        """
        Save RAID log to Excel.
        
        Args:
            raid_data: RAID log data
            project_id: Project identifier
            
        Returns:
            File path
        """
        try:
            filename = self.output_path / f"RAIDLog_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(raid_data, f, indent=2, default=str)
            
            logger.info(f"Saved RAID log to: {filename}")
            return str(filename)
            
        except Exception as e:
            logger.error(f"Error saving RAID log: {str(e)}")
            raise
