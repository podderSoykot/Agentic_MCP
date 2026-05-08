"""File read/write tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.config import settings
from app.core.tool_registry import MCPTool


class FileTool(MCPTool):
    name = "file_tool"
    description = "Read/write text files under the data directory."

    async def run(self, args: dict[str, Any]) -> Any:
        action = str(args.get("action", "")).lower()
        relative_path = str(args.get("path", "")).strip()
        if not relative_path:
            raise ValueError("Missing 'path'.")

        data_root = Path(settings.data_dir).resolve()
        data_root.mkdir(parents=True, exist_ok=True)
        target = (data_root / relative_path).resolve()

        if data_root not in target.parents and target != data_root:
            raise ValueError("Path escapes data directory.")

        if action == "read":
            content = target.read_text(encoding="utf-8")
            return {"path": str(target), "content": content}

        if action == "write":
            content = str(args.get("content", ""))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return {"path": str(target), "bytes_written": len(content.encode("utf-8"))}

        raise ValueError("Unsupported action. Use 'read' or 'write'.")


TOOL_CLASS = FileTool
