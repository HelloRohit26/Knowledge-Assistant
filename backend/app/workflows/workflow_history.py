"""
Workflow History Service — Persistence and Querying for Executed Workflows
"""

import json
from typing import List, Dict, Any, Optional
from app.database.db import get_connection
from app.core.logger import logger


def save_workflow_run(
    run_id: str,
    workflow_id: str,
    title: str,
    category: str,
    status: str,
    inputs: Dict[str, Any],
    steps: List[Dict[str, Any]],
    result: Dict[str, Any],
    execution_time_ms: float,
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Saves a completed or failed workflow run record.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO workflow_history
        (run_id, workflow_id, title, category, status, inputs_json, steps_json, result_json, execution_time_ms, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            workflow_id,
            title,
            category,
            status,
            json.dumps(inputs),
            json.dumps(steps),
            json.dumps(result),
            execution_time_ms,
            user_id
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to save workflow run history {run_id}: {e}")

    return {
        "run_id": run_id,
        "workflow_id": workflow_id,
        "title": title,
        "category": category,
        "status": status,
        "execution_time_ms": execution_time_ms
    }


def get_workflow_history(limit: int = 50, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves past executed workflows sorted by creation timestamp.
    """
    runs = []
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if category and category != "All":
            cursor.execute("""
            SELECT run_id, workflow_id, title, category, status, inputs_json, steps_json, result_json, execution_time_ms, created_at
            FROM workflow_history
            WHERE category = ?
            ORDER BY created_at DESC LIMIT ?
            """, (category, limit))
        else:
            cursor.execute("""
            SELECT run_id, workflow_id, title, category, status, inputs_json, steps_json, result_json, execution_time_ms, created_at
            FROM workflow_history
            ORDER BY created_at DESC LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            run_id, w_id, title, cat, status, in_json, st_json, res_json, exec_ms, created_at = row
            try:
                inputs = json.loads(in_json) if in_json else {}
            except Exception:
                inputs = {}
            try:
                steps = json.loads(st_json) if st_json else []
            except Exception:
                steps = []
            try:
                result = json.loads(res_json) if res_json else {}
            except Exception:
                result = {}

            runs.append({
                "run_id": run_id,
                "workflow_id": w_id,
                "title": title,
                "category": cat,
                "status": status,
                "inputs": inputs,
                "steps": steps,
                "result": result,
                "execution_time_ms": exec_ms,
                "created_at": str(created_at)
            })
    except Exception as e:
        logger.error(f"Error fetching workflow history: {e}")

    return runs


def get_workflow_run_by_id(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Lookup a specific workflow run record.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT run_id, workflow_id, title, category, status, inputs_json, steps_json, result_json, execution_time_ms, created_at
        FROM workflow_history
        WHERE run_id = ?
        """, (run_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        run_id, w_id, title, cat, status, in_json, st_json, res_json, exec_ms, created_at = row
        return {
            "run_id": run_id,
            "workflow_id": w_id,
            "title": title,
            "category": cat,
            "status": status,
            "inputs": json.loads(in_json) if in_json else {},
            "steps": json.loads(st_json) if st_json else [],
            "result": json.loads(res_json) if res_json else {},
            "execution_time_ms": exec_ms,
            "created_at": str(created_at)
        }
    except Exception as e:
        logger.error(f"Error fetching workflow run {run_id}: {e}")
        return None
