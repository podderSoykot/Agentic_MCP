"""FastAPI entrypoint (MCP server)."""

from fastapi import FastAPI

from app.api.routes import agent, files, health
from app.config import settings
from app.dependencies import get_registry
from app.core.logger import configure_logging

configure_logging()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def startup_event() -> None:
    registry = get_registry()
    # Load tool modules dynamically from the configured package.
    registry.discover_tools(settings.tools_package)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.app_name, "env": settings.app_env}


app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(agent.router, prefix=settings.api_prefix)
app.include_router(files.router, prefix=settings.api_prefix)
