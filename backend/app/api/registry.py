"""
Registry & System Health API Routes

GET  /api/registry/stats   — Registry document counts & distribution
GET  /api/registry/health  — System health check
POST /api/registry/reindex — Trigger incremental re-indexing
"""

from fastapi import APIRouter

from app.database.document_registry import get_registry_stats
from app.services.incremental_indexer import run_incremental_indexing
from app.services.vector_store import get_collection_count

router = APIRouter(
    prefix="/api/registry",
    tags=["Registry & Health"]
)


@router.get("/stats")
def registry_stats():
    """Get system registry stats."""

    stats = get_registry_stats()
    stats["total_vectors"] = get_collection_count()

    return stats


@router.get("/health")
def system_health():
    """Health check endpoint."""

    return {
        "status": "healthy",
        "database": "connected",
        "vector_store": "active",
        "vector_count": get_collection_count()
    }


@router.post("/reindex")
def trigger_reindex():
    """Manually trigger incremental indexing."""

    result = run_incremental_indexing()

    return {
        "message": "Incremental indexing executed",
        "result": result
    }
