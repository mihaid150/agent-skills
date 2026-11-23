---
name: repo-polish
description: "Clean up a GitHub repository so it does not look vibe-coded: audit code structure, AI-style comments, dead code, duplicates, stray files and the README, then fix approved items without changing behavior and rewrite the README from the real code. Use when the user says repo-polish, clean up / polish / de-slop a repo, make the code less vibe coded, or improve a repo's structure, comments or README."
---

# repo-polish

Adapted from `deep-refactor` and `doc-refactor` in [cedricfarinazzo/agile-skills](https://github.com/cedricfarinazzo/agile-skills) (MIT), slimmed down for personal and research repos: no ticket tracker, no PR train.

## Goal and contract

**Code that a stranger can read and trust, and a README that tells the truth.** Behavior must not change: the existing tests, or the recorded baseline run, prove it. A cleanup that needs a behavior change is a separate finding for the user, never smuggled into a polish commit.

A pattern is not a finding because it *looks* generated. Every finding names its concrete cost, `path:line` evidence, what must keep working, and the fix.

## Modes

- `repo-polish` or `repo-polish audit` (default): phases 0–2 only. Read-only on code; writes just the report.
- `repo-polish fix [IDs]`: phase 3 for approved items.
- `repo-polish readme`: phase 4 only.

Never jump from audit to fix without the user approving the item IDs.

**Codex:** run every pass inline and in order; never spawn sub-agents. **Claude Code:** read-only audit passes over disjoint areas may run as parallel subagents; big mechanical fix batches may go to Codex via `codex-first`.

## Phase 0 — Safety and baseline

1. `git status` must be clean. If not: STOP and ask the user to commit or stash.
2. Find how the project runs and is checked: tests (`pytest`, `npm test`, ...), entry points (`main.py`, scripts in README, Dockerfiles, `docker-compose`), linters already configured (`ruff`, `black`, `eslint`, `pre-commit`).
3. Record a **baseline**: run the tests (or the cheapest real entry point, e.g. `python -m <pkg> --help`, an import of every module) and save command + result. No tests and nothing runnable? Say so in the report: every fix then needs extra care, and "add a smoke test" becomes finding #1.

## Phase 1 — Audit

**Architecture first.** Before local smells, give a short verdict on the big shapes: module/package boundaries, where config lives, dependency direction, entry points, how components talk (for cloud/fog/edge style projects: what runs where, shared code, duplicated protocol logic). "The structure is sound; the debt is duplication and comments" is a valid verdict.

**Then the mechanical scan** (signals, not verdicts):

```bash
python -I <this-skill-dir>/scripts/audit.py <repo-root>            # Windows: python, Linux: python3
```

`<this-skill-dir>` is the folder holding this SKILL.md. It reports: committed junk, stray/backup files, huge files and functions, AI-style and commented-out-code comments, unused imports, bare/silent excepts, hardcoded absolute paths, duplicate function bodies, missing repo basics.

**Then read the code** against [references/taxonomy.md](references/taxonomy.md): AI residue, structure, naming, comments, error handling, config, repo hygiene. Read past the first file: follow entry point → core logic → I/O boundaries.

**Loop until dry.** After the first pass, do a second pass with fresh eyes on what was only skimmed. Stop when a pass finds nothing new.

**Vet every candidate before proposing it:**
- **Pins**: what depends on the current shape? Imports from other modules or repos, CLI flags and script names used in README/Docker/CI, file paths read at runtime, names used in config files, pickled/saved objects, notebooks importing the module, public API used by others. A move or rename ships with its pin list.
- **Evidence**: "unused" means grep found no other reference (including strings, configs, Dockerfiles); "duplicate" means you diffed the actual lines; "dead branch" means you proved the condition.

**Classify:**
1. **Defect**: a real bug found along the way (wrong result, crash path, silent data loss). Reported first; fixed only with the user's OK and a test.
2. **Safe cleanup**: behavior-preserving, proven by baseline.
3. **Needs proof**: plausible but no test covers it; needs a characterization/smoke test first.
4. **Deliberate, do not fix**: looks odd but is intentional (record why).

## Phase 2 — Report

Write `.repo-polish/report.md` in the repo and add `.repo-polish/` to `.git/info/exclude` (local only, never committed). Show the user a summary in chat.

Report shape:
1. Architecture verdict (5–10 lines).
2. Baseline: command, result, date, commit.
3. Defects.
4. Ledger table, one row per finding:

| ID | Class | Where (`path:line`) | Problem + evidence | Fix | Pins | Risk | Status |
|---|---|---|---|---|---|---|---|

   Status: `Proposed`, `Approved`, `Done`, `Rejected` (one-line reason), `Deliberate`.
5. README findings (from phase 4's check list), if the README was audited.

Every count carries the command that produced it ("12 bare excepts (`audit.py` at `abc1234`)"), never a bare number.

Then ask the user which IDs to apply. Group suggestions: "quick wins", "structural", "needs a test first".

## Phase 3 — Fix (approved IDs only)

**Branches.** The audit stays on the current branch (it changes no code). Before the first edit, branch off the default branch, one branch per kind of change, so each can become its own focused PR. Name the branch after the change, not after this skill:

| Kind of change | Branch | Example |
|---|---|---|
| Behavior-preserving code cleanup | `refactor/<scope>` | `refactor/fog-aggregation`, `refactor/dead-code` |
| Repo hygiene: `.gitignore`, junk files, dependency files | `chore/<scope>` | `chore/repo-hygiene`, `chore/pin-dependencies` |
| README and other docs | `docs/<scope>` | `docs/readme` |
| Approved defects | `fix/<scope>` | `fix/edge-silent-except` |

Lowercase kebab-case, at most ~40 characters, saying what changes. If the repo already has a branch-naming convention (check `git branch -a` and recent merged PRs), follow it instead. If the user prefers a single branch, use `refactor/codebase-cleanup`. Before creating a branch, check that the name is not already taken.

Commit messages follow the repo's existing style; if it has none, use the same type prefixes (`refactor: extract shared weight averaging`, `chore: untrack __pycache__`, `docs: rewrite README from code`). No `Co-Authored-By:` lines for Claude or any AI and no `Claude-Session:` lines: the user is the only author (`AGENTS.md`).

- One commit per logical change or per category (e.g. "Remove AI narration comments", "Delete unused imports", "Extract duplicated aggregation into shared/"). Never mix reformatting with logic changes in one commit.
- Formatting (`ruff format`, `black`, `prettier`) only if the project already uses it or the user agrees, and as its own commit.
- Renames/moves: update every pin from the report in the same commit; leave a re-export at the old import path when external code may import it.
- After each commit: rerun the baseline. Red → revert that commit, mark the item `Rejected` or `Needs proof` with the reason.
- Something unexpected (a new pin, the fix needs a behavior change, an out-of-scope edit): STOP that item, report it, continue with the others.
- Do not push. Do not commit unless the user asked for commits in this run; otherwise leave changes staged per item and say so.

## Phase 4 — README

Rules in [references/readme.md](references/readme.md). Work on a `docs/readme` branch (see phase 3 naming). Short version:

1. **Inventory**: every `.md` in the repo and who reads it (newcomer on GitHub, a reviewer, an agent via `CLAUDE.md`/`AGENTS.md`).
2. **Verify every claim**: each command is run in the repo, each path exists, each flag exists in the argparse/CLI source, each link resolves. False claims are fixed first; a confident false statement is worse than none.
3. **Write from the code**, not from the old README: what it is, architecture (optionally a diagram from `floorplan`), install, run, configuration, results/reproduction, project layout, citation/license. Drop what is not true or not needed.
4. Keep operative tokens (commands, env vars, config keys, flags) exact; never paraphrase a command.
5. Show the user the new README as a diff before replacing the old one.

## Definition of done

- Every approved item is `Done` or has a recorded reason.
- Baseline passes on the final tree, same as at the start.
- README commands were executed and work.
- Report updated with what changed and what was left (and why).
- Nothing pushed; the user decides.
