from app.database.db import get_connection


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ── Document Registry: Single source of truth for every document ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_registry (

        file_path       TEXT PRIMARY KEY,
        file_name       TEXT NOT NULL,
        collection      TEXT NOT NULL,

        checksum        TEXT NOT NULL,
        file_size       INTEGER DEFAULT 0,

        metadata_json   TEXT,

        vector_status   TEXT NOT NULL DEFAULT 'pending',
        version         INTEGER NOT NULL DEFAULT 1,

        last_modified   REAL NOT NULL,
        indexed_at      TIMESTAMP,
        metadata_updated_at TIMESTAMP,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Users table for auth ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        username        TEXT UNIQUE NOT NULL,
        email           TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        role            TEXT NOT NULL DEFAULT 'user',
        department      TEXT,
        is_active       INTEGER NOT NULL DEFAULT 1,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Search logs for analytics ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_logs (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        query           TEXT NOT NULL,
        filters_json    TEXT,
        result_count    INTEGER DEFAULT 0,
        latency_ms      REAL DEFAULT 0,
        user_id         INTEGER,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Indexing logs for analytics ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indexing_logs (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path       TEXT NOT NULL,
        action          TEXT NOT NULL,
        duration_ms     REAL DEFAULT 0,
        status          TEXT NOT NULL DEFAULT 'success',
        error_message   TEXT,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Error logs ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS error_logs (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type      TEXT NOT NULL,
        message         TEXT NOT NULL,
        traceback       TEXT,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()