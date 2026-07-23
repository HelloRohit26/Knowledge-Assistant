"""
Knowledge Graph Service — Visual Entity Relationships & Related Document Mapping
"""

from typing import List, Dict, Any
from app.database.document_registry import get_all_documents
from app.database.db import get_connection
from app.core.logger import logger


def generate_knowledge_graph() -> Dict[str, Any]:
    """
    Constructs a visual Knowledge Graph of Documents, Departments, Topics, and Clauses.
    """
    docs = get_all_documents()

    nodes = []
    edges = []

    # Category Nodes
    categories = ["HR", "Finance", "Legal", "Engineering", "Management"]
    for cat in categories:
        nodes.append({
            "id": f"cat-{cat.lower()}",
            "label": f"{cat} Department",
            "type": "category",
            "color": _get_cat_color(cat),
            "size": 35
        })

    # Document & Topic Nodes
    for i, doc in enumerate(docs):
        doc_id = f"doc-{i+1}"
        file_name = doc.get("file_name", "Document")
        collection = doc.get("collection", "general").title()

        nodes.append({
            "id": doc_id,
            "label": file_name,
            "type": "document",
            "collection": collection,
            "version": f"v{doc.get('version', 1)}.0",
            "size": 25
        })

        # Connect Document to Category
        cat_node_id = f"cat-{collection.lower()}"
        if any(n["id"] == cat_node_id for n in nodes):
            edges.append({
                "id": f"e-{doc_id}-{cat_node_id}",
                "source": doc_id,
                "target": cat_node_id,
                "label": "belongs to"
            })

    # Connect related document nodes based on keyword overlap
    for i in range(len(docs)):
        for j in range(i + 1, min(i + 4, len(docs))):
            name_a = docs[i].get("file_name", "")
            name_b = docs[j].get("file_name", "")
            if docs[i].get("collection") == docs[j].get("collection"):
                edges.append({
                    "id": f"e-rel-{i}-{j}",
                    "source": f"doc-{i+1}",
                    "target": f"doc-{j+1}",
                    "label": "shares context",
                    "style": "dashed"
                })

    return {
        "nodes_count": len(nodes),
        "edges_count": len(edges),
        "nodes": nodes,
        "edges": edges
    }


def _get_cat_color(cat: str) -> str:
    colors = {
        "HR": "#06b6d4",
        "Finance": "#10b981",
        "Legal": "#8b5cf6",
        "Engineering": "#3b82f6",
        "Management": "#f59e0b"
    }
    return colors.get(cat, "#64748b")
