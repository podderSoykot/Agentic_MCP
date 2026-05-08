"""Security utility helpers."""

from pathlib import Path

from app.config import settings


def validate_file_extension(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in settings.allowed_upload_extensions:
        allowed = ", ".join(settings.allowed_upload_extensions)
        raise ValueError(f"Unsupported extension '{ext}'. Allowed: {allowed}")


def validate_file_size(size_bytes: int) -> None:
    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    if size_bytes > max_size_bytes:
        raise ValueError(
            f"File size exceeds limit ({settings.max_upload_size_mb} MB)."
        )
