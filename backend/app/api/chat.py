"""
Chat API Routes

POST /api/chat — Standard & Agentic RAG Chat Endpoint
"""

from fastapi import APIRouter

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    Citation
)
from app.services.rag_service import ask_knowledge_base
from app.services.agent import run_agent

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    RAG Chat endpoint. Supports both 'standard' RAG
    and 'agent' multi-step retrieval mode.
    """

    if request.mode == "agent":

        result = run_agent(request.question)

        citations = [
            Citation(**c) for c in result.get("citations", [])
        ]

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            citations=citations,
            query_analysis={},
            sub_queries=result.get("sub_queries", []),
            is_multi_step=result.get("is_multi_step", False)
        )

    else:

        result = ask_knowledge_base(request.question)

        citations = [
            Citation(**c) for c in result.get("citations", [])
        ]

        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            citations=citations,
            query_analysis=result.get("query_analysis", {}),
            sub_queries=[],
            is_multi_step=False
        )
