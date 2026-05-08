"""Logging configuration and helpers."""

import logging


def configure_logging() -> None:
    """Configure a predictable logger for API + MCP internals."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
