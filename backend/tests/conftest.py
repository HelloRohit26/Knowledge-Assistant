"""
Pytest Fixtures for Unit and Integration Tests

Provides in-memory SQLite database, mock Gemini clients,
and FastAPI TestClient.
"""

import pytest
import sqlite3
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.database.init_db import initialize_database
from app.main import app


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Use temporary database for each test to keep tests isolated."""
    db_file = tmp_path / "test_tracking.db"

    def get_test_conn():
        return sqlite3.connect(str(db_file))

    monkeypatch.setattr("app.database.db.get_connection", get_test_conn)

    # Initialize DB schema
    initialize_database()

    yield


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_metadata():
    """Sample valid document metadata."""
    return {
        "department": "HR",
        "document_type": "Policy",
        "document_category": "Policy",
        "topic": "Leave Policy",
        "status": "Active",
        "version": "v1.0",
        "effective_date": "2026-01-01",
        "author": "HR Team",
        "tags": ["leave", "hr", "paid leave"],
        "summary": "Employee leave policy guidelines.",
        "authority_score": 100,
        "is_policy": True,
        "is_official": True,
        "source_type": "Official Policy"
    }
