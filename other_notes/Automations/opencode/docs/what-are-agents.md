# What is an Agent?

## Definition

An **agent** in opencode is a specialized AI persona with custom instructions, tools, and behaviors designed for specific tasks. Think of an agent as a "sub-personality" of the AI that's optimized for a particular domain or workflow.

## Key Characteristics

| Aspect | Description |
|--------|-------------|
| **Custom Instructions** | System prompt tailored to a specific role/task |
| **Tool Access** | Can restrict or extend available tools |
| **Trigger Conditions** | Defined via `description` frontmatter for auto-selection |
| **Portability** | Works across projects (global) or shared with team (project) |

## When to Use Agents

- **Code review specialist** - Focuses on security, performance, style
- **Documentation writer** - Creates docs, READMEs, API docs
- **Test generator** - Writes comprehensive test suites
- **Refactoring expert** - Safely restructures code
- **Debugger** - Systematic bug investigation
- **Architecture advisor** - High-level design decisions

## Agent vs Regular Conversation

| Regular Conversation | Agent |
|---------------------|-------|
| General purpose | Specialized for one domain |
| All tools available | Curated tool set |
| No persistent identity | Consistent persona |
| Ad-hoc instructions | Pre-defined prompt |

## Configuration Location

```
Global (user):    ~/.config/opencode/agents/
Project (team):   .opencode/agents/
```

## Naming Conventions

| Element | Convention | Example | Notes |
|---------|------------|---------|-------|
| Agent name | kebab-case | `code-reviewer`, `test-generator` | Dashes only. No underscores, spaces, or special chars |
| Agent file | `<name>.md` | `code-reviewer.md` | Must match the agent name |

## Agent File Structure

Each agent is a single `.md` file:

```markdown
---
name: agent-name
description: Trigger condition - when to use this agent
tools: [read, write, edit, bash, grep, glob, task, webfetch, websearch]  # optional
---

# System Prompt / Instructions

You are a [role]. Your job is to [specific task].

## Guidelines
- Rule 1
- Rule 2
- Rule 3

## Process
1. Step one
2. Step two
3. Step three

## Examples
[Optional examples of good/bad outputs]
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | Natural language trigger for auto-selection |
| `tools` | No | Array of allowed tools (default: all) |

## Tool Names

Available tools: `read`, `write`, `edit`, `bash`, `glob`, `grep`, `task`, `webfetch`, `websearch`, `question`, `skill`

## Example: Code Review Agent

```markdown
---
name: code-reviewer
description: Use for code reviews - security, performance, best practices
tools: [read, edit, grep, glob, bash]
---

# Code Review Agent

You are a senior engineer performing code reviews. Focus on:

## Security
- No hardcoded secrets
- Input validation
- SQL injection prevention

## Performance
- Avoid N+1 queries
- Efficient algorithms
- Proper indexing

## Style
- Follow project conventions
- Consistent naming
- Clear documentation

## Process
1. Read the changed files
2. Check for security issues
3. Verify performance
4. Suggest improvements
5. Approve or request changes
```