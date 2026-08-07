import type { Plugin } from "@opencode-ai/plugin";
import { existsSync, readdirSync } from "node:fs";
import { join, dirname, parse } from "node:path";

// ---------------------------------------------------------------------------
// Walk up from `cwd` to find a `pyproject.toml`.  If one is found and a
// `.venv/bin/` directory exists next to it, prepend the venv to PATH and
// set VIRTUAL_ENV.
// ---------------------------------------------------------------------------

/** Cache: project-root → venv bin directory. Only successful lookups are cached. */
const venvCache = new Map<string, string>();

function findProjectRoot(cwd: string): string | null {
    let dir = cwd;
    const root = parse(cwd).root; // ceiling: filesystem root (e.g. "/" on macOS/Linux)
    while (dir !== root) {
        if (existsSync(join(dir, "pyproject.toml"))) {
            return dir;
        }
        const parent = dirname(dir);
        if (parent === dir) break;
        dir = parent;
    }
    return null;
}

function getVenvBin(projectRoot: string): string | null {
    const cached = venvCache.get(projectRoot);
    if (cached !== undefined) return cached;

    const venvDir = join(projectRoot, ".venv");
    if (!existsSync(venvDir)) return null;

    // Platform-aware bin directory
    const binName = process.platform === "win32" ? "Scripts" : "bin";
    const binPath = join(venvDir, binName);

    if (!existsSync(binPath)) return null;

    // Sanity check: bin should contain at least Python
    try {
        const entries = readdirSync(binPath);
        const hasPython = entries.some(
            (e) => e === "python" || e === "python3" || e === "python.exe",
        );
        if (!hasPython) return null;
    } catch (err) {
        console.warn(`[venv-activate] failed to read ${binPath}: ${err}`);
        return null;
    }

    venvCache.set(projectRoot, binPath);
    return binPath;
}

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------
const plugin: Plugin = async (_ctx) => {
    return {
        "shell.env": async (input, output) => {
            const cwd = input.cwd;
            if (!cwd) return;

            const root = findProjectRoot(cwd);
            if (!root) return;

            const venvBin = getVenvBin(root);
            if (!venvBin) return;

            // Prepend the venv to PATH (first match wins)
            const existing = output.env["PATH"] || process.env["PATH"] || "";
            const separator = process.platform === "win32" ? ";" : ":";
            output.env["PATH"] = [venvBin, existing].join(separator);

            // Set VIRTUAL_ENV so tools that check it (e.g. pre-commit, pip)
            // behave as if the venv is active.
            output.env["VIRTUAL_ENV"] = join(root, ".venv");
        },
    };
};

export default plugin;
