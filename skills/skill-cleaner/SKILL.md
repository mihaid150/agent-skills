---
name: skill-cleaner
description: "Audit installed skills for Claude Code and Codex: duplicates, long descriptions that eat context, unused skills. Use when the user asks to clean up, audit, dedupe or trim their skills or plugins."
---

# Skill Cleaner

Idea from steipete/agent-scripts `skill-cleaner` (MIT), rewritten in Python for this setup.

Every installed skill puts its `description` into the context of every session. Duplicates and long descriptions cost tokens on every turn.

## Run

```powershell
python -I <this-skill-dir>/scripts/skill_cleaner.py --months 3
```

`<this-skill-dir>` is the folder holding this SKILL.md. On Linux use `python3`.

Flags: `--no-logs` (skip the usage scan, faster), `--months N`, `--max-desc N` (threshold for "long").

It scans `~/.claude/skills` (including the app's `synced/` folder), `~/.claude/plugins`, `~/.codex/skills`, `~/.codex/plugins`, and counts mentions in `~/.claude/projects/**/*.jsonl` and `~/.codex/sessions/**/*.jsonl`. Read-only.

## Read the report

1. **Per root**: how many skills and description tokens each source adds.
2. **Duplicates by name**: same skill from two real folders (e.g. repo + claude.ai cloud). Junctions to the same folder are not duplicates.
3. **Near-identical descriptions**: different names, same purpose.
4. **Long descriptions**: candidates to shorten. Keep the trigger words (tool, action, object).
5. **Usage**: sessions that mention each skill. 0 is a removal candidate, not proof.

## Before changing anything

- Propose the changes to the user first; never delete on your own.
- Personal skills live in the `agent-skills` repo (`~/agent-skills/skills`): edit there.
- Cloud duplicates (claude.ai Plugins → Skills): disable rather than delete.
- Built-in skills (Anthropic `synced/`, Codex `.system/`) are managed by the apps: leave them.
