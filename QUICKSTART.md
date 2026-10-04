# Quickstart — from nothing to a running app

*[Version française](QUICKSTART.fr.md)* · *Why any of this exists: [README.md](README.md)*

This page assumes you have never used this workspace. It is the shortest honest path.
Everything else in this repository is reference material you can ignore today.

---

## What you need first

| | Why | Check it |
|---|---|---|
| **git** | Required. Nothing works without it. | `git --version` |
| **An agent with a CLI** | Claude Code, Codex, Cursor, Gemini CLI, opencode… | `claude --version` |
| **[uv](https://astral.sh/uv)** | Installs `specify`, which scaffolds every project | `uv --version` |
| **Node.js** (optional) | Only for the `ponytail` plugin's hooks. Skip it and say so. | `node --version` |

Missing `uv`? `curl -LsSf https://astral.sh/uv/install.sh \| sh` on macOS/Linux,
`irm https://astral.sh/uv/install.ps1 \| iex` in PowerShell.

---

## Three commands

```bash
git clone https://github.com/MoradDev/skills-unified.git my-workspace
cd my-workspace
```

Pick a folder name that does not already exist. Windows and macOS filesystems are
case-insensitive, so a generic `workspace` will collide with an existing `Workspace` and the
clone fails.

Then open your agent **in that folder** and give it one instruction:

> Read SETUP.md and set up this workspace, then create a project called `books`.

It will check your OS, clone what the method needs at the commits this repository pinned,
install `specify`, scaffold `books/`, wire the skills into it and create its `STATE.md`. It
stops there on purpose — it does not start building.

Then open a **new** session, this time inside `my-workspace/books/`, and accept the
workspace-trust prompt if your agent shows one. Project skills only load from the folder
the session opened in.

---

## A worked example: "a page to track books I've read"

Type these in order, in the project session. Each one produces a file the next one reads,
which is the whole point: the agent cannot quietly forget what you agreed.

| You type | What you get | Your job |
|---|---|---|
| `/speckit-constitution` | `.specify/memory/constitution.md` — your non-negotiables | Answer its questions. "It must work offline" and "no accounts" belong here. |
| `/speckit-specify` *a page where I log books I finish, with title, author, date and a 1–5 rating* | `spec.md` — **what** and **why**, no technology | Read it. It is short on purpose. Fix anything that is not what you meant. |
| `/speckit-clarify` | Answers filled into `spec.md` | It asks about what you left vague. Answer plainly. |
| `/speckit-plan` | `plan.md` — the stack and the architecture | **This is where you say no.** If it proposes Postgres and Docker for a page you use alone, say so. |
| `/speckit-tasks` | `tasks.md` — an ordered list | Skim it. If a task is unclear to you, it is unclear to the agent. |
| `/speckit-implement` | Actual code | Let it run. Report failures with their output. |
| `/speckit-converge` | New tasks for the gaps between code and spec | Repeat implement → converge until it finds nothing. |

**Vague idea instead of a clear one?** Say *"grill me on this idea"* before
`/speckit-specify`. You get interrogated until the idea holds up. That is faster than
specifying something you have not thought through.

**Before you finish any session**, write what happened into `books/STATE.md`. That file is
the only thing another agent — or you in three weeks — can read to pick the work up. Even
"tried X, dead end, don't retry" is worth a line.

---

## What is working for you, silently

You do not invoke these. They trigger on what you are doing.

| | What it does to your session |
|---|---|
| **84 curated skills** | A React question pulls in the React skill, a Postgres question the Postgres one. You never name them. |
| **superpowers** | Pushes tests before code, systematic debugging, verification before anything is called done. |
| **ponytail** | Argues for the shortest thing that works. Say *"stop ponytail"* to turn it off for the session. |
| **taste-skill** | Makes generated interfaces look designed rather than templated. |
| **humanizer** | Strips the tells of machine-written prose from docs, READMEs and interface copy, without changing what they say. |
| **14 specialist agents** | Architecture, backend, frontend, review, database, devops, prototyping, UI, UX, test automation, accessibility, appsec, technical writing. Unlike skills, these you *do* call: *"use the backend architect for this"*. |

They sometimes overlap and compete. [`AGENTS.md`](AGENTS.md) § "When two skills compete"
lists the known cases and what to do about each.

---

## When it goes wrong

| Symptom | Cause |
|---|---|
| No skill ever fires | Session opened in the workspace root, not in the project folder. Reopen it in `my-workspace/books/`. |
| "Agent Detection Error: claude not found" | `specify` cannot see your agent's CLI. Add `--ignore-agent-tools`. |
| The agent writes a three-page spec for a tiny thing | Say so. `/speckit-specify` takes correction, and `ponytail` exists for exactly this argument. |
| It asks to interrogate you when you already know what you want | Two skills competing on the same trigger. Tell it to skip to `/speckit-specify`. |
| `ponytail` fails to load | Node.js missing. Harmless — everything else works. |

---

## Where to go next

- [`CHEATSHEET.md`](CHEATSHEET.md) — every command and every skill, one page
- [`AGENTS.md`](AGENTS.md) — the working method in full, and the rules the agent follows
- [`README.md`](README.md) — why this selection and not another
