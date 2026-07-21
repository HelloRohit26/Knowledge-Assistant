from app.services.scanner import scan_data_folder
from app.services.document_loader import load_multiple_files
from app.services.chunking import create_chunks
from app.services.embedding_service import get_embedding
from app.services.vector_store import add_document
import uuid

from app.core.config import settings


def run_indexing_pipeline():

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
    

    nodes = create_chunks(
        documents
    )

    inserted = 0

    for index, node in enumerate(nodes):

        embedding = get_embedding(
            node.text
        )

        add_document(
    doc_id=str(uuid.uuid4()),
    text=node.text,
    embedding=embedding,
    metadata=node.metadata
    
)

        inserted += 1

    return {
        "documents": len(documents),
        "nodes": len(nodes),
        "inserted_vectors": inserted
    }