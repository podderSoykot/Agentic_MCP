"""Utility helpers for file handling."""

from pathlib import Path
import uuid


def make_storage_filename(original_name: str) -> str:
    suffix = Path(original_name).suffix
    return f"{uuid.uuid4().hex}{suffix}"
