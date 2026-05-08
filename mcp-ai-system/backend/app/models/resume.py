"""Pydantic models for resume entities and file metadata."""

from datetime import datetime
from pydantic import BaseModel


class FileMetadata(BaseModel):
    file_id: str
    original_name: str
    stored_name: str
    path: str
    mime_type: str
    size_bytes: int
    uploaded_at: datetime
