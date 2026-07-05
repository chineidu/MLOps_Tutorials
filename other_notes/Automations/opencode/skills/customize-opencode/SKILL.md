---
name: customize-opencode
description: Use when editing opencode's own configuration - opencode.json, opencode.jsonc, .opencode/, ~/.config/opencode/ files, agents, subagents, skills, plugins, MCP servers, or permission rules.
---

This is a **built-in** skill that ships with opencode. It is NOT a file on disk — it is embedded in the application itself.

## When It Activates

This skill triggers when you work on opencode's own configuration:

- `opencode.json` / `opencode.jsonc` — project-level configuration
- `.opencode/` directory — project-level agents, skills, and settings
- `~/.config/opencode/` — user-level configuration, agents, and skills
- Agent files (`.md` files in agents/ directories)
- Skill files (`SKILL.md` in skills/ directories)
- Subagent definitions
- Plugin configuration
- MCP server configuration
- Permission rules

## Purpose

Prevents accidental misconfiguration of opencode itself by providing expert guidance on:

- JSON schema validation for config files
- Correct frontmatter structure for agents and skills
- Tool permission syntax
- LSP server configuration
- Agent and skill lifecycle management

## Notes

- This skill takes priority when config files are being edited
- It overrides other active skills during opencode configuration tasks
- It cannot be duplicated or overridden by user-created skills
