"""Pydantic models for agent requests/responses."""

from typing import Any
from pydantic import BaseModel, Field


class MCPToolCallRequest(BaseModel):
    tool: str = Field(..., description="Registered tool name.")
    args: dict[str, Any] = Field(default_factory=dict, description="JSON tool input.")
    request_id: str | None = Field(default=None, description="Optional request id.")


class MCPToolCallResponse(BaseModel):
    ok: bool
    tool: str
    request_id: str | None = None
    result: Any = None
    error: str | None = None


class MCPToolInfo(BaseModel):
    name: str
    description: str
