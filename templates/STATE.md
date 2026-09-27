<!--
  STATE.md — shared working state, readable and writable by ANY agent.

  This file exists because every harness keeps its own private memory: Claude Code,
  Codex, Cursor and the rest cannot read each other's. Whatever matters for continuing
  the work must live here, in the repository, or the next agent starts blind.

  Two rules make it work:
    1. Read this file BEFORE anything else when you open the project.
    2. Update it BEFORE you finish, even if the session produced nothing.

  Structure: the top half is current state and gets overwritten. The Journal at the
  bottom is APPEND-ONLY — never rewrite or delete an existing entry, only add a line.
  That way two agents can never destroy each other's history.
-->

# Working state — <PROJECT>

**Last updated:** <YYYY-MM-DD> by <harness, e.g. Claude Code / Codex / Cursor>

## Where we are

Current step in the spec-kit flow: **<constitution | specify | clarify | plan | tasks | analyze | implement | converge>**

<One paragraph in plain language: what the project is, and how far it has got. Written
for someone opening this repository for the first time with no conversation history.>

## Last action

<What the previous session actually did. Concrete: files touched, decisions applied,
tests run and their result.>

## Next action

<The single next thing to do. Be specific enough that another agent can start without
asking the human what was meant.>

## Decisions made

Only decisions that are NOT already recorded in `.specify/` artefacts. This is the part
that otherwise evaporates with the conversation — keep the reasoning, not just the choice.

| Date | Decision | Why | Rejected alternative |
|---|---|---|---|
| | | | |

## Open questions and blockers

<What is waiting on the human, on an external dependency, or on a decision not yet taken.
Write "none" rather than deleting the section.>

## Known traps

<Things learned the hard way in this project: a command that needs an extra flag, a test
that is flaky, an API that behaves differently than documented. Each one saved here is an
hour another agent does not lose.>

## Harness-specific notes

If your harness keeps private memory, rules or context that another agent cannot read,
**mirror the relevant part here**. Name the harness, so the next agent knows what it is
looking at and whether it still applies.

| Harness | What it holds privately | What matters to others |
|---|---|---|
| | | |

## Journal

Append-only. One line per session, newest at the bottom. Never edit an existing line.

| Date | Harness | What happened |
|---|---|---|
| | | |
