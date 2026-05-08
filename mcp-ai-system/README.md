# MCP AI System

## Use with uv

From the project root (`mcp-ai-system`):

```bash
uv sync
uv run --directory backend uvicorn app.main:app --reload
```

API docs:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Legacy requirements.txt

`requirements.txt` is kept for compatibility, but `pyproject.toml` + `uv sync` is the default workflow.
