# What is a Skill?

## Definition

A **skill** in opencode is a reusable piece of knowledge, capability, or workflow that can be loaded into any agent or conversation. Skills are like "plugins" that extend the AI's knowledge with domain-specific expertise, best practices, or project conventions.

## Key Characteristics

| Aspect | Description |
|--------|-------------|
| **Reusable** | Load once, use across many conversations/agents |
| **Composable** | Multiple skills can be active simultaneously |
| **Scoped** | Global (user), Project (team), or Built-in |
| **Self-contained** | Single directory with `SKILL.md` file |

## When to Use Skills

- **Project conventions** - Code style, testing patterns, architecture (e.g., `python-skills`)
- **Domain knowledge** - Git practices, API design, database patterns
- **Workflow guides** - How to create PRs, deploy, debug
- **Reference material** - FAQs, common commands, troubleshooting
- **Tool configurations** - Linter rules, formatter settings, CI/CD

## Skill vs Agent

| Skill | Agent |
|-------|-------|
| Knowledge/capability | Persona/workflow |
| Loaded into conversation | Replaces conversation |
| Multiple active at once | One active at a time |
| Reference material | Active participant |
| Passive (read-only) | Active (uses tools) |

## Configuration Location

```
Global (user):    ~/.config/opencode/skills/
Project (team):   .opencode/skills/
Built-in:         Included with opencode
```

## Naming Conventions

| Element | Convention | Example | Notes |
|---------|------------|---------|-------|
| Skill name | kebab-case | `git-commit`, `python-skills` | Dashes only. No underscores, spaces, or special chars |
| Skill directory | `<skill-name>/` | `git-commit/` | Matches skill name exactly |
| Skill file | `SKILL.md` | `SKILL.md` | Always literal `SKILL.md` (uppercase) |

## Skill Structure

```
skill-name/
└── SKILL.md   # Main content (required)
```

### SKILL.md Format

```markdown
---
name: skill-name
description: When to use this skill
---

# Skill Title

## Overview
Brief description of what this skill provides.

## Content
Markdown content - can be:
- Guidelines and best practices
- Reference documentation
- Step-by-step procedures
- Code examples
- FAQs

## Usage
How to apply this skill in practice.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | Natural language trigger for auto-loading |

## Loading Skills

Skills can be loaded in several ways:

1. **Auto-loaded** - Based on `description` matching conversation context
2. **Explicit** - User runs `/skill skill-name` command
3. **Agent default** - Agent declares default skills in its config
4. **Project default** - Configured in `.opencode/skill.json`

## Skill Content Types

### 1. Convention Guides (e.g., python-skills)
```
- Code style rules
- Testing patterns
- Project structure
- Common commands
- Architecture notes
```

### 2. Workflow Procedures (e.g., git-commit)
```
- Step-by-step processes
- Output formats
- Examples
- Common pitfalls
```

### 3. Reference Documentation
```
- API references
- Configuration options
- Troubleshooting
- FAQs
```

### 4. Domain Knowledge
```
- Best practices
- Patterns/anti-patterns
- Security guidelines
- Performance tips
```

## Example: Simple Skill

```markdown
---
name: rest-api-design
description: Use when designing or reviewing REST APIs
---

# REST API Design Guidelines

## Principles
- Use nouns for resources: `/users`, not `/getUsers`
- Use HTTP verbs: GET, POST, PUT, PATCH, DELETE
- Version in URL: `/api/v1/users`

## Status Codes
| Code | Use Case |
|------|----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

## Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [...]
  }
}
```
```

## Best Practices

1. **Single responsibility** - One skill per domain
2. **Actionable content** - Include examples, not just theory
3. **Clear triggers** - Description should match real use cases
4. **Keep updated** - Sync with project evolution
5. **Cross-reference** - Link to related skills