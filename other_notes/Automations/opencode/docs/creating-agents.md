# Creating OpenCode Agents

## Overview

This guide walks through creating custom agents for opencode. Agents are specialized AI personas with custom instructions and tool access.

## Prerequisites

- OpenCode installed and configured
- Understanding of [what agents are](what-are-agents.md)

---

## Step 1: Choose Scope

| Scope | Location | Use Case |
|-------|----------|----------|
| **Global** | `~/.config/opencode/agents/` | Personal, all projects |
| **Project** | `.opencode/agents/` | Team-shared, project-specific |

```bash
# Global
mkdir -p ~/.config/opencode/agents

# Project
mkdir -p .opencode/agents
```

---

## Step 2: Create Agent File

Create a markdown file: `<agent-name>.md`

### Naming Rules

| Aspect | Rule | Example |
|--------|------|---------|
| Name | kebab-case (dashes only) | `code-reviewer`, `test-generator` |
| File extension | `.md` | `code-reviewer.md` |
| Underscores | ❌ Not supported | `code_reviewer.md` → will NOT work |
| Whitespaces | ❌ Not supported | `code reviewer.md` → will NOT work |
| Special chars | ❌ Not supported | `code@reviewer.md` → will NOT work |

**Always use kebab-case**: `my-agent-name.md`

```bash
# Global example
touch ~/.config/opencode/agents/code-reviewer.md

# Project example
touch .opencode/agents/test-generator.md
```

---

## Step 3: Write Frontmatter

```markdown
---
name: code-reviewer
description: Use for code reviews - security, performance, best practices
tools: [read, edit, grep, glob, bash]
---
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique kebab-case identifier |
| `description` | Yes | Natural language trigger for auto-selection |
| `tools` | No | Array of allowed tools (default: all) |

### Tool Names

| Tool | Description |
|------|-------------|
| `read` | Read files |
| `write` | Create files |
| `edit` | Modify files |
| `bash` | Run commands |
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `task` | Launch sub-agents |
| `webfetch` | Fetch web content |
| `websearch` | Search the web |
| `question` | Ask user questions |
| `skill` | Load skills |

---

## Step 4: Write System Prompt

```markdown
---
name: code-reviewer
description: Use for code reviews - security, performance, best practices
tools: [read, edit, grep, glob, bash]
---

# Code Review Agent

You are a senior engineer performing code reviews. Your focus:

## Security
- No hardcoded secrets or API keys
- Input validation on all user data
- SQL injection prevention
- XSS protection

## Performance
- No N+1 database queries
- Efficient algorithms (avoid O(n²) where O(n log n) works)
- Proper database indexing
- Caching strategies

## Code Quality
- Follows project conventions (see python-skills skill)
- Clear, descriptive naming
- Appropriate abstraction levels
- No code duplication

## Process
1. Read all changed files
2. Run linter/type checker if available
3. Check for security issues
4. Verify tests exist for new code
5. Provide specific, actionable feedback
6. Approve or request changes with clear reasoning

## Output Format
```
## Review Summary
- **Status**: Approve / Request Changes
- **Priority**: Critical / Major / Minor / Nitpick

## Issues
### Critical
- [File:line] Description

### Major
- [File:line] Description

### Minor
- [File:line] Description
```
```

---

## Step 5: Test the Agent

```bash
# Start opencode
opencode

# Agent should auto-select based on description
# Or manually: /agent code-reviewer
```

Test with a code review task:
> "Review the changes in the auth module for security issues"

---

## Step 6: Iterate and Refine

1. Test with real tasks
2. Adjust prompt based on output quality
3. Tune tool permissions
4. Refine description for better auto-selection

---

## Complete Example: Test Generator Agent

**File**: `.opencode/agents/test-generator.md`

```markdown
---
name: test-generator
description: Use when writing tests for new or existing code
tools: [read, write, edit, glob, grep, bash]
---

# Test Generator Agent

You are a test engineering expert. Write comprehensive, maintainable tests.

## Principles
- Test behavior, not implementation
- One assertion per test (generally)
- Descriptive test names: `test_<method>_<scenario>_<expected>`
- Use pytest fixtures for setup
- Mock external dependencies

## Test Structure
```python
class Test<ClassName>:
    def test_<method>_<scenario>_<expected>(self, fixture):
        # Given
        ...
        # When
        ...
        # Then
        ...
```

## Coverage Targets
- New code: 90%+
- Critical paths: 100%
- Edge cases: Required

## Process
1. Read the implementation
2. Identify public API
3. List test scenarios (happy path, edge cases, errors)
4. Write tests using project conventions
5. Run tests to verify
```

---

## Best Practices

1. **Single responsibility** - One agent per distinct role
2. **Clear triggers** - Description should match natural requests
3. **Minimal tools** - Restrict tools to what's needed
4. **Iterative prompts** - Refine based on actual usage
5. **Version control** - Track agent files in git (project scope)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not auto-selecting | Make description more specific |
| Tool permission denied | Add tool to `tools` array |
| Poor output quality | Refine prompt with more examples |
| Agent not found | Check file location and `.md` extension |