"""Shared helpers for the cluster-security BDD tests (017-022, topics A-G).

Every check reads files from REPO_ROOT. To prove a test goes RED on the old
code and GREEN on the fix, point CGP_REPO_ROOT at another checkout, e.g. a
worktree of master:

    git worktree add ../condorgp_master master
    CGP_REPO_ROOT=../condorgp_master python -m pytest -m A_secrets  # red

The tests/ directory is never scanned: it holds example "bad" values.
"""

import os
import re
import subprocess
from collections.abc import Collection, Iterable, Sequence
from pathlib import Path
from typing import Any

import yaml

_DEFAULT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(os.environ.get("CGP_REPO_ROOT") or _DEFAULT_ROOT).resolve()

_SKIP_TOP_DIRS = {"tests", ".git", ".venv", "node_modules"}
_SKIP_NAMES = {"poetry.lock", "package-lock.json"}
_MAX_BYTES = 1_000_000

# (relative path, 1-based line number, line text)
Hit = tuple[str, int, str]


def run(
    cmd: Sequence[str],
    cwd: str | os.PathLike[str] | None = None,
    env: dict[str, str] | None = None,
    input: str | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    """subprocess.run with text output; never raises on a non-zero exit."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        input=input,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def repo_files() -> list[Path]:
    """Return repo files: tracked plus untracked-but-not-ignored.

    Untracked files are included so a leak is caught BEFORE `git add`.
    """
    res = run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ]
    )
    if res.returncode == 0:
        rels = [p for p in res.stdout.split("\0") if p]
    else:  # not a git checkout: walk the tree
        rels = [
            str(p.relative_to(REPO_ROOT))
            for p in REPO_ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts
        ]
    files: list[Path] = []
    for rel in sorted(set(rels)):
        path = Path(rel)
        if path.parts[0] in _SKIP_TOP_DIRS or path.name in _SKIP_NAMES:
            continue
        full = REPO_ROOT / path
        if full.is_file() and full.stat().st_size <= _MAX_BYTES:
            files.append(path)
    return files


def read_text(rel: str | os.PathLike[str]) -> str | None:
    """Text of a repo file, or None if it is missing or binary."""
    try:
        return (REPO_ROOT / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def require_text(rel: str | os.PathLike[str]) -> str:
    """Return a repo file's text, or fail the test if it is absent."""
    text = read_text(rel)
    assert text is not None, f"{rel} does not exist (or is not a text file)"
    return text


def find_lines(
    files: Iterable[str | Path],
    regex: str,
    suffixes: Collection[str] | None = None,
) -> list[Hit]:
    """Return (rel, line_no, line) for lines matching regex."""
    pattern = re.compile(regex)
    hits: list[Hit] = []
    for rel in files:
        if (
            suffixes
            and Path(rel).suffix not in suffixes
            and Path(rel).name not in suffixes
        ):
            continue
        text = read_text(rel)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                hits.append((str(rel), number, line.strip()))
    return hits


def logical_lines(
    files: Iterable[str | Path], suffixes: Collection[str] | None = None
) -> list[Hit]:
    """Return (rel, line_no, command), joining backslash continuations."""
    found: list[Hit] = []
    for rel in files:
        if (
            suffixes
            and Path(rel).suffix not in suffixes
            and Path(rel).name not in suffixes
        ):
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


def yaml_docs(rel: str | Path) -> list[dict[str, Any]]:
    """Return the mapping documents in a YAML file ([] if unreadable)."""
    text = read_text(rel)
    if text is None:
        return []
    try:
        return [d for d in yaml.safe_load_all(text) if isinstance(d, dict)]
    except yaml.YAMLError:
        return []


def is_git_ignored(rel: str) -> bool:
    """Return True if .gitignore would ignore this path."""
    result = run(
        ["git", "-C", str(REPO_ROOT), "check-ignore", "-q", "--no-index", rel]
    )
    return result.returncode == 0


def fmt_hits(hits: Iterable[Hit]) -> str:
    """Format hits as indented `path:line: text` lines."""
    return "\n".join(f"  {rel}:{n}: {line}" for rel, n, line in hits)
