"""
Router package entrypoint.

Exposes route() for runtime and safely ignores runtime-only kwargs.
"""
from __future__ import annotations

from .text_driver import route_text


def route(raw: str, **kwargs):
    kwargs.pop("is_awake", None)
    return route_text(raw, **kwargs)


__all__ = ["route"]
