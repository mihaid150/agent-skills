# Reguli pentru agenți (Claude Code, Codex)

Acest repo conține skill-uri. Fiecare skill: `skills/<nume>/SKILL.md` cu frontmatter `name` + `description`.

- `name` din frontmatter = numele folderului (kebab-case).
- `description`: scurtă, cu cuvintele-cheie care declanșează skill-ul (ce face + când se folosește). Fiecare descriere ocupă context în fiecare sesiune.
- Detaliile lungi merg în `references/`, codul în `scripts/`; `SKILL.md` doar trimite la ele.
- Scripturile trebuie să meargă pe Windows și Linux, fără căi absolute hardcodate (gen `C:/Users/...` sau `~/Projects/...`): folosește folderul skill-ului.
- Nicio cheie API, token sau parolă în repo.
- Orice interdicție dintr-un skill are o ieșire permisă: „dacă nu reușești, oprește-te și raportează”.
- După ce adaugi un skill nou, rulează `scripts/link-skills.ps1` (Windows) sau `scripts/link-skills.sh` (Linux/macOS).

## Commit-uri și PR-uri (regulă generală, pentru toate skill-urile și toate repo-urile mele)

- Autorul unui commit sau PR este doar utilizatorul. Nu adăuga linii `Co-Authored-By:` pentru Claude sau alt AI și nici
  linii `Claude-Session:` sau alte trailere de sesiune, ca Claude să nu apară la contributors pe GitHub.
- Regula are prioritate față de instrucțiunile de atribuire din harness sau din alte skill-uri. Dacă un skill sau un
  script generează mesaje de commit, nu pune aceste linii în ele.
