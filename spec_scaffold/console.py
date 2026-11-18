"""Tiny ANSI helper — no dependency, and it switches itself off when it should.

Colour is used for exactly four things: a file was written (green), a file was
skipped (yellow), the spec passed (green) and the spec failed (red). Anything
that is piped, redirected, or runs under ``NO_COLOR`` gets plain text.
"""

from __future__ import annotations

import os
import sys

_CODES = {
    "green": "32",
    "yellow": "33",
    "red": "31",
    "dim": "2",
}

RESET = "\x1b[0m"


def supports_color(stream=None) -> bool:
    """Decide whether *stream* (default: stdout) should get ANSI escapes.

    Honours the informal ``NO_COLOR`` and ``FORCE_COLOR`` conventions, so tests
    and CI never have to strip escapes they did not ask for.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    stream = stream if stream is not None else sys.stdout
    return hasattr(stream, "isatty") and stream.isatty()


def paint(text: str, color: str, enabled: bool | None = None) -> str:
    """Wrap *text* in *color* codes.

    *enabled* forces the decision; when it is ``None`` (the default) the stream
    capability check in :func:`supports_color` is used.
    """
    code = _CODES.get(color)
    if code is None:
        return text
    if enabled is None:
        enabled = supports_color()
    if not enabled:
        return text
    return f"\x1b[{code}m{text}{RESET}"
