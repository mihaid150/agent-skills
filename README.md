# agent-skills

My personal skills for **Claude Code** and **Codex**, in one place.
Each skill is a folder with a `SKILL.md` (plus optional `scripts/`, `references/`, `assets/`).
Both tools read the same format, so one source serves both.

## Skills

| Skill | What it does |
|---|---|
| `deepread` | Deep reading: claims, evidence, knowledge map, Feynman explanation, recall |
| `grill-me` | Relentless questioning of a plan or design until there is shared understanding |
| `karpathy-guidelines` | Coding behavior rules (simplicity, surgical changes). Source: [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), MIT |
| `lit-review` | Literature review in my house format: search protocol or analysis by research direction |
| `llm-wiki` | LLM-maintained Obsidian second brain: ingest, index, lint |
| `red-green-proof` | Proves a bug with a test that fails, then passes, then fails again when the fix is reverted |
| `syllabus` | Supplementary readings for a course, exported as .docx |
| `codex-first` | Claude writes the spec and verifies; Codex (`gpt-5.6-sol`) writes the code |
| `skill-cleaner` | Audits Claude + Codex skills: duplicates, long descriptions, unused skills |
| `markdown-converter` | PDF/DOCX/PPTX/XLSX/HTML/YouTube → Markdown with `markitdown` (needs `uv`) |
| `video-transcript-downloader` | Video transcripts and video/audio downloads (needs `npm ci` + `yt-dlp`, `ffmpeg`) |
| `oracle` | Second opinion from another model (GPT Pro) with project files attached |
| `create-cli` | UX spec for CLI tools: flags, help, output, errors, exit codes |
| `github-deep-review` | Issue/PR review with root cause, provenance, best fix and proof |
| `project-structure` | Compact symbol map for TypeScript/Swift repos (Node 20: via `npx tsx`; needs `typescript@5` in the skill folder) |
| `floorplan` | Interactive architecture map of an app (Node ≥ 18) |
| `graphify` | Knowledge graph over code and documents (needs the `graphify` CLI: `uv tool install graphifyy`) |
| `repo-polish` | De-vibe-code a repo: audit structure, AI-style comments, dead code, junk files and README; fix approved items without changing behavior |

### External sources

- `codex-first`, `skill-cleaner`, `markdown-converter`, `video-transcript-downloader`, `oracle`, `create-cli`, `github-deep-review`, `project-structure`: from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) (MIT, see `LICENSE-steipete-agent-scripts.txt`), adapted for Windows and Linux; `codex-first` and `skill-cleaner` rewritten.
- `repo-polish`: adapted from `deep-refactor` / `doc-refactor` in [cedricfarinazzo/agile-skills](https://github.com/cedricfarinazzo/agile-skills) (MIT), slimmed down for personal and research repos; `scripts/audit.py` is new.
- `floorplan`: [haydenschmitty/floorplan](https://github.com/haydenschmitty/floorplan) v0.11.0 (MIT).
- `graphify`: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) v0.9.115, Windows variant (MIT/Apache-2.0). On Windows, do not run `graphify install`: the skill is managed here.

To update an external skill: copy its folder again from the new release and keep the `Source:` line in `SKILL.md`.

## Setup on a new machine

### Windows

```powershell
git clone <private-repo-url> $HOME\agent-skills
& $HOME\agent-skills\scripts\link-skills.ps1
```

The script creates **junctions** (no admin rights needed):

- `~\.claude\skills\<skill>` → `agent-skills\skills\<skill>`
- `~\.codex\skills\<skill>` → `agent-skills\skills\<skill>`

If a real folder with the same name already exists, the script skips it. With `-Force` it moves
it to a backup (`~\.claude\skills-backup-<date>`) and puts the junction in its place.

Tools for the skills that need them:

```powershell
winget install astral-sh.uv yt-dlp.yt-dlp Gyan.FFmpeg
uv tool install graphifyy
cd $HOME\agent-skills\skills\video-transcript-downloader; npm ci
cd $HOME\agent-skills\skills\project-structure; npm i --no-save --no-package-lock typescript@5
```

### Ubuntu / Linux / macOS

```bash
git clone <private-repo-url> ~/agent-skills
bash ~/agent-skills/scripts/link-skills.sh          # --force moves existing folders to a backup
```

Creates **symlinks** in `~/.claude/skills` and `~/.codex/skills`. Exception: `graphify` is not linked
(the skill in this repo is the Windows/PowerShell variant); on Linux the CLI installs the matching version:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # uv
uv tool install graphifyy && graphify install && graphify install --platform codex
sudo apt install ffmpeg && pipx install yt-dlp       # video-transcript-downloader
(cd ~/agent-skills/skills/video-transcript-downloader && npm ci)
(cd ~/agent-skills/skills/project-structure && npm i --no-save --no-package-lock typescript@5)
```

### Rule for new skills

Add this to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` on each machine, so agents create new
skills in the repo: new skills go in `~/agent-skills/skills/<name>/`, then run `link-skills.ps1`
(Windows) or `link-skills.sh` (Linux/macOS).

## Workflow

1. Edit the skill in `agent-skills/skills/<skill>` (or through the link, it is the same file).
2. `git commit` + `git push`.
3. On another machine: `git pull`. The links see the change immediately.

New skill: create `skills/<name>/SKILL.md`, then run `link-skills.ps1` (Windows) or `link-skills.sh` (Linux/macOS) again.

## What does NOT go here

- Anthropic built-in skills (`pdf`, `docx`, `xlsx`, `pptx`, `skill-creator`, etc.) and the `~/.claude/skills/synced/` folder, which the Claude app manages.
- Plugins by other authors (`research-desk`, `heptabase`): install them through the plugin system.
- Secrets: API keys, tokens. Use environment variables.
