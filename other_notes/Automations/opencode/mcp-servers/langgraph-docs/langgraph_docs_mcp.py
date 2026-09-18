"""Offline docs MCP server (fastmcp version).

Reads markdown files from a local DOCS_PATH mirror and exposes three
tools over stdio: list_doc_sources, search_docs, get_doc. No outbound
network. Corpus label is derived from DOCS_PATH's basename.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from fastmcp import FastMCP

_TOKEN_PATTERN = re.compile(r"[a-z0-9]{3,}")
_DOC_EXTS = {".md", ".mdx"}
_DEFAULT_DOCS_PATH = Path("~/docs-mirror/langchain")

logger = logging.getLogger("docs-mcp")
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler(stream=sys.stderr)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_handler)


@dataclass(slots=True, frozen=True)
class Doc:
    rel_path: str
    title: str
    body: str
    term_freq: dict[str, int] = field(default_factory=dict)


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def _term_frequency(tokens: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for tok in tokens:
        out[tok] = out.get(tok, 0) + 1
    return out

_FRONTMATTER_TITLE = re.compile(r'^title:\s*["\']?([^"\'\n]+)["\']?', re.MULTILINE)

def _title_from_body(body: str, rel_path: str) -> str:
    # Check YAML frontmatter first
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            frontmatter = body[3:end]
            m = _FRONTMATTER_TITLE.search(frontmatter)
            if m:
                return m.group(1).strip()
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return Path(rel_path).stem.replace("-", " ").replace("_", " ")


def _index_docs(docs_root: Path) -> list[Doc]:
    docs: list[Doc] = []
    for path in sorted(docs_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _DOC_EXTS:
            continue
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
        docs.append(Doc(rel_path, title, body, _term_frequency(tokens)))
    return docs


def _score(query_tokens: list[str], doc: Doc) -> float:
    if not query_tokens:
        return 0.0
    tf_score = float(sum(doc.term_freq.get(tok, 0) for tok in query_tokens))
    body_lower = doc.body.lower()
    substring_bonus = float(sum(body_lower.count(tok) for tok in query_tokens))
    return tf_score + substring_bonus


def _corpus_label(docs_root: Path) -> str:
    stem = docs_root.name.strip()
    if not stem or stem in {".", "/"}:
        return "Documentation"
    normalized = stem.replace("-", " ").replace("_", " ").lower()
    acronyms = {
        "langchain": "LangChain", "langgraph": "LangGraph", "langsmith": "LangSmith",
        "fastapi": "FastAPI", "polars": "Polars", "numpy": "NumPy",
        "pandas": "pandas", "pydantic": "Pydantic", "sklearn": "scikit-learn",
    }
    return acronyms.get(normalized, normalized.title())


_docs_path = os.environ.get("DOCS_PATH") or str(_DEFAULT_DOCS_PATH)
DOCS_ROOT = Path(_docs_path).expanduser().resolve()
if not DOCS_ROOT.is_dir():
    sys.stderr.write(f"DOCS_PATH is not a directory: {DOCS_ROOT}\n")
    raise SystemExit(2)

DOCS = _index_docs(DOCS_ROOT)
BY_PATH = {doc.rel_path: doc for doc in DOCS}
LABEL = _corpus_label(DOCS_ROOT)
logger.info(json.dumps({"event": "indexed", "docs_path": str(DOCS_ROOT), "file_count": len(DOCS), "label": LABEL}))

mcp = FastMCP(
    name=f"{LABEL.lower()}-docs",
    instructions=(
        f"Offline {LABEL} docs. Use list_doc_sources to confirm coverage, "
        "search_docs to find relevant pages, and get_doc to read one page."
    ),
)


@mcp.tool
def list_doc_sources() -> str:
    """List the indexed docs corpus and a sample of paths."""
    sample = "\n".join(f"- {d.rel_path}: {d.title}" for d in DOCS[:50])
    return f"{LABEL}\nURL: file://{DOCS_ROOT}\n\nIndexed files ({len(DOCS)} total):\n{sample}"


@mcp.tool
def search_docs(query: str, limit: int = 10) -> str:
    """Rank docs by a query over title and body terms."""
    limit = max(1, min(limit, 50))
    tokens = _tokenize(query)
    if not tokens:
        return f"No tokens in query: {query!r}"
    ranked = sorted(((_score(tokens, d), d) for d in DOCS), key=lambda p: p[0], reverse=True)
    top = [(s, d) for s, d in ranked if s > 0][:limit]
    if not top:
        return f"No matches for: {query!r}"
    lines = [f"Top {len(top)} matches for: {query!r}"]
    lines += [f"- {d.rel_path} (score={s:.0f}) - {d.title}" for s, d in top]
    return "\n".join(lines)


@mcp.tool
def get_doc(path: str) -> str:
    """Return the body of one doc by its path from list_doc_sources."""
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return f"Invalid path (must be relative, no '..'): {path}"
    doc = BY_PATH.get(str(candidate).lstrip("/"))
    if doc is None:
        return f"Doc not found: {path}"
    return doc.body


if __name__ == "__main__":
    mcp.run()