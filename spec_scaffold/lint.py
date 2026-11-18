"""Structural lint for a spec folder.

The linter is deliberately shallow: it checks that the three files exist and that
each one still carries its top-level sections. It is meant to catch "I deleted
half the template" mistakes, not to judge the quality of the writing.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

#: Required ``## `` sections per file.
REQUIRED_SECTIONS = {
    "requirements.md": ("Overview", "User Stories", "Acceptance Criteria"),
    "design.md": ("Overview", "Architecture", "Testing"),
    "tasks.md": ("Phase 1",),
}


def headings(text: str) -> list[str]:
    """Return the titles of all level-2 headings, in document order."""
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            if title:
                found.append(title)
    return found


def has_open_task(text: str) -> bool:
    """True when the file contains at least one ``- [ ]`` checkbox."""
    return any(line.strip().startswith("- [ ]") for line in text.splitlines())


def lint_spec(folder: Path) -> list[str]:
    """Return a list of human-readable problems. Empty list means the spec is OK."""
    folder = Path(folder)
    if not folder.is_dir():
        return [f"{folder} is not a directory"]

    problems: list[str] = []
    for name, required in REQUIRED_SECTIONS.items():
        path = folder / name
        if not path.is_file():
            problems.append(f"missing {name}")
            continue

        text = path.read_text(encoding="utf-8")
        present = headings(text)
        for section in required:
            if not any(h.startswith(section) for h in present):
                problems.append(f"{name}: missing section '## {section}'")

        if name == "tasks.md" and not has_open_task(text):
            problems.append("tasks.md: no '- [ ]' checkboxes left to do")

    return problems


def as_report(folder: Path) -> dict[str, object]:
    """Machine-readable form of :func:`lint_spec`, used by ``--json``."""
    problems = lint_spec(folder)
    return {"folder": str(folder), "ok": not problems, "problems": problems}


def format_problems(folder: Path, problems: Iterable[str]) -> str:
    """Render linter output for humans."""
    items = list(problems)
    if not items:
        return f"OK  {folder} looks like a complete spec"
    lines = [f"FAIL  {folder} has {len(items)} problem(s):"]
    lines.extend(f"  - {p}" for p in items)
    return "\n".join(lines)
