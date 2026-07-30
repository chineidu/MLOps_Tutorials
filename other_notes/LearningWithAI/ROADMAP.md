# Portfolio Roadmap
- [Portfolio Roadmap](#portfolio-roadmap)
  - [How to Think Like an AI Engineer](#how-to-think-like-an-ai-engineer)
    - [Core Philosophy](#core-philosophy)
    - [Before Writing Code](#before-writing-code)
    - [The Engineering Loop](#the-engineering-loop)
    - [Experiment Discipline](#experiment-discipline)
    - [Understand Failures](#understand-failures)
    - [Think in Trade-offs](#think-in-trade-offs)
    - [Measure the Right Things](#measure-the-right-things)
    - [Treat AI Like Systems, Not Prompts](#treat-ai-like-systems-not-prompts)
    - [Production Thinking](#production-thinking)
    - [Document Every Iteration](#document-every-iteration)
    - [Keep a Project Journal (`notes.md`)](#keep-a-project-journal-notesmd)
    - [The Progression of an AI Engineer](#the-progression-of-an-ai-engineer)
    - [What Makes a Project Impressive](#what-makes-a-project-impressive)
  - [Guiding Principles](#guiding-principles)
  - [The Progression](#the-progression)
  - [Project 1 — FastAPI RAG + Evaluation Harness](#project-1--fastapi-rag--evaluation-harness)
  - [Project 2 — AI Coding Agent / Software Engineering Agent](#project-2--ai-coding-agent--software-engineering-agent)
  - [Project 3 — Financial Document Intelligence Platform](#project-3--financial-document-intelligence-platform)
  - [Project 4 — LLMOps Platform](#project-4--llmops-platform)
  - [Project 5 — Underwriting / Decision Support Agent](#project-5--underwriting--decision-support-agent)
  - [Summary](#summary)

A five-project portfolio roadmap synthesised from conversations with Claude and GPT.
The goal: a coherent progression from **retrieval → agents → real-world data → infrastructure → high-stakes application**, with evaluation as a cross-cutting requirement throughout.

---

## How to Think Like an AI Engineer

> **Build systems you can understand, measure, improve, and trust; not just demos that happen to work.**

The goal isn't to build AI that works. The goal is to build AI systems whose behaviour you can **explain, measure, improve, and trust**.

### Core Philosophy

Every project must answer four questions:

1. What problem am I solving?
2. How will I know if my solution is better?
3. Why did performance change?
4. Would I trust this in production?

### Before Writing Code

If you can't answer these, you're coding too early:

- What is the actual problem? What assumptions am I making?
- What does success look like? How will I measure it?
- What baseline am I comparing against?
- What trade-offs am I accepting?

### The Engineering Loop

```text
Problem → Hypothesis → Define Success Metrics → Establish Baseline
       → Implement One Change → Evaluate → Analyze Failure Modes
       → Decide → Document → Repeat
```

### Experiment Discipline

- **Build around experiments.** Treat every feature as a hypothesis to verify, not a feature to ship. *"Reranking will improve Answer Correctness because it filters noisy retrieval results"* — then prove it.
- **Change one variable at a time.** New model *or* new prompt *or* new chunking — never all at once. Measure, then continue.
- **Metrics are evidence, not goals.** A higher number isn't automatically a better system. Ask why it changed, what trade-off it introduced, and who it helps or hurts.

### Understand Failures

Every evaluation should answer: *What failed? Why? Can failures be grouped? Which matter most? Which are worth fixing?*

Failure analysis is often more valuable than average scores.

### Think in Trade-offs

Every decision costs something. Engineering is choosing trade-offs intentionally:

- Accuracy vs latency · Accuracy vs cost · Recall vs precision
- Simplicity vs flexibility · Automation vs human review · Context size vs model confusion

### Measure the Right Things

| Technical        | LLM Systems               | Business                    |
| ---------------- | ------------------------- | --------------------------- |
| Accuracy         | Answer correctness        | Time saved                  |
| Precision / Recall | Retrieval quality       | Money saved                 |
| F1               | Hallucination rate        | Manual work reduced         |
| Latency          | Citation quality         | Customer satisfaction       |
| Throughput       | Tool success rate        | Risk reduced                |
| Cost             | Structured output validity |                             |
| Reliability      | Human review rate        |                             |

Choose metrics that reflect the real objective.

### Treat AI Like Systems, Not Prompts

The prompt is one component. Think about the whole system: data, retrieval, models, prompts, tools, caching, evaluation, monitoring, human review, deployment, cost, observability.

### Production Thinking

A working prototype is not a production system. Ask:

- What happens if the model is wrong, retrieval fails, or an API times out?
- Can this be monitored, debugged, and recovered gracefully?
- Can humans intervene? Is it cost-effective?

### Document Every Iteration

Record: Problem · Hypothesis · Baseline · Change Made · Results · Unexpected Outcomes · Failure Analysis · Decision · Next Experiment.

Good engineering leaves evidence behind.

### Keep a Project Journal (`notes.md`)

Every project must include a `notes.md` — a short write-up narrating **what was tried, what worked, what didn't, and why**. This is the part that reads as **senior-level judgment** in interviews or a portfolio, not the code itself. The code shows *what* you built; the journal shows *how you thought*.

For each experiment, capture:

- Problem & hypothesis
- Baseline and metric definition
- Single change made
- Results (with numbers)
- Failure analysis — what broke and why
- Decision and rationale
- Next experiment

A repo with clean code but no story is forgettable. A repo with a `notes.md` that walks through honest trade-offs, dead ends, and reasoning is what makes a portfolio memorable.

### The Progression of an AI Engineer

```text
Can I build it? → measure it? → explain it? → trust it?
              → operate it? → safely deploy it?
```

### What Makes a Project Impressive

Not *"I built an agent."*

But *"I identified a failure mode, designed an intervention, measured the improvement, analyzed remaining failures, and documented the trade-offs."*

---

## Guiding Principles

1. **Evaluation is not a project — it is a requirement for every project.**
   Each project must define what "good" means and measure it. The portfolio demonstrates the ability to *measure and systematically improve* AI systems, not just build them.

2. **Three generalist + two fintech projects.**
   - Generalist: RAG, Coding Agent, LLMOps
   - Fintech: Financial Document Intelligence, Underwriting Agent

3. **Build from scratch, don't wrap frameworks.**
   Avoid LangChain/LlamaIndex and agent-framework wrappers initially. The interesting engineering is the machinery underneath, not the orchestration glue.

4. **Demonstrate the gap between "works" and "production-trustworthy."**
   Ademo should show measurable trade-offs (cost, latency, quality), not just a working UI.

---

## The Progression

| #   | Project                             | Core Question                                                                |
| --- | ----------------------------------- | ---------------------------------------------------------------------------- |
| 1   | RAG + Evaluation Harness            | Can I **measure and improve** an AI system?                                  |
| 2   | AI Coding Agent                     | Can I build a **reliable agent that takes action**?                          |
| 3   | Financial Document Intelligence     | Can I make AI **reliable on messy real-world data**?                          |
| 4   | LLMOps Platform                     | Can I **operate AI reliably and economically**?                              |
| 5   | Underwriting / Decision Agent       | Can I combine all of this into a **high-stakes, human-governed workflow**?   |

Each project builds on prior capabilities and layers a new category of difficulty:

- **Project 1** → Learn to *measure* AI
- **Project 2** → Measure *agent task success*
- **Project 3** → Measure *extraction quality* on messy inputs
- **Project 4** → Measure *reliability + cost + latency* at scale
- **Project 5** → Measure *end-to-end workflow quality* with human oversight

---

## Project 1 — FastAPI RAG + Evaluation Harness

**Category:** Generalist — Foundation

**Core question:**
> Can I measure and systematically improve retrieval and answer quality?

**Focus areas:**

- Ingestion
- Parsing
- Chunking (structure-aware)
- Embeddings
- Vector search
- BM25
- Hybrid retrieval
- Reranking
- Generation
- Retrieval evaluation
- Answer evaluation
- Experiment tracking

**Senior-level evidence of completion:**
> "Structure-aware chunking improved hit@5 from X% → Y%; hybrid retrieval improved recall on multi-hop queries by Z%; reranking improved answer correctness from A% → B%."

---

## Project 2 — AI Coding Agent / Software Engineering Agent

**Category:** Generalist — Agents + Context Engineering

**Core question:**
> Can I build an agent that reliably completes real multi-step tasks rather than merely calling tools?

**Agent loop:**

```text
User task
    → Understand repository
    → Build context
    → Plan
    → Search / inspect
    → Edit
    → Run tests
    → Analyze failures
    → Fix
    → Verify
    → Final diff
```

**Core tools:**

- File search
- grep / ripgrep
- Symbol / AST search
- File reading
- Patch / edit
- Shell execution
- Test execution
- git diff

**Advanced capabilities:**

- Repository indexing
- Dependency graph
- Context selection & compression
- Planning
- Retry loops
- Test-driven verification
- Checkpointing
- Long-running tasks

**Key distinction:** The project is *not* "an agent that edits files." It is the machinery that lets the agent **select the right context, choose tools, recover from failures, and verify its own work**.

**Metrics:**

- Task success rate
- Test pass rate
- Failed tool calls
- Retries
- Tokens per successful task
- Latency
- Cost
- Context size
- Percentage of tasks requiring human intervention

*Ref: [OpenAI Agents SDK guide][1]*

---

## Project 3 — Financial Document Intelligence Platform

**Category:** Fintech — Document AI + Reliable Extraction

**Core question:**
> Can I build an AI system that reliably turns messy real-world financial documents into trustworthy structured data?

**Document types:**

- Bank statements
- Payslips
- KYC documents
- Tax documents
- Business registration documents

**Pipeline:**

```text
Document
    → Classification
    → OCR / Parsing
    → Layout understanding
    → Schema selection
    → Extraction
    → Validation
    → Confidence scoring
    → Human review
    → Structured data
```

**Capabilities:**

- Document classification
- Transaction extraction & categorization
- Table extraction
- Entity extraction
- Schema validation
- Anomaly detection
- Confidence scoring
- Human-in-the-loop review
- Audit trail

**Key distinction:** This demonstrates understanding the gap between **"the LLM produced JSON"** and **"the business can actually trust this pipeline."**

**Metrics:**

- Field-level precision / recall / F1
- Exact-match accuracy
- Document-level success rate
- Invalid-schema rate
- OCR failure rate
- Human-review rate
- Cost per document
- Latency per document

---

## Project 4 — LLMOps Platform

**Category:** Generalist — Production AI Infrastructure

**Core question:**
> Can I operate AI systems reliably, cheaply, observably, and audibly at production scale?

**Architecture:**

```text
Application → LLM Gateway → Model Router → Cache → LLM / VLM → Observability → Evaluation → Analytics
```

**Features:**

- Model routing & fallback models
- Retries & rate limiting
- Caching
- Token accounting & cost tracking
- Latency tracking
- Prompt / version tracking
- Distributed tracing & structured logs
- Model / provider abstraction
- Audit logging

**Fintech-specific emphasis:**

- Request/response traceability
- Decision provenance
- Immutable audit records
- Evidence tracking
- PII handling
- Reproducibility

**Metrics:**

- p50 / p95 / p99 latency
- Cost per request
- Cache hit rate
- Fallback rate
- Error rate
- Throughput
- Availability
- Cost reduction from routing / caching

**Senior-level evidence of completion:**
> "I reduced average inference cost by 42% with model routing while keeping answer quality within 1.5 percentage points of the expensive baseline."

---

## Project 5 — Underwriting / Decision Support Agent

**Category:** Fintech — Agents + Decision Intelligence (Capstone)

**Core question:**
> Can I combine models, tools, retrieval, deterministic business logic, and human oversight into a trustworthy high-stakes AI workflow?

**Workflow:**

```text
Loan Application
    → Agent
    → [Customer Data | Bank Statements | Credit Data | Financial Documents | Company Information | Lending Policies]
    → Analysis
    → Risk Factors
    → Missing Information
    → Policy Checks
    → Evidence + Citations
    → Decision Summary
    → Human Underwriter
```

**Tools:**

- `parse_bank_statement()`
- `retrieve_customer()`
- `fetch_credit_data()`
- `calculate_financial_ratios()`
- `retrieve_lending_policy()`
- `check_policy_compliance()`
- `flag_anomalies()`
- `retrieve_evidence()`
- `generate_decision_summary()`

**Key design constraint:**
> **The LLM does not adjudicate the loan.**

The agent may retrieve evidence, analyze information, call deterministic tools, flag risk, surface inconsistencies, explain policy implications, summarize evidence, and recommend further investigation — but the actual decision remains in deterministic business logic and/or human review.

**Metrics:**

- Task completion rate
- Evidence retrieval accuracy
- Citation correctness
- Unsupported-claim rate
- Policy-check accuracy
- Hallucination rate
- Human agreement rate
- Average review time reduction
- Cost per application
- Time to decision

**Why this is the capstone:** it ties together retrieval (Project 1), agent reliability (Project 2), document extraction (Project 3), and production operations (Project 4) into one high-stakes, human-governed workflow.

---

## Summary

This progression yields a portfolio that is greater than the sum of its parts: three genuinely generalist projects (RAG, coding agent, LLMOps) and two domain-specialised fintech projects (document intelligence, underwriting agent), all unified by a single discipline — **evaluation as a first-class engineering concern**.

[1]: https://developers.openai.com/api/docs/guides/agents?utm_source=chatgpt.com "Agents SDK | OpenAI API"