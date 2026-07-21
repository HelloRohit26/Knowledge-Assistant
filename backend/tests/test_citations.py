"""
Tests for Citation Engine (Phase 7)
"""

from app.services.citation_engine import (
    generate_citations,
    format_citations_for_prompt,
    compute_confidence
)


def test_compute_confidence():
    result = {
        "vector_distance": 0.2,
        "composite_score": 85.0,
        "is_authoritative": True
    }

    conf = compute_confidence(result)
    assert 0.0 <= conf <= 1.0
    assert conf > 0.7


def test_generate_citations():
    results = [
        {
            "id": "1",
            "document": "Employees receive 30 days paid leave annually.",
            "vector_distance": 0.1,
            "composite_score": 90.0,
            "is_authoritative": True,
            "metadata": {
                "file_name": "leave_policy.txt",
                "file_path": "data/hr/leave_policy.txt",
                "department": "HR",
                "collection": "hr",
                "document_type": "Policy",
                "topic": "leave",
                "version": "v2.0",
                "status": "Active"
            }
        }
    ]

    citations = generate_citations(results)

    assert len(citations) == 1
    c = citations[0]
    assert c["index"] == 1
    assert c["source"] == "leave_policy.txt"
    assert c["department"] == "HR"
    assert c["confidence"] > 0.5
    assert c["is_authoritative"] is True


def test_format_citations_for_prompt():
    citations = [
        {
            "index": 1,
            "source": "leave_policy.txt",
            "department": "HR",
            "confidence": 0.95,
            "is_authoritative": True
        }
    ]

    text = format_citations_for_prompt(citations)
    assert "[Source 1]" in text
    assert "leave_policy.txt" in text
    assert "AUTHORITATIVE" in text
