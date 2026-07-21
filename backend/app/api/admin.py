"""
Admin API Routes

Admin management endpoints: list users, update status, delete users.
Protected by RBAC (require_role("admin")).
"""

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_role
from app.database.user_db import (
    get_all_users,
    delete_user,
    update_user_status
)
from app.schemas.auth_schemas import UserResponse
from typing import List

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Management"],
    dependencies=[Depends(require_role("admin"))]
)


@router.get("/users", response_model=List[UserResponse])
def list_users():
    """List all registered users (Admin only)."""

    users = get_all_users()

    return [
        UserResponse(
            id=u["id"],
            username=u["username"],
            email=u["email"],
            role=u["role"],
            department=u.get("department"),
            is_active=u["is_active"],
            created_at=u.get("created_at")
        )
        for u in users
    ]


@router.put("/users/{user_id}/status")
def toggle_user_active(user_id: int, is_active: bool):
    """Enable or disable a user account."""

    update_user_status(user_id, is_active)

    return {
        "message": f"User status updated to {'active' if is_active else 'inactive'}",
        "user_id": user_id
    }


@router.delete("/users/{user_id}")
def remove_user(user_id: int):
    """Delete a user account."""

    delete_user(user_id)

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }
