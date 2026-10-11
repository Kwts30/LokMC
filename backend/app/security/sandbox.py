"""LokMC — File-system sandbox.

Prevents path-traversal, symlink escapes, and unsafe uploads.
Every file operation in the panel MUST go through these helpers.
"""

import os
import re
from pathlib import Path
from typing import Optional

# Upload allow-list: only these MIME extensions can be uploaded
ALLOWED_EXTENSIONS = frozenset(
    {
        ".txt", ".yml", ".yaml", ".json", ".properties", ".cfg", ".conf",
        ".toml", ".ini", ".log", ".csv", ".md",
        ".jar", ".zip", ".tar", ".gz", ".tar.gz",
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
        ".sh", ".bat", ".cmd", ".ps1",
    }
)

# Maximum upload size per file: 500 MB
MAX_UPLOAD_BYTES = 500 * 1024 * 1024

# Characters forbidden in filenames (Windows + Unix dangers)
_UNSAFE_FILENAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class SandboxViolation(Exception):
    """Raised when a file operation attempts to escape its jail."""


def validate_path(requested: str, jail_root: str) -> Path:
    """Resolve *requested* and verify it lives inside *jail_root*.

    Returns the resolved absolute Path on success.
    Raises SandboxViolation if the path escapes the jail.
    """
    root = Path(jail_root).resolve()
    target = (root / requested).resolve()

    # Resolve symlinks and re-check
    if target.is_symlink():
        target = target.resolve()

    if not str(target).startswith(str(root)):
        raise SandboxViolation(
            f"Path traversal blocked: '{requested}' resolves outside the server root"
        )

    return target


def validate_filename(name: str) -> str:
    """Sanitize and validate a filename for safe storage.

    Returns the cleaned filename or raises SandboxViolation.
    """
    # Strip leading/trailing whitespace and dots
    name = name.strip().strip(".")

    if not name:
        raise SandboxViolation("Empty filename")

    if _UNSAFE_FILENAME_RE.search(name):
        raise SandboxViolation(f"Filename contains unsafe characters: '{name}'")

    # Block directory traversal components
    if ".." in name or "/" in name or "\\" in name:
        raise SandboxViolation(f"Filename contains path traversal: '{name}'")

    return name


def validate_extension(filename: str, extra_allowed: Optional[set[str]] = None) -> str:
    """Check that the file extension is in the allow-list.

    Returns the extension (lowercase, with dot) or raises SandboxViolation.
    """
    allowed = ALLOWED_EXTENSIONS | (extra_allowed or set())
    ext = Path(filename).suffix.lower()

    if not ext:
        raise SandboxViolation(f"File has no extension: '{filename}'")

    if ext not in allowed:
        raise SandboxViolation(
            f"File extension '{ext}' is not permitted. "
            f"Allowed: {', '.join(sorted(allowed))}"
        )

    return ext


def validate_upload_size(size_bytes: int):
    """Reject uploads that exceed the configured limit."""
    if size_bytes > MAX_UPLOAD_BYTES:
        mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise SandboxViolation(f"Upload exceeds {mb} MB limit")


def safe_join(root: str, *parts: str) -> Path:
    """Join path parts under a root, validating the result stays inside."""
    combined = os.path.join(*parts) if parts else ""
    return validate_path(combined, root)
