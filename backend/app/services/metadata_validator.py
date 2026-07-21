"""
Metadata Validator & Normalizer

Validates extracted metadata against known enterprise values
and normalizes fields for consistency.
"""

import re
from datetime import datetime


# ── Allowed values ──

VALID_DEPARTMENTS = {
    "hr", "policy", "technical", "sales",
    "research", "general", "finance",
    "legal", "operations", "marketing"
}

VALID_STATUSES = {
    "active", "draft", "archived",
    "superseded", "under review"
}

VALID_DOCUMENT_TYPES = {
    "policy", "sop", "handbook", "guideline",
    "faq", "memo", "report", "checklist",
    "manual", "specification", "analysis",
    "proposal", "summary", "directory",
    "matrix", "plan", "review", "code"
}

VALID_CATEGORIES = {
    "policy", "sop", "handbook", "guideline",
    "faq", "memo", "meeting notes",
    "report", "analysis", "manual"
}


def normalize_string(value):
    """Trim whitespace and normalize casing."""

    if value is None:
        return None

    cleaned = str(value).strip()

    if not cleaned:
        return None

    return cleaned


def normalize_date(value):
    """Try to normalize date to YYYY-MM-DD format."""

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Already in YYYY-MM-DD
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return value

    # Common patterns
    date_formats = [
        "%d/%m/%Y", "%m/%d/%Y",
        "%d-%m-%Y", "%m-%d-%Y",
        "%B %d, %Y", "%d %B %Y",
        "%b %d, %Y", "%d %b %Y",
        "%Y/%m/%d",
        "%d %B, %Y",
        "%B %Y", "%b %Y"
    ]

    for fmt in date_formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return value


def validate_department(value):
    """Validate and normalize department."""

    if value is None:
        return "General"

    normalized = normalize_string(value).lower()

    if normalized in ["hr", "human resources", "human resource"]:
        return "HR"

    if normalized in ["it", "tech", "technical", "information technology", "engineering"]:
        return "Technical"

    if normalized in VALID_DEPARTMENTS:
        return normalized.title()

    return "General"


def validate_status(value):
    """Validate and normalize status."""

    if value is None:
        return "Active"

    normalized = normalize_string(value).lower()

    if normalized in VALID_STATUSES:
        return normalized.title()

    # Common variants
    mapping = {
        "current": "Active",
        "live": "Active",
        "in effect": "Active",
        "effective": "Active",
        "deprecated": "Archived",
        "old": "Archived",
        "retired": "Archived",
        "replaced": "Superseded",
        "wip": "Draft",
        "in progress": "Draft",
        "pending": "Under Review",
        "review": "Under Review",
    }

    if normalized in mapping:
        return mapping[normalized]

    return "Active"


def validate_document_type(value):
    """Validate and normalize document type."""

    if value is None:
        return None

    normalized = normalize_string(value).lower()

    if normalized in VALID_DOCUMENT_TYPES:
        return normalized.title()

    return normalize_string(value)


def validate_category(value):
    """Validate and normalize document category."""

    if value is None:
        return None

    normalized = normalize_string(value).lower()

    if normalized in VALID_CATEGORIES:
        return normalized.title()

    return normalize_string(value)


def validate_tags(tags):
    """Normalize tags list."""

    if tags is None:
        return []

    if not isinstance(tags, list):
        return []

    normalized = []
    for tag in tags:
        cleaned = normalize_string(tag)
        if cleaned:
            normalized.append(cleaned.lower())

    return list(set(normalized))


def validate_metadata(metadata_dict):
    """
    Full validation and normalization pipeline.
    Takes a metadata dict, returns cleaned dict.
    """

    validated = dict(metadata_dict)

    # Validate each field
    validated["department"] = validate_department(
        validated.get("department")
    )

    validated["status"] = validate_status(
        validated.get("status")
    )

    validated["document_type"] = validate_document_type(
        validated.get("document_type")
    )

    validated["document_category"] = validate_category(
        validated.get("document_category")
    )

    validated["effective_date"] = normalize_date(
        validated.get("effective_date")
    )

    validated["tags"] = validate_tags(
        validated.get("tags")
    )

    # Normalize string fields
    for field in ["topic", "author", "summary",
                  "version", "source_type"]:

        validated[field] = normalize_string(
            validated.get(field)
        )

    # Ensure scores are valid
    raw_authority = validated.get("authority_score", 50)
    try:
        authority = int(raw_authority)
    except (ValueError, TypeError):
        authority = 50

    validated["authority_score"] = max(
        0, min(100, authority)
    )

    # Ensure booleans
    for field in ["is_policy", "is_official"]:
        val = validated.get(field)
        if not isinstance(val, bool):
            validated[field] = False

    return validated


def detect_metadata_conflicts(old_metadata, new_metadata):
    """
    Compare old and new metadata, return list of
    changed fields.
    """

    if old_metadata is None:
        return []

    conflicts = []

    important_fields = [
        "department", "status", "document_type",
        "version", "effective_date"
    ]

    for field in important_fields:

        old_val = old_metadata.get(field)
        new_val = new_metadata.get(field)

        if old_val != new_val:
            conflicts.append({
                "field": field,
                "old_value": old_val,
                "new_value": new_val
            })

    return conflicts
