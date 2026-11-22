# Reguli pentru agenți (Claude Code, Codex)

Acest repo conține skill-uri. Fiecare skill: `skills/<nume>/SKILL.md` cu frontmatter `name` + `description`.

- `name` din frontmatter = numele folderului (kebab-case).
- `description`: scurtă, cu cuvintele-cheie care declanșează skill-ul (ce face + când se folosește). Fiecare descriere ocupă context în fiecare sesiune.
- Detaliile lungi merg în `references/`, codul în `scripts/`; `SKILL.md` doar trimite la ele.
- Scripturile trebuie să meargă pe Windows (PowerShell / Python), fără căi hardcodate de tip `~/Projects/...`.
- Nicio cheie API, token sau parolă în repo.
- Orice interdicție dintr-un skill are o ieșire permisă: „dacă nu reușești, oprește-te și raportează”.
- După ce adaugi un skill nou, rulează `scripts/link-skills.ps1`.
