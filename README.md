# agent-skills

Skill-urile mele personale pentru **Claude Code** și **Codex**, într-un singur loc.
Fiecare skill e un folder cu `SKILL.md` (plus `scripts/`, `references/`, `assets/` opționale).
Ambele unelte citesc același format, deci aceeași sursă le servește pe amândouă.

## Skill-uri

| Skill | Ce face |
|---|---|
| `deepread` | Citire în profunzime: claims, evidence, hartă de cunoștințe, Feynman, recall |
| `grill-me` | Interogare insistentă a unui plan/design până la înțelegere comună |
| `karpathy-guidelines` | Reguli de comportament la scris cod (simplitate, schimbări chirurgicale). Sursa: [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), MIT |
| `lit-review` | Analiza literaturii în formatul meu: protocol de căutare sau analiză pe direcții |
| `llm-wiki` | Second brain în Obsidian întreținut de LLM: ingest, index, lint |
| `red-green-proof` | Dovedește un bug cu un test care pică, apoi trece, apoi pică iar la revert |
| `syllabus` | Lecturi suplimentare pentru un curs, exportate ca .docx |
| `codex-first` | Claude scrie spec-ul și verifică, Codex (`gpt-5.6-sol`) scrie codul |
| `skill-cleaner` | Audit skill-uri Claude + Codex: duplicate, descrieri lungi, nefolosite |
| `markdown-converter` | PDF/DOCX/PPTX/XLSX/HTML/YouTube → Markdown cu `markitdown` (cere `uv`) |
| `video-transcript-downloader` | Transcripturi și descărcări video/audio (cere `npm ci` + `yt-dlp`, `ffmpeg`) |
| `oracle` | A doua opinie de la alt model (GPT Pro) cu fișierele proiectului atașate |
| `create-cli` | Spec de UX pentru unelte CLI: flag-uri, help, ieșire, erori, exit codes |
| `github-deep-review` | Review de issue/PR cu cauză, proveniență, cea mai bună reparație, dovezi |
| `project-structure` | Hartă compactă de simboluri pentru repo-uri TypeScript/Swift (Node 20: prin `npx tsx`) |
| `floorplan` | Hartă interactivă a arhitecturii unei aplicații (Node ≥ 18) |
| `graphify` | Graf de cunoștințe peste cod/documente (cere CLI `graphify`: `uv tool install graphifyy`) |

### Surse externe

- `codex-first`, `skill-cleaner`, `markdown-converter`, `video-transcript-downloader`, `oracle`, `create-cli`, `github-deep-review`, `project-structure`: din [steipete/agent-scripts](https://github.com/steipete/agent-scripts) (MIT, vezi `LICENSE-steipete-agent-scripts.txt`), adaptate pentru Windows; `codex-first` și `skill-cleaner` rescrise.
- `floorplan`: [haydenschmitty/floorplan](https://github.com/haydenschmitty/floorplan) v0.11.0 (MIT).
- `graphify`: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) v0.9.115, varianta Windows (MIT/Apache-2.0). Nu rula `graphify install`: skill-ul e gestionat aici.

Actualizare: copiezi din nou folderul skill-ului din release-ul nou și păstrezi linia `Source:` din `SKILL.md`.

## Instalare pe un calculator nou

```powershell
git clone <url-repo-privat> $HOME\agent-skills
& $HOME\agent-skills\scripts\link-skills.ps1
```

Scriptul creează **junction-uri** (fără drepturi de admin) din:

- `~\.claude\skills\<skill>` → `agent-skills\skills\<skill>`
- `~\.codex\skills\<skill>` → `agent-skills\skills\<skill>`

Dacă există deja un folder real cu același nume, scriptul îl sare. Cu `-Force` îl mută
într-un backup (`~\.claude\skills-backup-<data>`) și pune junction-ul în loc.

## Flux de lucru

1. Editezi skill-ul în `agent-skills\skills\<skill>` (sau prin junction, e același fișier).
2. `git commit` + `git push`.
3. Pe alt calculator: `git pull`. Junction-urile văd imediat schimbarea.

Skill nou: creezi `skills\<nume>\SKILL.md`, apoi rulezi din nou `link-skills.ps1`.

## Ce NU intră aici

- Skill-uri built-in Anthropic (`pdf`, `docx`, `xlsx`, `pptx`, `skill-creator` etc.) și folderul `~\.claude\skills\synced\`, pe care îl gestionează aplicația Claude.
- Plugin-uri ale altor autori (`research-desk`, `heptabase`): se instalează prin sistemul de plugin-uri.
- Secrete: chei API, token-uri. Folosește variabile de mediu.
