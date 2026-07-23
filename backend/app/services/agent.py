"""
Agentic Retrieval (Rule-Based)

Multi-step reasoning agent that:
1. Decomposes complex queries into sub-queries
2. Runs each sub-query through the search pipeline
3. Synthesizes results across sub-queries
4. Generates a comprehensive answer

Uses rule-based decomposition (no extra Gemini calls
for planning). Gemini is only used for final synthesis.
"""

import re
from google import genai
from google.genai import types

from app.core.config import settings
from app.services.agent_tools import (
    tool_search,
    tool_get_registry_stats,
    tool_list_departments
)
from app.services.citation_engine import (
    generate_citations,
    format_citations_for_prompt
)
from app.services.conflict_resolver import (
    resolve_conflicts
)


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# ── Rule-based query decomposition ──

COMPOUND_PATTERNS = [
    # "X and Y" → split
    r'(.+?)\s+and\s+(.+)',
    # "X vs Y" / "X versus Y" → compare
    r'(.+?)\s+(?:vs\.?|versus)\s+(.+)',
    # "compare X with Y"
    r'compare\s+(.+?)\s+(?:with|and|to)\s+(.+)',
    # "difference between X and Y"
    r'difference\s+between\s+(.+?)\s+and\s+(.+)',
]

MULTI_TOPIC_KEYWORDS = [
    "compare", "difference", "both",
    "all departments", "across", "overview",
    "summary of all", "everything about"
]


def needs_decomposition(query):
    """Check if query needs multi-step reasoning."""

    query_lower = query.lower()

    # Check for multi-topic keywords
    for keyword in MULTI_TOPIC_KEYWORDS:
        if keyword in query_lower:
            return True

    # Check for compound patterns
    for pattern in COMPOUND_PATTERNS:
        if re.search(pattern, query_lower):
            return True

    # Long queries likely need decomposition
    if len(query.split()) > 15:
        return True

    return False


def decompose_query(query):
    """
    Split complex query into sub-queries.
    Rule-based: no Gemini call needed.
    """

    query_lower = query.lower()
    sub_queries = []

    # Try compound patterns
    for pattern in COMPOUND_PATTERNS:
        match = re.search(pattern, query_lower)
        if match:
            parts = match.groups()
            for part in parts:
                cleaned = part.strip()
                if len(cleaned) > 3:
                    sub_queries.append(cleaned)
            break

    # "across departments" → search each dept
    if "across" in query_lower and (
        "department" in query_lower
    ):
        departments = tool_list_departments()
        base_topic = re.sub(
            r'across\s+(?:all\s+)?departments?',
            '', query_lower
        ).strip()

        for dept in departments[:5]:
            sub_queries.append(
                f"{base_topic} {dept}"
            )

    # Fallback: use original query
    if not sub_queries:
        sub_queries = [query]

    return sub_queries


def run_agent(question, top_k=5):
    """
    Agentic retrieval pipeline:
    1. Check if decomposition needed
    2. Decompose into sub-queries
    3. Search each sub-query
    4. Merge and deduplicate results
    5. Resolve conflicts
    6. Generate citations
    7. Synthesize comprehensive answer
    """

    # Step 1-2: Decompose
    if needs_decomposition(question):
        sub_queries = decompose_query(question)
        is_multi_step = True
    else:
        sub_queries = [question]
        is_multi_step = False

    # Step 3: Search each sub-query
    all_results = []
    all_query_analyses = []

    for sq in sub_queries:
        search_output = tool_search(sq, top_k=3)
        all_results.extend(
            search_output["results"]
        )
        all_query_analyses.append(
            search_output.get("query_analysis", {})
        )

    # Step 4: Deduplicate by document id
    seen_ids = set()
    unique_results = []

    for result in all_results:
        doc_id = result.get("id", id(result))
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            unique_results.append(result)

    # Step 5: Conflict resolution
    resolved = resolve_conflicts(unique_results)

    # Step 6: Citations
    citations = generate_citations(
        resolved[:top_k]
    )

    citation_text = format_citations_for_prompt(
        citations
    )

    # Step 7: Build context from all results
    context_parts = []
    for i, result in enumerate(resolved[:top_k]):
        source = result.get("metadata", {}).get(
            "file_name", "Unknown"
        )
        context_parts.append(
            f"[Source {i+1}: {source}]\n"
            f"{result['document']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Synthesis prompt
    sub_query_text = ""
    if is_multi_step:
        sub_query_text = (
            "\n\nThis question was broken into "
            "sub-queries:\n"
            + "\n".join(
                f"- {sq}" for sq in sub_queries
            )
        )

    prompt = f"""
You are an enterprise knowledge assistant with
multi-document reasoning capabilities.

{sub_query_text}

Sources Available:
{citation_text}

Context from multiple documents:
{context}

Question: {question}

Provide a comprehensive answer that:
1. Synthesizes information across all sources
2. References sources using [Source N] format
3. Highlights any conflicts (prefer [AUTHORITATIVE])
4. Clearly states if information is incomplete
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

    sources = list(set(
        c["source"]
        for c in citations
        if c["source"] != "Unknown"
    ))

    return {
        "answer": response.text,
        "sources": sources,
        "citations": citations,
        "sub_queries": sub_queries,
        "is_multi_step": is_multi_step,
        "query_analyses": all_query_analyses
    }
