# Plan: Make `Shift+Enter` insert a newline in the terminal (VS Code-family IDE)

> Scope: This documents the fix applied in **this** session — a keybinding
> conflict inside a VS Code-family IDE (the editor is a VS Code fork; on this
> machine it is "Antigravity IDE"). It does NOT cover opencode's own `tui.json`
> or the Kitty keyboard protocol, which were not part of this fix.

## Symptom

- `shift+enter` inside the integrated terminal did nothing (the prompt did not
  get a newline, and nothing was submitted).
- `ctrl+j` and `alt+return` already worked as newlines, so only `shift+enter`
  was the problem.

## Root cause

Two `Terminal: Send Sequence` keybindings were bound to `shift+enter`:

- **User** binding: `when: terminalFocus`
- **System** (built-in) binding: `when: terminalFocus && <more specific>`

When two keybindings share the same key, VS Code / the fork applies the
**more specific `when` clause wins** rule. The System binding therefore
shadowed the User one, so the User binding was ignored entirely. That is why
nothing happened on `shift+enter`.

Additionally, sending a raw `\n` (newline byte) is swallowed by **zsh's line
editor**, which treats a bare newline as "execute." So even a working
`shift+enter` sending `\n` would still submit.

## Resolution

### 1. Add a User keybinding

In the IDE's `keybindings.json` (on this machine:
`/Users/mac/Library/Application Support/Antigravity IDE/User/keybindings.json`),
add a User keybinding that sends `Esc` followed by `Return` (`\u001b\r`).
zsh's default keymap already treats `Esc`+`Return` as "insert literal
newline," so this works at the shell level without relying on any terminal
keyboard protocol.

```json
{
  "key": "shift+enter",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "\u001b\r" },
  "when": "terminalFocus"
}
```

> Note: an earlier attempt used `"text": "\n"` (raw newline) but this gets
> swallowed by zsh as "execute." Use `\u001b\r` instead.

### 2. Remove the conflicting System keybinding

In the IDE:

- Open the Keyboard Shortcuts editor (`cmd+k cmd+s`).
- Find `Terminal: Send Sequence` bound to `shift+enter`.
- Right-click the **System** entry (the one with the longer / more specific
  `when` clause, e.g. `terminalFocus && terminal...`) and choose
  **"Remove Keybinding."**
- Keep only the **User** entry from step 1.

This is a GUI action; it is not stored in `keybindings.json` — it lives in the
IDE's internal keybindings state. On a fresh workstation, adding the User
keybinding from step 1 is usually sufficient, but if a System binding shadows
it, repeat this removal step.

## Verification

1. Reload the IDE window (`cmd+shift+p` → `Developer: Reload Window`) after
   the changes.
2. Focus the integrated terminal.
3. Type a line, press `shift+enter` → cursor moves to a new line WITHOUT
   submitting/executing.
4. Press `return` (plain enter) → line executes / submits normally.

## Re-use on other workstations

1. Merge the `shift+enter` User keybinding (step 1) into the target IDE's
   `keybindings.json`. For a VS Code fork, the path is typically
   `~/Library/Application Support/<IDE Name>/User/keybindings.json` (macOS) or
   `~/.config/<IDE Name>/User/keybindings.json` (Linux). **Confirm the exact
   path for your editor before copying.**
2. Check for a conflicting System `Terminal: Send Sequence` on `shift+enter`
   in the Keyboard Shortcuts editor and remove it if present (step 2).
3. Reload the window and verify (step 3).

## Not part of this fix (do not assume)

- opencode's `~/.config/opencode/tui.json` — not touched or discussed here.
- Kitty keyboard protocol / `terminal.integrated.enableKittyKeyboardProtocol`
  — not used; the `sendSequence` workaround is protocol-free.
