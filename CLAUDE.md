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

## Context7 MCP server

Install once, at **user scope**, so every project inherits it and no credential lands in a
project repository:

```bash
claude mcp add --transport http --scope user context7 https://mcp.context7.com/mcp   --header "Authorization: Bearer <YOUR_CONTEXT7_API_KEY>"
```

Get a key at [context7.com](https://context7.com). Check it is live with `claude mcp list`.
The tools then appear as `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`.

The usage discipline — when to call, one notion per query, and the obligation to verify the
documentation matches the version the project actually uses — is in `AGENTS.md`
§ "External library documentation". It applies in full.

## Private memory

Claude Code keeps memory under `~/.claude/` that no other harness can read — not Codex, not
Cursor, not a future Claude session opened elsewhere. Treat it as a scratchpad, never as the
record.

Anything another agent would need in order to continue goes into the project's `STATE.md`,
as described in `AGENTS.md` § "Continuity across agents". Mirror it there before you finish,
and name Claude Code in the harness-specific table so the next agent knows the origin.

## Subagents

If the human asked for agent personas, copy them into `<project>/.claude/agents/` rather
than linking — Claude Code reads that directory directly, so a junction to a repository full
of READMEs and scripts is not it. Copy **by division** and only files whose name starts with a
lowercase letter; `SETUP.md` step 4b has the exact commands and the reason the whole block is
not copied by default (about 15,800 tokens of agent descriptions per session for 297 personas,
against three or four actually used).

Note that subagents execute inside the main session, so any isolation mechanism that
wraps the agent from the outside cannot be invoked at delegation time.
