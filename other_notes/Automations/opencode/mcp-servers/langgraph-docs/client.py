#!/usr/bin/env python3
"""Test client for the docs MCP server.

Spawns the server with the SAME command/cwd/env opencode uses (copy them
straight from your opencode.jsonc entry) and prints the exact request
sent and response received for a tool call.

Usage:
    # No args: connect and list available tools + their input schemas
    uv run --with fastmcp python test_client.py

    # Call a specific tool
    uv run --with fastmcp python test_client.py list_doc_sources '{}'
    uv run --with fastmcp python test_client.py search_docs '{"query": "checkpoint", "limit": 5}'
    uv run --with fastmcp python test_client.py get_doc '{"path": "src/oss/langgraph/index.mdx"}'
"""

from __future__ import annotations

import asyncio
import json
import sys

from fastmcp import Client

# Mirror your opencode.jsonc entry exactly — same command, cwd, env —
# so this spawns the server identically to how opencode does.
SERVER_CONFIG = {
    "mcpServers": {
        "docs": {
            "command": "uv",
            "args": ["run", "--isolated", "--with", "fastmcp", "python", "langgraph_docs_mcp.py"],
            "cwd": "/Users/mac/.config/opencode/mcp-servers/langgraph-docs",
            "env": {
                "PATH": "/Users/mac/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
            },
        }
    }
}


async def main() -> None:
    client = Client(SERVER_CONFIG)

    async with client:
        tools = await client.list_tools()

        if len(sys.argv) < 2:
            print("Connected. Available tools:\n")
            for t in tools:
                print(f"- {t.name}: {t.description}")
                schema = getattr(t, "inputSchema", None) or getattr(t, "input_schema", None)
                print(f"  input schema: {json.dumps(schema, indent=2)}\n")
            print("Run again as: python test_client.py <tool_name> '<json args>'")
            return

        tool_name = sys.argv[1]
        raw_args = sys.argv[2] if len(sys.argv) > 2 else "{}"
        args = json.loads(raw_args)

        print("--- REQUEST ---")
        print(f"tool:      {tool_name}")
        print(f"arguments: {json.dumps(args, indent=2)}\n")

        result = await client.call_tool(tool_name, args)

        print("--- RAW RESPONSE OBJECT ---")
        print(repr(result))

        print("\n--- CONTENT ---")
        for block in getattr(result, "content", []):
            text = getattr(block, "text", None)
            print(text if text is not None else block)


if __name__ == "__main__":
    asyncio.run(main())
