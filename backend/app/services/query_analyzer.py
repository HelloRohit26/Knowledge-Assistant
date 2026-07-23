"""
Query Analyzer

Parses user queries into structured filters using Gemini.
Extracts department, status, document_type, and search text.
"""

from pydantic import BaseModel
from typing import Optional

from google import genai
from google.genai import types

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


class QueryAnalysis(BaseModel):
    """Structured query analysis output."""

    department: Optional[str] = None
    status: Optional[str] = None
    document_type: Optional[str] = None
    topic: Optional[str] = None
    search_text: str = ""
    date_filter: Optional[str] = None


def analyze_query(query: str) -> QueryAnalysis:
    """
    Parse a user query into structured filters.

    Example:
    Input: "Show active HR leave policies"
    Output: QueryAnalysis(
        department="HR",
        status="Active",
        document_type="Policy",
        topic="leave",
        search_text="leave policies"
    )
    """

    prompt = f"""
You are a query analyzer for an enterprise knowledge base.

Parse the user's query and extract structured filters.

Valid departments: HR, Policy, Technical, Sales, Research, General, Finance, Legal, Operations, Marketing
Valid statuses: Active, Draft, Archived, Superseded, Under Review
Valid document types: Policy, SOP, Handbook, Guideline, FAQ, Memo, Report, Checklist, Manual, Specification

If a filter is not mentioned, leave it as null.
The search_text should contain the core search terms.

Query: {query}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=QueryAnalysis,
        )
    )

    analysis = response.parsed

    # Ensure search_text is never empty
    if not analysis.search_text:
        analysis.search_text = query

    return analysis


def build_chroma_filters(analysis: QueryAnalysis):
    """
    Convert QueryAnalysis into ChromaDB where clause.
    Returns dict for ChromaDB metadata filtering.
    """

    conditions = []

    if analysis.department:
        conditions.append({
            "department": analysis.department
        })

    if analysis.status:
        conditions.append({
            "status": analysis.status
        })

    if analysis.document_type:
        conditions.append({
            "document_type": analysis.document_type
        })

    if analysis.topic:
        conditions.append({
            "topic": analysis.topic
        })

    if not conditions:
        return None

    if len(conditions) == 1:
        return conditions[0]

    return {"$and": conditions}
