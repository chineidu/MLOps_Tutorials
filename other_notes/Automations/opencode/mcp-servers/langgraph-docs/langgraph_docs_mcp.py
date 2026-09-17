"""Offline docs MCP server.

Reads markdown files from a local ``DOCS_PATH`` mirror of any
docs-shaped Git repository and exposes three tools over stdio:

* ``list_doc_sources`` - return the corpus location and file count
* ``search_docs``      - rank files by a query over title, headings, body
* ``get_doc``          - return the body of a single file

No outbound network. ``DOCS_PATH`` defaults to ``~/docs-mirror/langchain``
and can be overridden via the environment. The corpus label reported to
clients is derived from the mirror's directory basename (e.g. ``langchain``
becomes ``LangChain``), so the same server works for any docs mirror.

Usage
-----
::

    uv run --with "mcp>=2" python langgraph_docs_mcp.py
    # MCP client connects over stdio.

Configure in ``opencode.jsonc``::

    "langgraph-docs-mcp": {
      "type": "local",
      "command": ["uv", "run", "--with", "mcp>=2", "python", "langgraph_docs_mcp.py"],
      "cwd": "~/.config/opencode/mcp-servers/langgraph-docs",
      "timeout": 30000,
      "enabled": true
    }

``DOCS_PATH`` is read from the environment when the server starts. Set it
to override the default ``~/docs-mirror/langchain`` location, for example
when the mirror lives elsewhere or when pointing at a different corpus.

Refresh the mirror at any time inside ``DOCS_PATH``::

    git fetch origin --depth 1 && git reset --hard origin/main

(``git pull`` fails on shallow mirrors when the upstream force-pushes;
the fetch + reset pattern always works.) Then restart opencode for the
server to pick up new files.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from mcp.server.mcpserver import MCPServer

# Token pattern: lowercase alphanumeric runs of length >= 3.
_TOKEN_PATTERN = re.compile(r"[a-z0-9]{3,}")

# Extensions considered docs; ignore images, configs, partials.
_DOC_EXTS = {".md", ".mdx"}

# Default mirror location when DOCS_PATH is not set.
_DEFAULT_DOCS_PATH = Path("~/docs-mirror/langchain")

# Logger writes JSON lines to stderr (stdout is the JSON-RPC channel).
logger = logging.getLogger("langgraph-docs-mcp")
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler(stream=sys.stderr)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_handler)


@dataclass(slots=True, frozen=True)
class Doc:
    """One indexed document."""

    rel_path: str
    title: str
    body: str
    term_freq: dict[str, int] = field(default_factory=dict)


def _tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens of length >= 3."""
    return _TOKEN_PATTERN.findall(text.lower())


def _term_frequency(tokens: list[str]) -> dict[str, int]:
    """Count tokens in first-seen order without a Counter dependency."""
    out: dict[str, int] = {}
    for tok in tokens:
        out[tok] = out.get(tok, 0) + 1
    return out


def _title_from_body(body: str, rel_path: str) -> str:
    """Extract the first ATX heading or fall back to the file stem."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return Path(rel_path).stem.replace("-", " ").replace("_", " ")


def _index_docs(docs_root: Path) -> list[Doc]:
    """Walk the mirror once and build an in-memory index of all docs."""
    docs: list[Doc] = []
    for path in sorted(docs_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _DOC_EXTS:
            continue
        # Skip hidden, vendored, and node_modules noise.
        rel_parts = path.relative_to(docs_root).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if any(part in {"node_modules", "vendor"} for part in rel_parts):
            continue
        rel_path = "/".join(rel_parts)
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            logger.warning(json.dumps({"event": "skip_read_error", "path": rel_path}))
            continue
        title = _title_from_body(body, rel_path)
        tokens = _tokenize(title + "\n" + body)
        docs.append(
            Doc(
                rel_path=rel_path,
                title=title,
                body=body,
                term_freq=_term_frequency(tokens),
            )
        )
    return docs


def _score(query_tokens: list[str], raw_query: str, doc: Doc) -> float:
    """Sum of term-frequency hits plus a substring bonus for short queries.

    The substring bonus lets a query like ``checkpoint`` match a doc that
    contains ``checkpointing``; pure token-frequency scoring would miss it
    because the tokens do not align.
    """
    if not query_tokens:
        return 0.0
    tf_score = float(sum(doc.term_freq.get(tok, 0) for tok in query_tokens))
    # Substring bonus: count raw query term occurrences in lowercased body.
    if raw_query:
        body_lower = doc.body.lower()
        substring_bonus = float(sum(body_lower.count(tok) for tok in query_tokens))
    else:
        substring_bonus = 0.0
    return tf_score + substring_bonus


def _format_listing(corpus_label: str, docs: list[Doc], docs_root: Path) -> str:
    """Render ``list_doc_sources`` output as a multi-section string."""
    head = f"{corpus_label}\nURL: file://{docs_root}\n"
    sample = "\n".join(f"- {doc.rel_path}: {doc.title}" for doc in docs[:50])
    return f"{head}\nIndexed files ({len(docs)} total):\n{sample}"


def _build_server(docs: list[Doc], corpus_label: str, docs_root: Path) -> MCPServer:
    """Construct the MCP server and register the three tools.

    Parameters
    ----------
    docs : list[Doc]
        Indexed documents from ``_index_docs``.
    corpus_label : str
        Friendly name shown to clients (``LangGraph``).
    docs_root : Path
        Mirror root, used to verify ``get_doc`` paths stay inside it.
    """
    by_path: dict[str, Doc] = {doc.rel_path: doc for doc in docs}
    server = MCPServer(
        name="langgraph-docs",
        instructions=(
            "Offline LangGraph/LangChain/LangSmith docs. "
            "Use list_doc_sources to confirm coverage, search_docs to find "
            "relevant pages, and get_doc to read the body of one page."
        ),
    )

    @server.tool(
        name="list_doc_sources",
        description="List the indexed docs corpus and a sample of paths.",
    )
    def list_doc_sources() -> str:
        """Return corpus label, root URL, and the first 50 indexed paths."""
        return _format_listing(corpus_label, docs, docs_root)

    @server.tool(
        name="search_docs",
        description="Rank docs by a query over title and body terms.",
    )
    def search_docs(query: str, limit: int = 10) -> str:
        """Return the top ``limit`` docs whose term freq matches ``query``.

        Parameters
        ----------
        query : str
            Free-text search terms.
        limit : int
            Maximum number of results to return. Capped at 50.

        """
        if limit < 1:
            limit = 1
        if limit > 50:
            limit = 50
        tokens = _tokenize(query)
        if not tokens:
            return f"No tokens in query: {query!r}"
        ranked = sorted(
            ((_score(tokens, query, doc), doc) for doc in docs),
            key=lambda pair: pair[0],
            reverse=True,
        )
        top = [(score, doc) for score, doc in ranked if score > 0][:limit]
        if not top:
            return f"No matches for: {query!r}"
        lines = [f"Top {len(top)} matches for: {query!r}"]
        for score, doc in top:
            lines.append(f"- {doc.rel_path} (score={score:.0f}) - {doc.title}")
        return "\n".join(lines)

    @server.tool(
        name="get_doc",
        description="Return the body of one doc by its path from list_doc_sources.",
    )
    def get_doc(path: str) -> str:
        """Return the full body of the doc whose rel path matches ``path``.

        Parameters
        ----------
        path : str
            Path relative to the docs mirror root, e.g.
            ``src/langgraph/index.mdx``.

        """
        # Reject absolute paths and any traversal that escapes the mirror.
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            return f"Invalid path (must be relative, no '..'): {path}"
        doc = by_path.get(str(candidate).lstrip("/"))
        if doc is None:
            return f"Doc not found: {path}"
        return doc.body

    return server


def _corpus_label(docs_root: Path) -> str:
    """Derive the corpus label from the mirror directory basename.

    Acronyms and mixed-case names are handled via a small lookup so the
    result is ``LangChain``, not ``Langchain``. Unknown stems fall back
    to ``str.title()`` over whitespace-normalized input.

    """
    stem = docs_root.name.strip()
    if not stem or stem in {".", "/"}:
        return "Documentation"
    normalized = stem.replace("-", " ").replace("_", " ").lower()
    # Common dev-tool and framework names whose title-case is wrong.
    acronyms = {
        "langchain": "LangChain",
        "langgraph": "LangGraph",
        "langsmith": "LangSmith",
        "fastapi": "FastAPI",
        "polars": "Polars",
        "numpy": "NumPy",
        "pandas": "pandas",
        "pydantic": "Pydantic",
        "sklearn": "scikit-learn",
    }
    if normalized in acronyms:
        return acronyms[normalized]
    # Two-word cases like "lang chain" still get a sensible title.
    return normalized.title()


def main() -> None:
    """Resolve ``DOCS_PATH``, index it, then run the stdio server."""
    docs_path = os.environ.get("DOCS_PATH") or str(_DEFAULT_DOCS_PATH)
    docs_root = Path(docs_path).expanduser().resolve()
    if not docs_root.is_dir():
        sys.stderr.write(f"DOCS_PATH is not a directory: {docs_root}\n")
        raise SystemExit(2)
    docs = _index_docs(docs_root)
    label = _corpus_label(docs_root)
    logger.info(
        json.dumps(
            {
                "event": "indexed",
                "docs_path": str(docs_root),
                "file_count": len(docs),
                "label": label,
            }
        )
    )
    server = _build_server(docs, label, docs_root)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
