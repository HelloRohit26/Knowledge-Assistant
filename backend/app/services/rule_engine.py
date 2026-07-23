"""
Automation Rule Engine — Enterprise Event Triggers & Notification Workflows
"""

import json
from typing import List, Dict, Any
from app.database.db import get_connection
from app.core.logger import logger


DEFAULT_AUTOMATION_RULES = [
    {
        "id": "rule-auto-reindex",
        "name": "Auto-Index New File Additions",
        "event_trigger": "file_created",
        "action": "trigger_incremental_indexing",
        "is_active": True
    },
    {
        "id": "rule-conflict-alert",
        "name": "Flag High-Priority Policy Conflicts",
        "event_trigger": "conflict_detected",
        "action": "notify_compliance_lead",
        "is_active": True
    },
    {
        "id": "rule-weekly-exec-digest",
        "name": "Generate Weekly Executive Report",
        "event_trigger": "weekly_cron",
        "action": "execute_workflow_mgmt_weekly",
        "is_active": True
    }
]


def list_automation_rules() -> List[Dict[str, Any]]:
    """
    Returns active automation rules.
    """
    return DEFAULT_AUTOMATION_RULES


def dispatch_event_trigger(event_name: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatches an enterprise event trigger to matching rules.
    """
    triggered_rules = [r for r in DEFAULT_AUTOMATION_RULES if r["event_trigger"] == event_name and r["is_active"]]
    logger.info(f"Event trigger '{event_name}' matched {len(triggered_rules)} automation rules.")

    return {
        "event": event_name,
        "matched_rules_count": len(triggered_rules),
        "executed_rules": [r["name"] for r in triggered_rules]
    }
