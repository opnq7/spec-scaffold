# Contributing

Small project, small rules.

## Set up

```bash
git clone https://github.com/opnq7/spec-scaffold.git
cd spec-scaffold
python -m pip install -e ".[dev]"
```

## Before you open a PR

```bash
ruff check .
pytest --cov
```

Both must be clean. CI runs the same two commands on Python 3.9, 3.12 and 3.13,
so anything that works locally but breaks 3.9 will be caught there — check
`from __future__ import annotations` if you add new syntax.

## What is worth changing

- **Template wording.** If a section heading does not match how you actually
  write specs, open an issue with the heading you would use instead. The
  templates are the product.
- **The linter.** It is intentionally shallow. A rule earns its place only if it
  catches a real mistake without producing false positives on good writing.
- **Tests.** A behaviour change needs a test that fails before it.

## What is out of scope

- Dependencies. The package has none and should keep none; `argparse`,
  `pathlib`, `string.Template` and `json` are enough.
- Network calls of any kind.
- Generating real prose. The tool writes skeletons — filling them in is the
  user's job, and that is the point.

## Commits

Plain imperative subject lines, one concern per commit. The changelog is written
from commit subjects, so make them readable.
