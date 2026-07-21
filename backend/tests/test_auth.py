"""
Tests for Auth & JWT Security (Phase 9)
"""

from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.database.user_db import (
    create_user,
    get_user_by_username,
    get_all_users,
    delete_user
)


def test_password_hashing():
    raw_pass = "secret123"
    hashed = hash_password(raw_pass)

    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_jwt_tokens():
    payload = {"sub": "testuser", "role": "admin"}
    token = create_access_token(payload)

    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert decoded["type"] == "access"


def test_user_db_crud():
    hashed = hash_password("pass123")
    user_id = create_user(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed,
        role="user",
        department="HR"
    )

    assert user_id > 0

    user = get_user_by_username("testuser")
    assert user is not None
    assert user["email"] == "test@example.com"
    assert user["role"] == "user"

    all_users = get_all_users()
    assert len(all_users) >= 1

    delete_user(user_id)
    assert get_user_by_username("testuser") is None
