"""LokMC Backend — Application Settings.

All secrets and configuration are loaded from environment variables
or a .env file. Nothing is hardcoded.
"""

from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────
    app_name: str = "LokMC"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8443
    allowed_origins: list[str] = ["http://localhost:5173"]

    # ── Database ─────────────────────────────────────────
    db_path: str = str(BASE_DIR / "data" / "lokmc.db")
    db_key: str = "change-me-in-production"  # SQLCipher encryption key

    # ── JWT ──────────────────────────────────────────────
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 15
    jwt_refresh_expire_days: int = 7

    # ── Rate Limiting ────────────────────────────────────
    rate_limit_login: str = "5/minute"
    rate_limit_api: str = "100/minute"

    # ── Docker ───────────────────────────────────────────
    docker_base_url: str = "unix:///var/run/docker.sock"
    server_data_dir: str = str(BASE_DIR / "servers")
    backup_dir: str = str(BASE_DIR / "backups")

    model_config = {"env_prefix": "LOKMC_", "env_file": ".env"}


settings = Settings()
