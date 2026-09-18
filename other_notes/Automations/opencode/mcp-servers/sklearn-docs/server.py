"""Scikit-learn offline docs MCP server entry point."""

from mcp_for_agents import build_server

if __name__ == "__main__":
    build_server(label="scikit-learn").run()
