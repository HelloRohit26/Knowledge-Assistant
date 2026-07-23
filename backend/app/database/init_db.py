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

    # ── Workflow History: Stores completed or running AI workflow executions ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_history (

        run_id          TEXT PRIMARY KEY,
        workflow_id     TEXT NOT NULL,
        title           TEXT NOT NULL,
        category        TEXT NOT NULL,
        status          TEXT NOT NULL DEFAULT 'completed',
        inputs_json     TEXT,
        steps_json      TEXT,
        result_json     TEXT,
        execution_time_ms REAL DEFAULT 0,
        user_id         INTEGER,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Workflow Templates: Standard and custom workflows ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_templates (

        id              TEXT PRIMARY KEY,
        title           TEXT NOT NULL,
        description     TEXT NOT NULL,
        category        TEXT NOT NULL,
        icon            TEXT NOT NULL DEFAULT 'Zap',
        steps_json      TEXT NOT NULL,
        inputs_schema_json TEXT,
        is_custom       INTEGER NOT NULL DEFAULT 0,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Phase 1: AI Agent Memory ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_memory (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         TEXT NOT NULL DEFAULT 'default_user',
        session_id      TEXT NOT NULL,
        memory_type     TEXT NOT NULL, -- 'chat_turn', 'user_pref', 'workflow_mem', 'doc_context'
        key             TEXT NOT NULL,
        value_json      TEXT NOT NULL,
        updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Phase 4: Knowledge Graph Edges ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_graph_edges (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id       TEXT NOT NULL,
        source_name     TEXT NOT NULL,
        target_id       TEXT NOT NULL,
        target_name     TEXT NOT NULL,
        relationship    TEXT NOT NULL,
        weight          REAL DEFAULT 1.0,
        metadata_json   TEXT,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Phase 6: Collaboration Comments & Audit Trail ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_comments (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path       TEXT NOT NULL,
        user_name       TEXT NOT NULL,
        comment_text    TEXT NOT NULL,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (

        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name       TEXT NOT NULL,
        action          TEXT NOT NULL,
        resource        TEXT NOT NULL,
        details_json    TEXT,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Phase 9: Automation Rules Engine ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS automation_rules (

        id              TEXT PRIMARY KEY,
        name            TEXT NOT NULL,
        event_trigger   TEXT NOT NULL,
        condition_json  TEXT,
        action_json     TEXT NOT NULL,
        is_active       INTEGER DEFAULT 1,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── Phase 10: SaaS Multi-Tenancy & API Keys ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (

        id              TEXT PRIMARY KEY,
        name            TEXT NOT NULL,
        tier            TEXT NOT NULL DEFAULT 'enterprise',
        max_documents   INTEGER DEFAULT 1000,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (

        key_id          TEXT PRIMARY KEY,
        api_key         TEXT UNIQUE NOT NULL,
        name            TEXT NOT NULL,
        org_id          TEXT NOT NULL DEFAULT 'default_org',
        role            TEXT NOT NULL DEFAULT 'admin',
        is_active       INTEGER DEFAULT 1,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()