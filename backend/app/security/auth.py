"""LokMC — Authentication & token management.

Provides:
- Argon2id password hashing / verification
- JWT access + refresh token creation and validation
- Session lifecycle helpers
- Current-user dependency for FastAPI routes
"""

import datetime
import uuid
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings
from app.db.models import AuditLog, Session, User, db

_ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
_bearer = HTTPBearer(auto_error=False)


# ── Password Hashing ────────────────────────────────────────

def hash_password(plain: str) -> str:
    return _ph.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False


# ── JWT Tokens ───────────────────────────────────────────────

def _create_token(data: dict, expires_delta: datetime.timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + expires_delta
    payload["iat"] = datetime.datetime.utcnow()
    payload["jti"] = uuid.uuid4().hex
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int, username: str) -> str:
    return _create_token(
        {"sub": str(user_id), "username": username, "type": "access"},
        datetime.timedelta(minutes=settings.jwt_access_expire_minutes),
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        {"sub": str(user_id), "type": "refresh"},
        datetime.timedelta(days=settings.jwt_refresh_expire_days),
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ── Session Management ──────────────────────────────────────

def create_session(
    user: User,
    token_jti: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Session:
    """Persist a new login session for audit and revocation tracking."""
    return Session.create(
        user=user,
        token_jti=token_jti,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=datetime.datetime.utcnow()
        + datetime.timedelta(days=settings.jwt_refresh_expire_days),
    )


def revoke_session(token_jti: str):
    """Mark a session as revoked (logout)."""
    Session.update(is_revoked=True).where(Session.token_jti == token_jti).execute()


def is_session_valid(token_jti: str) -> bool:
    """Check that a session exists and has not been revoked."""
    session = Session.get_or_none(Session.token_jti == token_jti)
    if session is None or session.is_revoked:
        return False
    if session.expires_at < datetime.datetime.utcnow():
        return False
    return True


# ── Audit Logging ────────────────────────────────────────────

def log_audit(
    category: str,
    action: str,
    detail: Optional[str] = None,
    user: Optional[User] = None,
    ip_address: Optional[str] = None,
):
    """Append an entry to the immutable audit log."""
    AuditLog.create(
        user=user,
        category=category,
        action=action,
        detail=detail,
        ip_address=ip_address,
    )


# ── FastAPI Dependencies ─────────────────────────────────────

def _get_client_ip(request: Request) -> str:
    """Extract the real client IP, respecting X-Forwarded-For when
    behind a reverse proxy."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> User:
    """FastAPI dependency — resolves the authenticated user from the
    Authorization header, or raises 401."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    payload = decode_token(credentials.credentials)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = User.get_or_none(User.id == int(user_id))
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated",
        )

    return user


async def require_superuser(user: User = Depends(get_current_user)) -> User:
    """FastAPI dependency — ensures the current user is a superuser."""
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required",
        )
    return user
