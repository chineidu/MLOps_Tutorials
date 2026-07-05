# Creating OpenCode Skills

## Overview

This guide walks through creating custom skills for opencode. Skills are reusable knowledge packages that extend the AI's capabilities with domain-specific expertise.

## Prerequisites

- OpenCode installed and configured
- Understanding of [what skills are](what-are-skills.md)

---

## Step 1: Choose Scope

| Scope | Location | Use Case |
|-------|----------|----------|
| **Global** | `~/.config/opencode/skills/` | Personal, all projects |
| **Project** | `.opencode/skills/` | Team-shared, project-specific |

```bash
# Global
mkdir -p ~/.config/opencode/skills/my-skill

# Project
mkdir -p .opencode/skills/my-skill
```

---

## Step 2: Create Skill Directory

```bash
# Skill name in kebab-case
mkdir -p ~/.config/opencode/skills/rest-api-design
```

### Naming Rules

| Aspect | Rule | Example |
|--------|------|---------|
| Directory name | kebab-case (dashes only) | `rest-api-design` |
| Skill file | Exactly `SKILL.md` (uppercase, no variation) | `SKILL.md` |
| Underscores in name | ❌ Not supported | `rest_api_design` → will NOT work |
| Whitespaces in name | ❌ Not supported | `rest api design` → will NOT work |
| Special chars in name | ❌ Not supported | `rest@api` → will NOT work |

**Always use kebab-case for the directory, and the file must be literal `SKILL.md`.**

---

## Step 3: Create SKILL.md

```bash
touch ~/.config/opencode/skills/rest-api-design/SKILL.md
```

---

## Step 4: Write Frontmatter

```markdown
---
name: rest-api-design
description: Use when designing or reviewing REST APIs
---
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique kebab-case identifier (matches directory) |
| `description` | Yes | Natural language trigger for auto-loading |

---

## Step 5: Write Skill Content

```markdown
---
name: rest-api-design
description: Use when designing or reviewing REST APIs
---

# REST API Design Guidelines

## Overview
This skill provides best practices for designing RESTful APIs that are consistent, scalable, and maintainable.

## Resource Naming
- Use plural nouns: `/users`, `/orders`, `/products`
- Use kebab-case: `/user-profiles`, not `/userProfiles`
- Nest for relationships: `/users/{id}/orders`

## HTTP Methods
| Method | Use Case | Idempotent |
|--------|----------|------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | Yes* |
| DELETE | Remove resource | Yes |

* PATCH idempotency depends on implementation

## Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

## Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {"field": "email", "issue": "Invalid format"}
    ]
  }
}
```

## Versioning
- Include version in URL: `/api/v1/users`
- Maintain backward compatibility
- Deprecate with `Sunset` header

## Pagination
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

## Rate Limiting Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1699999999
```

## Usage
Load this skill when:
- Designing new API endpoints
- Reviewing API changes
- Debugging API issues
- Onboarding new team members
```

---

## Step 6: Test the Skill

```bash
# Start opencode
opencode

# Skill should auto-load based on description
# Or manually: /skill rest-api-design
```

Test with an API task:
> "Design a REST API for a user management system"

---

## Step 7: Iterate and Refine

1. Test with real scenarios
2. Add missing content based on questions
3. Refine description for better auto-loading
4. Cross-reference related skills

---

## Complete Example: Python Project Conventions Skill

**Directory**: `.opencode/skills/python-conventions/`

**File**: `SKILL.md`

```markdown
---
name: python-conventions
description: Use for Python code style, testing, and project conventions
---

# Python Project Conventions

## Environment
- **Python**: 3.11+
- **Package manager**: uv
- **Virtual env**: Auto-managed by uv

## Commands
| Task | Command |
|------|---------|
| Install deps | `uv sync --dev` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run ty check` |

## Code Style
- **Formatter**: Ruff (100 char line length)
- **Linter**: Ruff (all warnings = errors)
- **Types**: ty (strict mode)
- **Docstrings**: NumPy style for public APIs

## Naming
| Element | Convention |
|---------|------------|
| Functions/vars | `snake_case` |
| Classes | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` |
| Private | `_leading_underscore` |

## Testing
- **Framework**: pytest
- **Location**: `tests/` mirroring `src/`
- **Coverage**: 80% minimum
- **Structure**:
```python
class TestClassName:
    def test_method_scenario_expected(self, fixture):
        # Given
        ...
        # When
        ...
        # Then
        ...
```

## Project Structure
```
.
├── src/
│   └── package/
├── tests/
├── scripts/
├── docs/
├── pyproject.toml
└── AGENTS.md
```

## Dependencies
- Add: `uv add <pkg>` or `uv add --dev <pkg>`
- Commit: `pyproject.toml` + `uv.lock`
- Never edit pyproject.toml manually for deps

## Constraints
- No `print()` in library code (use logging)
- No `subprocess` without review
- No hardcoded secrets
- No silent exception swallowing
```

---

## Skill Content Patterns

### Pattern 1: Reference Guide
```markdown
# Topic Reference

## Quick Lookup
| Scenario | Solution |
|----------|----------|

## Details
### Section 1
...

### Section 2
...
```

### Pattern 2: Workflow/Procedure
```markdown
# Workflow Name

## When to Use
...

## Prerequisites
...

## Steps
1. Step one
2. Step two
3. Step three

## Verification
...

## Troubleshooting
| Issue | Fix |
```

### Pattern 3: Best Practices
```markdown
# Best Practices for X

## Principles
- Principle 1
- Principle 2

## Do's
✅ Good example

## Don'ts
❌ Bad example

## Examples
...
```

---

## Best Practices

1. **Focused scope** - One skill per clear domain
2. **Actionable content** - Include examples, commands, templates
3. **Clear triggers** - Description matches real questions
4. **Maintainable** - Easy to update as conventions evolve
5. **Cross-link** - Reference related skills

---

## Loading Skills in Agents

Agents can declare default skills:

```markdown
---
name: api-designer
description: Design REST APIs
tools: [read, write, edit]
skills: [rest-api-design, python-conventions]
---
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not auto-loading | Make description more specific |
| Content not applied | Check frontmatter name matches directory |
| Outdated info | Update SKILL.md directly |
| Conflicts with other skills | Use more specific descriptions |