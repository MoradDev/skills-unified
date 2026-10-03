#!/usr/bin/env python3
"""Check this repository against itself.

Every number this repository announces was wrong at least once, because nothing recounted
them. This script does. Standard library only, no dependencies, no network: it must be
runnable by anyone who just cloned, and cheap enough to sit in CI.

    python scripts/check.py          # report everything, exit 1 on any failure
    python scripts/check.py -v       # also print what passed

What it refuses to let drift:
  * the skill count, the per-family counts, and the per-category counts in both cheatsheets
  * every skill's frontmatter: a name, a description, a name that matches its directory
  * the ruleset count
  * catalog/repos.tsv: column arity, 40-hex commits, ISO dates, no duplicate names, and
    agreement between its `default` rows and what the docs claim
  * provenance: every skill on disk attributed exactly once in ATTRIBUTION.md, either to an
    upstream or as original, and both READMEs crediting the same upstream counts and
    naming every original skill
  * every relative Markdown link in the repository
  * the numbers the English and French documents state, which must agree with each other
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXEC_EXT = {".py", ".sh", ".js", ".ts", ".ps1", ".mjs", ".cjs", ".tsx", ".jsx", ".bash"}
SKIP_DIRS = {".git", "mes_depots", "node_modules", "__pycache__", ".venv"}

# Relative links that are known not to resolve and are deliberately left alone. Upstream
# text in curation/rules/README.md is written as though it lived inside a language folder,
# and `xxx.md` is a placeholder in a template sentence. Repairing it would mean editing
# redistributed content for no behavioural gain.
KNOWN_BROKEN_LINKS = {
    ("curation/rules/README.md", "../common/xxx.md"),
    ("curation/rules/README.md", "../common/coding-style.md"),
}

failures: list[str] = []
passes: list[str] = []


def ok(msg: str) -> None:
    passes.append(msg)


def fail(msg: str) -> None:
    failures.append(msg)


def check(label: str, got, want) -> None:
    if got == want:
        ok(f"{label}: {got}")
    else:
        fail(f"{label}: got {got!r}, expected {want!r}")


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def walk_md():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                full = os.path.join(dirpath, name)
                yield os.path.relpath(full, ROOT).replace(os.sep, "/"), full


# --------------------------------------------------------------------------- skills


def upstream_cache() -> str | None:
    """Where `mes_depots/` sits, if it is here at all.

    `SETUP.md` puts it at the workspace root, which is this repository's own root. Older
    layouts kept the repository inside a wider workspace folder, so the cache was a sibling.
    Try both, and return None when there is none — a fresh clone has no cache, and that is
    not a failure, only fewer checks.
    """
    for candidate in (os.path.join(ROOT, "mes_depots"), os.path.join(ROOT, "..", "mes_depots")):
        resolved = os.path.normpath(candidate)
        if os.path.isdir(resolved):
            return resolved
    return None


def frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return None
    body, fields = match.group(1), {}
    for key in ("name", "description"):
        # A frontmatter key may contain hyphens (`disable-model-invocation`), so the lookahead
        # that terminates a value has to accept them — otherwise the value sitting just before
        # such a key parses as absent, and the skill looks like it has no description.
        found = re.search(rf"^{key}:\s*((?:.|\n[ \t]+)+?)(?=\n[A-Za-z_][A-Za-z0-9_-]*:|\Z)", body, re.M)
        if found:
            fields[key] = " ".join(found.group(1).split())
    return fields


def check_skills() -> set[str]:
    skills_dir = os.path.join(ROOT, "curation", "skills")
    dirs = sorted(d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)))
    names: dict[str, str] = {}
    for d in dirs:
        path = os.path.join(skills_dir, d, "SKILL.md")
        if not os.path.isfile(path):
            fail(f"curation/skills/{d}: no SKILL.md")
            continue
        fields = frontmatter(open(path, encoding="utf-8").read())
        if fields is None:
            fail(f"curation/skills/{d}/SKILL.md: no YAML frontmatter")
            continue
        if not fields.get("name"):
            fail(f"curation/skills/{d}/SKILL.md: frontmatter has no name")
        elif fields["name"] != d:
            fail(f"curation/skills/{d}/SKILL.md: name is {fields['name']!r}, not the directory name")
        if not fields.get("description"):
            fail(f"curation/skills/{d}/SKILL.md: frontmatter has no description — it will never auto-invoke")
        if fields.get("name"):
            if fields["name"] in names:
                fail(f"duplicate skill name {fields['name']!r}: {names[fields['name']]} and {d}")
            names[fields["name"]] = d
    ok(f"{len(dirs)} skills, each with a SKILL.md, a unique name matching its directory, and a description")
    return set(dirs)


def check_rules() -> int:
    rules_dir = os.path.join(ROOT, "curation", "rules")
    dirs = [d for d in os.listdir(rules_dir) if os.path.isdir(os.path.join(rules_dir, d))]
    ok(f"{len(dirs)} ruleset directories")
    return len(dirs)


# --------------------------------------------------------------------------- catalogue


def check_catalog() -> list[dict[str, str]]:
    lines = [l for l in read("catalog/repos.tsv").split("\n") if l.strip()]
    header = lines[0].lstrip("# ").split("\t")
    check("repos.tsv columns", header, ["name", "url", "role", "activation", "commit", "scanned"])
    rows, seen = [], set()
    for number, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        if len(cells) != len(header):
            fail(f"repos.tsv line {number}: {len(cells)} columns, header has {len(header)}")
            continue
        row = dict(zip(header, cells))
        if row["name"] in seen:
            fail(f"repos.tsv line {number}: duplicate name {row['name']!r}")
        seen.add(row["name"])
        if not re.fullmatch(r"[0-9a-f]{40}", row["commit"]):
            fail(f"repos.tsv line {number} ({row['name']}): commit is not a 40-hex SHA")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["scanned"]):
            fail(f"repos.tsv line {number} ({row['name']}): scanned is not YYYY-MM-DD")
        if not row["url"].startswith("https://"):
            fail(f"repos.tsv line {number} ({row['name']}): url is not https")
        rows.append(row)
    ok(f"{len(rows)} catalogue rows, all six columns, 40-hex commits, ISO dates, no duplicate names")
    return rows


# --------------------------------------------------------------------------- links


def check_links() -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    total = broken = 0
    for rel, full in walk_md():
        directory = os.path.dirname(full)
        for match in pattern.finditer(open(full, encoding="utf-8", errors="replace").read()):
            target = match.group(1).split("#")[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            total += 1
            base = ROOT if target.startswith("/") else directory
            resolved = os.path.normpath(os.path.join(base, target.lstrip("/")))
            if not os.path.exists(resolved):
                if (rel, target) in KNOWN_BROKEN_LINKS:
                    continue
                broken += 1
                fail(f"{rel}: relative link does not resolve: {target}")
    if not broken:
        ok(f"{total} relative Markdown links, all resolving ({len(KNOWN_BROKEN_LINKS)} known exceptions allowed)")


def check_anchors() -> None:
    for rel, full in walk_md():
        text = open(full, encoding="utf-8", errors="replace").read()
        headings = set()
        for heading in re.findall(r"^#+\s+(.+)$", text, re.M):
            # GitHub strips punctuation, then maps each remaining space to one hyphen — so
            # "AI & LLM Security" becomes "ai--llm-security", with two hyphens where the
            # ampersand was. Collapsing runs of spaces here would reject working anchors.
            slug = re.sub(r"[^\w\s-]", "", heading.lower(), flags=re.U)
            headings.add(slug.strip().replace(" ", "-"))
        for anchor in re.findall(r"\]\(#([^)]+)\)", text):
            if anchor not in headings:
                fail(f"{rel}: in-page anchor #{anchor} matches no heading")
    ok("every in-page anchor matches a heading")


# ------------------------------------------------------------------ core persona set


def check_core_personas() -> None:
    """SETUP.md step 4b names a core set copied into every project, in three places: a plain
    list, a PowerShell array and a bash loop. Three copies of the same 14 names drift, and a
    typo in one of them is a persona that silently never arrives. So: all three must agree,
    the count stated in prose must match, and — when the upstream cache happens to be present —
    every named file must exist."""
    text = read("SETUP.md")
    start = text.index("## Step 4b")
    section = text[start:text.index("## Step 5 — Install spec-kit")]

    stated = re.search(r"a core of (\d+)", section)
    pattern = re.compile(r"(academic|design|engineering|finance|game-development|gis|healthcare"
                         r"|integrations|marketing|paid-media|product|project-management|research"
                         r"|sales|security|spatial-computing|specialized|strategy|support|testing)"
                         r"[/\\]([a-z][a-z0-9-]+)")

    groups = {}
    for block in re.findall(r"```(?:powershell|bash)?\n(.*?)```", section, re.S):
        if "$core" in block:
            groups["powershell"] = block
        elif "for p in" in block:
            groups["bash"] = block
        elif "engineering/" in block and "Get-ChildItem" not in block and "find " not in block:
            groups.setdefault("list", block)  # the plain two-column listing, first fence
    if set(groups) != {"list", "powershell", "bash"}:
        fail(f"SETUP.md step 4b: expected a plain list, a PowerShell array and a bash loop, found {sorted(groups)}")
        return

    sets = {}
    for label, block in groups.items():
        sets[label] = {f"{d}/{n}" for d, n in pattern.findall(block)}
    reference = sets["list"]
    for label in ("powershell", "bash"):
        if sets[label] != reference:
            only_here = sorted(sets[label] - reference)
            only_there = sorted(reference - sets[label])
            fail(f"SETUP.md step 4b: the {label} block disagrees with the list "
                 f"(only in {label}: {only_here}; missing from it: {only_there})")

    if stated and int(stated.group(1)) != len(reference):
        fail(f"SETUP.md step 4b: prose says a core of {stated.group(1)}, the list names {len(reference)}")

    # The upstream clone is optional (a fresh checkout has none), but when it is there the
    # names must resolve — a typo here is a persona that never arrives, with no error.
    root = upstream_cache()
    cache = os.path.join(root, "agency-agents") if root else None
    if cache and os.path.isdir(cache):
        missing = [n for n in sorted(reference) if not os.path.isfile(os.path.join(cache, *n.split("/")) + ".md")]
        if missing:
            fail(f"SETUP.md step 4b: these personas do not exist upstream: {missing}")
        else:
            ok(f"the {len(reference)} core personas all exist in the upstream cache")
    ok(f"SETUP.md step 4b: {len(reference)} core personas, identical across the list, PowerShell and bash")


# ------------------------------------------------------------------- declared numbers


def declared(path: str, pattern: str) -> list[int]:
    return [int(m) for m in re.findall(pattern, read(path))]


def check_cheatsheet(path: str, heading: str, skills: set[str]) -> None:
    text = read(path)
    start = text.index(heading)
    end = text.index("## 5. superpowers")
    section = text[start:end]
    listed, total = [], 0
    for block in re.split(r"\n### ", section)[1:]:
        title = block.split("\n")[0]
        count = re.search(r"\((\d+)\)", title)
        rows = re.findall(r"^\| `([a-z0-9-]+)` \|", block, re.M)
        if not count:
            fail(f"{path}: category {title!r} declares no count")
            continue
        if len(rows) != int(count.group(1)):
            fail(f"{path}: category {title!r} declares {count.group(1)} but lists {len(rows)}")
        listed += rows
        total += len(rows)
    missing = skills - set(listed)
    extra = set(listed) - skills
    if missing:
        fail(f"{path}: skills on disk but not in the tables: {sorted(missing)}")
    if extra:
        fail(f"{path}: skills in the tables but not on disk: {sorted(extra)}")
    declared_total = re.search(r"\((\d+)\)", section.split("\n")[0])
    if declared_total and int(declared_total.group(1)) != len(skills):
        fail(f"{path}: section heading declares {declared_total.group(1)} skills, {len(skills)} on disk")
    if total != len(skills):
        fail(f"{path}: categories sum to {total}, {len(skills)} skills on disk")
    ok(f"{path}: {total} skills listed, every category count correct, matches the disk exactly")


def check_provenance(skills: set[str]) -> None:
    """Every skill comes from somewhere, once — and the READMEs must say the same thing.

    The READMEs once credited 65 + 16 + 2 = 83 skills and claimed none was written here,
    while the disk held 84 and ATTRIBUTION.md named the original one. Each number was right;
    only the sum was not, so no count check saw it.
    """
    text = read("ATTRIBUTION.md")
    section = re.search(r"^## Provenance.*?$(.*?)(?=^## )", text, re.M | re.S)
    if not section:
        fail("ATTRIBUTION.md: the provenance section is gone — update the check or the file")
        return
    upstream: dict[str, int] = {}
    attributed: list[str] = []
    for count, repo, body in re.findall(
            r"^### (\d+) skills from \[`([\w.-]+/[\w.-]+)`\]\([^)]*\)$(.*?)(?=^### |\Z)",
            section.group(1), re.M | re.S):
        names = re.findall(r"`([a-z0-9][a-z0-9-]*)`", body)
        check(f"ATTRIBUTION.md: {repo} lists as many skills as its heading says", len(names), int(count))
        upstream[repo] = int(count)
        attributed += names
    originals = re.findall(r"`curation/skills/([a-z0-9-]+)` is original", text)
    attributed += originals
    duplicates = sorted({n for n in attributed if attributed.count(n) > 1})
    if duplicates:
        fail(f"ATTRIBUTION.md: attributed more than once: {duplicates}")
    missing, unknown = sorted(skills - set(attributed)), sorted(set(attributed) - skills)
    if missing or unknown:
        fail(f"ATTRIBUTION.md: not attributed {missing}, attributed but not on disk {unknown}")
    if not (duplicates or missing or unknown):
        ok(f"ATTRIBUTION.md: {len(skills)} skills, each attributed once "
           f"({sum(upstream.values())} upstream, {len(originals)} original)")

    for path, heading in (("README.md", "## Licence and credit"), ("README.fr.md", "## Licence et crédit")):
        credit = read(path).partition(heading)[2]
        if not credit:
            fail(f"{path}: the credit section is gone — update the check or the prose")
            continue
        stated = {repo: int(n) for repo, n in
                  re.findall(r"\[`([\w.-]+/[\w.-]+)`\]\([^)]*\) \((\d+)\)", credit)}
        check(f"{path}: upstream credit counts match ATTRIBUTION.md", stated, upstream)
        unnamed = [n for n in originals if f"`{n}`" not in credit]
        if unnamed:
            fail(f"{path}: the credit section does not name the original skills {unnamed}")
        else:
            ok(f"{path}: the credit section names every original skill")


def main(verbose: bool) -> int:
    skills = check_skills()
    check_provenance(skills)
    n_skills, n_rules = len(skills), check_rules()
    rows = check_catalog()

    # The two families must add up to the whole.
    method = re.search(r"\*Method\* \((\d+)\)", read("README.md"))
    app = re.search(r"\*Application building\* \((\d+)\)", read("README.md"))
    if method and app:
        check("README.md families sum to the skill count", int(method.group(1)) + int(app.group(1)), n_skills)
    else:
        fail("README.md: could not find the two family counts")

    # Numbers stated in prose, against the filesystem.
    for path, pattern, want, label in [
        ("README.md", r"\*\*(\d+) curated skills\*\*", n_skills, "README.md curated-skill count"),
        ("README.fr.md", r"\*\*(\d+) skills sélectionnées\*\*", n_skills, "README.fr.md curated-skill count"),
        ("AGENTS.md", r"holds (\d+) skills in two groups", n_skills, "AGENTS.md skill count"),
        ("AGENTS.md", r"Do not load all (\d+) at once", n_skills, "AGENTS.md context warning"),
        ("SETUP.md", r"curation/\s+(\d+) skills", n_skills, "SETUP.md layout skill count"),
        ("README.md", r"rulesets\*\* for (\d+) languages", n_rules, "README.md ruleset count"),
        ("README.fr.md", r"par langage\*\* pour (\d+) langages", n_rules, "README.fr.md ruleset count"),
        ("AGENTS.md", r"rulesets for (\d+) languages", n_rules, "AGENTS.md ruleset count"),
        ("README.md", r"\*\*catalogue\*\* of (\d+)", len(rows), "README.md catalogue size"),
        ("README.fr.md", r"\*\*catalogue\*\* de\s+(\d+) dépôts", len(rows), "README.fr.md catalogue size"),
        ("README.md", r"auditing the (\d+) catalogued", len(rows), "README.md audited-repo count"),
        ("README.fr.md", r"l'audit des (\d+) dépôts", len(rows), "README.fr.md audited-repo count"),
    ]:
        found = declared(path, pattern)
        if not found:
            fail(f"{label}: the sentence this checks for is gone from {path} — update the check or the prose")
        else:
            check(label, found[0], want)

    # Documented default rows must match the catalogue.
    defaults = sorted(r["name"] for r in rows if r["activation"] == "default")
    check("catalogue `default` rows", defaults, ["ponytail", "superpowers", "taste-skill"])
    # The headings spell the count as a word. Never index a dict by a count that malformed
    # input can change — a checker that raises instead of reporting is useless in CI.
    WORDS = {1: ("one", "un"), 2: ("two", "deux"), 3: ("three", "trois"),
             4: ("four", "quatre"), 5: ("five", "cinq"), 6: ("six", "six")}
    headings_agree = True
    for path, pattern in [("README.md", r"## The (\w+) repositories enabled by default"),
                          ("README.fr.md", r"## Les (\w+) dépôts activés par défaut")]:
        word = re.search(pattern, read(path))
        expect = WORDS.get(len(defaults))
        if not word:
            fail(f"{path}: the default-repositories heading is gone — update the check or the prose")
            headings_agree = False
        elif expect is None:
            fail(f"{path}: {len(defaults)} default rows in the catalogue, which this check cannot spell "
                 f"(heading says {word.group(1)!r}) — extend WORDS in scripts/check.py")
            headings_agree = False
        elif word.group(1) not in expect:
            fail(f"{path}: heading says {word.group(1)!r} but the catalogue has {len(defaults)} default rows")
            headings_agree = False
    if headings_agree:
        ok("both READMEs name as many default repositories as the catalogue has")

    # Every `default` row must actually be a skills plugin, since SETUP.md links it as one.
    for name in defaults:
        root = upstream_cache()
        plugin = os.path.join(root, name, ".claude-plugin", "plugin.json") if root else None
        if plugin and os.path.exists(plugin):
            ok(f"{name}: carries .claude-plugin/plugin.json, so linking it as a skills plugin works")
        # Absent cache is not a failure: a fresh clone has no mes_depots/.

    check_core_personas()

    check_cheatsheet("CHEATSHEET.md", "## 4. Curated skills", skills)
    check_cheatsheet("CHEATSHEET.fr.md", "## 4. Skills de la curation", skills)

    # The plugin counts in both cheatsheets must agree with each other.
    for pattern in (r"## 5\. superpowers \((\d+)\)", r"## 6\. taste-skill \((\d+)\)", r"## 7\. ponytail \((\d+)\)"):
        en, fr = declared("CHEATSHEET.md", pattern), declared("CHEATSHEET.fr.md", pattern)
        if en != fr:
            fail(f"cheatsheets disagree on {pattern}: EN {en}, FR {fr}")
    ok("the two cheatsheets agree on every plugin count")

    check_links()
    check_anchors()

    # Executable files shipped under curation/ are worth knowing about by name.
    shipped = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "curation")):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() in EXEC_EXT:
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")
                shipped.append(rel)
    check("executable files shipped under curation/", sorted(shipped),
          ["curation/skills/ios-icon-gen/scripts/iconify_gen.sh"])

    if verbose:
        for line in passes:
            print(f"  ok   {line}")
    for line in failures:
        print(f"  FAIL {line}", file=sys.stderr)
    print(f"\n{len(passes)} checks passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(verbose="-v" in sys.argv or "--verbose" in sys.argv))
