"""Stdio MCP client: spawns server.py and calls tools over the MCP protocol."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult, TextContent


def _format_payload(text: str) -> str:
    raw = text.strip()
    try:
        data: Any = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, ensure_ascii=False)
    return str(data)


def format_tool_result(title: str, result: CallToolResult) -> str:
    """Readable summary for MCP tool responses (no raw object repr)."""
    lines: list[str] = []
    rule = "-" * min(56, max(24, len(title) + 8))
    lines.append(rule)
    lines.append(title)
    lines.append(rule)

    if result.isError:
        lines.append("Status: error")
        for block in result.content:
            if isinstance(block, TextContent):
                lines.append(_format_payload(block.text))
        return "\n".join(lines)

    lines.append("Status: ok")
    texts = [block.text for block in result.content if isinstance(block, TextContent)]
    if not texts:
        lines.append("(no text content)")
        return "\n".join(lines)

    for chunk in texts:
        lines.append(_format_payload(chunk))
    return "\n".join(lines)


async def main() -> None:
    server_path = Path(__file__).resolve().parent / "server.py"
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        cwd=str(server_path.parent),
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            res1 = await session.call_tool("random_number", {"low": 10, "high": 50})
            print(format_tool_result("Tool: random_number  (low=10, high=50)", res1))

            print()

            res2 = await session.call_tool("random_text", {"length": 8})
            print(format_tool_result("Tool: random_text  (length=8)", res2))


if __name__ == "__main__":
    asyncio.run(main())
