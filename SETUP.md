# SETUP — instructions for the coding agent

> **You are an AI coding agent.** The human cloned this repository and asked you to set up
> their workspace. Execute the steps below in order. Report what you did, and what you
> skipped and why. Do not skip a step silently.

This file is the single source of truth for installation. It is written to work with any
agent (Claude Code, Codex, Cursor, Gemini CLI, opencode, Aider, Continue, …) on Windows,
macOS or Linux.

---

## Step 0 — Establish context

Determine and state explicitly, before doing anything else:

| Question | Why it matters |
|---|---|
| What is the operating system? | Decides the linking command in step 3 |
| Which agent/harness are you? | Decides whether step 4 (plugin wiring) applies |
| Is `git` available? | Required for step 2 |
| Is `uv` available? (`uv --version`) | Required for step 5; install from https://astral.sh/uv |

If `git` is missing, stop and tell the human. Everything else can degrade gracefully.

---

## Step 1 — Confirm the layout

After cloning, the repository root **is** the workspace root. It already contains:

```
<workspace>/
├── curation/          83 skills, rules/ and references/ — the curated payload
├── catalog/repos.tsv  the 21 upstream repositories, with their role
├── AGENTS.md          the operating procedure (read this next)
├── CLAUDE.md          Claude Code entry point, defers to AGENTS.md
└── SETUP.md           this file
```

Nothing in `curation/` needs installing. It is plain Markdown and works as-is.

---

## Step 2 — Populate the upstream cache

Create `mes_depots/` at the workspace root and clone into it. `mes_depots/` is
**deliberately not versioned** — it is a disposable cache, fully rebuildable.

Read `catalog/repos.tsv` (tab-separated: `name`, `url`, `role`, `activation`).

**Clone at minimum** every row whose `activation` is `default`. Those four are what the
working method depends on. Rows marked `tooling` are **not** cloned — they install as
command-line tools in step 5. Ask the human before cloning the rest — the full set is about
1.7 GB, and `Anthropic-Cybersecurity-Skills` alone is 817 skills nobody needs unless the
project is a security engagement.

```bash
mkdir -p mes_depots && cd mes_depots
# for each selected row:
git clone --depth 1 <url> <name>
```

Use `--depth 1` unless the human wants the full history: these are consumed as content,
not as repositories to contribute to.

> **Rule that matters: never modify anything inside `mes_depots/`.** It must stay pristine
> so `git pull` can never conflict. Anything worth keeping is copied into `curation/`
> and committed there. This is what makes the cache disposable.

---

## Step 3 — Make `curation/` reachable from a project

A project lives in its own folder at the workspace root: `<workspace>/<project>/`.

Link rather than copy, so that an update to `curation/` propagates everywhere at once.

| OS | Command |
|---|---|
| Windows | `New-Item -ItemType Junction -Path "<project>\.agent\skills\curation" -Target "<workspace>\curation"` |
| macOS / Linux | `ln -s "<workspace>/curation" "<project>/.agent/skills/curation"` |

Windows directory junctions need **no** administrator rights, unlike symbolic links.
If linking fails for any reason, fall back to copying and say so — the human needs to
know that updates will no longer propagate.

Replace `.agent/skills/` with whatever path your harness actually reads (see step 4).

---

## Step 4 — Wire it into the harness

**This step is harness-specific. Apply the row that matches you, skip the rest.**

| Harness | What to do |
|---|---|
| **Claude Code** | Link `curation/` into `<project>/.claude/skills/curation`. It carries `.claude-plugin/plugin.json`, so it auto-loads as `curation@skills-dir` — no marketplace, no install command. The human must accept the workspace-trust prompt on first launch. Also link the `default` plugins from `mes_depots/` the same way. |
| **Codex / any AGENTS.md-aware agent** | Copy or symlink `AGENTS.md` to the project root. It already tells you to consult `curation/skills/`. |
| **Cursor** | Point a rule file at `curation/skills/`, or symlink the folder into `.cursor/rules/`. |
| **Gemini CLI, opencode, Aider, Continue, others** | No plugin system needed. Add `AGENTS.md` to the project and load `curation/skills/<name>/SKILL.md` on demand, as described in AGENTS.md § "For agents without a plugin system". |

If you are none of the above: the skills are ordinary Markdown with YAML frontmatter
(`name`, `description`). Read `AGENTS.md`, index the `description` fields, and open a
`SKILL.md` when its description matches the task at hand. That is the entire mechanism.

---

## Step 5 — Install spec-kit

**Not optional.** Spec-driven development is the backbone of the method described in
`AGENTS.md`: every new project starts with it.

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Then, for each new project, from the workspace root:

```bash
specify init <project-name> --integration <your-harness> --non-interactive
```

Two things that will bite you, both confirmed by testing on a clean Ubuntu 26.04:

- **`specify` checks that your agent's CLI is on `PATH`** and aborts with an
  "Agent Detection Error" if it is not — which is common when the agent runs inside a
  container, a WSL distribution or a sandbox while its CLI lives elsewhere. Add
  `--ignore-agent-tools` to skip that check. The project scaffolds correctly without it.
- **Without `--non-interactive` and without a TTY, it silently defaults to Copilot.**
  Always pass your integration explicitly.

Run `specify init --help` for the full list. It creates `.specify/` and installs the
workflow as skills named with hyphens — `speckit-constitution`, `speckit-specify`,
`speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-analyze`,
`speckit-implement`, `speckit-converge`, `speckit-checklist`, `speckit-taskstoissues`.

It does **not** generate a `CLAUDE.md` or an `AGENTS.md` for the new project. Create one
yourself, pointing at the workspace's `AGENTS.md`.

If `uv` or `specify` cannot be installed in this environment, say so explicitly and tell
the human the method will have to be followed by hand, keeping each step's artefact as a
file. Do not silently skip this step.

## Step 5b — Optional tooling

Offer these; do not install them unprompted.

```bash
# Skill security scanner — run it manually on untrusted skills, never as a gate
uv tool install git+https://github.com/NVIDIA/skillspector.git

# Codebase graph — only once a project exceeds ~80 files
uv tool install graphifyy
```

---

## Step 6 — Report

Tell the human, in plain language:

- which repositories were cloned, and which were skipped
- whether linking used junctions, symlinks or copies
- which optional tools were installed
- **what they should do next**: open a fresh agent session in the project folder, accept
  the trust prompt if their harness has one, and start with the constitution step
  described in `AGENTS.md`

Then stop. Do not start building the project yourself.
