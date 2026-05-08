"""Business logic for file operations."""

from __future__ import annotations

from datetime import datetime, UTC
import json
from pathlib import Path
import uuid

from app.config import settings
from app.models.resume import FileMetadata
from app.utils.file_utils import make_storage_filename


class FileService:
    def __init__(self) -> None:
        self.upload_root = Path(settings.uploads_dir)
        self.meta_dir = self.upload_root / ".metadata"
        self.meta_index = self.meta_dir / "index.json"
        self.upload_root.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        if not self.meta_index.exists():
            self.meta_index.write_text("{}", encoding="utf-8")

    def _read_index(self) -> dict[str, dict]:
        return json.loads(self.meta_index.read_text(encoding="utf-8"))

    def _write_index(self, data: dict[str, dict]) -> None:
        self.meta_index.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def save_upload(self, original_name: str, mime_type: str, data: bytes) -> FileMetadata:
        file_id = uuid.uuid4().hex
        stored_name = make_storage_filename(original_name)
        target = self.upload_root / stored_name
        target.write_bytes(data)

        metadata = FileMetadata(
            file_id=file_id,
            original_name=original_name,
            stored_name=stored_name,
            path=str(target.resolve()),
            mime_type=mime_type or "application/octet-stream",
            size_bytes=len(data),
            uploaded_at=datetime.now(UTC),
        )

        index = self._read_index()
        index[file_id] = metadata.model_dump(mode="json")
        self._write_index(index)
        return metadata

    def get_metadata(self, file_id: str) -> FileMetadata:
        index = self._read_index()
        data = index.get(file_id)
        if data is None:
            raise FileNotFoundError("File metadata not found.")
        return FileMetadata.model_validate(data)

    def list_metadata(self) -> list[FileMetadata]:
        index = self._read_index()
        files = [FileMetadata.model_validate(raw) for raw in index.values()]
        files.sort(key=lambda x: x.uploaded_at, reverse=True)
        return files

    def get_file_path(self, file_id: str) -> tuple[FileMetadata, Path]:
        meta = self.get_metadata(file_id)
        fp = Path(meta.path)
        if not fp.exists():
            raise FileNotFoundError("Stored file not found on disk.")
        return meta, fp


file_service = FileService()
