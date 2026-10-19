#!/usr/bin/env python3
"""Run Skillspector over a whole repository, in pieces it can actually finish.

Pointed at a large repository, Skillspector reports almost nothing as fully inspected: a few
files it cannot finish (a lockfile it reads as obfuscated, a dependency list past its five
seconds) degrade whole analyzers, and every file is then counted as partial. `--recursive`
only looks one level down for SKILL.md, so a repository whose skills sit deeper is barely
scanned at all. This script does not change Skillspector. It decides what to hand it:

  * one unit per skill directory (a folder holding a SKILL.md, the top-most one when they nest);
  * one unit for everything else that can run or that tells a harness what to run: scripts and
    source files, and the manifests that declare hooks, plugins, MCP servers and npm scripts;
  * lockfiles, binaries, files over Skillspector's 1 MB ceiling, and dependency, build and
    VCS directories are left out, and every file left out is listed with its reason.

Each unit is copied to a short temporary path (deep repositories overflow Windows' 260-character
limit otherwise), scanned with `--no-llm` so no file content is sent to a model, and the reports
are merged back onto the repository's own paths. One network call remains, and it is worth
having: Skillspector's dependency check sends the package names and versions it finds in
manifests to api.osv.dev (Google's vulnerability database). That is how known-vulnerable
dependencies show up. It sends no file content.

It sorts what to read; it decides nothing. The rule in README.md § "On scanning skills for
safety" stands: only findings in executable files mean anything, a human reads every
executable change before a pin moves, and this is never an automatic gate. It always exits 0
once it has scanned, whatever it found.

    python scripts/scan.py mes_depots/<name>              # summary, findings to read first
    python scripts/scan.py mes_depots/<name> --out DIR    # keep the per-unit reports in DIR
    python scripts/scan.py mes_depots/<name> --jobs 4 --timeout 900

Standard library only. Needs `skillspector` on PATH (SETUP.md step 5b).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile

# The extensions the README's reading rule calls executable, as scripts/check.py counts them,
# plus the compiled languages a tool repository ships its behaviour in. C and C++ headers are
# in: a native engine (codebase-memory-mcp, 2026-10-14) is mostly .c and .h, and without them
# its whole binary went unscanned.
EXEC_EXT = {".py", ".sh", ".js", ".ts", ".ps1", ".mjs", ".cjs", ".tsx", ".jsx", ".bash",
            ".zsh", ".psm1", ".vbs", ".cmd", ".bat",
            ".rs", ".go", ".cs", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp", ".hh", ".hxx",
            ".m", ".mm", ".java", ".kt", ".swift", ".rb", ".php", ".lua", ".zig"}
# Not executable, but they tell a harness or a package manager what to execute.
MANIFESTS = {"hooks.json", "plugin.json", "marketplace.json", ".mcp.json", "settings.json",
             "package.json", "gemini-extension.json"}
LOCKFILES = {"package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
             "bun.lockb", "bun.lock", "Cargo.lock", "poetry.lock", "uv.lock", "Pipfile.lock",
             "composer.lock", "Gemfile.lock", "go.sum"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target", ".venv", "venv",
             "__pycache__", ".next", ".turbo", "coverage"}
MAX_FILE_BYTES = 1_000_000  # Skillspector's own constants.MAX_FILE_BYTES
SEVERITY = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def is_binary(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            return b"\0" in fh.read(8192)
    except OSError:
        return True


def make_temp_dir(prefix: str) -> str:
    """A fresh temporary directory that a sandboxed child process can still write into.

    `tempfile.mkdtemp` asks for mode 0o700, and since Python 3.13 Windows honours it with an
    owner-only ACL: a Skillspector run under the Windows sandbox is then refused writes in its
    own staging and report folders. Creating the directory with 0o777 keeps the default,
    inherited ACL (on POSIX the umask still applies).
    """
    base = tempfile.gettempdir()
    for _ in range(100):
        path = os.path.join(base, prefix + os.urandom(4).hex())
        try:
            os.mkdir(path, 0o777)
            return path
        except FileExistsError:
            continue
    raise FileExistsError(f"no free temporary directory name under {base}")


def walk(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            yield os.path.relpath(full, root).replace(os.sep, "/"), full


def excluded_reason(rel: str, full: str) -> str | None:
    name = rel.rsplit("/", 1)[-1]
    if name in LOCKFILES:
        return "lockfile"
    if os.path.getsize(full) > MAX_FILE_BYTES:
        return "over 1 MB: read by hand"
    if is_binary(full):
        return "binary"
    return None


def plan(root: str) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Units (a name and the repository paths in it) and the files left out, with why."""
    files = list(walk(root))
    skill_dirs = sorted({rel.rsplit("/", 1)[0] if "/" in rel else "."
                         for rel, _ in files if rel.rsplit("/", 1)[-1] == "SKILL.md"})
    # Keep the top-most skill directory when they nest: scanning it covers the inner ones.
    top = [d for d in skill_dirs
           if not any(d != o and (o == "." or d.startswith(o + "/")) for o in skill_dirs)]
    units: dict[str, list[str]] = {}
    left_out: dict[str, str] = {}
    for rel, full in files:
        owner = next((d for d in top if d == "." or rel.startswith(d + "/")), None)
        if owner is None:
            ext = os.path.splitext(rel)[1].lower()
            if ext not in EXEC_EXT and rel.rsplit("/", 1)[-1] not in MANIFESTS:
                continue  # prose and assets outside any skill: not this scan's business
            owner = "(executables and manifests outside skills)"
        reason = excluded_reason(rel, full)
        if reason:
            left_out[rel] = reason
        else:
            units.setdefault(owner, []).append(rel)
    return units, left_out


def run_unit(root: str, unit: str, rels: list[str], out_dir: str, timeout: int) -> dict:
    stage = make_temp_dir("ss-")
    try:
        prefix = "" if unit.startswith("(") or unit == "." else unit + "/"
        for rel in rels:
            dest = os.path.join(stage, rel[len(prefix):] if prefix else rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(os.path.join(root, rel), dest)
        slug = "".join(c if c.isalnum() else "_" for c in unit).strip("_")[:80] or "root"
        report = os.path.join(out_dir, slug + ".json")
        try:
            subprocess.run(["skillspector", "scan", stage, "--no-llm", "--format", "json",
                            "--output", report], capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"unit": unit, "files": len(rels), "error": f"timed out after {timeout} s"}
        if not os.path.exists(report):
            return {"unit": unit, "files": len(rels), "error": "no report written"}
        with open(report, encoding="utf-8") as fh:
            data = json.load(fh)
        return {"unit": unit, "files": len(rels), "prefix": prefix, "report": report, "data": data}
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repo", help="repository folder to scan, e.g. mes_depots/<name>")
    ap.add_argument("--out", help="folder for the per-unit reports and summary.json")
    ap.add_argument("--jobs", type=int, default=2, help="units scanned in parallel (default 2)")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per unit (default 900)")
    args = ap.parse_args()

    if shutil.which("skillspector") is None:
        print("skillspector is not on PATH: install it as SETUP.md step 5b says.", file=sys.stderr)
        return 2
    root = os.path.abspath(args.repo)
    out_dir = os.path.abspath(args.out) if args.out else make_temp_dir("skillspector-scan-")
    os.makedirs(out_dir, exist_ok=True)

    units, left_out = plan(root)
    print(f"{os.path.basename(root)}: {sum(map(len, units.values()))} files in {len(units)} units, "
          f"{len(left_out)} left out", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(lambda u: run_unit(root, u, units[u], out_dir, args.timeout), units))

    coverage = {"fully": 0, "partial": 0, "none": 0}
    to_read, on_prose, failed = [], 0, []
    for r in results:
        if "error" in r:
            failed.append(f"{r['unit']}: {r['error']}")
            continue
        ac = r["data"].get("analysis_completeness", {})
        coverage["fully"] += ac.get("fully_inspected_files") or 0
        coverage["partial"] += ac.get("partially_inspected_files") or 0
        coverage["none"] += ac.get("entirely_uninspected_files") or 0
        for issue in r["data"].get("issues", []):
            loc = issue.get("location") or {}
            path = r["prefix"] + str(loc.get("file", "?"))
            name = path.rsplit("/", 1)[-1]
            if os.path.splitext(name)[1].lower() in EXEC_EXT or name in MANIFESTS:
                to_read.append({"severity": str(issue.get("severity", "?")).upper(), "path": path,
                                "line": loc.get("start_line"), "category": issue.get("category"),
                                "snippet": " ".join(str(issue.get("code_snippet") or "").split())[:200]})
            else:
                on_prose += 1
    to_read.sort(key=lambda f: (SEVERITY.get(f["severity"], 9), f["path"], f["line"] or 0))

    reasons: dict[str, int] = {}
    for reason in left_out.values():
        reasons[reason] = reasons.get(reason, 0) + 1
    summary = {"repo": root, "units": {u: len(v) for u, v in units.items()}, "coverage": coverage,
               "left_out": left_out, "left_out_by_reason": reasons, "failed_units": failed,
               "findings_on_prose_ignored": on_prose, "findings_to_read": to_read}
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)

    inspected = sum(coverage.values())
    pct = 100 * coverage["fully"] / inspected if inspected else 0
    print(f"coverage: {coverage['fully']} fully, {coverage['partial']} partially, "
          f"{coverage['none']} not inspected ({pct:.0f} % fully)")
    if reasons:
        print("left out: " + ", ".join(f"{n} {r}" for r, n in sorted(reasons.items())))
    for line in failed:
        print(f"unit not scanned: {line}")
    print(f"findings: {len(to_read)} in executable files or manifests to read, "
          f"{on_prose} on prose ignored (README.md § \"On scanning skills for safety\")")
    for f in to_read:
        print(f"  {f['severity']:8} {f['path']}:{f['line']}  {f['category']}")
    print(f"reports and summary.json: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
