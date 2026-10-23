---
name: research-method-writeup
description: Document a research method as a METHOD.md with provenance and validation sections, in the format used by the research-methods repository. Use when asked to write up, record, or formalize a method, procedure, algorithm, or analysis recipe for reuse.
metadata:
  author: Angkon Biswas
  origin: human
---

# Research method write-up

Produce one `METHOD.md` that another researcher, or another agent, can follow without access to the conversation that produced the method.

## Steps

1. **Draw the boundary.** State what question the method answers, what it takes in, and what it produces. If the conversation contains several methods, write one file per method.
2. **Collect provenance first.** Who derived it (a person, an agent, or both), which tool and model, which skill or prompt, and on what date. Ask for anything missing instead of guessing.
3. **Write `METHOD.md`** from the template below. If the target repository has `methods/_template/METHOD.md`, use that instead, since it may be newer.
4. **Make the procedure executable.** Numbered steps, exact commands or equations, parameter defaults, and expected runtime.
5. **Make validation concrete.** Name the test, dataset, or sanity check that shows the method works, and record the numbers actually observed.
6. **Record limitations** and the failure modes seen while developing it.
7. **Set `status` honestly.** `draft` until validation has observed results, `validated` once the checks pass, `published` once it is cited in a paper.

## Rules

- Record only what was actually run or derived. Mark anything untested as untested.
- Keep the file self-contained. Link to code rather than pasting large blocks.
- Prefer plain language. The reader may not share the jargon of the project the method came from.
- Do not invent provenance. An unknown model or date is written as `unknown`.

## Template

```markdown
---
name: <folder-name>
description: <one sentence: what it does and when to use it>
status: draft
origin: human | agent | mixed
agent: claude-code | codex | none
model: <model id or unknown>
skill: <link to the SKILL.md used, or empty>
derived: YYYY-MM-DD
---

# <Method name>

## Summary
## Problem
## Inputs and outputs
## Procedure
## Validation
## Limitations and failure modes
## Provenance
## Used in
## References
```
