"""AI reasoning and tool selection orchestration."""

from app.core.mcp_router import MCPRouter
from app.models.agent import MCPToolCallRequest, MCPToolCallResponse


class MCPOrchestrator:
    """
    Minimal orchestrator for Feature 1.
    Later this can add task planning and multi-tool reasoning.
    """

    def __init__(self, router: MCPRouter) -> None:
        self.router = router

    async def execute(self, request: MCPToolCallRequest) -> MCPToolCallResponse:
        return await self.router.route(request)
