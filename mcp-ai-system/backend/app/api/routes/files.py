"""File upload/download endpoints."""

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.models.resume import FileMetadata
from app.services.file_service import file_service
from app.utils.security import validate_file_extension, validate_file_size

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileMetadata)
async def upload_file(file: UploadFile = File(...)):
    try:
        validate_file_extension(file.filename or "")
        content = await file.read()
        validate_file_size(len(content))
        metadata = file_service.save_upload(
            original_name=file.filename or "unnamed.bin",
            mime_type=file.content_type or "application/octet-stream",
            data=content,
        )
        return metadata
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[FileMetadata])
def list_uploaded_files():
    return file_service.list_metadata()


@router.get("/{file_id}/metadata", response_model=FileMetadata)
def get_file_metadata(file_id: str):
    try:
        return file_service.get_metadata(file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{file_id}/download")
def download_file(file_id: str):
    try:
        meta, file_path = file_service.get_file_path(file_id)
        return FileResponse(
            path=str(file_path),
            filename=meta.original_name,
            media_type=meta.mime_type,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
