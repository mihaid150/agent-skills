#!/usr/bin/env bash
# Symlink each skill from this repo into ~/.claude/skills and ~/.codex/skills (Linux/macOS).
# Without --force: skips existing real folders. With --force: moves them to a backup first.
# graphify is skipped: on Linux/macOS run `graphify install` (and `--platform codex`) instead.
set -u

force=0
[ "${1:-}" = "--force" ] && force=1

repo_skills="$(cd "$(dirname "$0")/../skills" && pwd)"
stamp="$(date +%Y%m%d-%H%M%S)"
skip="graphify"

for root in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$root"
  for skill in "$repo_skills"/*/; do
    name="$(basename "$skill")"
    target="${skill%/}"
    link="$root/$name"

    if [ "$name" = "$skip" ]; then echo "skip    $link (use: graphify install)"; continue; fi

    if [ -L "$link" ]; then
      if [ "$(readlink "$link")" = "$target" ]; then echo "ok      $link"; continue; fi
      rm "$link"  # symlink to another place: remove only the link
    elif [ -e "$link" ]; then
      if [ "$force" -eq 0 ]; then echo "SKIP    $link (real folder; rerun with --force)"; continue; fi
      backup="$root-backup-$stamp"
      mkdir -p "$backup"
      mv "$link" "$backup/$name"
      echo "backup  $link -> $backup"
    fi

    if ln -s "$target" "$link"; then echo "linked  $link"; else echo "FAILED  $link"; fi
  done
done
