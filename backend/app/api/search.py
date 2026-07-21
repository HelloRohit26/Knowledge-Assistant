"""
Search API Routes

POST /api/search         — Full hybrid search with filters & reranking
POST /api/search/simple  — Quick vector-only search
"""

from fastapi import APIRouter

from app.schemas.document_schemas import (
    SearchRequest
)
from app.services.search_service import (
    search_knowledge_base,
    simple_search
)
from app.services.embedding_service import (
    get_embedding
)

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


@router.post("")
def enterprise_search(request: SearchRequest):
    """Full enterprise search pipeline."""

    results = search_knowledge_base(
        query=request.query,
        top_k=request.top_k
    )

    return results


@router.post("/simple")
def quick_search(request: SearchRequest):
    """Quick vector-only search."""

    results = simple_search(
        query=request.query,
        top_k=request.top_k
    )

    return results
