---
name: opencode-go-pricing
description: Fetch the live opencode Go docs page (https://opencode.ai/docs/go/) and render a joined table of model name, usage allowance in USD, requests per 5 hours/week/month, and data retention. Use ONLY when the user asks about opencode Go pricing, opencode Go model usage limits, model request quotas, or data retention for Go models.
---

# opencode-go-pricing

The user wants a live, joined view of three tables on the
[opencode Go docs page](https://opencode.ai/docs/go/):

- **Pricing** — carries the per-model USD allowance per $10/month
  subscription. Current column name is `Monthly limit` (renamed from
  `Usage`). A higher number means more usage per dollar — the $15 tier
  (Grok 4.6, Kimi K3, GLM-5.3, Qwen3.8 Max, DeepSeek V4 Pro) is the
  expensive tier; the $60 tier is roughly 4x more generous.
- **Requests per period** — carries `requests per 5 hour / week / month`.
- **Privacy** — carries `Data retention`.

All three join on the model column, but the page has three gotchas that have
to be handled every fetch:

1. **Tiered pricing rows are duplicated.** Several models appear twice in
   the pricing table: `Grok 4.6 (≤ 200K tokens)` and `Grok 4.6 (> 200K
   tokens)`, `GPT 5.6 Luna` (≤/>272K), `Qwen3.7 Plus` and `Qwen3.6 Plus`
   (≤/>256K), and `DeepSeek V4 Pro / V4 Flash / V4 Flash Vision Exp`
   (Off-Peak / Peak). Their value column is identical across both tiers,
   so collapsing to one row per model is safe.
2. **MiMo name spacing differs across tables.** Pricing writes `MiMo V2.5`
   and `MiMo V2.5 Pro`; the other two tables write `MiMo-V2.5` and
   `MiMo-V2.5-Pro`. Naive joins will silently drop MiMo on both sides —
   and MiMo has the highest request counts on the page, so this is not a
   corner case.
3. **Promo markup carries struck-through old values.** A promoted model
   renders `<del>$15</del> <strong>$60</strong>` plus a `4x · Ends Sep 20`
   note (and `<del>6,500</del><br><strong>26,000</strong>` in the requests
   table). All digit parsing is regex-driven and takes the last (bold,
   current) value: usage extracts every `$` amount (commas and decimals
   included), counts extract every number (commas and k/M/B suffixes
   included), and model names have any promo suffix stripped before
   joining. Cells with no parseable digits yield `N/A`, never a crash.

**Column-rename resilience.** Each target column is resolved in passes,
first success wins: a header alias match against a list of known names
(so past renames like `Usage` → `Monthly limit` keep working), then a
value-pattern signature match over data cells (`-`/`N/A` placeholders
ignored). The pricing monthly-limit pattern `\$\d+(?![\d.])` matches a
whole-dollar amount anywhere in the cell while excluding per-token rates
(`$0.15`); known price columns (`Input`, `Output`, ...) are excluded
outright, and any remaining tie breaks by lowest cardinality (tiered
limits repeat; prices vary). The request windows are indistinguishable
by pattern, so their fallback is structural: the unique column
assignment satisfying 5h <= week <= month on every complete row (the
20%/50%/100% sizing relationship). Retention falls back to a
days-or-ZDR pattern. Tables are located by header hints first, then by
column signature. Integral floats render without decimals. Every
fallback prints a stderr warning naming what it found so it can be
promoted into the alias or hint lists; total failure still raises
instead of guessing.

The helper script owns both pieces deterministically:

```bash
uv run ~/.config/opencode/skills/opencode-go-pricing/scripts/fetch_go_pricing.py
```

Run it, paste the resulting markdown table into your reply. Do not
re-derive the join, sort, or normalization in the prompt — that is what
the script exists to prevent. If the script reports that a table could
not be located, say so plainly and ask the user how to proceed; do not
fall back to a hand-rolled join.