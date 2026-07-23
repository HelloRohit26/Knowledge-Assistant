"""
Reranker

Reranks search results using a composite score:
- Semantic relevance (from Gemini)
- Metadata quality score (authority, recency, official status)
- Final composite ranking
"""

from google import genai
from google.genai import types

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def compute_metadata_score(metadata):
    """
    Score 0-100 based on metadata quality signals.
    Higher = more authoritative and relevant.
    """

    score = 0

    # Authority score (0-100, already assigned by rules)
    authority = metadata.get("authority_score", 50)
    if isinstance(authority, str):
        try:
            authority = int(authority)
        except ValueError:
            authority = 50

    score += authority * 0.4

    # Is official document
    is_official = metadata.get("is_official", False)
    if is_official == "true" or is_official is True:
        score += 15

    # Active status boost
    status = str(metadata.get("status", "")).lower()
    status_scores = {
        "active": 20,
        "under review": 10,
        "draft": 5,
        "archived": 0,
        "superseded": -5
    }
    score += status_scores.get(status, 5)

    # Has version (shows maintained doc)
    if metadata.get("version"):
        score += 5

    # Has effective date (shows governance)
    if metadata.get("effective_date"):
        score += 5

    return min(100, max(0, score))


def gemini_rerank(query, candidates, top_k=5):
    """
    Use Gemini to score relevance of candidates.
    Returns candidates with semantic_score added.
    """

    if not candidates:
        return []

    # Limit to avoid huge prompts
    batch = candidates[:15]

    chunks_text = ""
    for i, item in enumerate(batch):
        doc_preview = item["document"][:300]
        chunks_text += f"\n[{i}] {doc_preview}\n"

    prompt = f"""
You are a search relevance judge.

Query: {query}

Rate each document chunk's relevance to the query.
Score from 0 to 100 (100 = perfectly relevant).

Documents:
{chunks_text}

Return a JSON array of objects with "index" and "score".
Example: [{{"index": 0, "score": 85}}, {{"index": 1, "score": 30}}]

Only return the JSON array, nothing else.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
            )
        )

        import json
        scores = json.loads(response.text)

        score_map = {}
        for item in scores:
            score_map[item["index"]] = item["score"]

        for i, item in enumerate(batch):
            item["semantic_score"] = score_map.get(
                i, 50
            )

    except Exception:
        # Fall back: use RRF scores as proxy
        for item in batch:
            item["semantic_score"] = 50

    return batch


def rerank(query, results, top_k=5):
    """
    Full reranking pipeline:
    1. Compute metadata scores
    2. Get Gemini semantic scores
    3. Combine into composite score
    4. Sort and return top_k
    """

    if not results:
        return []

    # Step 1: Metadata scores
    for item in results:
        item["metadata_score"] = compute_metadata_score(
            item.get("metadata", {})
        )

    # Step 2: Gemini semantic scoring
    results = gemini_rerank(
        query, results, top_k=top_k
    )

    # Step 3: Composite score
    # 0.50 * semantic + 0.30 * metadata + 0.20 * rrf
    for item in results:

        semantic = item.get("semantic_score", 50)
        meta = item.get("metadata_score", 50)
        rrf = item.get("rrf_score", 0) * 1000

        item["composite_score"] = (
            0.50 * semantic +
            0.30 * meta +
            0.20 * min(rrf, 100)
        )

    # Step 4: Sort by composite
    results.sort(
        key=lambda x: x.get(
            "composite_score", 0
        ),
        reverse=True
    )

    return results[:top_k]
