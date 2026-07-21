"""
Tests for Conflict Resolution Engine (Phase 6)
"""

from app.services.conflict_resolver import resolve_conflicts, compute_authority


def test_compute_authority():
    meta = {
        "authority_score": 100,
        "status": "Active",
        "version": "v2.0",
        "is_official": True
    }

    score = compute_authority(meta)
    assert score > 150


def test_resolve_conflicts_single_document():
    results = [
        {
            "id": "1",
            "document": "Leave policy text",
            "metadata": {"topic": "leave", "version": "v1", "status": "Active"}
        }
    ]

    resolved = resolve_conflicts(results)
    assert len(resolved) == 1
    assert resolved[0]["is_authoritative"] is True
    assert resolved[0]["conflict_status"] == "no_conflict"


def test_resolve_conflicts_two_versions():
    results = [
        {
            "id": "old_doc",
            "document": "Old leave policy: 20 days paid leave",
            "metadata": {
                "topic": "leave",
                "document_type": "Policy",
                "version": "v1",
                "status": "Archived",
                "authority_score": 50,
                "is_official": False
            }
        },
        {
            "id": "new_doc",
            "document": "New leave policy: 30 days paid leave",
            "metadata": {
                "topic": "leave",
                "document_type": "Policy",
                "version": "v2",
                "status": "Active",
                "authority_score": 100,
                "is_official": True
            }
        }
    ]

    resolved = resolve_conflicts(results)

    # Winner should be authoritative
    authoritative_item = next(r for r in resolved if r["is_authoritative"])
    assert authoritative_item["id"] == "new_doc"
    assert authoritative_item["conflict_status"] == "authoritative"

    superseded_item = next(r for r in resolved if not r["is_authoritative"])
    assert superseded_item["id"] == "old_doc"
    assert superseded_item["conflict_status"] == "superseded"
