"""
AI Copilot Service — Proactive Workspace Intelligence & Action Recommendations
"""

from typing import List, Dict, Any
from app.database.document_registry import get_all_documents, get_registry_stats
from app.core.logger import logger


def generate_copilot_suggestions() -> Dict[str, Any]:
    """
    Analyzes active workspace documents and returns proactive action suggestions.
    """
    docs = get_all_documents()
    stats = get_registry_stats()

    total_docs = stats.get("total_documents", 0)
    collections = stats.get("by_collection", {})

    suggestions = []

    # Category specific analysis
    hr_count = collections.get("hr", 0) + collections.get("HR", 0)
    fin_count = collections.get("finance", 0) + collections.get("Finance", 0)
    legal_count = collections.get("legal", 0) + collections.get("Legal", 0)
    eng_count = collections.get("engineering", 0) + collections.get("Engineering", 0) + collections.get("tech", 0)

    # If HR documents are detected
    if hr_count > 0 or total_docs > 0:
        suggestions.append({
            "id": "sug-hr-onboarding",
            "title": f"Generate Employee Handbook & Onboarding Checklist",
            "description": f"You have {hr_count or total_docs} HR/policy documents uploaded. Synthesize a unified 30-60-90 day onboarding checklist.",
            "workflow_id": "hr-onboarding",
            "category": "HR",
            "impact": "High",
            "badge": f"{hr_count or total_docs} Documents"
        })
        suggestions.append({
            "id": "sug-hr-leave",
            "title": "Compare Leave Policy Revisions",
            "description": "Detect policy conflicts between Leave Policy v2.1 vs v2.4 and highlight entitlement deltas.",
            "workflow_id": "hr-leave-analysis",
            "category": "HR",
            "impact": "Medium",
            "badge": "Version Audit"
        })

    # If Finance documents are present
    if fin_count > 0 or total_docs > 0:
        suggestions.append({
            "id": "sug-fin-summary",
            "title": "Expense Policy Summary & Cheat Sheet",
            "description": "Extract spending per diems, travel thresholds, and receipt rules into an employee reference guide.",
            "workflow_id": "fin-expense-summary",
            "category": "Finance",
            "impact": "High",
            "badge": "Audit Ready"
        })

    # If Engineering / Technical documents
    if eng_count > 0 or total_docs > 0:
        suggestions.append({
            "id": "sug-eng-sop",
            "title": "Generate Production SOP from Tech Docs",
            "description": "Transform architecture specs and deployment notes into an ISO-compliant Technical SOP.",
            "workflow_id": "eng-sop-generation",
            "category": "Engineering",
            "impact": "High",
            "badge": "SOP Standard"
        })

    # General Governance Suggestion
    suggestions.append({
        "id": "sug-mgmt-audit",
        "title": "Audit Outdated Policies & Duplicate Documents",
        "description": f"Perform a document health audit across {total_docs} files to identify stale policies and missing directives.",
        "workflow_id": "mgmt-org-insights",
        "category": "Management",
        "impact": "Medium",
        "badge": "Governance"
    })

    return {
        "summary_text": f"AI Copilot analyzed {total_docs} documents across your organization.",
        "total_documents": total_docs,
        "collection_breakdown": collections,
        "suggestions": suggestions
    }
