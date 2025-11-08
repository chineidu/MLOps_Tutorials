from typing import Any

import httpx
from fastmcp import FastMCP  # noqa: N999
from langchain_community.tools import DuckDuckGoSearchResults
from markdownify import markdownify

from src.settings import refresh_settings

settings = refresh_settings()


mcp = FastMCP("Demo")


async def afetch_raw_content(url: str, num_chars: int = 1_000) -> str | None:
    """
    Asynchronously fetch HTML content from a URL and convert it to markdown format.

    Parameters
    ----------
    url : str
        The URL to fetch content from.
    num_chars : int, optional
        The maximum number of characters to fetch from the content (default is 1000).

    Returns
    -------
    str or None
        The fetched content converted to markdown if successful,
        None if any error occurs during fetching or conversion.

    """
    try:
        # Create a client
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            response = f"{response.text[:num_chars]} [truncated]" if len(response.text) > num_chars else response.text
            return markdownify(response)

    except Exception as e:
        print(f"Warning: Failed to fetch full page content for {url}: {str(e)}")
        return None


@mcp.tool
async def duckduckgo_search(query: str, fetch_full_page: bool = False) -> dict[str, list[dict[str, Any]]]:
    """
    Perform an asynchronous DuckDuckGo search and optionally fetch full page content.

    Parameters
    ----------
    query : str
        The search query string.
    fetch_full_page : bool, optional
        Whether to fetch the full page content for each search result (default is False).

    Returns
    -------
    dict[str, list[dict[str, Any]]]
        A dictionary containing a list of search results with their titles, URLs, snippets,
        and optionally their full content.
    """
    try:
        search = DuckDuckGoSearchResults(output_format="list")
        raw_results = await search.ainvoke(query)

        # format the data
        raw_results: list[dict[str, Any]] = [
            {
                "title": row["title"],
                "url": row["link"],
                "content": row["snippet"],
            }
            for row in raw_results
        ]

        if fetch_full_page:
            raw_results = [
                {
                    **row,
                    **{
                        "raw_content": await afetch_raw_content(row["url"]),
                    },
                }
                for row in raw_results
            ]
        return {"results": raw_results}

    except Exception as e:
        print(f"Duckduckgo search failed: {str(e)}")
        return {"results": []}


@mcp.tool
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b


if __name__ == "__main__":
    mcp.run()

# fastmcp run my_server.py:mcp --transport http --port 8000
# PYTHONPATH=. uv run fastmcp run other_notes/MCP/01_ex.py:mcp --transport http --port 8000
