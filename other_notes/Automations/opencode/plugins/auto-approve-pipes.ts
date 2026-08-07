import type { Plugin } from "@opencode-ai/plugin";

// ---------------------------------------------------------------------------
// Commands that are NEVER auto-approved in a chain, even if the config
// contains an "allow" pattern.  These are destructive, mutative, or able to
// reach the network.
// ---------------------------------------------------------------------------
const DANGEROUS_COMMANDS = new Set([
    // Filesystem destruction / mutation
    "rm",
    "mv",
    "dd",
    "chmod",
    "chown",
    "chgrp",
    "mkfs",
    "mkswap",
    "swapon",
    "mount",
    "umount",
    "fdisk",
    "parted",
    "mkfs.ext4",
    "mkfs.fat",

    // System state
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
    "systemctl",
    "service",
    "launchctl",

    // Firewall / networking
    "iptables",
    "nft",
    "ip6tables",
    "ufw",
    "firewall-cmd",

    // Process signals
    "kill",
    "killall",
    "pkill",

    // Scheduled / background
    "crontab",
    "at",
    "batch",

    // Privilege escalation
    "su",
    "sudo",
    "doas",

    // User / group management
    "passwd",
    "chpasswd",
    "usermod",
    "useradd",
    "userdel",
    "groupadd",
    "groupmod",
    "groupdel",

    // Network clients
    "wget",
    "curl",
    "nc",
    "telnet",
    "ssh",
    "scp",
    "rsync",
    "ftp",
    "sftp",

    // Git write operations
    "git push",
    "git commit",
    "git add",
    "git rm",
    "git reset",
    "git rebase",
    "git merge",
    "git cherry-pick",
    "git revert",
    "git stash",
    "git branch -d",
    "git branch -D",
    "git tag -d",

    // Package managers (install / uninstall)
    "npm publish",
    "npm install",
    "npm uninstall",
    "npm update",
    "pip install",
    "pip uninstall",
    "uv pip install",
    "uv add",
    "uv remove",
    "brew install",
    "brew uninstall",

    // Container / orchestration
    "docker",
    "podman",
    "kubectl",
    "helm",

    // Shell built-ins that can execute or mutate
    "eval",
    "exec",
    "source",
]);

// ---------------------------------------------------------------------------
// Split a shell command on chain operators (|, |&, &&, ||, ;) while
// respecting single- and double-quoted strings.
// ---------------------------------------------------------------------------
function splitChainedCommand(command: string): string[] {
    const segments: string[] = [];
    let current = "";
    let inSingle = false;
    let inDouble = false;
    let i = 0;

    while (i < command.length) {
        const c = command[i];

        if (c === "'" && !inDouble) {
            inSingle = !inSingle;
            current += c;
        } else if (c === '"' && !inSingle) {
            inDouble = !inDouble;
            current += c;
        } else if (!inSingle && !inDouble) {
            if (c === "|" && command[i + 1] === "&") {
                const trimmed = current.trim();
                if (trimmed) segments.push(trimmed);
                current = "";
                i += 1;
            } else if (c === "|" && command[i + 1] === "|") {
                const trimmed = current.trim();
                if (trimmed) segments.push(trimmed);
                current = "";
                i += 1;
            } else if (c === "&" && command[i + 1] === "&") {
                const trimmed = current.trim();
                if (trimmed) segments.push(trimmed);
                current = "";
                i += 1;
            } else if (c === "|" || c === ";") {
                const trimmed = current.trim();
                if (trimmed) segments.push(trimmed);
                current = "";
            } else {
                current += c;
            }
        } else {
            current += c;
        }
        i++;
    }

    const trimmed = current.trim();
    if (trimmed) segments.push(trimmed);
    return segments;
}

// ---------------------------------------------------------------------------
// Check whether a sub-command matches an opencode-style permission pattern.
//
// Patterns:
//   "command *"  → must start with "command " (space required)
//   "command"    → exact match
//   "*"          → match everything
// ---------------------------------------------------------------------------
function commandMatchesPattern(command: string, pattern: string): boolean {
    if (pattern === "*") return true;
    if (pattern === command) return true;

    if (pattern.endsWith(" *")) {
        const prefix = pattern.slice(0, -2);
        return command.startsWith(prefix + " ");
    }

    return false;
}

// ---------------------------------------------------------------------------
// Return true if the command (or any 2- or 3-word prefix of it) is in the
// dangerous-commands deny-list.
// ---------------------------------------------------------------------------
function isCommandDangerous(command: string): boolean {
    const trimmed = command.trim();
    const words = trimmed.split(/\s+/);
    if (words.length === 0) return false;

    for (let len = 1; len <= Math.min(words.length, 3); len++) {
        const prefix = words.slice(0, len).join(" ");
        if (DANGEROUS_COMMANDS.has(prefix)) return true;
    }

    return false;
}

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------
const plugin: Plugin = async (_ctx) => {
    // Populated by the config hook — patterns with action === "allow",
    // excluding the "*" catch-all.
    let allowPatterns: string[] = [];

    return {
        // Receive the already-parsed merged config.  No I/O, no HTTP —
        // cannot hang at startup.
        config: (cfg) => {
            const bashPerm = cfg.permission?.bash;
            if (bashPerm && typeof bashPerm === "object") {
                for (const [pattern, action] of Object.entries(bashPerm)) {
                    if (pattern !== "*" && action === "allow") {
                        allowPatterns.push(pattern);
                    }
                }
            }
        },

        "permission.ask": async (input, output) => {
            if (input.type !== "bash") return;

            const command = input.title;
            if (!command) return;

            const segments = splitChainedCommand(command);

            // Single command — let opencode's normal permission rules decide.
            if (segments.length <= 1) return;

            // Multi-segment chain — check each segment.
            for (const segment of segments) {
                // Never auto-allow a dangerous command in a chain.
                if (isCommandDangerous(segment)) return;

                // Must match at least one explicit "allow" pattern.
                const allowed = allowPatterns.some((pattern) =>
                    commandMatchesPattern(segment, pattern),
                );
                if (!allowed) return;
            }

            // Every segment is individually allowed and not dangerous.
            output.status = "allow";
        },
    };
};

export default plugin;
