#!/usr/bin/env python3
"""Build or check the catalog table in README.md from each skill's frontmatter.

Usage:
    python scripts/build_catalog.py          rewrite the table in README.md
    python scripts/build_catalog.py --check  exit 1 if README.md is stale or an entry is invalid

Standard library only. Frontmatter parsing is deliberately minimal: top-level
``key: value`` pairs and block scalars (``key: |`` or ``key: >``). Indented
lines under a key with no value (for example ``metadata:``) are ignored.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = ROOT / "skills"
DOC_NAME = "SKILL.md"
README = ROOT / "README.md"
COLUMNS = [("Skill", "name"), ("Description", "description")]
ALLOWED: dict[str, set[str]] = {}
START, END = "<!-- catalog:start -->", "<!-- catalog:end -->"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    key: str | None = None
    block: list[str] | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if block is not None:
            if line.startswith((" ", "\t")) or not line.strip():
                block.append(line.strip())
                continue
            fields[key] = " ".join(s for s in block if s)
            block = None
        match = KEY_RE.match(line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in ("|", ">", "|-", ">-"):
            block = []
        else:
            fields[key] = value.strip("\"'")
    if block is not None and key is not None:
        fields[key] = " ".join(s for s in block if s)
    return fields


def load_items() -> tuple[list[dict[str, str]], list[str]]:
    items: list[dict[str, str]] = []
    errors: list[str] = []
    if not ITEMS_DIR.is_dir():
        return items, [f"missing directory {ITEMS_DIR.name}/"]
    for folder in sorted(p for p in ITEMS_DIR.iterdir() if p.is_dir()):
        if folder.name.startswith(("_", ".")):
            continue
        doc = folder / DOC_NAME
        if not doc.is_file():
            errors.append(f"{folder.name}: missing {DOC_NAME}")
            continue
        fm = parse_frontmatter(doc.read_text(encoding="utf-8"))
        if not NAME_RE.match(folder.name):
            errors.append(f"{folder.name}: folder name must be lowercase letters, digits and hyphens")
        if fm.get("name") != folder.name:
            errors.append(f"{folder.name}: frontmatter name {fm.get('name')!r} must equal the folder name")
        if not fm.get("description"):
            errors.append(f"{folder.name}: description is required")
        for field, allowed in ALLOWED.items():
            if fm.get(field, "") not in allowed:
                errors.append(f"{folder.name}: {field} must be one of {sorted(allowed)}")
        fm["name"] = folder.name
        fm["_path"] = f"{ITEMS_DIR.name}/{folder.name}/{DOC_NAME}"
        items.append(fm)
    return items, errors


def render(items: list[dict[str, str]]) -> str:
    header = "| " + " | ".join(title for title, _ in COLUMNS) + " |"
    separator = "|" + "|".join("---" for _ in COLUMNS) + "|"
    rows = []
    for item in items:
        cells = []
        for _, field in COLUMNS:
            value = item.get(field, "").replace("|", "\\|")
            if field == "name":
                value = f"[{value}]({item['_path']})"
            cells.append(value)
        rows.append("| " + " | ".join(cells) + " |")
    if not rows:
        rows.append("| _none yet_ |" + " |" * (len(COLUMNS) - 1))
    return "\n".join([header, separator, *rows])


def splice(readme: str, table: str) -> str:
    if START not in readme or END not in readme:
        sys.exit(f"error: {README.name} must contain {START} and {END}")
    before, rest = readme.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}\n{table}\n{END}{after}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check", action="store_true", help="verify instead of rewrite")
    args = parser.parse_args()

    items, errors = load_items()
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    current = README.read_text(encoding="utf-8")
    updated = splice(current, render(items))

    if args.check:
        if updated != current:
            print(f"error: {README.name} catalog is stale; run scripts/build_catalog.py", file=sys.stderr)
            return 1
        return 1 if errors else 0
    if errors:
        return 1
    if updated != current:
        README.write_text(updated, encoding="utf-8")
    print(f"catalog: {len(items)} entries in {README.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
