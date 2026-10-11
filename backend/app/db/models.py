"""LokMC Backend — Database layer.

Uses Peewee ORM with standard SQLite (SQLCipher can be swapped in
by replacing the `SqliteDatabase` import with `playhouse.sqlcipher_ext`
when the native library is available).

WAL mode + busy_timeout for safe concurrent reads.
"""

import datetime
from pathlib import Path

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    SqliteDatabase,
    TextField,
    Model,
    FloatField,
)

from app.config import settings

# Ensure the data directory exists
Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)

db = SqliteDatabase(
    settings.db_path,
    pragmas={
        "journal_mode": "wal",
        "cache_size": -64 * 1000,  # 64 MB
        "foreign_keys": 1,
        "busy_timeout": 5000,
        "synchronous": "NORMAL",
    },
)


# ── Base ─────────────────────────────────────────────────────

class BaseModel(Model):
    class Meta:
        database = db


# ── Users & Auth ─────────────────────────────────────────────

class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True, max_length=64)
    email = CharField(unique=True, max_length=255, null=True)
    password_hash = CharField(max_length=255)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)
    totp_secret = CharField(max_length=64, null=True)
    totp_enabled = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    last_login = DateTimeField(null=True)

    class Meta:
        table_name = "users"


class Role(BaseModel):
    id = AutoField()
    name = CharField(unique=True, max_length=64)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        table_name = "roles"


class UserRole(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="roles", on_delete="CASCADE")
    role = ForeignKeyField(Role, backref="users", on_delete="CASCADE")

    class Meta:
        table_name = "user_roles"
        indexes = ((("user", "role"), True),)  # Unique together


class Session(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="sessions", on_delete="CASCADE")
    token_jti = CharField(unique=True, max_length=64)
    ip_address = CharField(max_length=45, null=True)
    user_agent = CharField(max_length=512, null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    expires_at = DateTimeField()
    is_revoked = BooleanField(default=False)

    class Meta:
        table_name = "sessions"


# ── Servers ──────────────────────────────────────────────────

class Server(BaseModel):
    id = AutoField()
    name = CharField(max_length=128)
    server_type = CharField(max_length=32, default="java")  # java | bedrock
    version = CharField(max_length=32, null=True)
    jar_file = CharField(max_length=255, null=True)
    container_id = CharField(max_length=128, null=True)
    port = IntegerField(default=25565)
    memory_min = IntegerField(default=1024)  # MB
    memory_max = IntegerField(default=2048)  # MB
    cpu_limit = FloatField(default=2.0)  # CPU cores
    auto_start = BooleanField(default=False)
    status = CharField(max_length=32, default="stopped")
    path = CharField(max_length=512)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_by = ForeignKeyField(User, backref="servers", on_delete="SET NULL", null=True)

    class Meta:
        table_name = "servers"


class ServerPermission(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="server_permissions", on_delete="CASCADE")
    server = ForeignKeyField(Server, backref="permissions", on_delete="CASCADE")
    can_view = BooleanField(default=True)
    can_control = BooleanField(default=False)  # start/stop/restart
    can_console = BooleanField(default=False)
    can_files = BooleanField(default=False)
    can_backup = BooleanField(default=False)
    can_schedule = BooleanField(default=False)
    can_config = BooleanField(default=False)

    class Meta:
        table_name = "server_permissions"
        indexes = ((("user", "server"), True),)


# ── Audit Log ────────────────────────────────────────────────

class AuditLog(BaseModel):
    """Append-only audit trail.  No UPDATE or DELETE should ever run
    against this table — enforced at the application layer."""

    id = AutoField()
    user = ForeignKeyField(User, backref="audit_entries", on_delete="SET NULL", null=True)
    category = CharField(max_length=32)  # AUTH, SERVER, FILES, CONFIG, SCHEDULE, USER_MGMT
    action = CharField(max_length=128)
    detail = TextField(null=True)
    ip_address = CharField(max_length=45, null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        table_name = "audit_log"


# ── Schedules ────────────────────────────────────────────────

class Schedule(BaseModel):
    id = AutoField()
    server = ForeignKeyField(Server, backref="schedules", on_delete="CASCADE")
    name = CharField(max_length=128)
    task_type = CharField(max_length=32)  # command, restart, backup
    cron_expression = CharField(max_length=128, null=True)
    command = TextField(null=True)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        table_name = "schedules"


# ── Metrics ──────────────────────────────────────────────────

class Metric(BaseModel):
    id = AutoField()
    server = ForeignKeyField(Server, backref="metrics", on_delete="CASCADE", null=True)
    metric_type = CharField(max_length=32)  # cpu, ram, players, disk
    value = FloatField()
    recorded_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        table_name = "metrics"


# ── Table Creation ───────────────────────────────────────────

ALL_TABLES = [
    User,
    Role,
    UserRole,
    Session,
    Server,
    ServerPermission,
    AuditLog,
    Schedule,
    Metric,
]


def init_db():
    """Create all tables if they don't exist, and seed default roles."""
    db.connect(reuse_if_open=True)
    db.create_tables(ALL_TABLES)

    # Seed default roles
    for role_name, desc in [
        ("admin", "Full access to all servers and settings"),
        ("operator", "Can control assigned servers"),
        ("viewer", "Read-only access to assigned servers"),
    ]:
        Role.get_or_create(name=role_name, defaults={"description": desc})

    db.close()
