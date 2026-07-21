from app.database.document_registry import (
    get_document,
    save_document,
    get_all_documents
)


def is_file_indexed(file_path):
    """Check if file exists in registry."""

    doc = get_document(file_path)

    return doc is not None


def get_file_record(file_path):
    """Get checksum and last_modified for a file.
    Returns (checksum, last_modified) tuple or None.
    """

    doc = get_document(file_path)

    if doc is None:
        return None

    return (doc["checksum"], doc["last_modified"])


def add_indexed_file(
    file_name,
    file_path,
    collection,
    last_modified,
    checksum,
    file_size=0
):
    """Register a newly indexed file."""

    save_document(
        file_path=file_path,
        file_name=file_name,
        collection=collection,
        checksum=checksum,
        file_size=file_size,
        last_modified=last_modified,
        vector_status="indexed"
    )


def get_all_indexed_files():
    """Get all tracked files."""

    docs = get_all_documents()

    return [
        (
            doc["file_name"],
            doc["file_path"],
            doc["collection"],
            doc["vector_status"]
        )
        for doc in docs
    ]


def get_all_tracked_files():
    """Get all file paths."""

    docs = get_all_documents()

    return [doc["file_path"] for doc in docs]


def update_indexed_file(
    file_path,
    last_modified,
    checksum
):
    """Update tracking info after re-indexing."""

    from app.database.document_registry import (
        increment_version,
        update_vector_status
    )

    increment_version(
        file_path, checksum, last_modified
    )

    update_vector_status(file_path, "indexed")