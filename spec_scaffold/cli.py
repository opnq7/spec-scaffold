"""Command line interface for spec-scaffold."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .lint import format_problems, lint_spec
from .templates import FILES

#: Anything that is not a lowercase letter or digit becomes a single dash.
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Turn an idea into a filesystem-friendly slug.

    >>> slugify("Hello, World! 2026")
    'hello-world-2026'
    >>> slugify("   ???   ")
    'untitled-spec'
    """
    slug = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return slug or "untitled-spec"


def scaffold(
    idea: str,
    out: Path = Path("specs"),
    name: Optional[str] = None,
    force: bool = False,
    today: Optional[dt.date] = None,
) -> Path:
    """Write a spec folder for *idea* and return its path.

    Existing files are left alone unless *force* is true, so re-running the
    command is safe.
    """
    slug = slugify(name or idea)
    target = Path(out) / slug
    target.mkdir(parents=True, exist_ok=True)

    values = {
        "IDEA": idea.strip(),
        "SLUG": slug,
        "DATE": (today or dt.date.today()).isoformat(),
    }

    for filename, template in FILES.items():
        path = target / filename
        if path.exists() and not force:
            print(f"skip     {path} (exists, use --force to overwrite)")
            continue
        path.write_text(template.safe_substitute(values), encoding="utf-8")
        print(f"created  {path}")

    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spec-scaffold",
        description="Turn a one-line idea into a Kiro-style spec folder "
        "(requirements.md, design.md, tasks.md).",
    )
    parser.add_argument("idea", nargs="*", help="the idea, in a few words")
    parser.add_argument(
        "-o",
        "--out",
        default="specs",
        help="parent folder for the spec (default: specs)",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="override the folder name instead of slugifying the idea",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite files that already exist",
    )
    parser.add_argument(
        "--check",
        metavar="SPEC_DIR",
        help="lint an existing spec folder instead of creating one",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.check:
        folder = Path(args.check)
        problems = lint_spec(folder)
        print(format_problems(folder, problems))
        return 1 if problems else 0

    idea = " ".join(args.idea).strip()
    if not idea:
        parser.error("give me an idea, or use --check SPEC_DIR")

    try:
        target = scaffold(
            idea,
            out=Path(args.out),
            name=args.name,
            force=args.force,
        )
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"\nNext: open {target / 'requirements.md'} and replace the placeholders.")
    return 0
