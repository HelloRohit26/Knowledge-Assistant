"""
Verification script for AI Workflows & Copilot features
"""

from app.database.init_db import initialize_database
from app.workflows.workflow_templates import get_all_templates
from app.workflows.workflow_executor import run_workflow
from app.workflows.report_generator import generate_pdf_report, generate_docx_report
from app.services.copilot_service import generate_copilot_suggestions

def test_workflow_system():
    initialize_database()

    templates = get_all_templates()
    print(f"Templates loaded: {len(templates)}")
    assert len(templates) > 0

    run_res = run_workflow("hr-onboarding", {"role": "Senior Software Engineer"})
    print(f"Workflow Run ID: {run_res.get('run_id')}, Status: {run_res.get('status')}")
    assert run_res.get("status") == "completed"

    pdf_b = generate_pdf_report("Onboarding Report", "HR", run_res["result"]["report_markdown"])
    print(f"PDF Bytes Generated: {len(pdf_b)}")
    assert len(pdf_b) > 0

    docx_b = generate_docx_report("Onboarding Report", "HR", run_res["result"]["report_markdown"])
    print(f"DOCX Bytes Generated: {len(docx_b)}")
    assert len(docx_b) > 0

    copilot_sug = generate_copilot_suggestions()
    print(f"Copilot Suggestions: {len(copilot_sug['suggestions'])}")
    assert len(copilot_sug["suggestions"]) > 0

if __name__ == "__main__":
    test_workflow_system()
