#!/usr/bin/env bash
set -euo pipefail

# Run FastAPI app from backend package path using uv-managed env.
uv run --directory backend uvicorn app.main:app --reload
