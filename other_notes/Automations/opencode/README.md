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
│   ├── ask-only.md               # Read-only codebase Q&A agent
│   └── research.md               # External docs & dependency research agent
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

## Using Subagents

Subagents are specialized agents that handle focused tasks autonomously. They run in the background and return results when complete.

### Built-in Subagents

| Agent | Description | Permissions |
|-------|-------------|-------------|
| `@ask-only` | Read-only codebase Q&A | No edit, bash, or file writes |
| `@research` | External docs & dependency research | Read-only + can access external dirs |

### How to Invoke

**Automatic dispatch** — the main agent decides which subagent to use based on your request:

```
You: "How does the auth module work?"
→ opencode auto-selects @ask-only
```

**Explicit dispatch** — reference the agent directly:

```
You: "Use @ask-only to explain the database schema"
```

**Via the task tool** — the main agent spawns a subagent programmatically:

```
You: "Research how FastAPI handles dependency injection"
→ main agent dispatches @research with a detailed prompt
```

### Concrete Examples

#### Codebase Q&A with `@ask-only`

```
You: "What does the calculate_metrics function do?"

@ask-only: [reads src/metrics.py, searches for usages]
→ "calculate_metrics takes a DataFrame and returns precision, recall, and
   F1 score. It filters out NaN values before computing. Used in
   src/training/evaluate.py:42 and src/api/routes.py:18."
```

#### Dependency Research with `@research`

```
You: "How does SQLAlchemy 2.0 handle async sessions differently from 1.4?"

@research: [clones sqlalchemy repo, inspects source, reads docs]
→ "In 2.4, AsyncSession uses a separate connection pool...
   [returns with file paths to source evidence]"
```

#### Parallel Research

The main agent can dispatch multiple subagents simultaneously:

```
You: "Compare uv vs poetry for this project"

Main agent dispatches:
  ├─ @research: "Research uv's dependency resolution algorithm"
  └─ @research: "Research poetry's lock file format and resolution"
→ Results merged into a comparison table
```

### Creating Custom Subagents

See [creating-agents.md](docs/creating-agents.md) for a full walkthrough.

Minimal template:

```markdown
---
description: One-line trigger for when to use this agent
mode: subagent
permission:
  edit: deny
  bash: deny
  task: deny
  todowrite: deny
  external_directory: deny
---

You are a [role]. Your purpose is to [goal].

Use this agent when asked to:
- [trigger 1]
- [trigger 2]
```

### Permission Reference

| Permission | `allow` | `deny` |
|------------|---------|--------|
| `edit` | Can write/modify files | Read-only |
| `bash` | Can run shell commands | No command execution |
| `task` | Can spawn its own subagents | Cannot delegate further |
| `todowrite` | Can manage task lists | No task tracking |
| `external_directory` | Can access dirs outside workspace | Restricted to workspace |
| `doom_loop` | Can retry failing operations | Stops on failure |

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