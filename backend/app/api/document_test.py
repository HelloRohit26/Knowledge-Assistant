from fastapi import APIRouter
from app.services.scanner import scan_data_folder
from app.services.document_loader import load_multiple_files
from app.services.chunking import create_chunks
from app.services.embedding_service import get_embedding
from app.services.vector_store import collection
from app.core.config import settings
from app.services.vector_store import add_document
from app.services.index_pipeline import run_indexing_pipeline
from app.services.search_service import search_knowledge_base
from app.services.vector_store import get_sample
from app.services.vector_store import get_last_records
from app.services.vector_store import search_documents
from app.services.rag_service import ask_knowledge_base

from app.services.rag_service import (
    ask_knowledge_base
)
from app.services.incremental_indexer import (
    run_incremental_indexing
)
from app.services.vector_store import (
    get_latest_metadata
)

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)

from app.services.rag_service import (
    ask_knowledge_base
)

router = APIRouter(
    tags=["Document Test"]
)


@router.get("/load-all-documents")
def load_all_documents():

    files = scan_data_folder(
        settings.DATA_FOLDER
    )

    file_paths = [
        file["file_path"]
        for file in files
    ]

    documents = load_multiple_files(
    files
)
    

    return {
        "files_found": len(file_paths),
        "documents_loaded": len(docs),
        "total_characters": sum(
            len(doc.text)
            for doc in docs
        )
    }

@router.get("/chunk-test")
def chunk_test():

    files = scan_data_folder(
        settings.DATA_FOLDER
    )

    file_paths = [
        file["file_path"]
        for file in files
    ]

    documents = load_multiple_files(
        file_paths
    )

    chunks = create_chunks(
        documents
    )

    return {
        "documents": len(documents),
        "chunks_created": len(chunks),
        "first_chunk_preview": chunks[0].text[:300]
    }


@router.get("/embedding-test")
def embedding_test():

    embedding = get_embedding(
        "Paternity leave is 15 days"
    )

    return {
        "vector_length": len(embedding),
        "first_10_values": embedding[:10]
    }


@router.get("/chroma-test")
def chroma_test():

    return {
        "collection_name": collection.name,
        "count": collection.count()
    }

@router.get("/insert-test")
def insert_test():

    text = "Paternity leave is 15 days"

    embedding = get_embedding(text)

    add_document(
        doc_id="test_1",
        text=text,
        embedding=embedding
    )

    return {
        "status": "success"
    }


@router.get("/index-all")
def index_all():

    result = run_indexing_pipeline()

    return result

@router.get("/search-test")
def search_test():

    results = search_knowledge_base(
        "What is paternity leave?"
    )

    return {
        "results": results["documents"][0]
    }



@router.get("/incremental-index")
def incremental_index():

    return run_incremental_indexing()

@router.get("/metadata-test")
def metadata_test():

    return get_sample()

@router.get("/metadata-debug")
def metadata_debug():
    return get_last_records()

@router.get("/rag-test")
def rag_test():

    return ask_knowledge_base(
        "What is paternity leave?"
    )

@router.get("/metadata-check")
def metadata_check():

    files = scan_data_folder(
        settings.DATA_FOLDER
    )

    documents = load_multiple_files(
        files
    )

    doc = documents[0]

    return {
        "metadata": doc.metadata
    }


@router.get("/node-metadata-test")
def node_metadata_test():

    files = scan_data_folder(
        settings.DATA_FOLDER
    )

    documents = load_multiple_files(
        files
    )

    nodes = create_chunks(
        documents
    )

    return {
        "node_metadata": nodes[0].metadata
    }


@router.get("/latest-metadata")
def latest_metadata():

    return get_latest_metadata()


@router.get("/search-debug")
def search_debug():

    query_embedding = get_embedding(
        "remote work policy"
    )

    results = search_documents(
        query_embedding
    )

    return results

@router.get("/ask")
def ask(question: str):
    return ask_knowledge_base(question)

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    result = ask_knowledge_base(
        request.question
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )