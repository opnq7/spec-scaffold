# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A hand-written, filled-in spec for a real project:
  `examples/pomodoro-timer/`, with `docs/case-study.md` reading it against the
  shipped 577-line file it describes.

## [0.2.0] - 2026-11-18

### Added

- `--json` for `--check`, so the linter can feed a CI step or an editor.
- `--dry-run`, which prints the planned writes without touching the disk.
- `-q, --quiet`, for scripts that only care about the exit code.
- Colour for the four status words, disabled automatically for pipes, redirects
  and `NO_COLOR`, enabled by `FORCE_COLOR`.
- `py.typed`, so type checkers pick up the inline annotations.
- A `lint` CI job (ruff) alongside the test matrix.
- `CONTRIBUTING.md`, `CHANGELOG.md`, `.editorconfig`, and a terminal demo in the
  README.

### Changed

- Status labels are padded to a fixed column, so paths line up.
- Type annotations use builtin generics (`list[str]`, `str | None`).
- Coverage is measured in CI (`--cov`, 96% statement + branch).

## [0.1.0] - 2026-11-18

### Added

- `spec-scaffold <idea>` writes `requirements.md`, `design.md` and `tasks.md`
  under `specs/<slug>/`.
- `--check` lints an existing spec folder and exits non-zero when incomplete.
- `--force`, `--out` and `--name` flags.
- 15 tests, GitHub Actions matrix on Python 3.9, 3.12 and 3.13.

[Unreleased]: https://github.com/opnq7/spec-scaffold/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/opnq7/spec-scaffold/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/opnq7/spec-scaffold/releases/tag/v0.1.0
