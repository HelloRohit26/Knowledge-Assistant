"""
Auth API Routes

POST /api/auth/register — Create account
POST /api/auth/login    — Get JWT tokens
POST /api/auth/refresh  — Refresh access token
GET  /api/auth/me       — Get current user info
"""

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse
)
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)
from app.database.user_db import (
    create_user,
    get_user_by_username,
    get_user_by_email
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=TokenResponse
)
def register(request: RegisterRequest):

    # Check if username exists
    if get_user_by_username(request.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Check if email exists
    if get_user_by_email(request.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create user
    hashed = hash_password(request.password)

    create_user(
        username=request.username,
        email=request.email,
        hashed_password=hashed,
        role=request.role,
        department=request.department
    )

    # Generate tokens
    token_data = {"sub": request.username}

    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        role=request.role,
        username=request.username
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(request: LoginRequest):

    user = get_user_by_username(request.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        request.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=403,
            detail="Account is deactivated"
        )

    token_data = {"sub": user["username"]}

    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        role=user["role"],
        username=user["username"]
    )


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(request: RefreshRequest):

    payload = decode_token(request.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Not a refresh token"
        )

    username = payload.get("sub")
    user = get_user_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    token_data = {"sub": username}

    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        role=user["role"],
        username=username
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(user=Depends(get_current_user)):

    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        department=user.get("department"),
        is_active=user.get("is_active", True)
    )
