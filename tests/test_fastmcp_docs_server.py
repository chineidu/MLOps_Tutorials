"""Smoke tests for the FastMCP docs proxy server.

These hit the real upstream at https://gofastmcp.com/mcp. Mark them
with `-m "not network"` or skip via `pytest.skip` if you need offline CI.
"""
from __future__ import annotations

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from src.fastmcp_docs_server import (
    CAT_CACHE,
    PAGES_CACHE,
    mcp,
)


@pytest.fixture(autouse=True)
async def _clear_caches() -> None:
    """Each test starts with empty caches to avoid order coupling."""
    PAGES_CACHE._store.clear()
    CAT_CACHE._store.clear()


class TestServerRegistration:
    """Verify the server exposes the expected tools and resources."""

    async def test_exposes_two_tools(self) -> None:
        async with Client(mcp) as client:
            tools = await client.list_tools()
            names = {t.name for t in tools}
            # submit_feedback exists upstream but is intentionally NOT exposed
            # here - it lets the model post to a third party without
            # confirmation, which we don't want autonomous.
            assert names == {"search_docs", "query_docs_filesystem"}

    async def test_exposes_pages_resource(self) -> None:
        async with Client(mcp) as client:
            resources = await client.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "fastmcp://pages" in uris

    async def test_exposes_page_template(self) -> None:
        async with Client(mcp) as client:
            templates = await client.list_resource_templates()
            uris = {t.uriTemplate for t in templates}
            assert "fastmcp://page/{path*}" in uris


class TestToolValidation:
    """Tool argument validation should raise ToolError before hitting upstream."""

    async def test_search_rejects_empty_query(self) -> None:
        async with Client(mcp) as client:
            with pytest.raises(ToolError, match="must not be empty"):
                await client.call_tool("search_docs", {"query": ""})

    async def test_filesystem_rejects_empty_command(self) -> None:
        async with Client(mcp) as client:
            with pytest.raises(ToolError, match="must not be empty"):
                await client.call_tool("query_docs_filesystem", {"command": "   "})


class TestUpstreamIntegration:
    """End-to-end tests against the real upstream. Skip when offline."""

    async def test_pages_resource_returns_sorted_json_list(self) -> None:
        async with Client(mcp) as client:
            result = await client.read_resource("fastmcp://pages")
            import json

            pages = json.loads(result[0].text)
            assert isinstance(pages, list)
            assert "getting-started" in pages
            assert pages == sorted(pages)

    async def test_doc_page_resource_returns_markdown(self) -> None:
        async with Client(mcp) as client:
            result = await client.read_resource("fastmcp://page/getting-started/welcome")
            text = result[0].text
            assert "FastMCP" in text
            # Cache key should have been populated.
            assert await CAT_CACHE.get("cat::cat /getting-started/welcome.mdx") is not None

    async def test_filesystem_cat_is_cached(self) -> None:
        async with Client(mcp) as client:
            await client.call_tool(
                "query_docs_filesystem", {"command": "cat /v2/servers/tools.mdx"}
            )
            cached = await CAT_CACHE.get("cat::cat /v2/servers/tools.mdx")
            assert cached is not None
            assert "FastMCP" in cached
