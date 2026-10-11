"""LokMC Backend — FastAPI application factory.

Assembles the app with all middleware, routes, and lifecycle hooks.
Run with:  uvicorn app.main:app --reload --host 0.0.0.0 --port 8443
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import settings
from app.db.models import db, init_db
from app.security.headers import SecurityHeadersMiddleware


# ── Rate Limiter ─────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address)


# ── Lifespan ─────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Startup
    init_db()
    yield
    # Shutdown
    if not db.is_closed():
        db.close()


# ── App Factory ──────────────────────────────────────────────

app = FastAPI(
    title="LokMC API",
    description="Secure Minecraft Server Management Panel",
    version="0.1.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# State
app.state.limiter = limiter

# Exception handlers
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Middleware (order matters — last added = first executed) ──

# 1. Security headers on every response
app.add_middleware(SecurityHeadersMiddleware)

# 2. CORS — allow frontend origin, local network, and mobile devices
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)

# 3. GZip response compression for payloads > 1000 bytes
from starlette.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ── Routes ───────────────────────────────────────────────────

from app.api.auth import router as auth_router      # noqa: E402
from app.api.servers import router as servers_router  # noqa: E402

app.include_router(auth_router)
app.include_router(servers_router)


# ── Health check ─────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": "0.1.0"}


# ── Static Frontend Serving (Unified Daemon like Crafty) ─────

frontend_build = Path(__file__).resolve().parent.parent.parent / "frontend" / "build"

if frontend_build.exists():
    app_assets = frontend_build / "_app"
    if app_assets.exists():
        app.mount("/_app", StaticFiles(directory=str(app_assets)), name="app_assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Never intercept API or doc endpoints
        if full_path.startswith("api") or full_path in ("docs", "redoc", "openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")

        target = frontend_build / full_path
        if full_path and target.is_file():
            return FileResponse(str(target))

        index_file = frontend_build / "index.html"
        if index_file.is_file():
            return FileResponse(str(index_file))

        raise HTTPException(status_code=404, detail="Frontend build missing")

