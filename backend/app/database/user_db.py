"""
User Database Operations

CRUD for users table.
"""

from app.database.db import get_connection


def create_user(
    username, email,
    hashed_password, role="user",
    department=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (username, email, hashed_password,
         role, department)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username, email,
            hashed_password, role,
            department
        )
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return user_id


def get_user_by_username(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email,
               hashed_password, role,
               department, is_active
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "hashed_password": row[3],
        "role": row[4],
        "department": row[5],
        "is_active": bool(row[6])
    }


def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email,
               hashed_password, role,
               department, is_active
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "hashed_password": row[3],
        "role": row[4],
        "department": row[5],
        "is_active": bool(row[6])
    }


def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email,
               role, department, is_active,
               created_at
        FROM users
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "role": row[3],
            "department": row[4],
            "is_active": bool(row[5]),
            "created_at": row[6]
        }
        for row in rows
    ]


def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def update_user_status(user_id, is_active):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = ?
        WHERE id = ?
        """,
        (int(is_active), user_id)
    )

    conn.commit()
    conn.close()


def seed_admin_user(hashed_password):
    """Create default admin user if not exists."""

    existing = get_user_by_username("admin")

    if existing is None:
        create_user(
            username="admin",
            email="admin@knowledge.local",
            hashed_password=hashed_password,
            role="admin",
            department=None
        )
        return True

    return False
