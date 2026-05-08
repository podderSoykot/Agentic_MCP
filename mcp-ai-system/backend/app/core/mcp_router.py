"""MCP request router implementation."""

from __future__ import annotations

import logging

from app.core.tool_registry import ToolRegistry
from app.models.agent import MCPToolCallRequest, MCPToolCallResponse

logger = logging.getLogger(__name__)


class MCPRouter:
    """Routes JSON tool requests to the proper registered tool."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    async def route(self, payload: MCPToolCallRequest) -> MCPToolCallResponse:
        try:
            tool = self.registry.get(payload.tool)
            result = await tool.run(payload.args)
            return MCPToolCallResponse(
                ok=True,
                tool=payload.tool,
                request_id=payload.request_id,
                result=result,
            )
        except KeyError as exc:
            logger.warning("Unknown tool requested: %s", payload.tool)
            return MCPToolCallResponse(
                ok=False,
                tool=payload.tool,
                request_id=payload.request_id,
                error=str(exc),
            )
        except Exception as exc:  # pragma: no cover
            logger.exception("Tool execution failed for %s", payload.tool)
            return MCPToolCallResponse(
                ok=False,
                tool=payload.tool,
                request_id=payload.request_id,
                error=f"{type(exc).__name__}: {exc}",
            )
