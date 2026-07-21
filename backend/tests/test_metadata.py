"""
Tests for Metadata Engine & Validation (Phase 2)
"""

from app.services.metadata_validator import (
    validate_metadata,
    validate_department,
    validate_status,
    normalize_date,
    detect_metadata_conflicts
)


def test_department_validation():
    assert validate_department("hr") == "HR"
    assert validate_department("human resources") == "HR"
    assert validate_department("tech") == "Technical"
    assert validate_department("UNKNOWN_DEPT") == "General"


def test_status_validation():
    assert validate_status("active") == "Active"
    assert validate_status("in effect") == "Active"
    assert validate_status("deprecated") == "Archived"
    assert validate_status("wip") == "Draft"


def test_date_normalization():
    assert normalize_date("2026-07-21") == "2026-07-21"
    assert normalize_date("21/07/2026") == "2026-07-21"
    assert normalize_date("July 21, 2026") == "2026-07-21"
    assert normalize_date(None) is None


def test_full_metadata_validation(sample_metadata):
    raw_metadata = {
        "department": "human resources",
        "status": "in effect",
        "effective_date": "21/07/2026",
        "tags": ["Leave ", " HR ", "leave"],
        "authority_score": "95"
    }

    validated = validate_metadata(raw_metadata)

    assert validated["department"] == "HR"
    assert validated["status"] == "Active"
    assert validated["effective_date"] == "2026-07-21"
    assert "leave" in validated["tags"]
    assert validated["authority_score"] == 95


def test_detect_metadata_conflicts():
    old_meta = {"department": "HR", "status": "Active", "version": "v1"}
    new_meta = {"department": "HR", "status": "Archived", "version": "v2"}

    conflicts = detect_metadata_conflicts(old_meta, new_meta)

    assert len(conflicts) == 2
    fields = [c["field"] for c in conflicts]
    assert "status" in fields
    assert "version" in fields
