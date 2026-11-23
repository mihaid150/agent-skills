# README rules

A README optimizes for a newcomer's first ten minutes on GitHub: what is this, can I run it, where do I look. It is not a changelog, a tutorial for the language, or marketing.

## Verify, don't read

Every statement has a referent; check it:
- **Command**: run it in the repo (or a fresh clone when cheap). If it needs hardware or services you cannot run (GPU, cluster, Docker network), check that the script, flags and files it uses exist, and say "not executed" in the report.
- **Flag / option**: present in the argparse/click/typer source or `--help`.
- **Path**: exists at HEAD.
- **Link**: resolves; anchors (`#section`) exist.
- **Numbers** (results, accuracy, speedups): traceable to a script, log or paper table. Otherwise remove or mark as "reported in <paper>".
- **Counts** ("the 3 node types", "12 experiments"): replace with the property or point at the source of truth; a bare count rots silently.

Fix false statements first. Then stale ones (roadmaps, "coming soon", notes about versions nobody runs). Then duplication and bloat. Then write what is missing, found by walking the real journey: fresh clone → install → first successful run.

## Keep exact

Commands, env vars, config keys, flags, file names, error strings: copied exactly from the code, in code blocks, never paraphrased.

## Avoid

- Emoji headings, badge walls, "🚀 Features" lists of generic claims ("scalable", "robust", "production-ready") with nothing behind them.
- Restating the folder tree in prose.
- Installation steps for tools the reader obviously has (how to install Python).
- Placeholder text, "TODO: add docs", empty sections.
- Content that belongs in `docs/` (long tutorials, API references): link to it instead.

## Template (drop sections that do not apply)

```markdown
# <Project name>

<One or two sentences: what it does and for whom. For research code: the paper/thesis it accompanies.>

<Optional: one diagram or figure of the architecture or main result.>

## Overview
<How it works in 5–10 lines: components and how they interact
(e.g. edge nodes train locally, fog nodes aggregate, cloud coordinates).>

## Repository layout
| Path | Contents |
|---|---|
| `edge_node/` | ... |

## Requirements
<Language/runtime versions, hardware (GPU?), external services.>

## Installation
<exact commands>

## Usage
<exact commands for the main workflows, with the expected output or result file>

## Configuration
<config file(s) and the env vars/keys that matter, with defaults>

## Reproducing the results
<For research repos: which script produces which table/figure, datasets and where to get them, seeds.>

## Tests
<exact command>

## Citation
<BibTeX, for research repos>

## License
<name, link to LICENSE>
```

## Agent instruction files

`CLAUDE.md`, `AGENTS.md`, `.cursorrules` are executable instructions loaded into every agent session. Treat edits like code: never delete a rule or trigger phrase without stating what it governed; keep them short (they cost tokens every session).
