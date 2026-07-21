"""
Analytics API Routes

Provides reporting & dashboard metrics on document distributions,
departments, and document types.
"""

from fastapi import APIRouter

from app.database.document_registry import get_all_documents
from app.schemas.document_schemas import AnalyticsResponse

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("", response_model=AnalyticsResponse)
def get_analytics():
    """Get system-wide document analytics."""

    docs = get_all_documents()

    by_dept = {}
    by_type = {}
    by_status = {}
    by_collection = {}

    for doc in docs:

        # Collection
        coll = doc.get("collection", "unknown")
        by_collection[coll] = by_collection.get(coll, 0) + 1

        # Status
        status = doc.get("vector_status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1

        # Metadata metrics
        meta = doc.get("metadata") or {}

        dept = meta.get("department", "General")
        by_dept[dept] = by_dept.get(dept, 0) + 1

        dtype = meta.get("document_type", "Other")
        by_type[dtype] = by_type.get(dtype, 0) + 1

    return AnalyticsResponse(
        total_documents=len(docs),
        by_department=by_dept,
        by_type=by_type,
        by_status=by_status,
        by_collection=by_collection
    )
