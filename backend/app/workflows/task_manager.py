"""
Task Manager — Asynchronous Task Tracking & Background Job Registry
"""

import time
import threading
from typing import Dict, Any, Optional
from app.core.logger import logger

# In-memory registry of running and completed tasks
_ACTIVE_TASKS: Dict[str, Dict[str, Any]] = {}
_LOCK = threading.Lock()


def register_task(task_id: str, workflow_id: str, title: str, category: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Registers a new task in memory.
    """
    task_data = {
        "task_id": task_id,
        "workflow_id": workflow_id,
        "title": title,
        "category": category,
        "inputs": inputs,
        "status": "running",
        "progress": 10,
        "current_step": "Initializing Workflow Execution Pipeline...",
        "start_time": time.time(),
        "result": None,
        "error": None
    }
    with _LOCK:
        _ACTIVE_TASKS[task_id] = task_data
    return task_data


def update_task_progress(task_id: str, progress: int, current_step: str, result: Optional[Dict[str, Any]] = None, status: str = "running"):
    """
    Updates the live execution progress of a running task.
    """
    with _LOCK:
        if task_id in _ACTIVE_TASKS:
            _ACTIVE_TASKS[task_id]["progress"] = progress
            _ACTIVE_TASKS[task_id]["current_step"] = current_step
            _ACTIVE_TASKS[task_id]["status"] = status
            if result:
                _ACTIVE_TASKS[task_id]["result"] = result


def complete_task(task_id: str, result: Dict[str, Any]):
    """
    Marks a task as completed with final output payload.
    """
    with _LOCK:
        if task_id in _ACTIVE_TASKS:
            _ACTIVE_TASKS[task_id]["status"] = "completed"
            _ACTIVE_TASKS[task_id]["progress"] = 100
            _ACTIVE_TASKS[task_id]["current_step"] = "Workflow Execution Completed"
            _ACTIVE_TASKS[task_id]["result"] = result


def fail_task(task_id: str, error_msg: str):
    """
    Marks a task as failed with error details.
    """
    with _LOCK:
        if task_id in _ACTIVE_TASKS:
            _ACTIVE_TASKS[task_id]["status"] = "failed"
            _ACTIVE_TASKS[task_id]["progress"] = 100
            _ACTIVE_TASKS[task_id]["current_step"] = "Execution Failed"
            _ACTIVE_TASKS[task_id]["error"] = error_msg


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the status of a specific task.
    """
    with _LOCK:
        return _ACTIVE_TASKS.get(task_id)


def list_active_tasks() -> Dict[str, Dict[str, Any]]:
    """
    Returns all active tasks.
    """
    with _LOCK:
        return dict(_ACTIVE_TASKS)
