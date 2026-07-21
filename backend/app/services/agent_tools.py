"""
Agent Tools

Functions available to the agentic retrieval pipeline.
Provides structured access to search, registry,
and metadata operations.
"""

from app.services.search_service import (
    search_knowledge_base,
    simple_search
)
from app.database.document_registry import (
    get_all_documents,
    get_documents_by_status,
    get_registry_stats
)


def tool_search(query, top_k=3):
    """Search the knowledge base."""

    results = search_knowledge_base(
        query, top_k=top_k
    )

    return results


def tool_get_registry_stats():
    """Get document registry statistics."""

    return get_registry_stats()


def tool_list_documents(collection=None):
    """List all documents, optionally by collection."""

    docs = get_all_documents()

    if collection:
        docs = [
            d for d in docs
            if d["collection"] == collection
        ]

    return [
        {
            "file_name": d["file_name"],
            "collection": d["collection"],
            "vector_status": d["vector_status"],
            "version": d["version"]
        }
        for d in docs
    ]


def tool_list_departments():
    """Get all unique departments from registry."""

    docs = get_all_documents()

    departments = set()
    for doc in docs:
        if doc.get("metadata"):
            dept = doc["metadata"].get("department")
            if dept:
                departments.add(dept)

    return sorted(list(departments))


def tool_get_documents_by_collection(collection):
    """Get documents in a specific collection."""

    docs = get_all_documents()

    return [
        {
            "file_name": d["file_name"],
            "file_path": d["file_path"],
            "version": d["version"],
            "metadata": d.get("metadata")
        }
        for d in docs
        if d["collection"] == collection
    ]
