"""AI chat and tool-calling endpoints."""

from fastapi import APIRouter, Depends

from app.dependencies import get_orchestrator, get_registry
from app.core.orchestrator import MCPOrchestrator
from app.core.tool_registry import ToolRegistry
from app.models.agent import MCPToolCallRequest, MCPToolCallResponse, MCPToolInfo

router = APIRouter(prefix="/agent", tags=["agent"])


@router.get("/tools", response_model=list[MCPToolInfo])
def list_tools(registry: ToolRegistry = Depends(get_registry)):
    return registry.list_tools()


@router.post("/execute", response_model=MCPToolCallResponse)
async def execute_tool(
    payload: MCPToolCallRequest,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator),
):
    return await orchestrator.execute(payload)
