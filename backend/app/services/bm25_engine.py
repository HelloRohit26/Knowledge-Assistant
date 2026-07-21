"""
BM25 Keyword Search Engine

Builds an in-memory BM25 index from all document chunks
in ChromaDB. Provides keyword-based search alongside
vector search for hybrid retrieval.
"""

import re
from rank_bm25 import BM25Okapi

from app.services.vector_store import (
    get_all_documents_with_metadata
)


# Module-level index storage
_bm25_index = None
_bm25_docs = None
_bm25_ids = None
_bm25_metadatas = None


def tokenize(text):
    """Simple whitespace + punctuation tokenizer."""

    text = text.lower()
    tokens = re.findall(r'\w+', text)

    return tokens


def build_bm25_index():
    """
    Build BM25 index from all documents in ChromaDB.
    Call after indexing new documents.
    """

    global _bm25_index, _bm25_docs
    global _bm25_ids, _bm25_metadatas

    results = get_all_documents_with_metadata()

    if not results["documents"]:
        _bm25_index = None
        _bm25_docs = []
        _bm25_ids = []
        _bm25_metadatas = []
        return 0

    _bm25_docs = results["documents"]
    _bm25_ids = results["ids"]
    _bm25_metadatas = results["metadatas"]

    # Tokenize all documents
    tokenized = [
        tokenize(doc)
        for doc in _bm25_docs
    ]

    _bm25_index = BM25Okapi(tokenized)

    return len(_bm25_docs)


def search_bm25(query, top_k=10):
    """
    Keyword search using BM25.
    Returns list of (doc_id, document, metadata, score).
    """

    global _bm25_index

    if _bm25_index is None:
        build_bm25_index()

    if _bm25_index is None:
        return []

    query_tokens = tokenize(query)

    scores = _bm25_index.get_scores(query_tokens)

    # Get top_k indices sorted by score desc
    scored_indices = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    results = []
    for idx, score in scored_indices:

        if score <= 0:
            continue

        results.append({
            "id": _bm25_ids[idx],
            "document": _bm25_docs[idx],
            "metadata": _bm25_metadatas[idx],
            "bm25_score": float(score)
        })

    return results
