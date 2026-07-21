from pydantic import BaseModel
from typing import List, Optional, Dict


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[Dict] = None


class SearchResult(BaseModel):
    document: str
    metadata: dict = {}
    confidence: float = 0.0
    is_authoritative: bool = True
    composite_score: float = 0.0


class SearchResponse(BaseModel):
    results: List[SearchResult] = []
    query_analysis: dict = {}
    filters_applied: Optional[dict] = None
    total_candidates: int = 0


class DocumentUploadResponse(BaseModel):
    message: str
    file_path: str
    file_name: str
    status: str = "uploaded"


class DocumentListItem(BaseModel):
    file_path: str
    file_name: str
    collection: str
    vector_status: str
    version: int = 1
    metadata: Optional[dict] = None


class DocumentListResponse(BaseModel):
    total: int
    documents: List[DocumentListItem] = []


class DocumentDetailResponse(BaseModel):
    file_path: str
    file_name: str
    collection: str
    checksum: str
    file_size: int = 0
    metadata: Optional[dict] = None
    vector_status: str = "pending"
    version: int = 1
    indexed_at: Optional[str] = None
    created_at: Optional[str] = None


class RegistryStatsResponse(BaseModel):
    total_documents: int = 0
    by_status: dict = {}
    by_collection: dict = {}


class AnalyticsResponse(BaseModel):
    total_documents: int = 0
    by_department: dict = {}
    by_type: dict = {}
    by_status: dict = {}
    by_collection: dict = {}
