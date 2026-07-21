"""
Search Service

Orchestrates the full enterprise search pipeline:
1. Query analysis (extract filters)
2. Hybrid search (vector + BM25 + RRF)
3. Reranking (Gemini + metadata + composite)
"""

from app.services.embedding_service import get_embedding
from app.services.vector_store import search_documents
from app.services.query_analyzer import (
    analyze_query,
    build_chroma_filters
)
from app.services.hybrid_search import hybrid_search
from app.services.reranker import rerank


def search_knowledge_base(query, top_k=5):
    """
    Full enterprise search pipeline.
    """

    # Step 1: Analyze query for filters
    analysis = analyze_query(query)

    # Step 2: Build ChromaDB filters
    filters = build_chroma_filters(analysis)

    # Step 3: Hybrid search
    search_text = analysis.search_text or query
    results = hybrid_search(
        query=search_text,
        filters=filters,
        top_k=top_k * 2
    )

    # Step 4: Rerank
    ranked = rerank(
        query=query,
        results=results,
        top_k=top_k
    )

    return {
        "results": ranked,
        "query_analysis": analysis.model_dump(),
        "filters_applied": filters,
        "total_candidates": len(results)
    }


def simple_search(query, top_k=3):
    """
    Quick vector-only search (no analysis,
    no BM25, no reranking). Fast path.
    """

    query_embedding = get_embedding(query)

    results = search_documents(
        query_embedding=query_embedding,
        top_k=top_k
    )

    return results