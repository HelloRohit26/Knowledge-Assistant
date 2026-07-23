"""
Workflow Templates Library — Built-in & Custom Enterprise Workflows
"""

import json
from typing import List, Dict, Any, Optional
from app.database.db import get_connection
from app.core.logger import logger

# Built-in Enterprise Templates across HR, Finance, Legal, Engineering, Management
DEFAULT_WORKFLOW_TEMPLATES: List[Dict[str, Any]] = [
    # ── HR WORKFLOWS ──
    {
        "id": "hr-onboarding",
        "title": "Employee Onboarding Checklist & Guide",
        "description": "Synthesizes HR policies and role documentation to generate a comprehensive 30-60-90 day onboarding checklist for new hires.",
        "category": "HR",
        "icon": "UserPlus",
        "steps": [
            "Scan HR onboarding policies & handbook",
            "Extract role expectations & compliance milestones",
            "Synthesize week-by-week onboarding checklist",
            "Identify required form submissions & IT setup tasks",
            "Generate structured onboarding guide & action plan"
        ],
        "inputs_schema": [
            {"key": "role", "label": "Employee Role / Position", "type": "text", "placeholder": "e.g. Senior Software Engineer", "required": True},
            {"key": "department", "label": "Department", "type": "select", "options": ["Engineering", "HR", "Finance", "Legal", "Marketing", "Sales", "Operations"], "default": "Engineering"},
            {"key": "focus_areas", "label": "Specific Focus Areas", "type": "text", "placeholder": "e.g. Remote setup, Security compliance, Mentor pairing"}
        ]
    },
    {
        "id": "hr-leave-analysis",
        "title": "Leave Policy Version Comparison (v2.1 vs v2.4)",
        "description": "Compares leave policy revisions, highlighting structural changes, entitlement updates, approval hierarchy shifts, and legal compliance impacts.",
        "category": "HR",
        "icon": "GitCompare",
        "steps": [
            "Retrieve Leave Policy version 2.1 and version 2.4",
            "Extract leave categories (PTO, Sick, Parental, Bereavement)",
            "Identify structural delta and sentence-level changes",
            "Evaluate operational and employee compensation impact",
            "Produce executive comparison matrix & change advisory"
        ],
        "inputs_schema": [
            {"key": "doc_v1", "label": "Base Version Name/File", "type": "text", "default": "Leave Policy v2.1"},
            {"key": "doc_v2", "label": "Target Version Name/File", "type": "text", "default": "Leave Policy v2.4"},
            {"key": "key_topics", "label": "Key Clauses to Audit", "type": "text", "placeholder": "e.g. PTO carryover, Parental leave duration, Sick leave notice"}
        ]
    },
    {
        "id": "hr-report-gen",
        "title": "Weekly HR Operational Report",
        "description": "Aggregates all HR documents, policy updates, and employee tickets uploaded this week to produce a unified operational executive summary.",
        "category": "HR",
        "icon": "FileText",
        "steps": [
            "Query HR collection for documents modified in period",
            "Categorize updates by policy, benefit, and compliance",
            "Synthesize strategic trends and policy adjustments",
            "Generate actionable HR metrics summary"
        ],
        "inputs_schema": [
            {"key": "timeframe", "label": "Time Horizon", "type": "select", "options": ["This Week", "This Month", "Last 90 Days", "Year-to-Date"], "default": "This Month"}
        ]
    },
    {
        "id": "hr-exit-checklist",
        "title": "Employee Exit & Offboarding Protocol",
        "description": "Generates a complete offboarding checklist, security revoke protocol, equipment return ledger, and exit interview guidelines.",
        "category": "HR",
        "icon": "UserMinus",
        "steps": [
            "Retrieve offboarding & data retention policies",
            "Extract IT access revocation & hardware return criteria",
            "Draft customized exit interview questionnaire & protocol",
            "Generate final HR offboarding verification checklist"
        ],
        "inputs_schema": [
            {"key": "department", "label": "Department", "type": "text", "default": "Engineering"},
            {"key": "access_level", "label": "Access Level / Security Clearance", "type": "select", "options": ["Standard", "Elevated / Admin", "Executive"], "default": "Standard"}
        ]
    },

    # ── FINANCE WORKFLOWS ──
    {
        "id": "fin-expense-summary",
        "title": "Expense Policy Summary & Audit Guide",
        "description": "Extracts expense thresholds, per diem allowances, receipt rules, and approval workflows into a quick-reference card for employees.",
        "category": "Finance",
        "icon": "DollarSign",
        "steps": [
            "Scan expense & travel policy documents",
            "Extract spending thresholds by category (Travel, Meals, Tech)",
            "Identify non-reimbursable items & policy exceptions",
            "Format quick-reference expense cheat sheet"
        ],
        "inputs_schema": [
            {"key": "tier", "label": "Employee Tier", "type": "select", "options": ["All Employees", "Managers / Leads", "Executives"], "default": "All Employees"}
        ]
    },
    {
        "id": "fin-monthly-report",
        "title": "Monthly Finance & Procurement Synthesis",
        "description": "Analyzes all financial documentation, purchase orders, budget notes, and expense guidelines uploaded in the target billing cycle.",
        "category": "Finance",
        "icon": "BarChart3",
        "steps": [
            "Gather financial documentation uploaded in target month",
            "Extract spending patterns & vendor commitment changes",
            "Cross-reference compliance against corporate finance guidance",
            "Draft Finance Executive Brief & risk flags"
        ],
        "inputs_schema": [
            {"key": "month", "label": "Target Period", "type": "text", "default": "Current Billing Month"}
        ]
    },
    {
        "id": "fin-audit-prep",
        "title": "Financial Audit Preparation & Readiness Verification",
        "description": "Scans finance repositories to verify essential compliance documentation, identifies missing audit evidence, and flags outdated policies.",
        "category": "Finance",
        "icon": "ShieldCheck",
        "steps": [
            "Scan financial registry for compliance artifacts",
            "Check document currency & signature status",
            "Identify missing supporting audit evidence",
            "Generate Audit Preparedness Scorecard & gap report"
        ],
        "inputs_schema": [
            {"key": "audit_type", "label": "Audit Type", "type": "select", "options": ["Internal Audit", "SOC 2 Type II", "Financial Year-End", "Tax Compliance"], "default": "Internal Audit"}
        ]
    },

    # ── LEGAL WORKFLOWS ──
    {
        "id": "legal-contract-compare",
        "title": "Contract & Agreement Version Comparison",
        "description": "Deep clause-by-clause comparison of legal agreements, terms of service, or vendor master services agreements.",
        "category": "Legal",
        "icon": "FileCode",
        "steps": [
            "Load baseline legal document and revised agreement",
            "Extract legal clauses (Indemnification, Liability, Term, IP)",
            "Perform semantic differential analysis",
            "Flag elevated liability or risk exposures",
            "Generate redline clause breakdown report"
        ],
        "inputs_schema": [
            {"key": "contract_a", "label": "Original Contract", "type": "text", "placeholder": "e.g. MSA_v1.pdf or Contract Baseline"},
            {"key": "contract_b", "label": "Revised Contract", "type": "text", "placeholder": "e.g. MSA_v2_Redlined.pdf or Updated Draft"}
        ]
    },
    {
        "id": "legal-compliance-summary",
        "title": "Regulatory Compliance & Risk Assessment",
        "description": "Evaluates organizational policy documents against regulatory standards (GDPR, HIPAA, ISO27001) to identify liability gaps.",
        "category": "Legal",
        "icon": "Scale",
        "steps": [
            "Query policy collection for security and data handling rules",
            "Map policies against selected regulatory framework",
            "Detect non-compliant terms or missing mandatory clauses",
            "Synthesize Legal Compliance Risk Matrix"
        ],
        "inputs_schema": [
            {"key": "framework", "label": "Regulatory Standard", "type": "select", "options": ["GDPR & Privacy", "SOC 2 / ISO 27001", "HIPAA", "General Corporate Governance"], "default": "SOC 2 / ISO 27001"}
        ]
    },

    # ── ENGINEERING WORKFLOWS ──
    {
        "id": "eng-sop-generation",
        "title": "Standard Operating Procedure (SOP) Generator",
        "description": "Transforms existing technical architecture, deployment guides, or runbooks into a standardized, audit-ready Enterprise SOP.",
        "category": "Engineering",
        "icon": "Cpu",
        "steps": [
            "Scan technical documentation & architecture specifications",
            "Extract step-by-step operational workflows & safety controls",
            "Structure clear prerequisites, execution steps & verification",
            "Add troubleshooting matrix & escalation points",
            "Produce official ISO-compliant Technical SOP document"
        ],
        "inputs_schema": [
            {"key": "topic", "label": "Procedure Topic", "type": "text", "placeholder": "e.g. Production Deployment & Database Rollback"},
            {"key": "audience", "label": "Target Role", "type": "select", "options": ["DevOps / SRE", "Backend Engineers", "Support Engineers", "All Staff"], "default": "DevOps / SRE"}
        ]
    },
    {
        "id": "eng-incident-report",
        "title": "Incident Post-Mortem & Root Cause Analysis",
        "description": "Extracts incident logs, post-mortem notes, and operational metrics to generate a standardized Root Cause Analysis (RCA) report.",
        "category": "Engineering",
        "icon": "AlertTriangle",
        "steps": [
            "Load incident logs & retrospective notes",
            "Build incident timeline (Detection -> Triage -> Mitigation)",
            "Perform 5-Whys root cause analysis extraction",
            "Generate actionable preventive action items & SLA review"
        ],
        "inputs_schema": [
            {"key": "incident_id", "label": "Incident ID / Title", "type": "text", "placeholder": "e.g. INC-8492: API Gateway Outage"}
        ]
    },

    # ── MANAGEMENT WORKFLOWS ──
    {
        "id": "mgmt-weekly-exec-report",
        "title": "Weekly Executive Intelligence Report",
        "description": "Synthesizes multi-department document updates (HR, Finance, Engineering, Legal) into a 2-page executive summary for leadership.",
        "category": "Management",
        "icon": "Briefcase",
        "steps": [
            "Harvest key updates across all enterprise collections",
            "Extract strategic achievements, risks, and milestone progress",
            "Detect cross-department policy conflicts or resource bottlenecks",
            "Generate concise C-level Executive Briefing"
        ],
        "inputs_schema": [
            {"key": "priority_dept", "label": "Focus Department", "type": "select", "options": ["All Departments", "HR Focus", "Finance Focus", "Engineering Focus"], "default": "All Departments"}
        ]
    },
    {
        "id": "mgmt-org-insights",
        "title": "Document Health Audit & Outdated File Detector",
        "description": "Scans all indexed organizational documents to find outdated policies, conflicting directives, duplicate files, and missing documentations.",
        "category": "Management",
        "icon": "Search",
        "steps": [
            "Scan complete knowledge base metadata and checksums",
            "Identify stale documents (>180 days unupdated)",
            "Detect duplicate topics or conflicting version statements",
            "Provide actionable recommendations for document governance"
        ],
        "inputs_schema": [
            {"key": "stale_days", "label": "Threshold for Stale Documents (Days)", "type": "select", "options": ["90 Days", "180 Days", "365 Days"], "default": "180 Days"}
        ]
    }
]


def get_all_templates() -> List[Dict[str, Any]]:
    """
    Returns all templates (built-in + database custom templates).
    """
    templates = list(DEFAULT_WORKFLOW_TEMPLATES)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, category, icon, steps_json, inputs_schema_json, is_custom FROM workflow_templates")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            t_id, title, desc, cat, icon, steps_json, inputs_json, is_custom = row
            try:
                steps = json.loads(steps_json) if steps_json else []
            except Exception:
                steps = []
            try:
                inputs_schema = json.loads(inputs_json) if inputs_json else []
            except Exception:
                inputs_schema = []

            # Avoid duplicates if built-in id
            if not any(t["id"] == t_id for t in templates):
                templates.append({
                    "id": t_id,
                    "title": title,
                    "description": desc,
                    "category": cat,
                    "icon": icon,
                    "steps": steps,
                    "inputs_schema": inputs_schema,
                    "is_custom": bool(is_custom)
                })
    except Exception as e:
        logger.error(f"Error loading custom workflow templates: {e}")

    return templates


def get_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """
    Lookup a template by ID.
    """
    all_tpls = get_all_templates()
    for t in all_tpls:
        if t["id"] == template_id:
            return t
    return None


def save_custom_template(template_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a new custom user workflow template to SQLite.
    """
    t_id = template_data.get("id") or f"custom-{int(template_data.get('timestamp', 0)) or 'tpl'}"
    title = template_data.get("title", "Custom Workflow")
    description = template_data.get("description", "User-created workflow template")
    category = template_data.get("category", "Management")
    icon = template_data.get("icon", "Zap")
    steps = template_data.get("steps", ["Scan documents", "Analyze context", "Generate summary"])
    inputs_schema = template_data.get("inputs_schema", [])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO workflow_templates (id, title, description, category, icon, steps_json, inputs_schema_json, is_custom)
    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (t_id, title, description, category, icon, json.dumps(steps), json.dumps(inputs_schema)))
    conn.commit()
    conn.close()

    return {
        "id": t_id,
        "title": title,
        "description": description,
        "category": category,
        "icon": icon,
        "steps": steps,
        "inputs_schema": inputs_schema,
        "is_custom": True
    }
