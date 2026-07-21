"""
Hybrid Search Engine

Combines vector (semantic) search with BM25 (keyword) search
using Reciprocal Rank Fusion (RRF) for better recall.
"""

from app.services.embedding_service import get_embedding
from app.services.vector_store import search_with_filters
from app.services.bm25_engine import search_bm25


def reciprocal_rank_fusion(
    vector_results,
    bm25_results,
    k=60
):
    """
    Merge vector and BM25 results using RRF.
    k=60 is the standard RRF constant.
    """

    fused_scores = {}
    doc_data = {}

    # Score vector results
    for rank, item in enumerate(vector_results):

        doc_id = item["id"]
        rrf_score = 1.0 / (k + rank + 1)

        fused_scores[doc_id] = (
            fused_scores.get(doc_id, 0) + rrf_score
        )

        doc_data[doc_id] = {
            "document": item["document"],
            "metadata": item["metadata"],
            "vector_distance": item.get(
                "distance", None
            )
        }

    # Score BM25 results
    for rank, item in enumerate(bm25_results):

        doc_id = item["id"]
        rrf_score = 1.0 / (k + rank + 1)

        fused_scores[doc_id] = (
            fused_scores.get(doc_id, 0) + rrf_score
        )

        if doc_id not in doc_data:
            doc_data[doc_id] = {
                "document": item["document"],
                "metadata": item["metadata"],
                "vector_distance": None
            }

        doc_data[doc_id]["bm25_score"] = item.get(
            "bm25_score", 0
        )

    # Sort by fused score
    sorted_ids = sorted(
        fused_scores.keys(),
        key=lambda x: fused_scores[x],
        reverse=True
    )

    merged = []
    for doc_id in sorted_ids:
        data = doc_data[doc_id]
        data["id"] = doc_id
        data["rrf_score"] = fused_scores[doc_id]
        merged.append(data)

    return merged


def hybrid_search(
    query,
    filters=None,
    top_k=5
):
    """
    Full hybrid search pipeline:
    1. Vector search (with optional filters)
    2. BM25 keyword search
    3. RRF fusion
    4. Return top_k deduplicated results
    """

    # Get query embedding
    query_embedding = get_embedding(query)

    # ── Vector search ──
    fetch_k = top_k * 3

    vector_raw = search_with_filters(
        query_embedding=query_embedding,
        filters=filters,
        top_k=fetch_k
    )

    vector_results = []
    if vector_raw["ids"] and vector_raw["ids"][0]:
        for i in range(len(vector_raw["ids"][0])):
            vector_results.append({
                "id": vector_raw["ids"][0][i],
                "document": vector_raw["documents"][0][i],
                "metadata": vector_raw["metadatas"][0][i],
                "distance": vector_raw["distances"][0][i]
            })

    # ── BM25 search ──
    bm25_results = search_bm25(
        query, top_k=fetch_k
    )

    # ── Reciprocal Rank Fusion ──
    merged = reciprocal_rank_fusion(
        vector_results,
        bm25_results
    )

    return merged[:top_k]
