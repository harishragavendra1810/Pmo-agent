"""Main FastAPI application for PMO Agent."""
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from src.config import settings
from src.utils.logger import configure_logging
from src.agents.cr_agent import CRAgent
from src.agents.plan_agent import PlanAgent
from src.agents.raid_agent import RAIDAgent
from src.integrations.jira_integration import JIRAIntegration
from src.integrations.smartsheet_integration import SmartsheetIntegration
from src.integrations.excel_integration import ExcelIntegration
from src.models.pmo_models import (
    ChangeRequest, ProjectPlan, RAIDLog, PMOAgentResponse, ProcessedInput
)

# Configure logging
logger = configure_logging()

# Initialize FastAPI app
app = FastAPI(
    title="PMO Agent API",
    description="AI-powered Project Management Office Agent",
    version="1.0.0"
)

# Initialize agents and integrations
cr_agent = CRAgent()
plan_agent = PlanAgent()
raid_agent = RAIDAgent()
jira_integration = JIRAIntegration()
smartsheet_integration = SmartsheetIntegration()
excel_integration = ExcelIntegration()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/api/v1/change-request", response_model=PMOAgentResponse)
async def generate_change_request(
    project_id: str,
    sow: str,
    current_content: str
) -> PMOAgentResponse:
    """
    Generate change request from SOW and current content.
    
    Args:
        project_id: Project identifier
        sow: Scope of work document
        current_content: Current meeting/email content
        
    Returns:
        PMOAgentResponse with generated CR
    """
    try:
        logger.info(f"Generating CR for project: {project_id}")
        
        cr = await cr_agent.generate_cr(sow, current_content)
        
        if not cr:
            return PMOAgentResponse(
                status="SUCCESS",
                message="No significant changes detected",
                data={"cr": None}
            )
        
        # Validate CR
        validation = await cr_agent.validate_cr(cr)
        if not validation["valid"]:
            return PMOAgentResponse(
                status="ERROR",
                message="CR validation failed",
                errors=validation["issues"]
            )
        
        # Create JIRA ticket if enabled
        jira_ticket = await jira_integration.create_change_request(cr.model_dump())
        if jira_ticket:
            cr.jira_ticket = jira_ticket
        
        # Save to Excel
        excel_file = await excel_integration.save_change_request(cr.model_dump(), project_id)
        
        return PMOAgentResponse(
            status="SUCCESS",
            message="Change request generated successfully",
            data={
                "cr": cr.model_dump(),
                "jira_ticket": jira_ticket,
                "excel_file": excel_file
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating CR: {str(e)}")
        return PMOAgentResponse(
            status="ERROR",
            message=f"Error generating change request: {str(e)}",
            errors=[str(e)]
        )


@app.post("/api/v1/project-plan", response_model=PMOAgentResponse)
async def generate_project_plan(
    project_id: str,
    project_name: str,
    sow: str,
    meeting_notes: str
) -> PMOAgentResponse:
    """
    Generate project plan.
    
    Args:
        project_id: Project identifier
        project_name: Project name
        sow: Scope of work document
        meeting_notes: Meeting notes
        
    Returns:
        PMOAgentResponse with generated plan
    """
    try:
        logger.info(f"Generating project plan for: {project_name}")
        
        plan = await plan_agent.generate_plan(project_id, project_name, sow, meeting_notes)
        
        # Optimize plan
        optimized_plan = await plan_agent.optimize_plan(plan)
        
        # Validate plan
        validation = await plan_agent.validate_plan(optimized_plan)
        if not validation["valid"]:
            return PMOAgentResponse(
                status="ERROR",
                message="Plan validation failed",
                errors=validation["issues"]
            )
        
        # Upload to Smartsheet if enabled
        smartsheet_id = await smartsheet_integration.upload_project_plan(optimized_plan.model_dump())
        
        # Save to Excel
        excel_file = await excel_integration.save_project_plan(optimized_plan.model_dump(), project_id)
        
        return PMOAgentResponse(
            status="SUCCESS",
            message="Project plan generated successfully",
            data={
                "plan": optimized_plan.model_dump(),
                "smartsheet_id": smartsheet_id,
                "excel_file": excel_file,
                "task_count": len(optimized_plan.tasks),
                "duration_days": optimized_plan.total_duration_days
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating project plan: {str(e)}")
        return PMOAgentResponse(
            status="ERROR",
            message=f"Error generating project plan: {str(e)}",
            errors=[str(e)]
        )


@app.post("/api/v1/raid-log", response_model=PMOAgentResponse)
async def generate_raid_log(
    project_id: str,
    project_name: str,
    project_context: str,
    plan: Dict[str, Any]
) -> PMOAgentResponse:
    """
    Generate RAID log.
    
    Args:
        project_id: Project identifier
        project_name: Project name
        project_context: Overall project context
        plan: Project plan
        
    Returns:
        PMOAgentResponse with generated RAID log
    """
    try:
        logger.info(f"Generating RAID log for: {project_name}")
        
        raid_log = await raid_agent.generate_raid_log(project_id, project_name, project_context, plan)
        
        # Validate RAID log
        validation = await raid_agent.validate_raid_log(raid_log)
        if not validation["valid"]:
            return PMOAgentResponse(
                status="ERROR",
                message="RAID log validation failed",
                errors=validation["issues"]
            )
        
        # Get high priority items
        high_priority = raid_agent.get_high_priority_items(raid_log)
        
        # Upload to Smartsheet if enabled
        smartsheet_id = await smartsheet_integration.upload_raid_log(raid_log.model_dump())
        
        # Save to Excel
        excel_file = await excel_integration.save_raid_log(raid_log.model_dump(), project_id)
        
        return PMOAgentResponse(
            status="SUCCESS",
            message="RAID log generated successfully",
            data={
                "raid_log": raid_log.model_dump(),
                "smartsheet_id": smartsheet_id,
                "excel_file": excel_file,
                "item_count": len(raid_log.items),
                "high_priority_count": len(high_priority),
                "categorized": {
                    "RISK": len([i for i in raid_log.items if i.category == "RISK"]),
                    "ASSUMPTION": len([i for i in raid_log.items if i.category == "ASSUMPTION"]),
                    "ISSUE": len([i for i in raid_log.items if i.category == "ISSUE"]),
                    "DEPENDENCY": len([i for i in raid_log.items if i.category == "DEPENDENCY"])
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating RAID log: {str(e)}")
        return PMOAgentResponse(
            status="ERROR",
            message=f"Error generating RAID log: {str(e)}",
            errors=[str(e)]
        )


@app.post("/api/v1/full-analysis", response_model=PMOAgentResponse)
async def run_full_analysis(
    project_id: str,
    project_name: str,
    sow: str,
    meeting_transcript: str,
    kickoff_notes: str
) -> PMOAgentResponse:
    """
    Run full PMO analysis generating CR, Plan, and RAID log.
    
    Args:
        project_id: Project identifier
        project_name: Project name
        sow: Scope of work document
        meeting_transcript: Latest meeting transcript
        kickoff_notes: Initial kick-off meeting notes
        
    Returns:
        PMOAgentResponse with all outputs
    """
    try:
        logger.info(f"Running full analysis for: {project_name}")
        
        results = {}
        
        # Generate Change Request
        try:
            cr = await cr_agent.generate_cr(sow, meeting_transcript)
            if cr:
                jira_ticket = await jira_integration.create_change_request(cr.model_dump())
                results["change_request"] = {
                    "data": cr.model_dump(),
                    "jira_ticket": jira_ticket
                }
        except Exception as e:
            logger.warning(f"CR generation failed: {str(e)}")
            results["change_request"] = {"error": str(e)}
        
        # Generate Project Plan
        try:
            plan = await plan_agent.generate_plan(project_id, project_name, sow, kickoff_notes)
            optimized_plan = await plan_agent.optimize_plan(plan)
            smartsheet_id = await smartsheet_integration.upload_project_plan(optimized_plan.model_dump())
            results["project_plan"] = {
                "data": optimized_plan.model_dump(),
                "smartsheet_id": smartsheet_id,
                "task_count": len(optimized_plan.tasks)
            }
        except Exception as e:
            logger.warning(f"Plan generation failed: {str(e)}")
            results["project_plan"] = {"error": str(e)}
        
        # Generate RAID Log
        try:
            raid_log = await raid_agent.generate_raid_log(
                project_id, project_name, meeting_transcript, results.get("project_plan", {}).get("data")
            )
            smartsheet_id = await smartsheet_integration.upload_raid_log(raid_log.model_dump())
            results["raid_log"] = {
                "data": raid_log.model_dump(),
                "smartsheet_id": smartsheet_id,
                "item_count": len(raid_log.items)
            }
        except Exception as e:
            logger.warning(f"RAID generation failed: {str(e)}")
            results["raid_log"] = {"error": str(e)}
        
        return PMOAgentResponse(
            status="SUCCESS",
            message="Full analysis completed",
            data=results
        )
        
    except Exception as e:
        logger.error(f"Error in full analysis: {str(e)}")
        return PMOAgentResponse(
            status="ERROR",
            message=f"Error in full analysis: {str(e)}",
            errors=[str(e)]
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
