"""Calculator tool."""

from __future__ import annotations

import ast
import operator
from typing import Any

from app.core.tool_registry import MCPTool

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_expr(node.left), _eval_expr(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_expr(node.operand))
    raise ValueError("Unsupported expression.")


class CalculatorTool(MCPTool):
    name = "calculator"
    description = "Evaluate basic arithmetic expressions."

    async def run(self, args: dict[str, Any]) -> Any:
        expression = str(args.get("expression", "")).strip()
        if not expression:
            raise ValueError("Missing 'expression'.")
        tree = ast.parse(expression, mode="eval")
        value = _eval_expr(tree.body)
        return {"expression": expression, "value": value}


TOOL_CLASS = CalculatorTool
