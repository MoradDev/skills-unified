# Skills Unified

**A ready-to-use workspace for AI coding agents. Clone it, tell your agent to read
`SETUP.md`, and it installs the rest itself.**

*[Version française](README.fr.md)*

Agent skills are scattered across dozens of repositories, with overlapping names,
competing descriptions and wildly varying quality. This repository is the result of
auditing 21 of them — 2808 skill files in total — and keeping the 83 that earn their
place, with the reasoning kept in the open.

It is not tied to Claude Code. Any agent that can read Markdown can use it.

---

## Quickstart

```bash
git clone https://github.com/MoradDev/skills-unified.git workspace
cd workspace
```

Then open your agent in that folder and give it one instruction:

> Read SETUP.md and set up this workspace.

That is all. The agent determines your OS, clones what the method needs into
`mes_depots/`, wires `curation/` into your projects using whatever mechanism your harness
supports, and reports what it did.

Nothing is installed globally. Nothing is activated behind your back.

---

## What you get

**83 curated skills**, in two families.

*Method* (18) — turning a vague idea into working software: structured interrogation of
an idea before writing a spec, API design, CI/CD, security hardening, performance,
observability, git workflow, ADRs, migration, incremental delivery, context engineering,
browser testing, and constraint-, doubt- and source-driven development.

*Application building* (65) — the actual craft:

| Target | Coverage |
|---|---|
| **Web front-end** | React (patterns, performance, testing), Vue, Nuxt 4, Next.js/Turbopack, Angular, Vite, design systems, WCAG 2.2 accessibility, motion design |
| **Web back-end** | FastAPI, Django, NestJS, Laravel, Spring Boot, Rails, Go, hexagonal architecture, contract-first, error handling — with dedicated security skills for Django, Laravel and Spring Boot |
| **Data** | PostgreSQL, MySQL, Redis, Prisma, migrations |
| **Mobile** | SwiftUI, Swift 6.2 concurrency, Liquid Glass, on-device foundation models, Android clean architecture, Kotlin, Compose Multiplatform, Flutter/Dart, React Native |
| **Desktop** | .NET, Rust, C++, native Windows E2E testing, Bun |
| **Testing & delivery** | Playwright, Python/Go/C# testing, Docker, Kubernetes, deployment |

Plus **per-language rulesets** for 21 languages and frameworks, and a **catalogue** of 21
upstream repositories with their role and activation policy.

---

## Why a curation rather than a pile

Adding every skill you find makes an agent *worse*, not better. Auto-invocation is driven
by the `description` field, so two skills with similar descriptions compete — and
namespacing does not prevent it. Every skill you add is also context you spend.

So the selection rejects more than it keeps:

- **227 of ECC's 292 skills** — off-topic for most projects (healthcare, logistics,
  trading, homelab) or duplicating what is already here.
- **832 of awesome-claude-skills' 864** — SaaS connectors, kept as a reference index only.
- **9 of agent-skills' 25** — one exact name collision on `test-driven-development`, plus
  eight conceptual duplicates.
- **Three tempting ones dropped for trigger overlap**: `frontend-patterns` (covered by
  `react-patterns` + `react-performance`), `frontend-a11y` (covered by `accessibility`),
  `browser-qa` (covered by `browser-testing-with-devtools`).

The selection is **closed under its own cross-references**: every `../skill/SKILL.md`
link was followed transitively so nothing points into the void. Final check: 18 relative
links, 0 broken. 83 skills, 83 distinct names, every one carrying a `description`.

---

## On scanning skills for safety

Everything here was scanned with [NVIDIA SkillSpector](https://github.com/NVIDIA/Skillspector).
**No malicious code was found.** But the raw report said otherwise — 4969 findings, 157
CRITICAL — and that gap is worth publishing, because anyone scanning skills will hit it.

71 % of findings were raised on Markdown prose, not code. Anthropic's own official skills
(`docx`, `xlsx`, `pptx`, `skill-creator`, `mcp-builder`) all scored **100/100 "DO NOT
INSTALL"**. One prompt-injection finding pointed at an ECMA Office XML schema file.
A skill scored 100/100 because the words *"Write skill"* appeared in a Markdown table and
matched a "Self-Modification" pattern. A security-hardening skill was flagged for SSRF
because it contains `169.254.169.254` — the address it teaches you to **block**. A
browser-testing skill was flagged for *"Ignore previous instructions"*, the attack it
teaches you to **test for**.

**Read scanner reports with this filter: only findings located in executable files
(`.py`, `.sh`, `.js`, `.ts`) mean anything. Ignore findings on `.md`.** And never wire
such a scan in as an automatic gate — it would block official skills.

Independent verification was run alongside: every outbound domain in the new
repositories' scripts was extracted by hand (all legitimate), and dropper patterns
(`curl | sh`, `base64 -d | sh`, `eval` on a network response) were searched for — the only
hit was a project's own documented installer.

*Caveat, stated plainly:* 1517 skills were marked "incomplete" by the scanner and 165
files were never inspected at all, due to its 1 MB per-file ceiling. Coverage is not total.

---

## Works with any agent

| Harness | How |
|---|---|
| **Claude Code** | `curation/` carries a `plugin.json`, so it auto-loads as a skills-directory plugin. No marketplace, no install step. |
| **Codex** and other `AGENTS.md`-aware agents | `AGENTS.md` is already written for you. |
| **Cursor** | Point a rule file at `curation/skills/`. |
| **Gemini CLI, opencode, Aider, Continue, …** | No plugin system needed — index the `description` frontmatter and open a `SKILL.md` when it matches the task. |

`AGENTS.md` is harness-neutral and holds the working method. `CLAUDE.md` adds only what
is Claude Code specific. `SETUP.md` is the installation procedure, written to be executed
by an agent rather than read by a human.

---

## Licence and credit

MIT. **None of the skills were written here** — the contribution is the selection, the
de-duplication, the cross-reference repair and the method around them.

They come from [`affaan-m/ECC`](https://github.com/affaan-m/ECC) (65),
[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) (16) and
[`mattpocock/skills`](https://github.com/mattpocock/skills) (2), all MIT.
Full provenance, skill by skill, plus the three modifications made and the projects
referenced but not redistributed: [`ATTRIBUTION.md`](ATTRIBUTION.md).

If you are one of those authors and would rather not be redistributed here, open an
issue — it will be removed and replaced by a pointer to your repository.
