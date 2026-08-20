# opencode Permission System — Investigation Notes

> **Date:** August 20, 2026
> **opencode versions investigated:** 1.18.5, 1.18.18
> **Plugin package:** `@opencode-ai/plugin@1.17.11`

---

## TL;DR

The `auto-approve-pipes.ts` plugin does not work because the `permission.ask`
plugin hook is **dead** — it is declared in the type definition but never
invoked at runtime. This was already true in v1.18.5; the upgrade to v1.18.18
did not break it.

opencode's **native** permission rules already split chained commands on `&&`
into per-segment patterns and evaluate each independently against the config
allow-list. The correct mechanism for rule-based auto-approval is the `bash`
permission block in `opencode.jsonc` — no plugin is needed.

---

## How opencode's Permission System Works

### 1. Config → Ruleset

`Permission.fromConfig()` (`permission/index.ts:186`) converts the config's
`permission` object into a flat array of `Rule` objects:

```
{ permission: "bash", pattern: "git log *", action: "allow" }
{ permission: "bash", pattern: "*",         action: "ask"   }
```

Key insertion order is preserved (Effect's `propertyOrder: "original"` parse
option), so the order in the JSONC file matters for `findLast` evaluation.

### 2. Agent Ruleset Construction

`agent/agent.ts:119-152` builds each agent's ruleset via:

```ts
Permission.merge(defaults, build-specific, user)
```

Where `defaults` includes `{ "*": "allow", doom_loop: "ask", ... }` and
`user = Permission.fromConfig(cfg.permission ?? {})`.

The `build` agent merges `defaults` + `{ question: "allow", plan_enter: "allow" }` + `user`.

### 3. Per-Tool-Call Ruleset

`session/tools.ts:87` — each tool call's `ctx.ask()` receives:

```ts
ruleset: Permission.merge(input.agent.permission, input.session.permission ?? [])
```

Session-level permissions (from "always" approvals) are appended **after**
agent permissions, so they win in `findLast` evaluation.

### 4. Pattern Scanning (Shell Tool)

`tool/shell.ts:378-414` — the `collect()` function uses a tree-sitter bash
parser to find all `command` nodes in the input. For each command:

- `scan.patterns.add(source(node))` — the raw text of the command node
  (or `node.parent.text` if inside a redirected_statement)
- `scan.always.add(BashArity.prefix(tokens).join(" ") + " *")` — an
  arity-based prefix pattern for "always allow" after user approves once

**Chained commands are split natively.** The tree-sitter parser produces
separate `command` nodes for each segment of `A && B && C`. A probe
confirmed that `ls && rm --version` produces `patterns: ["ls", "rm --version"]`.

### 5. The `ask()` Gate

`tool/shell.ts:263-291` — the `ask()` function:

1. If `scan.dirs.size > 0` → asks `external_directory` permission first
2. If `scan.patterns.size === 0` → **returns without asking bash permission**
   (some commands skip the permission check entirely)
3. Otherwise → calls `ctx.ask()` with `permission: "bash"`, `patterns`, `always`

### 6. Evaluation

`permission/index.ts:28-38` — `evaluate()`:

```ts
function evaluate(permission, pattern, ...rulesets) {
  return rulesets
    .flat()
    .findLast((rule) =>
      Wildcard.match(permission, rule.permission) &&
      Wildcard.match(pattern, rule.pattern)
    ) ?? { action: "ask", permission, pattern: "*" }
}
```

- Uses `findLast` — **last matching rule wins**
- Falls back to `{ action: "ask" }` if no rule matches
- The `ask()` function iterates all patterns; if any returns `"deny"` →
  immediate `DeniedError`; if any returns `"ask"` → `needsAsk = true`; if
  all return `"allow"` → proceeds without prompting

### 7. Wildcard Matching

`core/util/wildcard.ts` — `Wildcard.match(input, pattern)`:

- Converts `*` → `.*`, `?` → `.`
- Trailing ` *` becomes `( .*)?` (optional space + anything)
- Full-match regex: `^...$` with `s` flag (dotall)
- Backslashes normalized to `/`

So `"git log *"` matches `"git log --oneline -3"` via regex
`^git\ log( .*)?$`.

### 8. BashArity Prefix

`permission/arity.ts` — `BashArity.prefix(tokens)` determines the
"human-understandable command" from tokens using an arity dictionary:

- `git` has arity 2 → `git checkout main` → prefix is `git checkout`
- `npm` has arity 2 → `npm install` → prefix is `npm install`
- `npm run` has arity 3 → `npm run dev` → prefix is `npm run dev`
- `ls` has arity 1 → `ls -la` → prefix is `ls`

This prefix is used for the `always` set (the pattern added to `approved`
when the user clicks "always allow"), NOT for the initial `patterns` set.

---

## The Dead `permission.ask` Hook

### What the plugin type declares

`packages/plugin/src/index.ts:261`:

```ts
"permission.ask"?: (
  input: Permission,
  output: { status: "ask" | "deny" | "allow" }
) => Promise<void>
```

### What actually happens at runtime

The `Permission.ask` function (`permission/index.ts:67-107`) **never calls
any plugin hook**. It:

1. Evaluates each pattern against the ruleset + approved list
2. If all allow → returns silently
3. If any ask → publishes an `Event.Asked` event via `events.publish()` and
   awaits a `Deferred`

The `Event.Asked` event IS delivered to plugins via the `event` hook (a
probe confirmed this), but it is **observational only** — there is no
mechanism for a plugin to inject a decision back into the permission flow.

### Verification method

- A probe plugin at `~/.config/opencode/plugins/permission-probe.ts` logged
  all events and confirmed `permission.asked` events arrive with full
  payload: `{ id, sessionID, permission: "bash", patterns: [...], metadata: { command }, always: [...], tool: { messageID, callID } }`
- Source grep across both v1.18.5 and v1.18.18 tags: the string
  `"permission.ask"` appears only in the plugin type definition, never in
  runtime code

---

## The Unsolved Mystery

**`git log --oneline -3 && wc -l pyproject.toml && date && which python`**
prompts despite ALL segments matching config allow rules (`git log *`, `wc *`,
`date`, `which *`).

The `evaluate()` function uses `findLast`, and the allow rules come after
`*: ask` in insertion order, so they should win. `Wildcard.match` traces
confirm matches for each pattern.

Possible explanations that were not fully ruled out:

1. **Config not loaded** — the `user` ruleset might be empty if config
   parsing failed silently
2. **Session permission interference** — a stale session-level rule might
   shadow the agent ruleset
3. **A scan/evaluate edge case** — something in the tree-sitter parsing or
   pattern generation that doesn't match expectations

### How to investigate further

1. **Test a single non-chained command** like `git log --oneline -3` alone —
   if it prompts, the issue is pattern-matching, not chaining
2. **Check opencode logs** at `~/.local/share/opencode/log/` for the
   `"evaluated"` log lines (`permission/index.ts:74`) — these show what
   action `evaluate()` returned for each pattern
3. **Add debug logging to the probe** to also log the `evaluate()` results
4. **Verify config loading** — add a `config` hook to the probe and log the
   received `cfg.permission.bash` object

---

## Conclusion: The Right Mechanism

The `bash` permission block in `opencode.jsonc` is the correct and working
mechanism for rule-based auto-approval:

```jsonc
{
  "permission": {
    "bash": {
      "*": "ask",           // catch-all: ask for anything not explicitly allowed
      "git log *": "allow", // allow git log with any args
      "wc *": "allow",      // allow wc with any args
      "date": "allow",      // allow date (exact match)
      "which *": "allow"    // allow which with any args
    }
  }
}
```

opencode natively splits `A && B && C` into `["A", "B", "C"]` and evaluates
each segment independently. If all segments match allow rules, the chain
runs without prompting. If any segment matches `"*": "ask"`, the user is
prompted once for the whole chain.

This is believed to work but is not fully proven — see the "Unsolved
Mystery" above, where a chain with every segment matching an allow rule
still prompted. Treat per-segment auto-approval as the intended and usually
correct behavior, not a guarantee.

### Dangerous commands

There is no built-in deny-list mechanism in the config. To prevent
auto-approval of dangerous commands, simply **do not add them to the
allow-list**. The `"*": "ask"` catch-all ensures anything not explicitly
allowed will prompt the user.

If you need a hard deny (never prompt, just refuse), you could add explicit
deny rules before the allow rules:

```jsonc
{
  "permission": {
    "bash": {
      "*": "ask",
      "git log *": "allow",
      "rm *": "deny",       // never allow rm, never even prompt
      "sudo *": "deny"
    }
  }
}
```

Note: `findLast` means **last match wins**, and `"*"` matches every command
just like a specific rule does — it isn't a fallback that only applies when
nothing else matches. So a deny (or allow) rule only takes effect if it comes
**after** `"*"` in the JSONC object; placed before it, the catch-all matches
too and, being later, wins instead. Always put `"*"` first and every
more-specific rule after it.
