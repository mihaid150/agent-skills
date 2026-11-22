---
name: codex-first
description: "Delegate hands-on coding work from Claude to Codex CLI (gpt-5.6-sol) to save Claude tokens: implementation from a clear spec, refactors, bug fixes, tests, scripts. Claude keeps design, spec writing and final verification. Use when the user says codex-first, delegate to Codex, or when a large amount of code must be written from a settled plan."
---

# Codex First (light)

Inspired by steipete/agent-scripts `codex-first` (MIT), simplified for this machine.

Claude writes the spec and checks the result. Codex (`gpt-5.6-sol`, cheaper than the GPT-6 family) writes the code.

## Gate: only from Claude

- Running inside **Codex** (or any non-Claude model)? Do not call `codex exec`. Do the work directly.
- Running in **Claude Code**: delegate per the routing below.

## Route

Delegate to Codex:
- implementation from a settled spec, refactors, mechanical migrations
- bug fixes with a known repro, failing tests/lint/types
- writing tests, scripts, tooling
- read-heavy exploration where the reading is much bigger than the answer

Keep in Claude:
- design, architecture, naming, anything where writing the spec *is* the work
- tiny edits (under ~20 lines): delegation costs more than it saves
- anything needing MCP tools, browser, secrets, or the user's accounts
- git commits/pushes, releases, and the final review of Codex's output

Mixed task: Claude designs and freezes the spec first, then delegates the build-out.

## Work order (Codex starts with zero context)

Write it to a file in the scratchpad (never inline-quote a long prompt). Every order contains:

1. **Goal**: one or two sentences.
2. **Where**: repo path, exact files/dirs to touch, files to read first (AGENTS.md, relevant skill).
3. **Constraints and non-goals**: what must not change.
4. **Proof**: the exact command(s) to run (tests, build, lint) and that they must pass.
5. **Escape hatch**: "If a constraint cannot be met after honest attempts, STOP and report the exact blocker. Do not work around it." Without this, a cornered worker satisfies the letter of the rule and breaks its intent.
6. **Report shape**: "List files changed, commands run with their output, and anything left undone."
7. **Stop**: "Do exactly this. Do not commit, push, or start follow-up work."

## Launch

```powershell
# Windows (PowerShell)
Get-Content $ORDER -Raw | codex exec -m gpt-5.6-sol -c 'model_reasoning_effort="medium"' --sandbox workspace-write -C $REPO -o $OUT -
```

```bash
# Linux/macOS (bash)
codex exec -m gpt-5.6-sol -c 'model_reasoning_effort="medium"' --sandbox workspace-write -C "$REPO" -o "$OUT" - < "$ORDER"
```

- `$ORDER`: the work-order file. `$OUT`: where Codex writes its final message. `$REPO`: the working root.
- `model_reasoning_effort`: `low` for mechanical work, `medium` default, `high` only for hard bugs.
- Outside a git repo add `--skip-git-repo-check`.
- Codex needs another writable folder? Add `--add-dir <dir>`. Avoid `--dangerously-bypass-approvals-and-sandbox`.
- Run every worker as its **own background command** (Bash/PowerShell tool with `run_in_background: true`) so the app tracks it and notifies on completion. Never `&`-fork several workers from one command.
- Parallel workers only on separate files/dirs, each with its own `-o` file.
- New task → new `codex exec` session. Resume (`codex exec resume <SESSION_ID> ...`, same flags again) only to correct the same task.

## After Codex finishes

1. Read `$OUT`.
2. Review the diff yourself (`git diff`): does it match the spec, any shortcuts or stubs, anything outside scope?
3. Re-run the proof commands yourself. Do not trust "tests pass" from the report.
4. Fix small issues directly; send larger ones back as a resume with a precise correction.
5. Tell the user what Codex did and what you verified.

## Troubleshooting

- `model not found` / unsupported: run `codex --version`, update with `npm i -g @openai/codex`, check `~/.codex/models_cache.json` for current slugs.
- Rate limit or capacity error: retry once with `-m gpt-5.6-terra`; if that fails too, tell the user and do the work in Claude.
- Codex blocked by the sandbox: read the error, add the needed `--add-dir`, rerun. Do not switch to bypass mode without asking the user.
