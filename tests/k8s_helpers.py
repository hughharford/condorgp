"""Shared helpers for the cluster-security BDD tests (features 017-022, topics A-G).

Every check reads files from REPO_ROOT. To prove a test goes RED on the old code and
GREEN on the fix, point CGP_REPO_ROOT at another checkout, e.g. a worktree of master:

    git worktree add ../condorgp_master master
    CGP_REPO_ROOT=../condorgp_master python -m pytest -m A_secrets   # expect failures

The tests/ directory itself is never scanned: it holds example "bad" values on purpose.
"""
import os
import re
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(os.environ.get("CGP_REPO_ROOT") or Path(__file__).resolve().parents[1]).resolve()

_SKIP_TOP_DIRS = {"tests", ".git", ".venv", "node_modules"}
_SKIP_NAMES = {"poetry.lock", "package-lock.json"}
_MAX_BYTES = 1_000_000


def run(cmd, cwd=None, env=None, input=None, timeout=120):
    """subprocess.run with text output; never raises on a non-zero exit."""
    return subprocess.run(
        cmd, cwd=cwd, env=env, input=input, capture_output=True, text=True, timeout=timeout
    )


def repo_files():
    """Files that are part of the repo: tracked + untracked-but-not-git-ignored.

    Untracked files are included on purpose, so a leak is caught BEFORE `git add`.
    """
    res = run(["git", "-C", str(REPO_ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard"])
    if res.returncode == 0:
        rels = [p for p in res.stdout.split("\0") if p]
    else:  # not a git checkout: walk the tree
        rels = [
            str(p.relative_to(REPO_ROOT))
            for p in REPO_ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts
        ]
    files = []
    for rel in sorted(set(rels)):
        path = Path(rel)
        if path.parts[0] in _SKIP_TOP_DIRS or path.name in _SKIP_NAMES:
            continue
        full = REPO_ROOT / path
        if full.is_file() and full.stat().st_size <= _MAX_BYTES:
            files.append(path)
    return files


def read_text(rel):
    """Text of a repo file, or None if it is missing or binary."""
    try:
        return (REPO_ROOT / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def find_lines(files, regex, suffixes=None):
    """[(rel, line_no, line)] for every line matching regex in the given files."""
    pattern = re.compile(regex)
    hits = []
    for rel in files:
        if suffixes and Path(rel).suffix not in suffixes and Path(rel).name not in suffixes:
            continue
        text = read_text(rel)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                hits.append((str(rel), number, line.strip()))
    return hits


def logical_lines(files, suffixes=None):
    """[(rel, first_line_no, command)] with backslash-continued lines joined into one command."""
    found = []
    for rel in files:
        if suffixes and Path(rel).suffix not in suffixes and Path(rel).name not in suffixes:
            continue
        text = read_text(rel)
        if text is None:
            continue
        buffer, start = "", 0
        for number, raw in enumerate(text.splitlines(), 1):
            if not buffer:
                start = number
            if raw.rstrip().endswith("\\"):
                buffer += raw.rstrip()[:-1] + " "
                continue
            found.append((str(rel), start, (buffer + raw).strip()))
            buffer = ""
        if buffer:
            found.append((str(rel), start, buffer.strip()))
    return found


def yaml_docs(rel):
    """All mapping documents in a YAML file ([] if unreadable or not valid YAML)."""
    text = read_text(rel)
    if text is None:
        return []
    try:
        return [d for d in yaml.safe_load_all(text) if isinstance(d, dict)]
    except yaml.YAMLError:
        return []


def is_git_ignored(rel):
    """True if the .gitignore rules would ignore this path (even if it is tracked)."""
    return run(["git", "-C", str(REPO_ROOT), "check-ignore", "-q", "--no-index", rel]).returncode == 0


def fmt_hits(hits):
    return "\n".join(f"  {rel}:{n}: {line}" for rel, n, line in hits)
