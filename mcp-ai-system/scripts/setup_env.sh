#!/usr/bin/env bash
set -euo pipefail

# Install project dependencies with uv.
uv sync

echo "Environment ready via uv."
