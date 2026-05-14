import logging
import random
from logging.handlers import RotatingFileHandler

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = RotatingFileHandler("server.log", maxBytes=1_000_000, backupCount=3)
    _handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(_handler)

mcp = FastMCP("sampling-mcp")


@mcp.tool()
def random_number(low: int = 1, high: int = 100) -> dict[str, int]:
    value = random.randint(low, high)
    logger.info("random_number | %s-%s => %s", low, high, value)
    return {"value": value}


@mcp.tool()
def random_text(length: int = 10) -> dict[str, str]:
    letters = "abcdefghijklmnopqrstuvwxyz"
    value = "".join(random.choice(letters) for _ in range(length))
    logger.info("random_text | length=%s => %s", length, value)
    return {"value": value}


if __name__ == "__main__":
    mcp.run()
