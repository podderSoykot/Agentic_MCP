"""Tool registration and discovery."""

from __future__ import annotations

from abc import ABC, abstractmethod
import importlib
import logging
import pkgutil
from typing import Any

logger = logging.getLogger(__name__)


class MCPTool(ABC):
    """Contract every MCP tool must implement."""

    name: str
    description: str

    @abstractmethod
    async def run(self, args: dict[str, Any]) -> Any:
        """Execute tool with JSON args and return JSON-serializable output."""


class ToolRegistry:
    """In-memory registry for MCP tools."""

    def __init__(self) -> None:
        self._tools: dict[str, MCPTool] = {}

    def register(self, tool: MCPTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered.")
        self._tools[tool.name] = tool
        logger.info("Registered tool: %s", tool.name)

    def get(self, tool_name: str) -> MCPTool:
        tool = self._tools.get(tool_name)
        if tool is None:
            raise KeyError(f"Tool '{tool_name}' not found.")
        return tool

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._tools.values()
        ]

    def discover_tools(self, package_name: str) -> int:
        """
        Dynamically load tools from a package.
        Tool module convention: define `TOOL_CLASS` that extends MCPTool.
        """
        count = 0
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_module = f"{package_name}.{module_name}"
            module = importlib.import_module(full_module)
            tool_cls = getattr(module, "TOOL_CLASS", None)
            if tool_cls is None:
                continue
            self.register(tool_cls())
            count += 1
        return count
