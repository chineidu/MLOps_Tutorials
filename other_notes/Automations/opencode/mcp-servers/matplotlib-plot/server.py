"""Matplotlib chart-rendering MCP server.

Exposes one tool, `render_plot`, that runs plotting code in a fresh
subprocess with the headless Agg backend and saves every open figure to a
temporary plots directory. Returned absolute paths can be read or
previewed directly by the agent; old renders are pruned automatically so
they do not accumulate on disk.
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
import time
from enum import StrEnum
from pathlib import Path

# Force headless rendering before anything can import pyplot.
os.environ.setdefault("MPLBACKEND", "Agg")

from fastmcp import FastMCP

logger = logging.getLogger(__name__)


class PlotFormat(StrEnum):
    """Output formats accepted by the `render_plot` tool."""

    PNG = "png"
    SVG = "svg"
    PDF = "pdf"


# Renders are temporary by default: they live under the OS temp directory,
# which the system reclaims, and are pruned after _PRUNE_AFTER_HOURS. The
# opencode config tree is deliberately avoided - the drift checker treats
# every file under a mapped server directory as syncable. Set PLOT_OUT_DIR
# for a persistent location (never auto-pruned).
_OUT_DIR_OVERRIDE = os.environ.get("PLOT_OUT_DIR")
_OUT_DIR = (
    Path(_OUT_DIR_OVERRIDE).expanduser()
    if _OUT_DIR_OVERRIDE
    else Path(tempfile.gettempdir()) / "opencode-plots"
)

_TIMEOUT_S = 90
_PRUNE_AFTER_HOURS = 12

mcp = FastMCP(
    name="matplotlib-plot",
    instructions=(
        "Render charts with matplotlib (headless Agg backend). Pass Python "
        "code that builds figures with matplotlib.pyplot as plt; every open "
        "figure is saved automatically to a temporary plots directory and "
        "absolute paths are returned. An Agg backend, plt, and numpy are "
        "already set up for the code."
    ),
)

# Child-process template: set up plotting, exec the user code, auto-save all
# open figures, and report results as JSON via a marker file. A per-render
# interpreter keeps style and rcParams changes from leaking between renders.
_CHILD_TEMPLATE = """\
import json, os, sys, traceback

_RESULT_PATH = os.environ["_PLOT_RESULT_PATH"]
_result = {"ok": False, "paths": [], "error": None, "traceback": None}
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np  # required matplotlib dependency; exposed as a convenience

    # Run the user's plotting code; plt and np are pre-imported globals.
    _user_code = os.environ["_PLOT_USER_CODE"]
    exec(compile(_user_code, "<agent plot code>", "exec"), {"plt": plt, "np": np, "__name__": "__main__"})

    fignums = plt.get_fignums()
    if not fignums:
        raise RuntimeError(
            "No figures were created. Build at least one figure, "
            "e.g. fig, ax = plt.subplots()."
        )
    fmt = os.environ["_PLOT_FMT"]
    # base is the output path without extension; append the figure suffix.
    base = os.environ["_PLOT_BASE"]
    figures = [plt.figure(n) for n in fignums]
    suffixes = [""] if len(figures) == 1 else [f"-{i + 1}" for i in range(len(figures))]
    for fig, suffix in zip(figures, suffixes):
        path = f"{base}{suffix}.{fmt}"
        fig.savefig(path, dpi=int(os.environ["_PLOT_DPI"]), bbox_inches="tight", facecolor="white")
        _result["paths"].append(path)
    _result["ok"] = True
except BaseException as exc:
    _result["error"] = f"{type(exc).__name__}: {exc}"
    _result["traceback"] = traceback.format_exc(limit=25)
finally:
    with open(_RESULT_PATH, "w", encoding="utf-8") as fh:
        json.dump(_result, fh)
"""


def _sanitize_name(out_name: str) -> str:
    # Bare file stem only: strip directory components and any suffix.
    name = Path(out_name).name if out_name else ""
    if not name:
        name = f"plot-{time.strftime('%Y%m%d-%H%M%S')}"
    return Path(name).stem


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[-limit:]


def _prune_old_renders() -> None:
    # Bound disk use in the default temp directory; a user-set PLOT_OUT_DIR
    # is treated as persistent and left alone.
    if _OUT_DIR_OVERRIDE:
        return
    cutoff = time.time() - _PRUNE_AFTER_HOURS * 3600
    for path in _OUT_DIR.iterdir():
        try:
            if path.is_file() and path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError as exc:
            # Best effort: a concurrent render or the OS may have removed it.
            logger.debug("Prune skipped %s: %s", path, exc)


@mcp.tool
def render_plot(
    code: str,
    *,
    fmt: PlotFormat = PlotFormat.PNG,
    dpi: int = 130,
    out_name: str = "",
) -> str:
    """Run matplotlib plotting code headlessly and save every open figure.

    Executes `code` in a fresh subprocess with the Agg backend, then saves
    all open figures into a temporary plots directory (the OS temp dir by
    default, or `PLOT_OUT_DIR` when set) using `bbox_inches="tight"`.
    Renders in the default directory are pruned after 12 hours; a
    `PLOT_OUT_DIR` override is never pruned. One open figure saves as
    `<name>.<fmt>`; multiple figures save as `<name>-1.<fmt>`,
    `<name>-2.<fmt>`, ...

    The code runs with this server's privileges and is treated as trusted;
    it is not sandboxed.

    Parameters
    ----------
    code : str
        Python code that creates at least one figure. `plt` and `np` are
        pre-imported; calling `plt.savefig` yourself is optional.
    fmt : PlotFormat
        Output format: png, svg, or pdf.
    dpi : int
        Render resolution for raster formats, 50 to 600.
    out_name : str
        Optional bare file name (no directories). Defaults to
        `plot-<timestamp>`.

    Returns
    -------
    str
        "Saved <N> figure(s):" plus one absolute path per line and any
        captured stdout, or the tail of the traceback when the code
        raised.
    """
    # Validate arguments before paying subprocess startup cost. bool is an
    # int subclass, so reject it explicitly before the range check.
    if isinstance(dpi, bool) or not isinstance(dpi, int) or not 50 <= dpi <= 600:
        return f"dpi must be an integer between 50 and 600, got {dpi!r}."

    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    _prune_old_renders()
    base = str(_OUT_DIR / _sanitize_name(out_name))

    with tempfile.TemporaryDirectory(prefix="plot-mcp-") as tmp:
        result_path = str(Path(tmp) / "result.json")
        env = {
            **os.environ,
            "MPLBACKEND": "Agg",
            "_PLOT_RESULT_PATH": result_path,
            "_PLOT_USER_CODE": code,
            "_PLOT_FMT": fmt.value,
            "_PLOT_DPI": str(dpi),
            "_PLOT_BASE": base,
        }
        try:
            # Runs in a fresh interpreter with a MARKER result file for clean
            # separation of the report from any user stdout noise.
            proc = subprocess.run(
                [sys.executable, "-c", _CHILD_TEMPLATE],
                cwd=_OUT_DIR,
                env=env,
                capture_output=True,
                text=True,
                timeout=_TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return f"Timed out after {_TIMEOUT_S}s; long-running or blocking code?"
        except OSError as exc:
            # Report spawn failures (missing interpreter, permissions)
            # instead of letting them kill the stdio server.
            return f"Failed to start the render subprocess: {exc}"

        try:
            result = json.loads(Path(result_path).read_text(encoding="utf-8"))
        except OSError, json.JSONDecodeError:
            # Crash before the child wrote its result (e.g. hard kill).
            tail = _truncate(proc.stderr, 2000) or _truncate(proc.stdout, 2000)
            return f"Render subprocess failed without a result report:\n{tail}"

    if result["ok"]:
        lines = [
            f"Saved {len(result['paths'])} figure(s):",
            *result["paths"],
            "Use browser.preview or Read to view the file(s).",
        ]
        stdout = _truncate(proc.stdout, 2000)
        if stdout:
            lines.append(f"stdout:\n{stdout}")
        return "\n".join(lines)

    detail = result.get("traceback") or ""
    return f"Plot code raised {result.get('error')}:\n{_truncate(detail, 2000)}"


if __name__ == "__main__":
    mcp.run()
