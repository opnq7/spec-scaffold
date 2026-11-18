"""Command line interface for spec-scaffold."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from . import __version__
from .console import paint
from .lint import as_report, format_problems, lint_spec
from .templates import FILES

#: Anything that is not a lowercase letter or digit becomes a single dash.
_SLUG_RE = re.compile(r"[^a-z0-9]+")

#: Width of the status column, so file paths line up.
_LABEL = 7


def slugify(text: str) -> str:
    """Turn an idea into a filesystem-friendly slug.

    >>> slugify("Hello, World! 2026")
    'hello-world-2026'
    >>> slugify("   ???   ")
    'untitled-spec'
    """
    slug = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return slug or "untitled-spec"


def _pad(label: str, color: str) -> str:
    """Colour *label* but pad to the status column width in plain characters."""
    return paint(label, color) + " " * (_LABEL - len(label))


def scaffold(
    idea: str,
    out: Path = Path("specs"),
    name: str | None = None,
    force: bool = False,
    today: dt.date | None = None,
    dry_run: bool = False,
    quiet: bool = False,
) -> Path:
    """Write a spec folder for *idea* and return its path.

    Existing files are left alone unless *force* is true, so re-running the
    command is safe. With *dry_run* nothing touches the disk.
    """
    slug = slugify(name or idea)
    target = Path(out) / slug
    values = {
        "IDEA": idea.strip(),
        "SLUG": slug,
        "DATE": (today or dt.date.today()).isoformat(),
    }

    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    for filename, template in FILES.items():
        path = target / filename
        if path.exists() and not force:
            if not quiet:
                print(f"{_pad('skip', 'yellow')} {path} (exists, use --force to overwrite)")
            continue

        if not dry_run:
            path.write_text(template.safe_substitute(values), encoding="utf-8")
        if not quiet:
            label = "would" if dry_run else "created"
            print(f"{_pad(label, 'green')} {path}")

    if not quiet:
        if dry_run:
            print(f"\ndry run — would create {len(FILES)} file(s) under {target}")
        else:
            print(f"\nNext: open {target / 'requirements.md'} and replace the placeholders.")

    return target


def _status_report(folder: Path, ok: bool) -> str:
    """Format the human linter result, colouring just the verdict word."""
    text = format_problems(folder, [] if ok else lint_spec(folder))
    head, sep, tail = text.partition("  ")
    return f"{paint(head, 'green' if ok else 'red')}{sep}{tail}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spec-scaffold",
        description="Turn a one-line idea into a Kiro-style spec folder "
        "(requirements.md, design.md, tasks.md).",
        epilog="Exit codes: 0 ok, 1 incomplete spec or write error, 2 usage error.",
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
        "--dry-run",
        action="store_true",
        help="show what would be written, write nothing",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="only print errors",
    )
    parser.add_argument(
        "--check",
        metavar="SPEC_DIR",
        help="lint an existing spec folder instead of creating one",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="with --check: print the report as JSON",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.json and not args.check:
        parser.error("--json only makes sense together with --check")

    if args.check:
        folder = Path(args.check)
        ok = not lint_spec(folder)
        if args.json:
            print(json.dumps(as_report(folder), indent=2, ensure_ascii=False))
        elif not args.quiet:
            print(_status_report(folder, ok))
        return 0 if ok else 1

    idea = " ".join(args.idea).strip()
    if not idea:
        parser.error("give me an idea, or use --check SPEC_DIR")

    try:
        scaffold(
            idea,
            out=Path(args.out),
            name=args.name,
            force=args.force,
            dry_run=args.dry_run,
            quiet=args.quiet,
        )
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
