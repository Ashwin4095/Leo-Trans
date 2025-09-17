"""Lightweight TTL cache used until Redis is provisioned."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Optional


class GlossaryCache:
    """In-memory cache placeholder mirroring planned Redis behavior."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl = ttl_seconds
        self._lock = asyncio.Lock()
        self._entries: Optional[list[dict[str, Any]]] = None
        self._expires_at: float = 0.0

    async def get_entries(self) -> Optional[list[dict[str, Any]]]:
        async with self._lock:
            if self._entries is None or time.time() >= self._expires_at:
                return None
            return list(self._entries)

    async def set_entries(self, entries: list[dict[str, Any]]) -> None:
        async with self._lock:
            self._entries = list(entries)
            self._expires_at = time.time() + self._ttl

    async def invalidate(self) -> None:
        async with self._lock:
            self._entries = None
            self._expires_at = 0.0
