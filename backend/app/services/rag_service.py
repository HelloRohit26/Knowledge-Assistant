"""
RAG Service

Full retrieval-augmented generation pipeline:
1. Search → Hybrid + Reranked results
2. Conflict Resolution
3. Citation Generation
4. Gemini Answer Generation with source references
"""

from google import genai
from google.genai import types

from app.core.config import settings
from app.services.search_service import (
    search_knowledge_base,
    simple_search
)
from app.services.conflict_resolver import (
    resolve_conflicts
)
from app.services.citation_engine import (
    generate_citations,
    format_citations_for_prompt
)


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def ask_knowledge_base(question, top_k=5):
    """
    Full enterprise RAG pipeline with citations.
    """

    # Step 1: Enterprise search
    search_results = search_knowledge_base(
        question, top_k=top_k
    )

    results = search_results["results"]

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": [],
            "citations": [],
            "query_analysis": search_results.get(
                "query_analysis", {}
            )
        }

    # Step 2: Conflict resolution
    results = resolve_conflicts(results)

    # Step 3: Generate citations
    citations = generate_citations(results)

    # Step 4: Build context
    context_parts = []
    for i, result in enumerate(results):
        source = result.get("metadata", {}).get(
            "file_name", "Unknown"
        )
        auth_tag = ""
        if result.get("is_authoritative"):
            auth_tag = " [AUTHORITATIVE]"

        context_parts.append(
            f"[Source {i+1}: {source}{auth_tag}]\n"
            f"{result['document']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    citation_text = format_citations_for_prompt(
        citations
    )

    # Step 5: Generate answer with Gemini
    prompt = f"""
You are an enterprise knowledge assistant.

Use the context below to answer the question.
Reference sources using [Source N] format.

If documents conflict, prefer the one marked
[AUTHORITATIVE] (latest official version).

If the context doesn't contain enough information,
say so clearly.

Sources Available:
{citation_text}

Context:
{context}

Question: {question}

Provide a clear, well-structured answer with
source references.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

    # Extract unique source file names
    sources = list(set(
        c["source"]
        for c in citations
        if c["source"] != "Unknown"
    ))

    return {
        "answer": response.text,
        "sources": sources,
        "citations": citations,
        "query_analysis": search_results.get(
            "query_analysis", {}
        )
    }


def ask_simple(question):
    """
    Quick RAG without full pipeline.
    Uses simple vector search only.
    """

    results = simple_search(question, top_k=3)

    if not results["documents"][0]:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }

    context = "\n\n".join(
        results["documents"][0]
    )

    sources = list(set(
        m.get("file_name", "Unknown")
        for m in results["metadatas"][0]
        if "file_name" in m
    ))

    prompt = f"""
You are a helpful company knowledge assistant.

Use the context below to answer the question.

Context:
{context}

Question: {question}

Provide a clear answer.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

    return {
        "answer": response.text,
        "sources": sources
    }