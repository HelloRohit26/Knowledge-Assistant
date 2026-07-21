"""
Tests for Document Registry (Phase 1)
"""

import pytest
from app.database.db import get_connection
from app.database.document_registry import (
    save_document,
    get_document,
    get_all_documents,
    update_metadata,
    increment_version,
    delete_document,
    get_registry_stats
)


@pytest.fixture(autouse=True)
def clear_registry():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM document_registry")
    conn.commit()
    conn.close()
    yield


def test_save_and_get_document(sample_metadata):
    save_document(
        file_path="data/hr/test_policy.txt",
        file_name="test_policy.txt",
        collection="hr",
        checksum="abc123md5",
        file_size=1024,
        last_modified=123456789.0,
        metadata_dict=sample_metadata,
        vector_status="indexed"
    )

    doc = get_document("data/hr/test_policy.txt")

    assert doc is not None
    assert doc["file_name"] == "test_policy.txt"
    assert doc["collection"] == "hr"
    assert doc["checksum"] == "abc123md5"
    assert doc["vector_status"] == "indexed"
    assert doc["metadata"]["department"] == "HR"


def test_get_all_documents(sample_metadata):
    save_document("doc1.txt", "doc1.txt", "hr", "sum1", 100, 1.0, sample_metadata)
    save_document("doc2.txt", "doc2.txt", "policy", "sum2", 200, 2.0, sample_metadata)

    docs = get_all_documents()
    assert len(docs) == 2


def test_update_metadata():
    save_document("doc.txt", "doc.txt", "hr", "sum1", 100, 1.0, {"department": "HR"})

    update_metadata("doc.txt", {"department": "Technical", "status": "Active"})

    doc = get_document("doc.txt")
    assert doc["metadata"]["department"] == "Technical"


def test_increment_version():
    save_document("doc.txt", "doc.txt", "hr", "sum1", 100, 1.0)
    doc_initial = get_document("doc.txt")
    assert doc_initial["version"] == 1

    increment_version("doc.txt", "sum2_new", 2.0)
    doc_updated = get_document("doc.txt")

    assert doc_updated["version"] == 2
    assert doc_updated["checksum"] == "sum2_new"
    assert doc_updated["vector_status"] == "dirty"


def test_delete_document():
    save_document("doc.txt", "doc.txt", "hr", "sum1", 100, 1.0)
    assert get_document("doc.txt") is not None

    delete_document("doc.txt")
    assert get_document("doc.txt") is None


def test_registry_stats():
    save_document("doc1.txt", "doc1.txt", "hr", "s1", 100, 1.0, vector_status="indexed")
    save_document("doc2.txt", "doc2.txt", "sales", "s2", 100, 1.0, vector_status="pending")

    stats = get_registry_stats()
    assert stats["total_documents"] == 2
    assert stats["by_status"]["indexed"] == 1
    assert stats["by_status"]["pending"] == 1
