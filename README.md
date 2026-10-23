# agent-skills

Skills I write for coding agents. Each skill is a folder with a `SKILL.md` in the [Agent Skills](https://agentskills.io) format, which both [Claude Code](https://code.claude.com/docs/en/skills) and [Codex](https://developers.openai.com/codex/skills) load, so one copy serves both tools.

## Catalog

<!-- catalog:start -->
| Skill | Description |
|---|---|
| [research-method-writeup](skills/research-method-writeup/SKILL.md) | Document a research method as a METHOD.md with provenance and validation sections, in the format used by the research-methods repository. Use when asked to write up, record, or formalize a method, procedure, algorithm, or analysis recipe for reuse. |
<!-- catalog:end -->

The table is generated. Regenerate it with `python scripts/build_catalog.py`; CI fails if it is stale.

## Layout

```
skills/<skill-name>/SKILL.md            required: frontmatter (name, description) and instructions
skills/<skill-name>/scripts/            optional helper scripts the skill runs
skills/<skill-name>/references/         optional material the agent reads on demand
skills/<skill-name>/assets/             optional templates and files the skill produces
skills/<skill-name>/agents/openai.yaml  optional Codex-only metadata
templates/skill/SKILL.md                starting point for a new skill
scripts/install.sh                      links or copies the skills into both tools
scripts/build_catalog.py                regenerates the catalog table above
```

## Install

Claude Code reads personal skills from `~/.claude/skills/<name>/SKILL.md` and project skills from `<repo>/.claude/skills/<name>/SKILL.md`. Codex reads personal skills from `~/.agents/skills/<name>/SKILL.md` and project skills from `<repo>/.agents/skills/<name>/SKILL.md`. Paths are as of October 2026; the links at the top of this page are the authoritative references.

`scripts/install.sh` links every skill into both personal locations:

```sh
git clone https://github.com/Angkon/agent-skills ~/agent-skills
~/agent-skills/scripts/install.sh                   # symlink into both tools
~/agent-skills/scripts/install.sh --copy            # copy instead of symlink
~/agent-skills/scripts/install.sh --target claude   # one tool only (claude or codex)
~/agent-skills/scripts/install.sh --force           # replace existing entries
```

To ship a skill with a particular project instead, copy its folder into that repository's `.claude/skills/` and `.agents/skills/`.

## Writing a new skill

1. `cp -r templates/skill skills/<skill-name>`.
2. Fill in the frontmatter. `name` must equal the folder name (lowercase letters, digits, hyphens). `description` says what the skill does and when to use it; this is all the agent sees before deciding whether to load the skill, so make it specific.
3. Keep `SKILL.md` focused. Move long reference material to `references/` and point to it from the instructions.
4. Try it in both tools and fix anything that only works in one.
5. Run `python scripts/build_catalog.py` and commit.

## Provenance

Each skill's frontmatter carries a `metadata` block with `author` and `origin` (`human`, `agent`, or `mixed`), so it is clear who or what wrote it.

## License

MIT, see [LICENSE](LICENSE).
