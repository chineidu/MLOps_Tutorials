# Guide to Using AI When Learning to Code

> **Use AI to expand and challenge your thinking—not to replace your judgment.**

The real question when learning to code with AI isn't *whether* to use it — it's *which parts of the work* to hand over and which parts have to stay yours. There are two ways to get this wrong, and both are common:

- **Pure memory-only**: refuse AI entirely, and you get stuck on syntax/API details that have nothing to do with the actual learning (e.g. "what's the Qdrant client method signature") and burn your time budget on trivia.
- **Fully AI-assisted**: let autocomplete drive, and your hands write code your brain never actually decided on — the project gets built, but you don't. That's the vibe-coding failure mode.

The split that actually works: **you own the thinking; AI handles the lookup.** This guide draws that line across the full lifecycle — first designing the project with AI's help, then building it in a way that actually makes you learn.

## Table of Contents

- [Guide to Using AI When Learning to Code](#guide-to-using-ai-when-learning-to-code)
  - [Table of Contents](#table-of-contents)
  - [Part I: Designing the Project With AI](#part-i-designing-the-project-with-ai)
    - [The Design Pipeline](#the-design-pipeline)
    - [1. Start With Your Own Rough Idea](#1-start-with-your-own-rough-idea)
    - [2. Ask AI to Interrogate the Idea](#2-ask-ai-to-interrogate-the-idea)
    - [3. Define the Problem and Success](#3-define-the-problem-and-success)
    - [4. Explore Multiple Interpretations](#4-explore-multiple-interpretations)
    - [5. Challenge the Scope](#5-challenge-the-scope)
    - [6. Explore Architecture Options](#6-explore-architecture-options)
    - [7. Defend Your Decisions](#7-defend-your-decisions)
    - [8. Write `plan.md`](#8-write-planmd)
    - [9. Turn the Plan Into Execution](#9-turn-the-plan-into-execution)
  - [Part II: Building While Learning](#part-ii-building-while-learning)
    - [The Split: You Own the Thinking, AI Handles the Lookup](#the-split-you-own-the-thinking-ai-handles-the-lookup)
    - [Design and Interfaces: No AI, `plan.md` Only](#design-and-interfaces-no-ai-planmd-only)
    - [Implementation: AI as a Lookup Tool, Not a Generator](#implementation-ai-as-a-lookup-tool-not-a-generator)
    - [The Signature-First Rule](#the-signature-first-rule)
    - [Predict Before You Run](#predict-before-you-run)
    - [AI as a Critic, Not Just a Lookup](#ai-as-a-critic-not-just-a-lookup)
    - [The Hard Parts: The Ladder of Struggle](#the-hard-parts-the-ladder-of-struggle)
    - [Practical Setup](#practical-setup)
    - [The Implementation Loop](#the-implementation-loop)
    - [What to Use AI For During Implementation](#what-to-use-ai-for-during-implementation)
  - [Part III: Retention: The Part the Rules Above Don't Cover](#part-iii-retention-the-part-the-rules-above-dont-cover)
    - [Rebuild From Memory, No AI, After the Session](#rebuild-from-memory-no-ai-after-the-session)
    - [Keep a Decision Journal](#keep-a-decision-journal)
    - [Review on a Spaced Schedule](#review-on-a-spaced-schedule)
    - [The Honest Test, Weeks Later](#the-honest-test-weeks-later)
  - [Part IV: Compressed Mental Models: The "Why" Chain](#part-iv-compressed-mental-models-the-why-chain)
  - [The Core Principle](#the-core-principle)
  - [The Loop](#the-loop)

---

## Part I: Designing the Project With AI

### The Design Pipeline

When you already have a project topic, don't jump directly from **idea → architecture → code**. Use this process:

```text
Topic
  ↓
Problem
  ↓
Requirements
  ↓
Success Criteria
  ↓
Scope & Constraints
  ↓
Architecture Options
  ↓
Trade-offs & Critique
  ↓
Your Final Decisions
  ↓
plan.md
  ↓
Execution
  ↓
Evaluation
  ↓
Iteration
```

### 1. Start With Your Own Rough Idea

Write down what you currently think the project is.

Don't try to make it perfect.

This gives you a baseline for your own thinking before AI influences it.

### 2. Ask AI to Interrogate the Idea

Use AI to identify:

- What problem am I actually solving?
- Who is the user?
- What capabilities are required?
- What assumptions am I making?
- What's ambiguous or underspecified?
- What makes this a serious engineering project rather than a demo?
- What questions must be answered before designing the system?

**Don't ask for architecture yet.**

### 3. Define the Problem and Success

Refine the topic into a concrete problem statement.

Then define what success means across relevant dimensions:

- Functional correctness
- Quality
- Reliability
- Latency
- Cost
- Operational performance
- Business impact

**Choose the metrics yourself.**

AI can suggest metrics, but you decide what actually matters.

### 4. Explore Multiple Interpretations

Ask AI to propose different ways the project could be framed.

For example:

```text
Project Topic
├── Interpretation A
├── Interpretation B
└── Interpretation C
```

Compare each in terms of:

- Problem solved
- Engineering challenges
- Learning value
- Evaluation strategy
- Complexity

Then choose the framing that best fits your goal.

### 5. Challenge the Scope

Ask AI to critique your proposed scope.

Look for:

- Unnecessary complexity
- Missing requirements
- Hidden dependencies
- Rabbit holes
- Features that look impressive but add little value
- Areas that are under-scoped

Use AI as a **technical reviewer**, not an authority.

### 6. Explore Architecture Options

Only after the problem is clear, ask AI for multiple architectures.

Compare them based on:

- Complexity
- Learning value
- Reliability
- Operational burden
- Scalability
- Failure modes
- Fit for the project's objective

Then make the final architectural decision yourself.

### 7. Defend Your Decisions

For every important decision, be able to explain:

- Why did I choose this?
- What alternatives did I consider?
- What trade-off am I accepting?
- What assumptions does this depend on?
- What evidence would cause me to change it?

A good test:

> **Could I explain this design without AI?**

You don't need to memorize every API or implementation detail.

You should understand the **reasoning behind the system**.

### 8. Write `plan.md`

Create your own project plan containing:

```text
# Problem
# Goal
# Non-goals
# Users
# Constraints
# Success Metrics
# Architecture
# Key Design Decisions
# Alternatives Rejected
# Failure Modes
# Evaluation Strategy
# Milestones
```

Try to write it yourself first.

Then give it to AI for review.

Ask AI to identify:

- Contradictions
- Missing assumptions
- Weak reasoning
- Unclear requirements
- Risky design decisions

Ask it to **critique, not rewrite**.

### 9. Turn the Plan Into Execution

Use AI to convert the approved plan into milestones.

Each milestone should have:

- Objective
- Inputs
- Expected output
- Components affected
- Tests/evaluation
- Definition of done
- Likely failure modes

Prefer milestones that produce a **working, testable increment**.

---

## Part II: Building While Learning

### The Split: You Own the Thinking, AI Handles the Lookup

The split that actually works: **you own the thinking; AI handles the lookup.** The rest of this section is about drawing that line in practice.

### Design and Interfaces: No AI, `plan.md` Only

Before writing any code for a module, write down on paper/notes: what does this class take in, what does it return, what are the 2-3 design decisions it has to make. E.g. for the chunker: "does it return raw strings or objects with metadata? Does overlap happen before or after boundary detection?" This is where the actual learning lives, and it's also fast — it's thinking, not typing.

### Implementation: AI as a Lookup Tool, Not a Generator

Once you know what you want the code to do, you're allowed to ask AI things like "what's the Qdrant Python client call for hybrid search with RRF fusion" or "how do I structure a Pydantic model for this" — that's equivalent to looking up documentation, not outsourcing the thinking. The test: if you can explain in your own words why the code does what it does before you run it, you're fine. If you're pasting an error and accepting whatever fix comes back without understanding why it broke, you've crossed over.

### The Signature-First Rule

**A concrete rule that keeps this honest: write the function signature and a comment describing the logic yourself, first, every time.** Only after that can you ask AI to help fill in or debug. This one habit does most of the work — it forces the design decision to be yours before any code exists, regardless of who typed the implementation.

### Predict Before You Run

Before executing anything, pause and state (out loud or in a comment) what you expect to happen and why: "I expect dense results to dominate this hybrid search because the query has few exact keyword matches." Then run it. Every mismatch between prediction and reality is a bug in your mental model getting fixed for free — that's where a large share of the learning actually lives.

### AI as a Critic, Not Just a Lookup

There's a third mode between lookup and generator: paste your design or code and ask "what assumptions are wrong here?", "what edge cases am I missing?", "would a senior engineer reject this architecture, and why?" Ownership stays with you — AI does review, not authorship — and it's one of the highest-value uses there is.

### The Hard Parts: The Ladder of Struggle

For the genuinely tricky parts (header-breadcrumb algorithm, RRF wiring, failure-mode logic) — struggle with these first, even if it's slower, because this is exactly where engineering judgment is built. But don't make "AI-free" absolute: some problems are hard because they're novel, and grinding past a certain point teaches nothing. Instead, climb this ladder only as far as you actually need:

1. Think it through yourself.
2. Read the documentation.
3. Ask AI for a hint (not a solution).
4. Ask AI to critique your approach.
5. Read a full solution — then close it and rebuild it from memory.

Every rung you skip costs you learning; every rung you climb past what you need costs you learning too. Getting stuck ~30-45 min is a fine trigger to move up one rung — just never jump straight to the bottom, and never leave the ladder without being able to explain the solution in your own words.

### Practical Setup

Close Claude Code/Copilot autocomplete while writing these modules. Keep a separate tab open for "documentation-style" questions only (API lookups, "what does this error mean"). That physical separation makes the boundary real instead of a discipline you have to maintain in your head every 30 seconds.

### The Implementation Loop

Once you're in code, a good loop is:

```text
Choose milestone
    ↓
Understand the problem
    ↓
Attempt your own design
    ↓
Implement
    ↓
Use AI when blocked
    ↓
Test / Evaluate
    ↓
Analyze failures
    ↓
Update plan
    ↓
Repeat
```

### What to Use AI For During Implementation

Use AI to:

- Explain unfamiliar concepts
- Explore alternatives
- Debug
- Review your approach
- Generate tests
- Identify edge cases
- Critique results

Don't blindly accept generated code or designs you don't understand.

---

## Part III: Retention: The Part the Rules Above Don't Cover

Everything above governs how you *learn while building*. But building it once — even honestly, even with the signature-first rule — doesn't mean you'll *remember* it later. Retention is a separate problem and needs its own habits:

### Rebuild From Memory, No AI, After the Session

Within a day or two of finishing a module, close all tabs and re-implement the core of it cold — e.g. write the RRF fusion or the header-breadcrumb logic from memory. The struggle to recall is what actually stamps it in; writing it once with AI nearby is not the same as being able to reproduce it without help. If you can't rebuild it, that's your signal for what to re-study — not a failure, just information.

### Keep a Decision Journal

One short entry per tricky concept or design choice: the problem, your decision, the alternatives you considered, why you rejected them, and what you learned afterward. 2-5 sentences each, in your own words. E.g. "RRF: thought I needed normalized scores; actually it works on raw ranks, which is why score scale doesn't matter." Engineering is mostly decision-making, so a journal of *decisions* transfers across projects in a way API trivia never will — and because the entries are indexed by your own confusions, they're the highest-value study material you'll ever have.

### Review on a Spaced Schedule

Re-read the decision journal ~2 days later, then ~a week later, then ~a month. Re-attempt one rebuild at each review. This is spaced repetition, and it's the difference between "I understood it for an hour" and "I know it." Understanding decays on a predictable curve; each recall flattens it.

### The Honest Test, Weeks Later

Could you explain the design decisions (not the API calls — the *decisions*) to someone without opening the code? If yes, the learning stuck. If no, no amount of AI-free typing during the session saved it — only recall practice does.

---

## Part IV: Compressed Mental Models: The "Why" Chain

API knowledge is trivia; what compounds is knowing *why each layer exists*. For every new concept, answer five questions:

- What problem does this solve?
- Why wasn't the previous solution enough?
- What assumptions does it make?
- When would I *not* use it?
- What simpler idea is this extending?

Example chain: **RAG** exists because LLM context is limited and parametric memory goes stale → **hybrid retrieval** because dense search misses exact keywords → **RRF** because dense and sparse scores aren't directly comparable → **reranking** because retrieval optimizes recall while reranking optimizes precision. Each link is a reusable building block — once the chain is in your head, entirely new systems become combinations of ideas you already own, which is why experienced engineers pick up new stacks so fast.

---

## The Core Principle

> **AI should help you discover the shape of the problem; you should decide what problem you're actually solving.**

The goal is not:

> "Design everything without AI."

The goal is:

> **"Use AI throughout the process while retaining ownership of the important engineering decisions."**

A strong AI-assisted workflow is:

```text
AI expands the search space
        +
You apply judgment
        +
AI critiques your decisions
        +
You make the final call
        +
You verify with evidence
```

**Use AI to think more, not to think less.**

---

## The Loop

This loop isn't specific to this project — it generalizes to basically any technical field.

```text
Understand the problem
        ↓
Design it yourself
        ↓
Write signatures first
        ↓
Implement (AI for lookup and critique only)
        ↓
Predict, then run
        ↓
Test
        ↓
Journal the decisions
        ↓
Rebuild from memory
        ↓
Review on a spaced schedule
```