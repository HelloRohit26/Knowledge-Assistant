"""
Citation Engine

Generates structured citations for every chunk
used in an answer. Each citation includes source file,
department, chunk position, and confidence score.
"""

import json


def compute_confidence(result):
    """
    Compute confidence score (0.0 - 1.0) from search signals.
    """

    confidence = 0.5

    # Vector distance (lower = better, typically 0-2)
    distance = result.get("vector_distance")
    if distance is not None:
        # Convert distance to 0-1 (inverse)
        distance_score = max(0, 1.0 - distance / 2.0)
        confidence = distance_score * 0.4 + 0.3

    # Composite score boost
    composite = result.get("composite_score", 0)
    if composite > 0:
        confidence += min(composite / 200.0, 0.3)

    # Authoritative document boost
    if result.get("is_authoritative", False):
        confidence += 0.1

    return round(min(1.0, confidence), 3)


def generate_citations(results):
    """
    Generate citation objects for search results.

    Returns list of citation dicts with:
    - source: file name
    - file_path: full path
    - department: document department
    - collection: folder/collection name
    - chunk_preview: first 150 chars of chunk
    - confidence: 0.0-1.0 confidence score
    - version: document version if available
    - is_authoritative: conflict resolution flag
    """

    citations = []

    for i, result in enumerate(results):

        metadata = result.get("metadata", {})

        # Parse tags if stored as JSON string
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            try:
                tags = json.loads(tags)
            except (json.JSONDecodeError, TypeError):
                tags = []

        citation = {
            "index": i + 1,
            "source": metadata.get(
                "file_name", "Unknown"
            ),
            "file_path": metadata.get(
                "file_path", ""
            ),
            "department": metadata.get(
                "department", "General"
            ),
            "collection": metadata.get(
                "collection", ""
            ),
            "document_type": metadata.get(
                "document_type", ""
            ),
            "topic": metadata.get("topic", ""),
            "chunk_preview": result.get(
                "document", ""
            )[:200],
            "confidence": compute_confidence(result),
            "version": metadata.get("version"),
            "status": metadata.get("status", "Active"),
            "is_authoritative": result.get(
                "is_authoritative", True
            ),
        }

        citations.append(citation)

    return citations


def format_citations_for_prompt(citations):
    """
    Format citations as text for inclusion in
    the Gemini prompt. This helps the model
    reference specific sources.
    """

    lines = []

    for c in citations:
        auth = " [AUTHORITATIVE]" if c[
            "is_authoritative"
        ] else ""

        lines.append(
            f"[Source {c['index']}] "
            f"{c['source']} "
            f"(Dept: {c['department']}, "
            f"Confidence: {c['confidence']:.0%})"
            f"{auth}"
        )

    return "\n".join(lines)
