"""Audit installed agent skills for Claude Code and Codex.

Reports: every skill found per root, description size (context cost), duplicates
(same name, or near-identical description), long descriptions, and skills not
mentioned in recent Claude/Codex transcripts. Read-only: never edits or deletes.

Usage: python skill_cleaner.py [--months 3] [--no-logs] [--max-desc 300]
"""
import argparse
import difflib
import os
import re
import time
from collections import defaultdict
from pathlib import Path

HOME = Path.home()
ROOTS = {
    "claude": HOME / ".claude" / "skills",
    "claude-plugins": HOME / ".claude" / "plugins",
    "codex": HOME / ".codex" / "skills",
    "codex-plugins": HOME / ".codex" / "plugins",
}
LOG_DIRS = [HOME / ".claude" / "projects", HOME / ".codex" / "sessions"]


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "\t", "-")):
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def scan():
    skills = []
    for root_name, root in ROOTS.items():
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            parts = set(skill_md.parts)
            if ".staging" in parts or any(p.startswith(".replaced-") for p in skill_md.parts):
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = frontmatter(text)
            desc = fm.get("description", "")
            skills.append({
                "root": root_name,
                "name": fm.get("name") or skill_md.parent.name,
                "path": str(skill_md.parent),
                "real": os.path.realpath(skill_md.parent),
                "desc": desc,
                "desc_tokens": len(desc) // 4,
                "body_tokens": len(text) // 4,
            })
    return skills


def recent_mentions(names, months):
    cutoff = time.time() - months * 30 * 86400
    counts = defaultdict(int)
    pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])")
    for d in LOG_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*.jsonl"):
            if f.stat().st_mtime < cutoff:
                continue
            seen = set(pattern.findall(f.read_text(encoding="utf-8", errors="replace")))
            for n in seen:
                counts[n] += 1  # number of sessions mentioning the skill
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--months", type=int, default=3)
    ap.add_argument("--no-logs", action="store_true")
    ap.add_argument("--max-desc", type=int, default=300, help="flag descriptions longer than this (chars)")
    a = ap.parse_args()

    skills = scan()
    print(f"# Skill audit ({len(skills)} SKILL.md files)\n")

    print("## Per root (description tokens = loaded into every session)")
    by_root = defaultdict(list)
    for s in skills:
        by_root[s["root"]].append(s)
    for root, items in by_root.items():
        print(f"- {root}: {len(items)} skills, ~{sum(s['desc_tokens'] for s in items)} description tokens")

    print("\n## Duplicates by name (different real folders)")
    by_name = defaultdict(list)
    for s in skills:
        by_name[s["name"]].append(s)
    found = False
    for name, items in sorted(by_name.items()):
        reals = {s["real"] for s in items}
        if len(reals) > 1:
            found = True
            print(f"- {name}:")
            for s in items:
                print(f"    [{s['root']}] {s['path']}")
    if not found:
        print("- none")

    print("\n## Near-identical descriptions (different names)")
    uniq = {s["real"]: s for s in skills}.values()
    uniq = [s for s in uniq if s["desc"]]
    found = False
    for i, x in enumerate(uniq):
        for y in uniq[i + 1:]:
            if x["name"] != y["name"]:
                r = difflib.SequenceMatcher(None, x["desc"], y["desc"]).ratio()
                if r > 0.8:
                    found = True
                    print(f"- {x['name']} ~ {y['name']} ({r:.0%})")
    if not found:
        print("- none")

    print(f"\n## Long descriptions (> {a.max_desc} chars)")
    long = sorted((s for s in uniq if len(s["desc"]) > a.max_desc), key=lambda s: -len(s["desc"]))
    for s in long:
        print(f"- {s['name']}: {len(s['desc'])} chars [{s['root']}]")
    if not long:
        print("- none")

    if not a.no_logs:
        names = sorted({s["name"] for s in skills})
        counts = recent_mentions(names, a.months)
        print(f"\n## Usage: sessions mentioning each skill (last {a.months} months)")
        for n in sorted(names, key=lambda n: counts.get(n, 0)):
            print(f"- {n}: {counts.get(n, 0)}")
        print("\n(0 = candidate for removal. A mention is a hint, not proof of use.)")


if __name__ == "__main__":
    main()
