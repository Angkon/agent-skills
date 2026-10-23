#!/usr/bin/env bash
# Link (or copy) every skill under skills/ into the personal skill folders of
# Claude Code (~/.claude/skills) and Codex (~/.agents/skills).
#
# Usage:
#   scripts/install.sh                  symlink into both tools
#   scripts/install.sh --copy           copy instead of symlink
#   scripts/install.sh --target claude  one tool only: claude or codex
#   scripts/install.sh --force          replace entries that already exist
#
# Override the destinations with CLAUDE_SKILLS_DIR and CODEX_SKILLS_DIR.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mode="link"
targets="claude codex"
force=0

usage() {
  sed -n '2,11p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) mode="copy" ;;
    --target)
      [[ $# -ge 2 ]] || { echo "--target needs a value" >&2; exit 1; }
      targets="$2"; shift ;;
    --force) force=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

dest_for() {
  case "$1" in
    claude) echo "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" ;;
    codex)  echo "${CODEX_SKILLS_DIR:-$HOME/.agents/skills}" ;;
    *) echo "unknown target: $1 (expected claude or codex)" >&2; exit 1 ;;
  esac
}

installed=0
for target in $targets; do
  dest="$(dest_for "$target")"
  mkdir -p "$dest"
  for skill in "$here"/skills/*/; do
    skill="${skill%/}"
    [[ -f "$skill/SKILL.md" ]] || continue
    name="$(basename "$skill")"
    [[ -n "$name" && "$name" != "." && "$name" != ".." ]] || continue
    out="$dest/$name"
    if [[ -e "$out" || -L "$out" ]]; then
      if [[ $force -eq 1 ]]; then
        rm -rf "$out"
      else
        echo "skip  $out (exists; use --force to replace)"
        continue
      fi
    fi
    if [[ $mode == "link" ]]; then
      ln -s "$skill" "$out"
    else
      cp -R "$skill" "$out"
    fi
    echo "$mode  $name -> $out"
    installed=$((installed + 1))
  done
done
echo "done: $installed installed"
