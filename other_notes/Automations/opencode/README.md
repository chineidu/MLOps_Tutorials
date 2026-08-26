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
│   ├── creating-skills.md       # Step-by-step guide to create skills
│   └── permission-system.md     # How opencode's permission system works (investigation notes)
├── configs/
│   └── opencode.jsonc           # Global config (from ~/.config/opencode/)
├── command/
│   ├── changelog.md             # `/changelog` slash command: draft next CHANGELOG.md entry
│   ├── check-opencode-drift.md  # `/check-opencode-drift` slash command: verify global vs project drift
│   ├── commit.md                # `/commit` slash command: stage all + commit with generated message
│   ├── sync-opencode.md         # `/sync-opencode` slash command: sync global config to docs mirror
│   └── validate.md              # `/validate` slash command: review uncommitted changes (read-only)
├── agents/
│   ├── ask-only.md               # Read-only codebase Q&A agent (minimax-m3)
│   ├── brainstorm.md             # Progressive idea development (primary agent, minimax-m3)
│   ├── debug.md                  # Diagnoses failing `make check` runs (deepseek-v4-flash)
│   ├── research.md               # External docs & dependency research agent (muse-spark-1.2-contributor)
│   └── review.md                 # Diff review agent (used by /validate, longcat-2.0)
├── plugins/
│   └── venv-activate.ts          # Auto-activate Python venv in shell tool
├── archives/
│   └── auto-approve-pipes.ts     # DEAD plugin (permission.ask hook never fires in 1.18.x)
└── skills/
     ├── cause-and-effect/
     │   └── SKILL.md             # Root-cause / Fishbone analysis skill
     ├── changelog/
     │   └── SKILL.md             # Keep a Changelog conventions skill
     ├── critique/
     │   └── SKILL.md             # Multi-perspective code review skill
     ├── git-commit/
     │   └── SKILL.md             # Git commit message skill
     ├── jupyter-notebook/
     │   └── SKILL.md             # Python → Jupyter notebook (jupytext) skill
     ├── polars/
     │   └── SKILL.md             # Polars lazy-API data work skill
     ├── thought-based-reasoning/
     │   └── SKILL.md             # Chain-of-Thought reasoning techniques skill
     ├── python-skills/
     │   └── SKILL.md             # Python project conventions skill (local)
     └── customize-opencode/
         └── SKILL.md             # Built-in opencode customization skill (local)
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

### Primary Agents

| Agent | Description | Model | Permissions |
|-------|-------------|-------|-------------|
| `brainstorm` | Progressive idea development through dialogue before plan/build | `opencode-go/minimax-m3` | edit ask; bash read-only allow (`ls`/`cat`/`grep`/`git status`/`log` etc.), else ask; todowrite deny |

### Built-in Subagents

| Agent | Description | Model | Permissions |
|-------|-------------|-------|-------------|
| `@ask-only` | Read-only codebase Q&A | `opencode-go/minimax-m3` | No edit, bash, task, todowrite, external_directory deny |
| `@research` | External docs & dependency research | `opencode-go/muse-spark-1.2-contributor` | Read-only + external_directory allow |
| `@debug` | Diagnoses failing `make check` runs | `opencode-go/deepseek-v4-flash` | edit deny; bash allow; task deny |
| `@review` | Diff review (plan → code gaps, scope creep, etc.) | `opencode-go/longcat-2.0` | edit deny; bash limited to git diff/log/status/show |

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

#### Idea development with `brainstorm`

```
You: "I want to add caching to the API"

brainstorm: [asks one clarifying question at a time]
→ explores goals, constraints, and options through dialogue
→ does not implement; hand off to plan/build when ready
```

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

## What is a Command?

A **command** (or slash command) in opencode is a custom shortcut triggered via `/commandname` in the chat. Commands allow you to:

- Execute multi-step workflows with a single short invocation
- Combine skills, agents, and shell commands into repeatable routines
- Define them globally (`~/.config/opencode/command/`) or per-project (`.opencode/command/`)

### Available Commands

| Command | File | Description |
|---------|------|-------------|
| `/commit` | `command/commit.md` | Stage all changes (`git add -A`), load the `git-commit` skill to generate a message, show the proposed message, then commit. Pass `--quick`/`-Q` to skip the review step. Optional arguments are treated as extra context for the message. |
| `/changelog` | `command/changelog.md` | Gather commits/diff since the last release and draft the next `CHANGELOG.md` entry using the `changelog` skill. |
| `/validate` | `command/validate.md` | Dispatch the `review` subagent to review uncommitted changes. Validate-only — never builds, edits, fixes, or commits. |
| `/sync-opencode` | `command/sync-opencode.md` | Sync global `~/.config/opencode/` agents/commands/skills to this docs mirror. |
| `/check-opencode-drift` | `command/check-opencode-drift.md` | Verify global config has not drifted from the mirror; report mismatches. |

### `/commit` Usage

```
/commit                                   # Stage all + generate message from diff
/commit --quick                           # Skip the review step
/commit fix the login redirect bug        # Same, but with extra context for the message
```

The command:
1. Runs `git status` to inspect the working tree
2. Stages everything with `git add -A`
3. Runs a code review on the staged changes
4. Inspects the staged diff
5. Loads the `git-commit` skill to produce a conventional commit message
6. Shows the message to the user, then commits
7. Prints the commit hash and summary

**Constraint:** Does not push, amend, or force-push. If a pre-commit hook fails, it reports and stops.

---

## Quick Reference

| Concept | Purpose | Scope |
|---------|---------|-------|
| **Agent** | Specialized AI persona for tasks | Global or Project |
| **Skill** | Reusable knowledge/capability | Global, Project, or Built-in |
| **Command** | Custom slash command for multi-step workflows | Global (`~/.config/opencode/command/`) or Project (`.opencode/command/`) |
| **Config** | Tool permissions, LSP settings | Global (`opencode.jsonc`) or Project (`opencode.jsonc`) |

---

## Source of Configurations

All configs in this directory are **exact copies** from:
- **Global user config**: `~/.config/opencode/`
- **Built-in skills**: opencode's internal skills

Last synced: August 26, 2026 — models: brainstorm/minimax-m3, ask-only/minimax-m3, debug/deepseek-v4-flash, review/longcat-2.0, research/muse-spark-1.2-contributor

---

## Archived Plugins

The `archives/` directory contains plugins that are no longer active but kept
for reference. Each archived plugin includes a header explaining why it was
retired.

| Plugin | Reason |
|--------|--------|
| `auto-approve-pipes.ts` | Relied on the `permission.ask` plugin hook, which is declared in the type definition but never invoked at runtime in opencode 1.18.x. opencode's native bash permission rules are believed to already split chained commands and evaluate each segment independently, though this isn't fully proven. See [docs/permission-system.md](docs/permission-system.md). |
