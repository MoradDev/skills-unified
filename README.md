# Skills Unified

**A ready-to-use workspace for AI coding agents. Clone it, tell your agent to read
`SETUP.md`, and it installs the rest itself.**

*[Version française](README.fr.md)* · *Every command on one page: [CHEATSHEET.md](CHEATSHEET.md)*

Agent skills are scattered across dozens of repositories, with overlapping names,
competing descriptions and wildly varying quality. This repository is the result of
auditing 21 of them — 2808 skill files in total — and keeping the 83 that earn their
place, with the reasoning kept in the open.

It is not tied to Claude Code. Any agent that can read Markdown can use it.

---

## Quickstart

```bash
git clone https://github.com/MoradDev/skills-unified.git my-workspace
cd my-workspace
```

The folder name is yours to choose — nothing depends on it. Pick one that does not
already exist: Windows and macOS have case-insensitive filesystems, so a generic name
like `workspace` will collide with an existing `Workspace` and the clone will fail.

Then open your agent in that folder and give it one instruction:

> Read SETUP.md and set up this workspace.

That is all. The agent determines your OS, clones what the method needs into
`mes_depots/`, wires `curation/` into your projects using whatever mechanism your harness
supports, and reports what it did.

Nothing is installed globally. Nothing is activated behind your back.

---

## What you get

**83 curated skills**, in two families.

Plus the working method itself, built on [spec-kit](https://github.com/github/spec-kit):
every project starts with `specify init`, then runs constitution → specify → clarify →
plan → tasks → analyze → implement. Each step produces an artefact the next one consumes,
which is what keeps an agent from inventing requirements halfway through.

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

## The four repositories enabled by default

Four upstream repositories are linked into every new project without passing through the
curation above: `superpowers`, `taste-skill`, `ponytail` and `agency-agents`. That is a
deliberate exception, and the reason is plain — **for me this is the minimum required to code
well with an AI harness.** Not a vetted selection: a floor.

What each one actually contributes, from its own README and its own skills:

- **[`obra/superpowers`](https://github.com/obra/superpowers)** (15 skills) — a complete
  development methodology rather than a skill pack: it makes the agent tease a spec out of the
  conversation, write a plan a junior engineer could follow, then execute it through subagents
  under red/green TDD, with code review and a verification step before anything is called done.
- **[`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill)** (13 skills) — visual
  judgement. It carries a concrete design direction per style (editorial minimalist, Swiss
  brutalist, agency-grade polish) with the exact fonts, spacing and shadow rules, so a
  generated interface stops looking templated.
- **[`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail)** (6 skills) — a
  permanent YAGNI mode, active from session start, that pushes the agent to the shortest
  solution that works and reviews a diff or a whole repository for over-engineering. Its own
  benchmark reports ~54 % less code across 12 feature tasks against the same agent without it.
- **[`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents)** (297
  personas) — specialist subagents to delegate to, across engineering, design, security,
  testing, product and more, so a narrow task goes to something written for it instead of to
  the generalist.

**The overlaps were checked, and nothing was silently resolved.** Their skill and agent
`description` fields were compared against those of `curation/skills/`, because auto-invocation
is decided by description matching and namespacing does not prevent competition. Several real
overlaps exist — `superpowers:test-driven-development` against the per-language testing skills
(`react-testing` already points at it by name), `superpowers:using-superpowers` against
`using-agent-skills`, `superpowers:brainstorming` against `grill-me` and against spec-kit's own
specify step, `taste-skill:high-end-visual-design` against `make-interfaces-feel-better`, and a
handful of `agency-agents` personas against the skills covering the same stack. They are listed
in full in the pull request that added this section. None was removed: the floor stays whole,
and knowing where two triggers compete is more useful than pretending they do not.

## Why VoiceStudio, voicebox and SCAIL-2 are in the catalogue

They are never enabled — their `activation` is `stock`, meaning they sit in the catalogue as
parts, not as skills, and no agent loads them on its own. They are listed because the
applications bootstrapped here routinely ship AI of their own, and when one needs speech or a
vision-language model it is better to reach for a known, already-inspected project than to
improvise one. Propose them as components of the application being built, never as part of the
method.

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

## Pinned upstreams, and updating one

`catalog/repos.tsv` carries a `commit` column and a `scanned` date for every upstream
repository. `SETUP.md` clones **that commit**, not the branch tip, so what you install is the
state that was actually inspected. Without the pin, the scan above describes a past state of
a moving branch and says nothing about the code on your disk.

A pin has to be moved by hand, on purpose. The procedure:

1. **Read the diff.** `git -C mes_depots/<name> fetch origin && git -C mes_depots/<name> diff
   <old-sha>..origin/HEAD --stat`, or `https://github.com/<owner>/<repo>/compare/<old-sha>...<new-sha>`
   in a browser.
2. **Scan only the executable files the diff touched.** `git diff --name-only
   <old-sha>..<new-sha> -- '*.py' '*.sh' '*.js' '*.ts' '*.ps1'` gives the list. Extract the
   outbound domains, and look for `curl | sh`, `base64 -d | sh` and `eval` on a network
   response. Markdown changes are prose: read them if you like, but a scanner finding on a
   `.md` means nothing (see above).
3. **Read it yourself.** A human looks at every executable change before the pin moves. The
   scanner is an aid to that reading, never a substitute — and **never wire it in as an
   automatic gate**: it classifies Anthropic's own official skills as "DO NOT INSTALL", so a
   gate built on it would block correct code and teach everyone to skip it.
4. **Move the pin.** Write the new SHA into the `commit` column and the date you inspected it
   into `scanned`. Commit the TSV change on its own, with the comparison link in the message.
5. **Re-clone.** Delete `mes_depots/<name>` and run step 2 of `SETUP.md` again. Never
   `git pull` inside a pinned clone — that is how a cache quietly drifts away from its record.

A monthly GitHub Action ([`.github/workflows/upstream-watch.yml`](.github/workflows/upstream-watch.yml))
compares each pin against its branch tip and keeps a single issue listing what has moved. It
only reports. It changes nothing and blocks nothing.

## One project, several agents

Every harness keeps its own private memory, and none of them can read another's. Start a
project in Claude Code, continue it in Cursor next week, and the second agent arrives
blind — the spec is on disk, but every decision taken in conversation is gone.

So the shared state lives in the repository, in **`STATE.md` at the project root**: current
step, last and next action, decisions taken in conversation *with their reasoning*,
blockers, and traps discovered the hard way. Plain Markdown, no tooling.

`AGENTS.md` makes it binding — read it on arrival, update it before leaving, even after a
session that produced nothing ("explored X, dead end, do not retry" is worth writing). The
`Journal` section is append-only, so two agents can never overwrite each other's history,
and a "harness-specific notes" table is where an agent mirrors anything its private memory
holds that others would need.

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
