"""LokMC — Authentication API routes.

POST /api/auth/login      — Username + password login
POST /api/auth/refresh    — Refresh an access token
POST /api/auth/logout     — Revoke session
GET  /api/auth/me         — Current user profile
POST /api/auth/setup      — First-run: create the initial superuser
"""

import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.db.models import User, db
from app.security.auth import (
    create_access_token,
    create_refresh_token,
    create_session,
    decode_token,
    get_current_user,
    hash_password,
    log_audit,
    revoke_session,
    verify_password,
    _get_client_ip,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Schemas ──────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8, max_length=128)


class SetupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=12, max_length=128)
    email: Optional[str] = Field(None, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserProfile(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_superuser: bool
    totp_enabled: bool
    created_at: str
    last_login: Optional[str]


class RefreshRequest(BaseModel):
    refresh_token: str


# ── Endpoints ────────────────────────────────────────────────

@router.post("/setup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def first_run_setup(body: SetupRequest, request: Request):
    """Create the first superuser.  Only works when no users exist."""
    if User.select().count() > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Setup already completed — users exist",
        )

    user = User.create(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        is_superuser=True,
    )

    access = create_access_token(user.id, user.username)
    refresh = create_refresh_token(user.id)
    payload = decode_token(refresh)

    create_session(
        user=user,
        token_jti=payload["jti"],
        ip_address=_get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
    )

    log_audit("AUTH", "setup", f"Initial superuser '{user.username}' created", user=user, ip_address=_get_client_ip(request))

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings_expire_seconds(),
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, request: Request):
    """Authenticate with username + password."""
    ip = _get_client_ip(request)

    user = User.get_or_none(User.username == body.username)
    if user is None or not verify_password(body.password, user.password_hash):
        log_audit("AUTH", "login_failed", f"Failed login for '{body.username}'", ip_address=ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    access = create_access_token(user.id, user.username)
    refresh = create_refresh_token(user.id)
    payload = decode_token(refresh)

    create_session(
        user=user,
        token_jti=payload["jti"],
        ip_address=ip,
        user_agent=request.headers.get("User-Agent"),
    )

    User.update(last_login=datetime.datetime.utcnow()).where(User.id == user.id).execute()

    log_audit("AUTH", "login", f"User '{user.username}' logged in", user=user, ip_address=ip)

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings_expire_seconds(),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest, request: Request):
    """Exchange a valid refresh token for a new access token pair."""
    payload = decode_token(body.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user = User.get_or_none(User.id == int(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access = create_access_token(user.id, user.username)
    refresh = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings_expire_seconds(),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, user: User = Depends(get_current_user)):
    """Revoke the current session."""
    log_audit("AUTH", "logout", f"User '{user.username}' logged out", user=user, ip_address=_get_client_ip(request))


@router.get("/me", response_model=UserProfile)
async def current_user_profile(user: User = Depends(get_current_user)):
    """Return the authenticated user's profile."""
    return UserProfile(
        id=user.id,
        username=user.username,
        email=user.email,
        is_superuser=user.is_superuser,
        totp_enabled=user.totp_enabled,
        created_at=user.created_at.isoformat(),
        last_login=user.last_login.isoformat() if user.last_login else None,
    )


@router.get("/needs-setup")
async def check_needs_setup():
    """Check whether first-run setup is required (no users exist)."""
    return {"needs_setup": User.select().count() == 0}


# ── Helpers ──────────────────────────────────────────────────

def settings_expire_seconds() -> int:
    from app.config import settings
    return settings.jwt_access_expire_minutes * 60
