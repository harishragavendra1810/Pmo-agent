"""Plan Agent - generates project plans."""
import logging
from typing import Dict, Any, List, Optional
from src.models.pmo_models import ProjectPlan, PlannedTask
from src.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class PlanAgent:
    """Plan Agent - creates detailed project plans."""
    
    def __init__(self):
        """Initialize Plan Agent."""
        self.openai_service = OpenAIService()
    
    async def generate_plan(self, project_id: str, project_name: str, sow: str, meeting_notes: str) -> ProjectPlan:
        """
        Generate project plan.
        
        Args:
            project_id: Project identifier
            project_name: Project name
            sow: Scope of work document
            meeting_notes: Meeting notes
            
        Returns:
            ProjectPlan object
        """
        try:
            plan_data = await self.openai_service.generate_project_plan(sow, meeting_notes)
            
            # Convert tasks to PlannedTask objects
            tasks = []
            for task_data in plan_data.get('tasks', []):
                task = PlannedTask(
                    name=task_data.get('name'),
                    description=task_data.get('description'),
                    duration_days=task_data.get('duration_days', 1),
                    estimated_effort_hours=task_data.get('estimated_effort_hours', 8),
                    dependencies=task_data.get('dependencies', []),
                    assigned_to=task_data.get('assigned_to')
                )
                tasks.append(task)
            
            # Create ProjectPlan object
            project_plan = ProjectPlan(
                project_id=project_id,
                project_name=project_name,
                scope_document=sow,
                total_duration_days=plan_data.get('total_duration_days', sum(t.duration_days for t in tasks)),
                total_effort_hours=plan_data.get('total_effort_hours', sum(t.estimated_effort_hours for t in tasks)),
                tasks=tasks,
                risks=plan_data.get('risks', []),
                resources=plan_data.get('resources')
            )
            
            logger.info(f"Project plan generated with {len(tasks)} tasks")
            return project_plan
            
        except Exception as e:
            logger.error(f"Error generating project plan: {str(e)}")
            raise
    
    async def optimize_plan(self, plan: ProjectPlan) -> ProjectPlan:
        """
        Optimize project plan by scheduling tasks with dependencies.
        
        Args:
            plan: Project plan to optimize
            
        Returns:
            Optimized project plan
        """
        # Create task map for dependency tracking
        task_map = {i: task for i, task in enumerate(plan.tasks)}
        start_day = 1
        
        # Simple critical path scheduling
        for i, task in enumerate(plan.tasks):
            if not task.dependencies:
                task.start_date = f"Day {start_day}"
                task.end_date = f"Day {start_day + task.duration_days - 1}"
                start_day += task.duration_days
            else:
                # Find when dependencies end
                max_end_day = start_day
                for dep_id in task.dependencies:
                    if dep_id < len(plan.tasks):
                        dep_task = plan.tasks[dep_id]
                        if dep_task.end_date:
                            day_num = int(dep_task.end_date.split()[-1])
                            max_end_day = max(max_end_day, day_num + 1)
                
                task.start_date = f"Day {max_end_day}"
                task.end_date = f"Day {max_end_day + task.duration_days - 1}"
        
        logger.info("Project plan optimized")
        return plan
    
    async def validate_plan(self, plan: ProjectPlan) -> Dict[str, Any]:
        """
        Validate project plan.
        
        Args:
            plan: Plan to validate
            
        Returns:
            Validation result
        """
        issues = []
        
        if not plan.project_name:
            issues.append("Project name is required")
        if not plan.tasks:
            issues.append("Plan must contain at least one task")
        if plan.total_duration_days <= 0:
            issues.append("Project duration must be positive")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "task_count": len(plan.tasks),
            "duration_days": plan.total_duration_days
        }
