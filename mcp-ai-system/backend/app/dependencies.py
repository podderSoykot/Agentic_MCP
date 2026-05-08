"""Shared dependencies (auth, db sessions, etc.)."""

from app.config import settings
from app.core.mcp_router import MCPRouter
from app.core.orchestrator import MCPOrchestrator
from app.core.tool_registry import ToolRegistry

registry = ToolRegistry()
router = MCPRouter(registry=registry)
orchestrator = MCPOrchestrator(router=router)


def get_settings():
    return settings


def get_registry() -> ToolRegistry:
    return registry


def get_orchestrator() -> MCPOrchestrator:
    return orchestrator
