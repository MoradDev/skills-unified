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
├── curation/          84 skills, rules/ and references/ — the curated payload
├── QUICKSTART.md      the short path, if you are setting this up for a human who is new
├── catalog/repos.tsv  the upstream repositories: role, activation, pinned commit
├── templates/         STATE.md template, copied into each new project
├── AGENTS.md          the operating procedure (read this next)
├── CLAUDE.md          Claude Code entry point, defers to AGENTS.md
└── SETUP.md           this file
```

Nothing in `curation/` needs installing. It is plain Markdown and works as-is.

---

## Step 2 — Populate the upstream cache

Create `mes_depots/` at the workspace root and clone into it. `mes_depots/` is
**deliberately not versioned** — it is a disposable cache, fully rebuildable.

Read `catalog/repos.tsv`. It is tab-separated, with six columns:

| Column | Meaning |
|---|---|
| `name` | The folder name to clone into, under `mes_depots/` |
| `url` | The upstream repository |
| `role` | What it is: `skills`, `agents`, `source`, `cli`, `mcp`, `tool`, `index`, `rules`, `marketplace`, `app-tool` |
| `activation` | `default`, `tooling`, `curated`, `on-demand`, `threshold`, `manual`, `opt-in`, `reference`, `linux-only`, `stock` |
| `commit` | The exact commit that was inspected. **Clone this, not the branch tip.** |
| `scanned` | The date that commit was inspected, `YYYY-MM-DD` |

**Clone at minimum** every row whose `activation` is `default`. Those three — `superpowers`,
`taste-skill`, `ponytail` — are what the working method depends on, and all three are skills
plugins. Rows marked `tooling` are **not** cloned — they install as
command-line tools in step 5. Ask the human before cloning the rest — the full set is about
1.7 GB, and `Anthropic-Cybersecurity-Skills` alone is 817 skills nobody needs unless the
project is a security engagement.

**Clone the pinned commit, not the branch tip.** The `commit` column holds the state that was
actually inspected; a branch tip moves and may carry code nobody here has looked at. Since
`git clone --depth 1` cannot target a SHA, fetch it explicitly:

```bash
mkdir -p mes_depots && cd mes_depots
# for each selected row — <name>, <url> and <sha> from repos.tsv:
git init <name> && cd <name>
git remote add origin <url>
git fetch --depth 1 origin <sha>
git checkout FETCH_HEAD
cd ..
```

This leaves the clone on a detached HEAD at exactly `<sha>`, with no history: these are
consumed as content, not as repositories to contribute to. Confirm it with
`git -C <name> rev-parse HEAD` and compare against the TSV.

If a `git fetch` of a specific SHA is refused, the server has
`uploadpack.allowReachableSHA1InWant` disabled. Fall back to `git clone <url> <name> &&
git -C <name> checkout <sha>` — a full clone, then the same pinned state — and say so.

If the human explicitly wants the current branch tip instead, that is their call: clone with
`git clone --depth 1 <url> <name>`, and **tell them plainly that what they got is not what
was scanned.** Do not make that the default.

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
| **Claude Code** | Link `curation/` into `<project>/.claude/skills/curation`. It carries `.claude-plugin/plugin.json`, so it auto-loads as `curation@skills-dir` — no marketplace, no install command. The human must accept the workspace-trust prompt on first launch. Link the three `default` rows from `mes_depots/` the same way — each carries its own `.claude-plugin/plugin.json`. **Do not link `agency-agents` here**: it holds agent personas, not skills, and has no `plugin.json`. See step 4b. |
| **Codex / any AGENTS.md-aware agent** | Copy or symlink `AGENTS.md` to the project root. It already tells you to consult `curation/skills/`. |
| **Cursor** | Point a rule file at `curation/skills/`, or symlink the folder into `.cursor/rules/`. |
| **Gemini CLI, opencode, Aider, Continue, others** | No plugin system needed. Add `AGENTS.md` to the project and load `curation/skills/<name>/SKILL.md` on demand, as described in AGENTS.md § "For agents without a plugin system". |

If you are none of the above: the skills are ordinary Markdown with YAML frontmatter
(`name`, `description`). Read `AGENTS.md`, index the `description` fields, and open a
`SKILL.md` when its description matches the task at hand. That is the entire mechanism.

---

## Step 4b — Agent personas, only if the human asks

`agency-agents` is **not** cloned or installed by default, and its `activation` is
`on-demand` for one measurable reason: its 297 personas carry about **15,800 tokens of
`description` frontmatter**, and a harness that lists its agents loads every one of those
descriptions into **every session**, before the human has typed anything. A project uses
three or four. Paying 15,800 tokens per session for the other 293 is a bad trade, and it
contradicts this repository's own argument that every addition is context you spend.

So: offer them, by division, and only install what the project will actually use.

```bash
git init agency-agents && cd agency-agents
git remote add origin https://github.com/msitarzewski/agency-agents
git fetch --depth 1 origin <sha from repos.tsv>
git checkout FETCH_HEAD
```

They are **copied**, never linked — a harness reads its agents directory directly, and a
junction to a repository full of READMEs and scripts is not that directory. Copy only the
divisions that match the project, and only files whose name starts with a **lowercase**
letter: everything else (`README.md`, `CONTRIBUTING.md`, `LICENSE`, `SECURITY.md`,
`CODE_OF_CONDUCT.md`, `QUICKSTART.md`, `EXECUTIVE-BRIEF.md`…) is documentation, not a
persona, and would be loaded as a broken agent.

The divisions are `academic`, `design`, `engineering`, `finance`, `game-development`, `gis`,
`healthcare`, `integrations`, `marketing`, `paid-media`, `product`, `project-management`,
`research`, `sales`, `security`, `spatial-computing`, `specialized`, `strategy`, `support`,
`testing`. For a web application, `engineering` + `design` + `testing` is a reasonable
default; it is 84 personas instead of 297.

```powershell
# Windows — one division
New-Item -ItemType Directory -Force "<project>\.claude\agents" | Out-Null
Get-ChildItem "mes_depots\agency-agents\engineering" -Filter *.md |
  Where-Object { $_.Name -cmatch '^[a-z]' } |
  Copy-Item -Destination "<project>\.claude\agents"
```

```bash
# macOS / Linux — one division
mkdir -p "<project>/.claude/agents"
find "mes_depots/agency-agents/engineering" -maxdepth 1 -name '[a-z]*.md' \
  -exec cp {} "<project>/.claude/agents/" \;
```

Some divisions have sub-folders (`game-development/unity`, `strategy/playbooks`, …). Add
`-Recurse` / drop `-maxdepth 1` when the human wants those too, keeping the lowercase filter
and excluding `examples`, `scripts` and `.github`.

**Tell the human the count you copied and roughly what it costs them per session** — about
55 tokens per persona. That is the number that lets them decide, and it is the number nobody
was given before.

## Step 5 — Install spec-kit

**Not optional.** Spec-driven development is the backbone of the method described in
`AGENTS.md`: every new project starts with it.

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@838f1184d1b2ed254a99e8b818dbc23aa80a7f1f
```

The `@<sha>` suffix pins the install to the commit recorded in `catalog/repos.tsv`, for the
same reason step 2 pins the clones. Drop it only if the human asks for the latest, and tell
them that is unscanned code.

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

Both are pinned, for the same reason as step 2.

```bash
# Skill security scanner — run it manually on untrusted skills, never as a gate
uv tool install git+https://github.com/NVIDIA/Skillspector.git@2226747e4ca97198bb82faf5085b8a75f2e1dc02

# Codebase graph — only once a project exceeds ~80 files
uv tool install graphifyy==0.9.73
```

---

## Step 5c — Offer Context7

Context7 serves current documentation for external libraries over MCP. Offer it; install
only if the human agrees, and **at user scope**, never per project — the credential does
not belong in a project repository.

For Claude Code:

```bash
claude mcp add --transport http --scope user context7 https://mcp.context7.com/mcp   --header "Authorization: Bearer <YOUR_CONTEXT7_API_KEY>"
```

Other harnesses: add an HTTP MCP server pointing at `https://mcp.context7.com/mcp` with an
`Authorization: Bearer` header, using whatever configuration file your harness uses. A free
key comes from [context7.com](https://context7.com).

The rules for using it are in `AGENTS.md` § "External library documentation" — read them
before the first call, particularly the obligation to check the documentation matches the
version the project actually uses.

## Step 5c bis — Offer Laya MCP (optional)

Only if the human wants it. [Laya](https://github.com/NandhaKishorM/laya) is an open-source
(Apache-2.0) non-autoregressive decision model: you hand it a block of state and typed
questions, it returns typed answers with probabilities and confidence in a single forward
pass. No text generation, so nothing to parse and nothing to hallucinate. Its own MCP server
ships in the same repository, so **everything runs locally and costs nothing per call** —
there is no API key and no account.

That buys one specific thing for the method: **the mechanical checks an agent normally skips
because running a frontier model on every page, claim or candidate is too slow.** The rules
for using it are in `AGENTS.md` § "Cheap mechanical checks".

**Prerequisites**, from the project's own README:

- **Python 3.10 or newer** (its `huggingface_hub` 1.x, `transformers` 5.x and `torch` 2.14
  dependencies set that floor).
- **CPU or GPU.** `LAYA_DEVICE` selects one; CPU works, a GPU is faster.
- **Room for the weights.** The first prediction downloads a checkpoint from Hugging Face
  into the `huggingface_hub` cache (`HF_HUB_CACHE` moves it). The English and
  typed-decisions checkpoints are about 421M parameters, the multilingual one about 322M.
  Nothing is downloaded until the first call.

Install, with the version pinned so what you get is what was checked:

```bash
pip install "laya[mcp]==0.3.23"
```

`laya[mcp]` is an optional extra — the core package carries no `mcp` dependency. It
installs the `laya-mcp-server` entry point (`python -m laya.mcp.server` is the same thing).

Register it in Claude Code. `-e` sets an environment variable, then `--` separates Claude's
own options from the server command (verified against `claude mcp add --help`):

```bash
claude mcp add --scope user laya -e LAYA_DEVICE=cpu -- laya-mcp-server
```

Use `--scope user` so every project inherits it; there is no credential to keep out of a
repository, but there is no reason to repeat the registration either. Set
`LAYA_DEVICE=cuda` (or `mps`) instead of `cpu` where the machine has a GPU.

For any other MCP client, the equivalent stdio configuration from the project's README is:

```json
{
  "mcpServers": {
    "laya": {
      "command": "laya-mcp-server",
      "env": { "LAYA_DEVICE": "cpu" }
    }
  }
}
```

The server exposes `laya_predict`, `laya_predict_batch`, `laya_route`, `laya_route_batch`,
`laya_decide`, `laya_shortlist`, `laya_preset` and `laya_status`. Other environment
variables it reads: `LAYA_PRELOAD` (build checkpoints at startup rather than lazily,
default `1`), `LAYA_MODELS` (comma list to preload, default `english,multilingual`),
`LAYA_THREADS` (cap torch intra-op threads on CPU) and `LAYA_AUTO_TASK`.

Two things worth saying to the human before they install it: the first call is slow because
it downloads weights, and **a low-confidence verdict means ask a human, never proceed
anyway.**

## Step 5d — Create the project's `STATE.md`

`specify init` does not create one. Copy [`templates/STATE.md`](templates/STATE.md) to the
project root and fill in the header — project name, today's date, your harness, and the
current step (`constitution`, since nothing has started yet).

```bash
cp templates/STATE.md <project>/STATE.md
```

This is what lets a different agent pick the project up later. Explain to the human, in one
sentence, that this file is the shared memory between harnesses and that every agent is
expected to read it on arrival and update it before leaving.

## Step 6 — Report

Tell the human, in plain language:

- which repositories were cloned, and which were skipped
- whether linking used junctions, symlinks or copies
- which optional tools were installed
- **what they should do next**: open a fresh agent session in the project folder, accept
  the trust prompt if their harness has one, and start with the constitution step
  described in `AGENTS.md`

Then stop. Do not start building the project yourself.
