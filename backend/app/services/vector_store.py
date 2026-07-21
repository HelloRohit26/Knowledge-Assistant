import json
import chromadb

from app.core.config import settings


client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="knowledge_base"
)


def sanitize_metadata(metadata: dict):

    cleaned = {}

    for key, value in metadata.items():

        if value is None:
            continue

        if isinstance(value, (str, int, float, bool)):
            cleaned[key] = value

        elif isinstance(value, (list, dict)):
            cleaned[key] = json.dumps(value)

        else:
            cleaned[key] = str(value)

    return cleaned


def add_document(doc_id, text, embedding, metadata):

    metadata = sanitize_metadata(metadata)

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search_documents(query_embedding, top_k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    return results


def search_with_filters(
    query_embedding,
    filters=None,
    top_k=10
):
    """
    Search with optional ChromaDB metadata filters.

    filters: dict compatible with ChromaDB where clause
    e.g. {"department": "HR"}
    e.g. {"$and": [{"department": "HR"}, {"status": "Active"}]}
    """

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if filters:
        query_params["where"] = filters

    try:
        results = collection.query(**query_params)
    except Exception:
        # Fall back to unfiltered if filter fails
        query_params.pop("where", None)
        results = collection.query(**query_params)

    return results


def get_all_documents_with_metadata():
    """Get all stored documents with metadata.
    Used by BM25 engine to build index."""

    results = collection.get(
        include=["documents", "metadatas"]
    )

    return results


def get_collection_count():

    return collection.count()


def get_sample():

    results = collection.get(
        limit=1,
        include=["metadatas", "documents"]
    )

    return results


def get_last_records():

    results = collection.get(
        include=["metadatas", "documents"]
    )

    return {
        "total_records": len(results["ids"]),
        "last_5_ids": results["ids"][-5:],
        "last_5_metadata": results["metadatas"][-5:]
    }


def get_latest_metadata():

    results = collection.get(
        include=["metadatas"]
    )

    if not results["metadatas"]:
        return {}

    return results["metadatas"][-1]


def delete_by_file_path(file_path):

    results = collection.get(
        include=["metadatas"]
    )

    found_ids = []

    for doc_id, metadata in zip(
        results["ids"],
        results["metadatas"]
    ):
        if metadata.get("file_path") == file_path:
            found_ids.append(doc_id)

    if found_ids:
        collection.delete(ids=found_ids)

    return len(found_ids)