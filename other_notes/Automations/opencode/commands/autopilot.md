---
description: Autopilot - the agent decides, you review the diff
agent: architect
---

Enable autopilot mode for the current task.

Follow section 4.10 (Autopilot) of Architect Mode for the rest of the
current task:

- Fill the chosen contract items yourself, choosing the most defensible
  option for each and grounding it in the ADR, the spec, or the library
  documentation. Record every such row in the contract ledger with
  provenance `autopilot`.
- Answer the sign-off check yourself: state the identity key and one
  rejected alternative explicitly, and record both in the ledger.
- Decide at every decision moment during implementation, log the choice
  inline as `# call: <one-line rationale>`, and keep going. Do not raise
  a `question` prompt.
- Work through the steps of the task in order instead of stopping after
  each one.
- Still request write/edit approval for the same writes strict mode
  would request. Never commit, push, or merge without explicit user
  confirmation.
- Still flag scope-creep items instead of fixing them inline.

Task scope: $ARGUMENTS

If `$ARGUMENTS` is empty, autopilot covers the task you are already
working on. If it names a task, that is the task to run in autopilot.

Confirm autopilot is active in one line, then proceed. When the task is
done, report in this order: the contract ledger with `autopilot` rows
flagged, the files changed (path, what changed, why), the verification
output, and the decisions you made that the user might want to reverse,
each with the file and line to change.
