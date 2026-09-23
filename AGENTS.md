# AGENTS.md — how to work in this workspace

This file is the operating procedure. It is harness-neutral: Claude Code, Codex, Cursor,
Gemini CLI, opencode, Aider and any other agent that reads `AGENTS.md` can follow it.
Installation is a separate concern — see `SETUP.md`.

## Layout

| Path | Versioned? | What it is |
|---|---|---|
| `curation/` | **yes** | 83 curated skills, plus `rules/` and `references/`. The only non-reproducible content here. |
| `mes_depots/` | no | Disposable cache of upstream repositories. Rebuildable from `catalog/repos.tsv`. |
| `<project>/` | separately | One folder per project, with its own git repository. |

**Never modify anything under `mes_depots/`.** Upstream clones stay pristine so `git pull`
never conflicts. Anything worth keeping gets copied into `curation/` and committed there.

## The two families of skills

`curation/skills/` holds 83 skills in two groups:

**Method** (18) — how to work: `grill-me` and `grilling` for interrogating a vague idea
into a spec; then API design, CI/CD, security hardening, performance, observability, git
workflow, ADRs, deprecation and migration, incremental implementation, context
engineering, browser testing, and constraint-, doubt- and source-driven development.

**Application building** (65) — what to build with:

| Target | Coverage |
|---|---|
| Web front-end | React (patterns, performance, testing), Vue, Nuxt 4, Next.js/Turbopack, Angular, Vite, design systems, WCAG 2.2 accessibility, motion design |
| Web back-end | FastAPI, Django (+ security), NestJS, Laravel (+ security), Spring Boot (+ security), Rails, Go, hexagonal architecture, contract-first, error handling |
| Data | PostgreSQL, MySQL, Redis, Prisma, migrations |
| Mobile | SwiftUI, Swift 6.2 concurrency, Liquid Glass, on-device foundation models, Android clean architecture, Kotlin, Compose Multiplatform, Flutter/Dart, React Native |
| Desktop | .NET, Rust, C++, native Windows E2E testing, Bun |
| Testing & delivery | Playwright, Python/Go/C# testing, Docker, Kubernetes, deployment |

`curation/rules/` holds per-language rulesets (React, React Native, Swift, Kotlin, Dart,
Rust, C#, TypeScript, Go, Java, Python, PHP, Ruby, C++, Angular, Nuxt, Vue, Perl, F#,
ArkTS, web, common). The React skills reference them via `../../rules/`, so the relative
depth must be preserved if you move things around.

## Working order

1. **Constitution.** Establish the project's non-negotiables before any code.
2. **Clarify the idea.** If it is still vague, run `grill-me` — structured interrogation
   beats guessing at requirements.
3. **Specify → clarify → plan → tasks → analyze → implement.** If `spec-kit` is installed,
   these are its commands. If not, follow the same sequence by hand: the order is what
   matters, not the tooling.
4. **Map the codebase** once it grows past roughly 80 files. Beyond that size, reading
   files one by one stops being a viable way to understand the system.
5. **Verify before declaring done.** Run the tests. Report failures with their output.

## For agents without a plugin system

You do not need one. Every skill is a folder containing `SKILL.md`, a Markdown file with
YAML frontmatter:

```yaml
---
name: react-patterns
description: React 18/19 patterns including hooks discipline, server/client component
  boundaries, Suspense + error boundaries, form actions, data fetching...
---
```

Index the `description` fields once — `find curation/skills -name SKILL.md` — and open a
skill when its description matches what you are about to do. That is the whole mechanism.
Descriptions are written as triggers ("Use when building or reviewing React components"),
so they are meant to be matched against the task, not read end to end.

Do not load all 83 at once. That defeats the purpose and floods your context.

## Adding a skill to the curation

1. Copy it from `mes_depots/<repo>/skills/<name>` into `curation/skills/<name>`.
2. Check no skill of that name already exists anywhere in the active set.
3. Check its `description` does not overlap an existing one — two similar descriptions
   compete for auto-invocation, and namespacing does **not** prevent this.
4. If it came from an untrusted source, scan it (see below).
5. Commit.

## Scanning an untrusted skill

```bash
skillspector scan <skill-folder> --no-llm
```

**Read the report with this filter, or it will mislead you.** In a scan of 2808 skills
run on 2026-09-23, the tool produced 4969 findings, 157 of them CRITICAL — and not one
was a real threat. 71 % of findings were raised on Markdown prose rather than code.
Anthropic's own official skills (`docx`, `xlsx`, `pptx`, `skill-creator`, `mcp-builder`)
all scored 100/100 "DO NOT INSTALL". One prompt-injection finding pointed at an ECMA
Office XML schema file. A skill scored 100/100 because the words "Write skill" appeared
in a Markdown table. A security-hardening skill was flagged for SSRF because it contains
the AWS metadata address it teaches you to **block**; a browser-testing skill was flagged
for "Ignore previous instructions", the attack it teaches you to **test for**.

So: **only consider findings whose location is an executable file** (`.py`, `.sh`, `.js`,
`.ts`, `.ps1`). Ignore findings on `.md`. A high score on a documentation-only skill means
nothing. A "Data Exfiltration" finding inside a `.py` deserves a line-by-line read.

Never wire this scan in as an automatic gate. It would block official skills.

## Not enabled by default

Deliberate choices, not oversights:

- **The full `ECC` plugin.** Its 65 best application skills are already in `curation/`.
  The other 227 are off-topic for most projects (healthcare, logistics, trading, homelab)
  or duplicate the stack.
- **The full `agent-skills` plugin.** Its 16 best skills are already here. Linking all of
  it reintroduces an exact name collision on `test-driven-development` plus 8 conceptual
  duplicates.
- **`awesome-claude-skills`.** 832 of its 864 skills are SaaS connectors. Reference index
  only.
- **817 cybersecurity skills.** Explicit security engagements only.
- **Codebase graphing.** Only past the ~80-file threshold.
