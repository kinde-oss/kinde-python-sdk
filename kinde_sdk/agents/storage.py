"""
Pluggable storage for the agent client: tokens and dynamic client registrations.

Tokens are keyed by resource and account, and carry the issuer they came from.
Registrations are keyed by issuer and redirect URI. Values are plain JSON-safe
dicts so any store (a database, an encrypted session, a keychain) can hold them.
"""

import asyncio
import json
import os
import tempfile
from typing import Any, Dict, Optional, Protocol


class AgentClientStorage(Protocol):
    async def get_tokens(self, key: str) -> Optional[Dict[str, Any]]: ...

    async def set_tokens(self, key: str, tokens: Dict[str, Any]) -> None: ...

    async def delete_tokens(self, key: str) -> None: ...

    async def get_registration(self, key: str) -> Optional[Dict[str, Any]]: ...

    async def set_registration(self, key: str, registration: Dict[str, Any]) -> None: ...

    async def delete_registration(self, key: str) -> None: ...


class InMemoryAgentStorage:
    """Keeps everything in the process. For tests and short-lived agents."""

    def __init__(self):
        self._tokens: Dict[str, Dict[str, Any]] = {}
        self._registrations: Dict[str, Dict[str, Any]] = {}

    async def get_tokens(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._tokens.get(key)
        return dict(value) if value is not None else None

    async def set_tokens(self, key: str, tokens: Dict[str, Any]) -> None:
        self._tokens[key] = dict(tokens)

    async def delete_tokens(self, key: str) -> None:
        self._tokens.pop(key, None)

    async def get_registration(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._registrations.get(key)
        return dict(value) if value is not None else None

    async def set_registration(self, key: str, registration: Dict[str, Any]) -> None:
        self._registrations[key] = dict(registration)

    async def delete_registration(self, key: str) -> None:
        self._registrations.pop(key, None)


class FileAgentStorage:
    """Keeps everything in one JSON file readable only by the current user (mode 0600).

    Suitable for CLI agents on a single-user machine. The file holds refresh
    tokens and client secrets in plain text, so prefer the OS keychain or an
    encrypted store where one is available.
    """

    def __init__(self, path: str):
        self.path = os.path.expanduser(path)
        self._lock: Optional[asyncio.Lock] = None

    def _read(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            return {"tokens": {}, "registrations": {}}
        data.setdefault("tokens", {})
        data.setdefault("registrations", {})
        return data

    def _write(self, data: Dict[str, Dict[str, Any]]) -> None:
        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, mode=0o700, exist_ok=True)
        # Write then rename so a crash never leaves a half-written file
        fd, temp_path = tempfile.mkstemp(dir=directory, prefix=".kinde-agent-")
        try:
            os.chmod(temp_path, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle)
            os.replace(temp_path, self.path)
        except BaseException:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _guard(self) -> asyncio.Lock:
        # Created lazily so it binds to the running event loop (Python 3.9)
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    async def _get(self, section: str, key: str) -> Optional[Dict[str, Any]]:
        async with self._guard():
            return self._read()[section].get(key)

    async def _set(self, section: str, key: str, value: Optional[Dict[str, Any]]) -> None:
        async with self._guard():
            data = self._read()
            if value is None:
                data[section].pop(key, None)
            else:
                data[section][key] = value
            self._write(data)

    async def get_tokens(self, key: str) -> Optional[Dict[str, Any]]:
        return await self._get("tokens", key)

    async def set_tokens(self, key: str, tokens: Dict[str, Any]) -> None:
        await self._set("tokens", key, tokens)

    async def delete_tokens(self, key: str) -> None:
        await self._set("tokens", key, None)

    async def get_registration(self, key: str) -> Optional[Dict[str, Any]]:
        return await self._get("registrations", key)

    async def set_registration(self, key: str, registration: Dict[str, Any]) -> None:
        await self._set("registrations", key, registration)

    async def delete_registration(self, key: str) -> None:
        await self._set("registrations", key, None)
