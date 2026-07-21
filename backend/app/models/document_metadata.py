from pydantic import BaseModel
from typing import List, Optional


class DocumentMetadata(BaseModel):

    department: Optional[str] = None

    document_type: Optional[str] = None

    document_category: Optional[str] = None

    topic: Optional[str] = None

    status: Optional[str] = None

    version: Optional[str] = None

    effective_date: Optional[str] = None

    author: Optional[str] = None

    tags: List[str] = []

    summary: Optional[str] = None

    authority_score: int = 50

    is_policy: bool = False

    is_official: bool = False

    source_type: Optional[str] = None