import asyncio  # noqa: N999
from typing import Any

from fastmcp import Client
from fastmcp.client.client import CallToolResult

client = Client("http://localhost:8000/mcp")


async def call_add(a: float, b: float) -> None:
    """Calls the 'add' tool on the MCP server and prints the result."""
    async with client:
        result = await client.call_tool("add", {"a": a, "b": b})
        print(result)
        print(result.structured_content)


async def call_ddg_search(query: str, fetch_full_page: bool = False) -> Any:
    """Calls the 'duckduckgo_search' tool on the MCP server and prints the result."""
    async with client:
        result: CallToolResult = await client.call_tool(
            "duckduckgo_search", {"query": query, "fetch_full_page": fetch_full_page}
        )
        print(f"[RESULT]:\n{result.structured_content}")
        return result


if __name__ == "__main__":
    asyncio.run(call_add(5, 7))
    asyncio.run(call_ddg_search("FastMCP library", fetch_full_page=False))
