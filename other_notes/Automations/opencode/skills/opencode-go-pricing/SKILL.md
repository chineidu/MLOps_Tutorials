---
name: opencode-go-pricing
description: Fetch the live opencode Go docs page (https://opencode.ai/docs/go/) and render a joined table of model name, usage allowance in USD, requests per 5 hours/week/month, and data retention. Use ONLY when the user asks about opencode Go pricing, opencode Go model usage limits, model request quotas, or data retention for Go models.
---

# opencode-go-pricing

The user wants a live, joined view of three tables on the
[opencode Go docs page](https://opencode.ai/docs/go/):

- **Pricing** — carries the per-model `Usage` allowance in USD.
- **Requests per period** — carries `requests per 5 hour / week / month`.
- **Privacy** — carries `Data retention`.

All three join on the model column, but the page has two gotchas that have
to be handled every fetch:

1. **Tiered pricing rows are duplicated.** Several models appear twice in
   the pricing table: `Grok 4.6 (≤ 200K tokens)` and `Grok 4.6 (> 200K
   tokens)`, `GPT 5.6 Luna` (≤/>272K), `Qwen3.7 Plus` and `Qwen3.6 Plus`
   (≤/>256K), and `DeepSeek V4 Pro / V4 Flash / V4 Flash Vision Exp`
   (Off-Peak / Peak). Their `Usage` column is identical across both tiers,
   so collapsing to one row per model is safe.
2. **MiMo name spacing differs across tables.** Pricing writes `MiMo V2.5`
   and `MiMo V2.5 Pro`; the other two tables write `MiMo-V2.5` and
   `MiMo-V2.5-Pro`. Naive joins will silently drop MiMo on both sides —
   and MiMo has the highest request counts on the page, so this is not a
   corner case.

The helper script owns both pieces deterministically:

```bash
uv run ~/.config/opencode/skills/opencode-go-pricing/scripts/fetch_go_pricing.py
```

Run it, paste the resulting markdown table into your reply. Do not
re-derive the join, sort, or normalization in the prompt — that is what
the script exists to prevent. If the script reports that a table could
not be located, say so plainly and ask the user how to proceed; do not
fall back to a hand-rolled join.