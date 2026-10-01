"""Local stdio MCP server that proxies the official FastMCP docs MCP.

Wraps the upstream MCP at https://gofastmcp.com/mcp and re-exposes its tools
through this process, with a small in-memory TTL cache for `ls /` and `cat`
calls so the model can revisit pages without re-hitting upstream.

Run via the `fastmcp-docs-mcp` console script installed by `uv tool install`,
or directly with `uv run python -m src.fastmcp_docs_server`.

Installing globally from this repo:

    uv tool install .                  # initial install
    uv tool install --force .          # pick up changes to pyproject/deps

`uv tool install` snapshots dependencies at install time, so changes to
`pyproject.toml` need `--force` (or uninstall + install) to take effect.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any

from fastmcp import Client, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from mcp.types import ToolAnnotations

logger = logging.getLogger(__name__)

UPSTREAM_URL = "https://gofastmcp.com/mcp"
DEFAULT_TIMEOUT_SECONDS = 30.0

# Tool names exposed by the upstream server. Re-declared here so a typo in
# one place is a single grep away. Verified against gofastmcp.com/mcp on
# the date this module was written; the upstream is owned by the FastMCP
# team and may add or rename tools over time.
UPSTREAM_SEARCH_TOOL = "search_fast_mcp"
UPSTREAM_FILESYSTEM_TOOL = "query_docs_filesystem_fast_mcp"
# submit_feedback exists upstream but is intentionally not exposed as a tool
# on this server: it would let the model post messages to a third party under
# your network identity without an explicit human confirmation step.


@dataclass(slots=True)
class CacheEntry:
    """Single cached upstream response with expiry."""

    value: str
    expires_at: float


class TTLCache:
    """Tiny in-memory TTL cache, single-process, not thread-safe."""

    def __init__(self, ttl_seconds: float) -> None:
        self._ttl = ttl_seconds
        self._store: dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> str | None:
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if entry.expires_at < time.monotonic():
                del self._store[key]
                return None
            return entry.value

    async def set(self, key: str, value: str) -> None:
        async with self._lock:
            self._store[key] = CacheEntry(value=value, expires_at=time.monotonic() + self._ttl)


def _extract_text(result: Any) -> str:
    """Pull the first text block out of a CallToolResult.

    The upstream always returns content as a single TextContent block, but
    guard against unexpected shapes rather than crashing the server.
    """
    content = getattr(result, "content", None) or []
    if not content:
        raise ToolError("Upstream returned no content")
    first = content[0]
    text = getattr(first, "text", None)
    if text is None:
        raise ToolError(f"Upstream returned non-text content: {type(first).__name__}")
    return text


# Cache TTLs: page listings change rarely; doc bodies change more often.
PAGES_CACHE = TTLCache(ttl_seconds=3600.0)
CAT_CACHE = TTLCache(ttl_seconds=300.0)

mcp = FastMCP(
    name="fastmcp-docs",
    instructions=(
        "Local proxy to the official FastMCP documentation MCP "
        "(https://gofastmcp.com/mcp). Use search_docs to find pages by "
        "topic, then query_docs_filesystem to read them with cat/grep/ls."
    ),
    website_url="https://gofastmcp.com",
)


UPSTREAM_MAX_ATTEMPTS = 3
UPSTREAM_RETRY_BASE_SECONDS = 0.5

# Errors worth retrying: any connection-level issue or timeout. Logic errors
# raised by the upstream server (validation, "not found", etc.) bubble up
# immediately because a retry won't help.
_RETRYABLE_EXC_TYPES: tuple[type[BaseException], ...] = (
    ConnectionError,
    TimeoutError,
    OSError,
)


async def _call_upstream(tool_name: str, arguments: dict[str, Any]) -> str:
    """Run a single tool call against the upstream MCP and return its text.

    Retries transient connection failures with exponential backoff. Logic
    errors raised upstream (validation failures, missing paths, etc.) are
    not retried - they're deterministic and won't change on a second attempt.
    """
    last_exc: BaseException | None = None
    for attempt in range(1, UPSTREAM_MAX_ATTEMPTS + 1):
        try:
            async with Client(UPSTREAM_URL, timeout=DEFAULT_TIMEOUT_SECONDS) as client:
                result = await client.call_tool(tool_name, arguments)
            return _extract_text(result)
        except _RETRYABLE_EXC_TYPES as exc:
            last_exc = exc
            if attempt == UPSTREAM_MAX_ATTEMPTS:
                break
            backoff = UPSTREAM_RETRY_BASE_SECONDS * (2 ** (attempt - 1))
            logger.warning(
                "Upstream %s failed (attempt %d/%d), retrying in %.1fs: %s",
                tool_name, attempt, UPSTREAM_MAX_ATTEMPTS, backoff, exc,
            )
            await asyncio.sleep(backoff)
        except Exception as exc:
            logger.exception("Upstream call failed", extra={"tool": tool_name})
            raise ToolError(f"Upstream {tool_name} failed: {exc}") from exc
    raise ToolError(
        f"Upstream {tool_name} unreachable after {UPSTREAM_MAX_ATTEMPTS} attempts: {last_exc}"
    ) from last_exc


@mcp.tool(
    name="search_docs",
    description=(
        "Search the FastMCP documentation by free-text query. Returns a list "
        "of matching pages with title, link, page path, and a content "
        "snippet. Use this before query_docs_filesystem to discover the "
        "right page path (e.g. 'v2/servers/tools')."
    ),
    annotations=ToolAnnotations(
        title="Search FastMCP docs",
        readOnlyHint=True,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
async def search_docs(query: str) -> str:
    """Search the FastMCP knowledge base for pages matching `query`."""
    if not query.strip():
        raise ToolError("query must not be empty")
    return await _call_upstream(UPSTREAM_SEARCH_TOOL, {"query": query})


@mcp.tool(
    name="query_docs_filesystem",
    description=(
        "Run a read-only shell-like command against the FastMCP docs "
        "virtual filesystem. Supported commands include `ls <path>`, "
        "`cat <file>`, `grep -r <pattern> <path>`, and similar. Use this "
        "to read specific doc pages after finding their paths via "
        "search_docs. Example: command='cat /v2/servers/tools.mdx'."
    ),
    annotations=ToolAnnotations(
        title="Query FastMCP docs filesystem",
        readOnlyHint=True,
        idempotentHint=True,
        openWorldHint=True,
    ),
)
async def query_docs_filesystem(command: str) -> str:
    """Run a shell-like query against the docs virtual filesystem."""
    if not command.strip():
        raise ToolError("command must not be empty")

    # Cache only the two operations that are safe to dedupe within a session.
    # ls of the root is the page list; cat is content read. Anything else
    # (grep, find, etc.) goes straight to upstream.
    stripped = command.strip()
    cache_key: str | None = None
    if stripped.startswith("ls "):
        cache_key = f"ls::{stripped}"
    elif stripped.startswith("cat "):
        cache_key = f"cat::{stripped}"

    if cache_key is not None:
        cached = await PAGES_CACHE.get(cache_key) if cache_key.startswith("ls::") else await CAT_CACHE.get(cache_key)
        if cached is not None:
            return cached
        text = await _call_upstream(UPSTREAM_FILESYSTEM_TOOL, {"command": stripped})
        if cache_key.startswith("ls::"):
            await PAGES_CACHE.set(cache_key, text)
        else:
            await CAT_CACHE.set(cache_key, text)
        return text

    return await _call_upstream(UPSTREAM_FILESYSTEM_TOOL, {"command": stripped})


@mcp.resource(
    uri="fastmcp://pages",
    name="docs_page_index",
    description=(
        "JSON listing of every FastMCP documentation page, derived from "
        "`ls /` on the upstream virtual filesystem. Cached for one hour."
    ),
    mime_type="application/json",
)
async def list_doc_pages() -> str:
    """Return a JSON list of page paths available in the docs filesystem."""
    cached = await PAGES_CACHE.get("ls::ls /")
    if cached is None:
        cached = await _call_upstream(UPSTREAM_FILESYSTEM_TOOL, {"command": "ls /"})
        await PAGES_CACHE.set("ls::ls /", cached)
    # The upstream text starts with "exit: 0\n--- stdout ---\n<names>\n".
    # Split off the stdout payload so consumers get clean paths.
    parts = cached.split("--- stdout ---\n", 1)
    names = parts[1].strip().splitlines() if len(parts) == 2 else []
    return json.dumps(sorted(names))


@mcp.resource(
    uri="fastmcp://page/{path*}",
    name="doc_page",
    description=(
        "Read a FastMCP documentation page by path (e.g. "
        "`fastmcp://page/v2/servers/tools`). The path is passed to "
        "`cat /<path>` on the upstream filesystem; if it has no extension "
        "the canonical `.mdx` is appended. Pass the extension explicitly "
        "to override. Cached for five minutes."
    ),
    mime_type="text/markdown",
)
async def read_doc_page(path: str) -> str:
    """Read a single docs page by path."""
    # FastMCP already screens path traversal; this guard is belt-and-braces.
    if ".." in path.split("/"):
        raise ResourceError("Invalid path")
    if "." not in path.rsplit("/", 1)[-1]:
        path = f"{path}.mdx"
    cmd = f"cat /{path}"
    cache_key = f"cat::{cmd}"
    cached = await CAT_CACHE.get(cache_key)
    if cached is not None:
        return cached
    text = await _call_upstream(UPSTREAM_FILESYSTEM_TOOL, {"command": cmd})
    parts = text.split("--- stdout ---\n", 1)
    body = parts[1] if len(parts) == 2 else text
    await CAT_CACHE.set(cache_key, text)
    return body


def main() -> None:
    """Console-script entry point: run the server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
