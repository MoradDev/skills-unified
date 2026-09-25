# Cheat sheet

*[Version française](CHEATSHEET.fr.md)*

Every command this workspace gives you, on one page. Claude Code gets a short section;
everything the workspace itself ships or installs is listed in full.

**How to invoke a skill depends on your agent.** Skills trigger on their own when their
`description` matches the task, so you rarely need to call one explicitly. When you do:

| Agent | Curated skill | Plugin skill |
|---|---|---|
| Claude Code | `/curation:<name>` | `/<plugin>:<name>`, e.g. `/superpowers:writing-plans` |
| Any other agent | Ask for it by name, or open `curation/skills/<name>/SKILL.md` | Same, in `mes_depots/<plugin>/skills/` (Codex uses `@<name>` where the plugin supports it) |

---

## Contents

1. [Claude Code essentials](#1-claude-code-essentials)
2. [Workspace setup and maintenance](#2-workspace-setup-and-maintenance)
3. [spec-kit](#3-spec-kit)
4. [Curated skills (83)](#4-curated-skills-83)
5. [superpowers (15)](#5-superpowers-15)
6. [taste-skill (13)](#6-taste-skill-13)
7. [ponytail (6)](#7-ponytail-6)
8. [agency-agents](#8-agency-agents)
9. [Optional tools](#9-optional-tools)

---

## 1. Claude Code essentials

A short list on purpose: Claude Code changes between versions. Type `/help` in a session
for the full, current list.

**Starting a session** (run it from the project folder, or project skills will not load)

| Command | What it does |
|---|---|
| `claude` | New session in the current folder |
| `claude -c` | Continue the last conversation in this folder (`--continue`) |
| `claude -r` | Pick an older conversation to resume (`--resume`) |
| `claude --rc` | Session you can drive from the Claude mobile app (`--remote-control`) |
| `claude -p "question"` | One answer, no interactive session |

**Inside a session**

| Command | What it does |
|---|---|
| `/help` | Every available command |
| `/exit` | Quit |
| `/clear` | Start again from an empty conversation |
| `/compact` | Summarise the conversation to free up context |
| `/rewind` | Go back to an earlier point, file edits included |
| `/model` | Change model and effort level |
| `/mcp` | List, enable or disable MCP servers |
| `/memory` | Edit memory and `CLAUDE.md` files |
| `/remote-control` | Make this session reachable from the mobile app |

**Keys**: `Esc` interrupts, `Shift+Tab` cycles permission modes (including plan mode),
`!` runs a shell command, `@` points at a file.

---

## 2. Workspace setup and maintenance

The full procedure is in [`SETUP.md`](SETUP.md), written for an agent to execute.

| Task | Command |
|---|---|
| Clone the workspace | `git clone https://github.com/MoradDev/skills-unified.git my-workspace` |
| Let your agent install it | Say: *"Read SETUP.md and set up this workspace."* |
| Fill the upstream cache | `git clone --depth 1 <url> mes_depots/<name>` for each `default` row of `catalog/repos.tsv` |
| Update a cached repo | `git -C mes_depots/<name> pull` (never edit files there) |
| Link the curation into a project (Windows) | `New-Item -ItemType Junction -Path "<project>\.claude\skills\curation" -Target "<workspace>\curation"` |
| Link the curation into a project (macOS / Linux) | `ln -s "<workspace>/curation" "<project>/.claude/skills/curation"` |
| Index skills without a plugin system | `find curation/skills -name SKILL.md` |

Replace `.claude/skills/` with the path your agent reads. Windows junctions need no
administrator rights. Link the three `default` plugins (superpowers, taste-skill, ponytail)
the same way.

---

## 3. spec-kit

The backbone of the method: every new project starts here.

**Install and create a project**

| Command | What it does |
|---|---|
| `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | Install the `specify` CLI (once) |
| `specify init <project> --integration <agent> --non-interactive` | Scaffold a new project |
| `specify init … --ignore-agent-tools` | Skip the check that your agent's CLI is on `PATH` (containers, WSL, sandboxes) |
| `specify init --help` | Every option, including the list of integrations |

Always pass `--integration`: without it and without a TTY, `specify` silently picks
Copilot.

**The workflow, in order.** Each step waits until the previous one is agreed.

| Step | Skill | What it produces |
|---|---|---|
| 0 | `speckit-constitution` | The project's non-negotiables. Once, first. |
| 1 | `grill-me` / `grilling` | A clear idea, if it is still vague (see §4) |
| 2 | `speckit-specify` | The spec: what and why, never the tech stack |
| 3 | `speckit-clarify` | Answers to the spec's underspecified areas |
| 4 | `speckit-plan` | Tech stack and architecture |
| 5 | `speckit-tasks` | An ordered, actionable task list |
| 6 | `speckit-analyze` | A cross-check of spec, plan and tasks (optional) |
| 7 | `speckit-implement` | The code |
| 8 | `speckit-converge` | Remaining gaps between code and spec, as new tasks. Repeat 7–8. |

**At any time**

| Skill | What it does |
|---|---|
| `speckit-checklist` | Generate a custom checklist for the current feature |
| `speckit-taskstoissues` | Turn `tasks.md` into GitHub issues |

In Claude Code these are called as `/speckit-constitution`, `/speckit-specify`, and so on.

---

## 4. Curated skills (83)

All in `curation/skills/`. Per-language rulesets live in `curation/rules/`.

### Method (18)

| Skill | Use it to |
|---|---|
| `grill-me` | Get interrogated about a plan or idea until it holds up |
| `grilling` | Same, as a design tree worked in rounds of questions |
| `using-agent-skills` | Decide which skill applies to the task at hand |
| `context-engineering` | Set up or repair an agent's context and rules files |
| `constraint-driven-development` | Write down the quality bar and stop agents lowering it |
| `doubt-driven-development` | Put every non-trivial decision through an adversarial review |
| `source-driven-development` | Ground each decision in official documentation |
| `incremental-implementation` | Deliver a change in thin, verifiable slices |
| `api-and-interface-design` | Design stable APIs, module boundaries and contracts |
| `git-workflow-and-versioning` | Commit, branch, open PRs, cut releases |
| `documentation-and-adrs` | Record decisions (ADRs) and the reasoning behind them |
| `deprecation-and-migration` | Retire code or migrate users and schemas safely |
| `ci-cd-and-automation` | Set up build, test and deploy pipelines |
| `security-and-hardening` | Harden input handling, auth, storage and dependencies |
| `performance-optimization` | Find and fix performance problems |
| `observability-and-instrumentation` | Add logging, metrics, tracing and alerts |
| `browser-testing-with-devtools` | Test in a real browser through Chrome DevTools MCP |
| `shipping-and-launch` | Prepare a production launch and its rollback |

### Web front-end (15)

| Skill | Use it for |
|---|---|
| `react-patterns` | React 18/19 components, hooks, server/client boundaries |
| `react-performance` | React and Next.js performance |
| `react-testing` | React Testing Library, Vitest/Jest, MSW |
| `nextjs-turbopack` | Next.js 16+ and Turbopack |
| `vue-patterns` | Vue 3, Composition API, Pinia |
| `nuxt4-patterns` | Nuxt 4, hydration safety, SSR data fetching |
| `angular-developer` | Angular code and architecture |
| `vite-patterns` | Vite config, plugins, HMR, builds |
| `design-system` | Generating or auditing a design system |
| `make-interfaces-feel-better` | Polishing spacing, type, motion and interaction details |
| `accessibility` | WCAG 2.2 AA on web and native |
| `motion-foundations` | Motion tokens, springs, reduced motion (required by the two below) |
| `motion-patterns` | Animating buttons, modals, toasts, page transitions |
| `motion-advanced` | Drag and drop, gestures, text and SVG animation |
| `ui-demo` | Recording demo videos of a web app with Playwright |

### Web back-end (16)

| Skill | Use it for |
|---|---|
| `backend-patterns` | Node.js, Express and Next.js API routes |
| `nestjs-patterns` | NestJS modules, providers, guards |
| `fastapi-patterns` | FastAPI, Pydantic v2, async handlers |
| `django-patterns` | Django, DRF, ORM |
| `django-security` | Django auth, CSRF, XSS, deployment settings |
| `laravel-patterns` | Laravel, Eloquent, queues |
| `laravel-security` | Laravel auth, Eloquent safety, API security |
| `springboot-patterns` | Spring Boot REST, services, data access |
| `springboot-security` | Spring Security authn/authz and hardening |
| `java-coding-standards` | Java in Spring Boot or Quarkus services |
| `rails-patterns` | Rails 7.1+ and 8.x |
| `golang-patterns` | Idiomatic Go |
| `python-patterns` | Idiomatic Python, typing, PEP 8 |
| `hexagonal-architecture` | Ports and adapters, domain boundaries |
| `contract-first` | API or event schemas shared by several consumers |
| `error-handling` | Typed errors, retries, circuit breakers (TS, Python, Go) |

### Data (5)

| Skill | Use it for |
|---|---|
| `postgres-patterns` | PostgreSQL schemas, indexes, RLS, slow queries |
| `mysql-patterns` | MySQL and MariaDB |
| `redis-patterns` | Caching, locks, rate limiting, pub/sub |
| `prisma-patterns` | Prisma schemas, queries and its known traps |
| `database-migrations` | Schema and data migrations, zero-downtime rollouts |

### Mobile (15)

| Skill | Use it for |
|---|---|
| `react-native-patterns` | React Native and Expo apps |
| `swiftui-patterns` | SwiftUI views, `@Observable`, navigation |
| `swift-concurrency-6-2` | Swift 6.2 concurrency |
| `swift-actor-persistence` | Thread-safe persistence with actors |
| `swift-protocol-di-testing` | Testable Swift with protocol-based injection |
| `liquid-glass-design` | iOS 26 Liquid Glass UI |
| `foundation-models-on-device` | Apple on-device LLM (iOS 26+) |
| `ios-icon-gen` | iOS app icons from SF Symbols or Iconify |
| `android-clean-architecture` | Android and KMP module structure |
| `kotlin-patterns` | Idiomatic Kotlin |
| `kotlin-coroutines-flows` | Coroutines and Flow on Android and KMP |
| `kotlin-testing` | Kotest, MockK, coverage |
| `compose-multiplatform-patterns` | Jetpack Compose and Compose Multiplatform UI |
| `dart-flutter-patterns` | Dart and Flutter apps |
| `flutter-dart-code-review` | Reviewing Flutter and Dart code |

### Desktop and systems (7)

| Skill | Use it for |
|---|---|
| `dotnet-patterns` | C# and .NET |
| `rust-patterns` | Idiomatic Rust |
| `rust-testing` | Rust tests |
| `cpp-coding-standards` | Modern C++ (Core Guidelines) |
| `cpp-testing` | GoogleTest, CTest, sanitizers |
| `windows-desktop-e2e` | E2E tests for native Windows apps |
| `bun-runtime` | Bun as runtime, bundler and test runner |

### Testing and delivery (7)

| Skill | Use it for |
|---|---|
| `e2e-testing` | Playwright E2E tests and flaky CI runs |
| `python-testing` | pytest |
| `golang-testing` | Go tests, benchmarks, fuzzing |
| `csharp-testing` | xUnit and .NET tests |
| `docker-patterns` | Dockerfiles and Compose |
| `kubernetes-patterns` | Kubernetes manifests and debugging |
| `deployment-patterns` | CI/CD, containers, health checks, rollbacks |

---

## 5. superpowers (15)

Working methods. In Claude Code: `/superpowers:<skill>`.

| Skill | Use it when |
|---|---|
| `using-superpowers` | Starting a session: how to find and use skills |
| `brainstorming` | Before any creative work, to explore intent and design |
| `writing-plans` | You have requirements for a multi-step task |
| `executing-plans` | Carrying out a plan yourself, in this session |
| `subagent-driven-development` | Carrying out a plan with independent tasks via subagents |
| `dispatching-parallel-agents` | Two or more independent tasks can run in parallel |
| `test-driven-development` | Writing any feature or bug fix, tests first |
| `systematic-debugging` | Facing any bug, test failure or unexpected behaviour |
| `verification-before-completion` | About to claim something is done, fixed or passing |
| `requesting-code-review` | Finishing a task or before merging |
| `receiving-code-review` | Acting on review feedback |
| `using-git-worktrees` | Feature work that needs an isolated workspace |
| `finishing-a-development-branch` | Deciding how to integrate finished work |
| `writing-skills` | Creating or editing a skill |
| `diagnosing-superpowers` | Understanding why a session went wrong |

---

## 6. taste-skill (13)

Visual design. In Claude Code the command uses the **folder** name:
`/taste-skill:<folder>`.

| Folder | Skill name | Use it for |
|---|---|---|
| `taste-skill` | `design-taste-frontend` | Landing pages, portfolios, redesigns: the default |
| `taste-skill-v1` | `design-taste-frontend-v1` | The original v1, for projects relying on it |
| `redesign-skill` | `redesign-existing-projects` | Upgrading an existing site or app |
| `soft-skill` | `high-end-visual-design` | Agency-grade polish: fonts, spacing, shadows |
| `minimalist-skill` | `minimalist-ui` | Clean editorial interfaces |
| `brutalist-skill` | `industrial-brutalist-ui` | Raw Swiss and terminal-style interfaces |
| `gpt-tasteskill` | `gpt-taste` | Editorial layouts with GSAP motion |
| `stitch-skill` | `stitch-design-taste` | `DESIGN.md` files for Google Stitch |
| `image-to-code-skill` | `image-to-code` | Generate a design image, then build it |
| `imagegen-frontend-web` | `imagegen-frontend-web` | Website design references as images |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | Mobile screen concepts as images |
| `brandkit` | `brandkit` | Brand guidelines boards and logo systems |
| `output-skill` | `full-output-enforcement` | Forcing complete output, no placeholders |

---

## 7. ponytail (6)

Pushes the agent towards the simplest solution that works. Active from session start.

| Command | What it does |
|---|---|
| `/ponytail` | Full mode, the default: YAGNI, stdlib, native, then minimal code |
| `/ponytail lite` | Builds what is asked, names the lazier alternative in one line |
| `/ponytail ultra` | Deletion before addition; challenges requirements first |
| `/ponytail off`, or say *"stop ponytail"* | Turn it off for the session |
| `/ponytail-review` | Over-engineering review of the current diff |
| `/ponytail-audit` | The same, across the whole repository |
| `/ponytail-debt` | Collect every `ponytail:` shortcut comment into a ledger |
| `/ponytail-gain` | Scoreboard of measured impact |
| `/ponytail-help` | Reference card |

Claude Code may show the skills namespaced (`/ponytail:ponytail-review`). Codex uses
`@ponytail`, `@ponytail-review` and `@ponytail-help`.

**Default mode**: set `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off`, or
`{ "defaultMode": "lite" }` in `~/.config/ponytail/config.json`
(Windows: `%APPDATA%\ponytail\config.json`).

---

## 8. agency-agents

Specialist personas: engineering, design, marketing, security, testing, product, game
development, GIS and more (about 300, in `mes_depots/agency-agents/<division>/`).

| Task | Command |
|---|---|
| Add them to a Claude Code project | Copy the `.md` files into `<project>/.claude/agents/` (copy, do not link) |
| Install them for another tool | `./scripts/install.sh --tool <tool>` from `mes_depots/agency-agents/` |
| Use one | Ask for the specialist by name: *"Use the Backend Architect agent to…"* |

---

## 9. Optional tools

Offered by `SETUP.md`, never installed unprompted.

| Tool | Command | When |
|---|---|---|
| graphify | `uv tool install graphifyy`, then `graphify install` | Once a project passes ~80 files |
| graphify | `/graphify .` | Build the codebase graph, then read `graph.html` / `GRAPH_REPORT.md` |
| Skillspector | `uv tool install git+https://github.com/NVIDIA/skillspector.git` | Before trusting a skill from an unknown source |
| Skillspector | `skillspector scan <skill-folder> --no-llm` | Scan it. Only findings in `.py`, `.sh`, `.js`, `.ts`, `.ps1` files matter. |

---

*Plugin lists reflect the upstream repositories on 2026-09-25: superpowers `5bf4e78`,
taste-skill `c184364`, ponytail `e3ba2aa`, agency-agents `053ddbb`. They may have moved
since; the curated skills in §4 only change when this repository does.*
