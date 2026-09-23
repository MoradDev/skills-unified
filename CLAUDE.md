# CLAUDE.md

**Read `AGENTS.md` first — it holds the operating procedure and applies to you in full.**
This file only adds what is specific to Claude Code.

## Installing the curation

`curation/` is a skills-directory plugin: it carries `.claude-plugin/plugin.json`, so
placing it under a project's `.claude/skills/` makes it auto-load as `curation@skills-dir`.
No marketplace, no install command.

```powershell
# Windows — junctions need no administrator rights
New-Item -ItemType Junction -Path ".claude\skills\curation" -Target "<workspace>\curation"
```

```bash
# macOS / Linux
ln -s "<workspace>/curation" ".claude/skills/curation"
```

Two things to know, both learned the hard way:

- Project scope loads only from the session's **primary working directory**. It does not
  walk up to the repository root. Open the session *in the project folder*.
- The human must accept the workspace-trust prompt once, or nothing loads.

## Namespacing

Plugin skills are invoked as `/curation:react-patterns`. A bare `<name>/SKILL.md` placed
directly under `.claude/skills/` loads unnamespaced as `/name` instead.

Namespacing affects invocation only. It does **not** stop two skills with similar
`description` fields from competing for auto-invocation — that is decided purely by
description matching. Check descriptions, not just names, before adding a skill.

## Subagents

If the workspace includes agent personas, copy them into `<project>/.claude/agents/`
rather than linking — Claude Code reads that directory directly.

Note that subagents execute inside the main session, so any isolation mechanism that
wraps the agent from the outside cannot be invoked at delegation time.
