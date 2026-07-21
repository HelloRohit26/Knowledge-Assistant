"""
Document API Routes

GET    /api/documents          — List all documents
GET    /api/documents/{path}   — Get document details
DELETE /api/documents/{path}   — Delete a document
POST   /api/documents/upload   — Upload a document
PUT    /api/documents/{path}/metadata — Update metadata
"""

import os
import shutil
from fastapi import (
    APIRouter, HTTPException,
    UploadFile, File, Form
)

from app.database.document_registry import (
    get_all_documents,
    get_document,
    delete_document,
    update_metadata
)
from app.services.vector_store import (
    delete_by_file_path
)
from app.services.incremental_indexer import (
    run_incremental_indexing
)
from app.core.config import settings
from app.schemas.document_schemas import (
    DocumentListResponse,
    DocumentListItem,
    DocumentDetailResponse,
    DocumentUploadResponse
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


@router.get(
    "",
    response_model=DocumentListResponse
)
def list_documents(
    collection: str = None,
    status: str = None
):
    docs = get_all_documents()

    if collection:
        docs = [
            d for d in docs
            if d["collection"] == collection
        ]

    if status:
        docs = [
            d for d in docs
            if d["vector_status"] == status
        ]

    items = [
        DocumentListItem(
            file_path=d["file_path"],
            file_name=d["file_name"],
            collection=d["collection"],
            vector_status=d["vector_status"],
            version=d["version"],
            metadata=d.get("metadata")
        )
        for d in docs
    ]

    return DocumentListResponse(
        total=len(items),
        documents=items
    )


@router.get("/detail")
def get_document_detail(file_path: str):

    doc = get_document(file_path)

    if doc is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return doc


@router.delete("/remove")
def remove_document(file_path: str):

    doc = get_document(file_path)

    if doc is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete vectors from ChromaDB
    deleted_vectors = delete_by_file_path(file_path)

    # Delete from registry
    delete_document(file_path)

    return {
        "message": "Document deleted",
        "file_path": file_path,
        "vectors_removed": deleted_vectors
    }


@router.post(
    "/upload",
    response_model=DocumentUploadResponse
)
async def upload_document(
    file: UploadFile = File(...),
    collection: str = Form(default="general")
):
    """Upload a file to the data folder."""

    # Validate extension
    allowed = {
        ".pdf", ".docx", ".txt",
        ".json", ".csv", ".xlsx"
    }

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    # Save to data folder
    target_dir = os.path.join(
        settings.DATA_FOLDER, collection
    )

    os.makedirs(target_dir, exist_ok=True)

    target_path = os.path.join(
        target_dir, file.filename
    )

    with open(target_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Trigger indexing
    run_incremental_indexing()

    return DocumentUploadResponse(
        message="File uploaded and indexing triggered",
        file_path=target_path,
        file_name=file.filename,
        status="indexing"
    )


@router.put("/metadata")
def update_doc_metadata(
    file_path: str,
    metadata: dict
):
    doc = get_document(file_path)

    if doc is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    update_metadata(file_path, metadata)

    return {
        "message": "Metadata updated",
        "file_path": file_path
    }
