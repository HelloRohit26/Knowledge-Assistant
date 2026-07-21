import json
from datetime import datetime

from app.database.db import get_connection


# ── Save / Insert ──

def save_document(
    file_path,
    file_name,
    collection,
    checksum,
    file_size,
    last_modified,
    metadata_dict=None,
    vector_status="pending"
):
    conn = get_connection()
    cursor = conn.cursor()

    metadata_json = (
        json.dumps(metadata_dict)
        if metadata_dict else None
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO document_registry
        (
            file_path, file_name, collection,
            checksum, file_size, metadata_json,
            vector_status, last_modified,
            indexed_at, metadata_updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            file_path, file_name, collection,
            checksum, file_size, metadata_json,
            vector_status, last_modified,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
            if metadata_dict else None
        )
    )

    conn.commit()
    conn.close()


# ── Get single document ──

def get_document(file_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            file_path, file_name, collection,
            checksum, file_size, metadata_json,
            vector_status, version, last_modified,
            indexed_at, metadata_updated_at, created_at
        FROM document_registry
        WHERE file_path = ?
        """,
        (file_path,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "file_path": row[0],
        "file_name": row[1],
        "collection": row[2],
        "checksum": row[3],
        "file_size": row[4],
        "metadata": (
            json.loads(row[5])
            if row[5] else None
        ),
        "vector_status": row[6],
        "version": row[7],
        "last_modified": row[8],
        "indexed_at": row[9],
        "metadata_updated_at": row[10],
        "created_at": row[11]
    }


# ── Get all documents ──

def get_all_documents():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            file_path, file_name, collection,
            checksum, vector_status, version,
            metadata_json
        FROM document_registry
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    documents = []
    for row in rows:
        documents.append({
            "file_path": row[0],
            "file_name": row[1],
            "collection": row[2],
            "checksum": row[3],
            "vector_status": row[4],
            "version": row[5],
            "metadata": (
                json.loads(row[6])
                if row[6] else None
            )
        })

    return documents


# ── Get documents by status ──

def get_documents_by_status(status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_path, file_name, collection,
               vector_status, version
        FROM document_registry
        WHERE vector_status = ?
        """,
        (status,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "file_path": row[0],
            "file_name": row[1],
            "collection": row[2],
            "vector_status": row[3],
            "version": row[4]
        }
        for row in rows
    ]


# ── Update metadata ──

def update_metadata(file_path, metadata_dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE document_registry
        SET
            metadata_json = ?,
            metadata_updated_at = ?
        WHERE file_path = ?
        """,
        (
            json.dumps(metadata_dict),
            datetime.utcnow().isoformat(),
            file_path
        )
    )

    conn.commit()
    conn.close()


# ── Update vector status ──

def update_vector_status(file_path, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE document_registry
        SET vector_status = ?
        WHERE file_path = ?
        """,
        (status, file_path)
    )

    conn.commit()
    conn.close()


# ── Mark dirty (needs re-index) ──

def mark_dirty(file_path):

    update_vector_status(file_path, "dirty")


# ── Increment version ──

def increment_version(file_path, new_checksum, last_modified):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE document_registry
        SET
            version = version + 1,
            checksum = ?,
            last_modified = ?,
            vector_status = 'dirty'
        WHERE file_path = ?
        """,
        (new_checksum, last_modified, file_path)
    )

    conn.commit()
    conn.close()


# ── Delete document ──

def delete_document(file_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM document_registry
        WHERE file_path = ?
        """,
        (file_path,)
    )

    conn.commit()
    conn.close()


# ── Load metadata (backwards compat) ──

def load_metadata(file_path):

    doc = get_document(file_path)

    if doc is None:
        return None

    return doc["metadata"]


# ── Save metadata (backwards compat) ──

def save_metadata(file_path, metadata_dict):

    update_metadata(file_path, metadata_dict)


# ── Registry stats ──

def get_registry_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM document_registry"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT vector_status, COUNT(*)
        FROM document_registry
        GROUP BY vector_status
        """
    )
    status_counts = dict(cursor.fetchall())

    cursor.execute(
        """
        SELECT collection, COUNT(*)
        FROM document_registry
        GROUP BY collection
        """
    )
    collection_counts = dict(cursor.fetchall())

    conn.close()

    return {
        "total_documents": total,
        "by_status": status_counts,
        "by_collection": collection_counts
    }
