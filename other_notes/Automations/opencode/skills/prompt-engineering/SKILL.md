---
name: prompt-engineering
description: Prompt engineering for LLM prompts - system prompts, user templates, few-shot examples, XML tags, roles, reasoning and verification steps. Use when writing, reviewing, or improving any LLM prompt, structuring prompt content, adding examples, or tuning model behavior. Triggers on prompt engineering, prompt style, system prompt, user prompt, few-shot, multishot, XML tags, LLM-as-judge, or response format tuning.
---

# Prompt Engineering

Follows Anthropic's prompting best practices (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Apply these rules whenever writing or editing LLM prompts.

## Rules

### 1. Be clear and direct

State the exact output format and constraints. Give instructions as numbered sequential steps when order or completeness matters. If you want above-and-beyond behavior, request it explicitly instead of hoping the model infers it.

### 2. Explain the why

Add the motivation behind a rule (e.g. why a formatting constraint exists) so the model generalizes instead of pattern-matching its letter. The model is smart enough to generalize from the explanation.

### 3. Prefer positive instructions

Say what to do instead of what not to do:

- Instead of: "do not use markdown in your response"
- Try: "write in smoothly flowing prose paragraphs"

### 4. Structure with XML tags

Wrap each content type in consistent, descriptive tags so the model can tell instructions, context, and variable inputs apart. Nest when content has hierarchy.

```xml
<role>...</role>
<instructions>...</instructions>
<context>...</context>
<documents>
  <document index="1">...</document>
  <document index="2">...</document>
</documents>
<input>...</input>
<task>...</task>
```

### 5. Set a role

One sentence in the system prompt focusing behavior and tone (e.g. "You are a helpful coding assistant specializing in Python."). Even a single sentence makes a difference.

### 6. Use few-shot examples

3-5 relevant, diverse examples covering typical and edge cases. Put each in `<example>` tags inside `<examples>` so the model can distinguish them from instructions, and label them as illustrations so they are never mistaken for live input.

### 7. Put longform data first, task last

Documents and variable inputs go above the query and instructions; end with the task. Queries at the end measurably improve response quality on data-rich inputs.

### 8. Ask for reasoning, then verify

Prefer general reasoning guidance ("think thoroughly") over prescriptive step-by-step plans. End with a self-check step ("verify your answer against the stated criteria"). When thinking is disabled, use explicit `<thinking>` and `<answer>` tags to separate reasoning from the final output.

### 9. Do not duplicate the output schema in prose

When a JSON schema, tool definition, or structured-output setting already constrains the format, skip redundant formatting lectures.

## Workflow

1. Read the existing prompt and every test or consumer that asserts on its content before editing.
2. Preserve placeholders, anchors, and output contracts that downstream code or tests depend on.
3. Keep prompt additions token-aware: every line ships on each call, so prefer compact examples and short verification steps.
4. After editing, run the project's checks (format, lint, type check, tests) in the project's stated order.
