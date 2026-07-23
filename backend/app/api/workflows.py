"""
API Router for AI Workflows & AI Copilot Platform Capabilities
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Response, Depends
from pydantic import BaseModel

from app.workflows.workflow_templates import get_all_templates, get_template_by_id, save_custom_template
from app.workflows.workflow_executor import run_workflow
from app.workflows.workflow_history import get_workflow_history, get_workflow_run_by_id
from app.workflows.report_generator import generate_pdf_report, generate_docx_report
from app.services.copilot_service import generate_copilot_suggestions
from app.core.logger import logger

router = APIRouter(prefix="/api/workflows", tags=["workflows"])
copilot_router = APIRouter(prefix="/api/copilot", tags=["copilot"])


class WorkflowExecutionRequest(BaseModel):
    workflow_id: str
    inputs: Dict[str, Any] = {}
    custom_template: Optional[Dict[str, Any]] = None


class CustomTemplateRequest(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    category: str
    icon: Optional[str] = "Zap"
    steps: list[str] = []
    inputs_schema: list[dict] = []


class ExportRequest(BaseModel):
    title: str
    category: str
    markdown_content: str


@router.get("/templates")
def list_templates():
    """
    Get all workflow templates (built-in + user created).
    """
    return {"templates": get_all_templates()}


@router.post("/templates")
def create_template(req: CustomTemplateRequest):
    """
    Create and save a custom user workflow template.
    """
    created = save_custom_template(req.model_dump())
    return {"status": "success", "template": created}


@router.post("/execute")
def execute_workflow(req: WorkflowExecutionRequest):
    """
    Executes an enterprise workflow pipeline and returns execution details and report.
    """
    try:
        run_result = run_workflow(
            workflow_id=req.workflow_id,
            inputs=req.inputs,
            custom_template=req.custom_template
        )
        return run_result
    except Exception as e:
        logger.error(f"Error executing workflow endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
def list_history(limit: int = 50, category: Optional[str] = None):
    """
    Get list of recently executed workflows.
    """
    history = get_workflow_history(limit=limit, category=category)
    return {"history": history}


@router.get("/history/{run_id}")
def get_history_detail(run_id: str):
    """
    Get full details for a specific workflow execution run.
    """
    run_detail = get_workflow_run_by_id(run_id)
    if not run_detail:
        raise HTTPException(status_code=404, detail="Workflow execution run not found")
    return run_detail


@router.post("/export/pdf")
def export_pdf(req: ExportRequest):
    """
    Exports a workflow report as a styled PDF document download.
    """
    try:
        pdf_bytes = generate_pdf_report(
            title=req.title,
            category=req.category,
            markdown_content=req.markdown_content
        )
        safe_filename = req.title.lower().replace(" ", "_").replace("/", "-")
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}_report.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.post("/export/docx")
def export_docx(req: ExportRequest):
    """
    Exports a workflow report as a Word DOCX document download.
    """
    try:
        docx_bytes = generate_docx_report(
            title=req.title,
            category=req.category,
            markdown_content=req.markdown_content
        )
        safe_filename = req.title.lower().replace(" ", "_").replace("/", "-")
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}_report.docx"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate DOCX: {e}")
        raise HTTPException(status_code=500, detail=f"DOCX generation failed: {str(e)}")


@copilot_router.get("/suggestions")
def get_copilot_suggestions():
    """
    Returns proactive AI Copilot action suggestions based on workspace state.
    """
    return generate_copilot_suggestions()
