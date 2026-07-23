"""
Workflow Executor — Execution Lifecycle Management
"""

import uuid
import time
from typing import Dict, Any, Optional
from app.workflows.workflow_engine import execute_workflow_pipeline
from app.workflows.workflow_history import save_workflow_run
from app.core.logger import logger


def run_workflow(
    workflow_id: str,
    inputs: Dict[str, Any],
    user_id: Optional[int] = None,
    custom_template: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes a workflow pipeline end-to-end, logs history, and returns execution result.
    """
    run_id = f"run-{uuid.uuid4().hex[:10]}"
    logger.info(f"Starting execution of workflow '{workflow_id}' (run_id: {run_id})...")

    try:
        execution_payload = execute_workflow_pipeline(
            workflow_id=workflow_id,
            inputs=inputs,
            custom_template=custom_template
        )

        title = execution_payload.get("title", f"Workflow {workflow_id}")
        category = execution_payload.get("category", "General")
        steps = execution_payload.get("steps", [])
        result = execution_payload.get("result", {})
        exec_ms = execution_payload.get("execution_time_ms", 0.0)

        # Save run record to SQLite database
        save_workflow_run(
            run_id=run_id,
            workflow_id=workflow_id,
            title=title,
            category=category,
            status="completed",
            inputs=inputs,
            steps=steps,
            result=result,
            execution_time_ms=exec_ms,
            user_id=user_id
        )

        return {
            "run_id": run_id,
            "workflow_id": workflow_id,
            "title": title,
            "category": category,
            "status": "completed",
            "execution_time_ms": exec_ms,
            "inputs": inputs,
            "steps": steps,
            "result": result
        }

    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {e}", exc_info=True)

        failed_result = {
            "error": str(e),
            "report_markdown": f"# Workflow Execution Failed\n\nAn error occurred while processing workflow `{workflow_id}`: {str(e)}",
            "key_takeaways": [],
            "next_actions": ["Check system logs", "Verify input parameters"]
        }

        save_workflow_run(
            run_id=run_id,
            workflow_id=workflow_id,
            title=f"Workflow {workflow_id}",
            category="General",
            status="failed",
            inputs=inputs,
            steps=[{"step": 1, "name": "Execution Failed", "status": "failed", "detail": str(e)}],
            result=failed_result,
            execution_time_ms=0.0,
            user_id=user_id
        )

        return {
            "run_id": run_id,
            "workflow_id": workflow_id,
            "title": f"Workflow {workflow_id}",
            "category": "General",
            "status": "failed",
            "execution_time_ms": 0.0,
            "inputs": inputs,
            "steps": [{"step": 1, "name": "Execution Failed", "status": "failed", "detail": str(e)}],
            "result": failed_result
        }
