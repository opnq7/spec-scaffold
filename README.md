# spec-scaffold

[![ci](https://github.com/opnq7/spec-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/opnq7/spec-scaffold/actions/workflows/ci.yml)

Turn a one-line idea into a ready-to-fill spec folder, in the three-file shape that
[Kiro](https://kiro.dev) uses for spec-driven development:

```
specs/<slug>/
├── requirements.md   what and why
├── design.md         how
└── tasks.md          ordered checklist
```

The point is to skip the blank-page phase. You describe the idea, the tool writes
the skeleton with the right headings, and you replace the placeholders.

## Why

Spec-driven tools work best when the spec has a fixed structure — every section
present, acceptance criteria written as testable statements, tasks broken into
phases. That structure is exactly the part that is tedious to type from scratch,
and easy to get subtly wrong. `spec-scaffold` makes it one command, and `--check`
catches the case where someone deleted half the template.

## Install

```bash
git clone https://github.com/opnq7/spec-scaffold.git
cd spec-scaffold
python -m pip install -e .
```

Requires Python 3.9+. No runtime dependencies.

## Usage

```bash
spec-scaffold "dark mode toggle for a web app"
```

```
created  specs/dark-mode-toggle-for-a-web-app/requirements.md
created  specs/dark-mode-toggle-for-a-web-app/design.md
created  specs/dark-mode-toggle-for-a-web-app/tasks.md

Next: open specs/dark-mode-toggle-for-a-web-app/requirements.md and replace the placeholders.
```

Options:

| Flag | Meaning |
| --- | --- |
| `-o, --out DIR` | parent folder (default `specs`) |
| `-n, --name NAME` | override the folder name instead of slugifying the idea |
| `-f, --force` | overwrite files that already exist |
| `--check DIR` | lint an existing spec folder instead of creating one |
| `--version` | print the version |

Re-running is safe: existing files are skipped, so you can regenerate a single
deleted file without losing the ones you have already edited.

### Linting an existing spec

```bash
spec-scaffold --check specs/dark-mode-toggle-for-a-web-app
```

```
OK  specs/dark-mode-toggle-for-a-web-app looks like a complete spec
```

Exit code is `0` when the spec is complete and `1` when sections are missing, so
it drops straight into CI:

```bash
spec-scaffold --check specs/my-feature || echo "spec is incomplete"
```

## What gets generated

`requirements.md` — overview, user stories, acceptance criteria written as
WHEN / THE SYSTEM SHALL pairs, out-of-scope and open questions.

`design.md` — approach, an ASCII architecture sketch, data model table, error
handling, testing plan.

`tasks.md` — three phases of `- [ ]` checkboxes. Tick a box only when the tests
for it exist and pass.

A generated example is committed under [`examples/`](examples/).

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

15 tests, no network access needed. CI runs them on Python 3.9, 3.12 and 3.13.

## Project layout

```
spec_scaffold/
├── cli.py         argparse wiring, slugify, scaffold()
├── templates.py   the three markdown templates
└── lint.py        section / checkbox checks
tests/test_cli.py
```

## Roadmap

- [ ] `--template` flag for alternative spec shapes (API, data pipeline, CLI tool)
- [ ] `spec-scaffold --check` also warns on empty sections, not just missing ones
- [ ] Optional `--git` to create the folder with an initial commit

## License

MIT — see [LICENSE](LICENSE).
