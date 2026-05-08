"""Environment and application settings."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Podder_MCP AI System")
    app_env: str = os.getenv("APP_ENV", "dev")
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    tools_package: str = os.getenv("TOOLS_PACKAGE", "app.tools")
    data_dir: str = os.getenv("DATA_DIR", "data")
    uploads_dir: str = os.getenv("UPLOADS_DIR", "data/uploads")
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    allowed_upload_extensions: tuple[str, ...] = (
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
    )


settings = Settings()
