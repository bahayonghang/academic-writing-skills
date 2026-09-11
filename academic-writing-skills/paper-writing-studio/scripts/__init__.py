"""Core routing and output contract for Paper Writing Studio."""

from .core import Result, Section, Selection, render_result, select_profile

__all__ = ["Result", "Section", "Selection", "render_result", "select_profile"]
SCRIPT_INTERFACE = "internal-module"
