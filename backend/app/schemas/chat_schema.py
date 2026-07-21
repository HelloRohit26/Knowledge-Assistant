from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str
    mode: str = "standard"  # standard | agent


class Citation(BaseModel):
    index: int
    source: str
    file_path: str = ""
    department: str = "General"
    collection: str = ""
    document_type: str = ""
    topic: str = ""
    chunk_preview: str = ""
    confidence: float = 0.0
    version: Optional[str] = None
    status: str = "Active"
    is_authoritative: bool = True


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    citations: List[Citation] = []
    query_analysis: dict = {}
    sub_queries: List[str] = []
    is_multi_step: bool = False