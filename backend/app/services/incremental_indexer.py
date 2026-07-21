import os
import uuid
import time

from app.services.scanner import scan_data_folder
from app.services.document_loader import load_multiple_files
from app.services.chunking import create_chunks
from app.services.embedding_service import get_embedding
from app.services.metadata_extractor import extract_metadata

from app.database.document_registry import (
    get_document,
    save_document,
    update_metadata,
    update_vector_status,
    increment_version,
    load_metadata
)

from app.services.vector_store import (
    add_document,
    delete_by_file_path
)

from app.core.config import settings


def run_incremental_indexing():

    files = scan_data_folder(
        settings.DATA_FOLDER
    )

    new_files = []
    modified_files = []

    for file in files:

        doc = get_document(
            file["file_path"]
        )

        if doc is None:
            new_files.append(file)
            continue

        old_checksum = doc["checksum"]

        if old_checksum != file["checksum"]:

            # File modified → delete old vectors
            delete_by_file_path(
                file["file_path"]
            )

            # Increment version, mark dirty
            increment_version(
                file["file_path"],
                file["checksum"],
                file["last_modified"]
            )

            modified_files.append(file)

    files_to_process = (
        new_files + modified_files
    )

    if not files_to_process:

        return {
            "new_files": 0,
            "modified_files": 0,
            "vectors_inserted": 0
        }

    documents = load_multiple_files(
        files_to_process
    )

    # ── Metadata extraction ──

    for doc in documents:

        file_path = doc.metadata["file_path"]

        cached_metadata = load_metadata(file_path)

        if cached_metadata is None:

            metadata = extract_metadata(doc.text)
            metadata_dict = metadata.model_dump()

            # For new files: save full registry entry
            file_info = next(
                f for f in files_to_process
                if f["file_path"] == file_path
            )

            save_document(
                file_path=file_path,
                file_name=file_info["file_name"],
                collection=file_info["collection"],
                checksum=file_info["checksum"],
                file_size=os.path.getsize(file_path)
                if os.path.exists(file_path) else 0,
                last_modified=file_info["last_modified"],
                metadata_dict=metadata_dict,
                vector_status="pending"
            )

        else:

            # Modified files: re-extract if needed
            is_modified = any(
                f["file_path"] == file_path
                for f in modified_files
            )

            if is_modified:
                metadata = extract_metadata(doc.text)
                metadata_dict = metadata.model_dump()
                update_metadata(
                    file_path, metadata_dict
                )
            else:
                metadata_dict = cached_metadata

        doc.metadata.update(metadata_dict)

    # ── Chunking & Embedding ──

    nodes = create_chunks(documents)

    inserted = 0

    for node in nodes:

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

    # ── Update vector status to indexed ──

    for file in files_to_process:

        update_vector_status(
            file["file_path"], "indexed"
        )

    return {
        "new_files": len(new_files),
        "modified_files": len(modified_files),
        "vectors_inserted": inserted
    }