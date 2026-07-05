# OpenCode Agents & Skills Documentation

This directory contains documentation and exact copies of global opencode configurations, agents, and skills for personal reference.

## Directory Structure

```
opencode/
├── README.md                    # This file
├── docs/
│   ├── what-are-agents.md       # Definition and explanation of agents
│   ├── what-are-skills.md       # Definition and explanation of skills
│   ├── creating-agents.md       # Step-by-step guide to create agents
│   └── creating-skills.md       # Step-by-step guide to create skills
├── configs/
│   ├── opencode.jsonc           # Project-level config (from ~/.config/opencode/)
│   └── config.json              # User-level config (from ~/.config/opencode/)
├── agents/
│   └── (empty - no global agents configured)
└── skills/
    ├── git-commit/
    │   └── SKILL.md             # Git commit message skill
    ├── python-skills/
    │   └── SKILL.md             # Python project conventions skill
    └── customize-opencode/
        └── SKILL.md             # Built-in opencode customization skill
```

---

## What is an Agent?

An **agent** in opencode is a specialized AI persona with custom instructions, tools, and behaviors designed for specific tasks. Agents allow you to:

- Define custom system prompts for specific workflows
- Restrict or extend tool access per agent
- Create reusable task-specific assistants
- Share agent configurations across projects

### Agent Configuration Location
- **Global**: `~/.config/opencode/agents/` (user-level, available everywhere)
- **Project**: `.opencode/agents/` (project-level, shared with team)

### Agent Structure
Each agent is a markdown file with frontmatter:
```markdown
---
name: agent-name
description: When to use this agent
tools: [read, write, edit, bash, ...]  # optional, defaults to all
---
# Agent instructions/prompt
```

---

## What is a Skill?

A **skill** in opencode is a reusable piece of knowledge or capability that can be loaded into any agent or conversation. Skills provide:

- Domain-specific knowledge (e.g., Python conventions, Git practices)
- Reusable prompts and workflows
- Project-specific guidance (like AGENTS.md)
- Best practices and conventions

### Skill Configuration Location
- **Global**: `~/.config/opencode/skills/` (user-level)
- **Project**: `.opencode/skills/` (project-level)
- **Built-in**: Included with opencode (e.g., `customize-opencode`)

### Skill Structure
Each skill is a directory with a `SKILL.md` file:
```
skill-name/
└── SKILL.md   # Contains frontmatter + markdown content
```

Frontmatter:
```markdown
---
name: skill-name
description: When to use this skill
---
# Skill content (markdown)
```

---

## Quick Reference

| Concept | Purpose | Scope |
|---------|---------|-------|
| **Agent** | Specialized AI persona for tasks | Global or Project |
| **Skill** | Reusable knowledge/capability | Global, Project, or Built-in |
| **Config** | Tool permissions, LSP settings | Global (`config.json`) or Project (`opencode.jsonc`) |

---

## Source of Configurations

All configs in this directory are **exact copies** from:
- **Global user config**: `~/.config/opencode/`
- **Built-in skills**: opencode's internal skills

Last synced: July 5, 2026