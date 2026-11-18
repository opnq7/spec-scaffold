"""Tests for the scaffolder itself."""

from pathlib import Path

import pytest

from spec_scaffold.cli import main, scaffold, slugify
from spec_scaffold.lint import has_open_task, headings, lint_spec


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Hello, World! 2026", "hello-world-2026"),
        ("  spaced   out  ", "spaced-out"),
        ("CamelCase", "camelcase"),
        ("???", "untitled-spec"),
        ("", "untitled-spec"),
    ],
)
def test_slugify(raw, expected):
    assert slugify(raw) == expected


def test_scaffold_writes_three_files(tmp_path):
    target = scaffold("Dark mode toggle", out=tmp_path / "specs")

    assert target == tmp_path / "specs" / "dark-mode-toggle"
    assert sorted(p.name for p in target.iterdir()) == [
        "design.md",
        "requirements.md",
        "tasks.md",
    ]
    text = (target / "requirements.md").read_text(encoding="utf-8")
    assert "Dark mode toggle" in text
    assert "$IDEA" not in text


def test_scaffold_keeps_existing_files_unless_forced(tmp_path, capsys):
    target = scaffold("Dark mode toggle", out=tmp_path)
    (target / "design.md").write_text("hand written", encoding="utf-8")

    scaffold("Dark mode toggle", out=tmp_path)
    assert (target / "design.md").read_text(encoding="utf-8") == "hand written"
    assert "skip" in capsys.readouterr().out

    scaffold("Dark mode toggle", out=tmp_path, force=True)
    assert "hand written" not in (target / "design.md").read_text(encoding="utf-8")


def test_generated_spec_passes_lint(tmp_path):
    target = scaffold("Dark mode toggle", out=tmp_path)
    assert lint_spec(target) == []


def test_lint_reports_missing_section_and_file(tmp_path):
    target = scaffold("Dark mode toggle", out=tmp_path)
    text = (target / "requirements.md").read_text(encoding="utf-8")
    (target / "requirements.md").write_text(
        text.replace("## User Stories", "## Notes"), encoding="utf-8"
    )
    (target / "design.md").unlink()

    problems = lint_spec(target)
    assert "missing design.md" in problems
    assert any("User Stories" in p for p in problems)


def test_lint_rejects_non_directory(tmp_path):
    assert lint_spec(tmp_path / "nope") == [f"{tmp_path / 'nope'} is not a directory"]


def test_headings_and_checkbox_helpers():
    text = "# T\n\n## One\n- [ ] a\n##Two\n  ## Three\n"
    assert headings(text) == ["One", "Three"]
    assert has_open_task(text) is True
    assert has_open_task("## T\n- [x] done\n") is False


def test_main_creates_spec_and_exits_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["Export", "playlist", "as", "csv"]) == 0
    out = capsys.readouterr().out
    assert "created" in out
    assert (tmp_path / "specs" / "export-playlist-as-csv" / "tasks.md").is_file()


def test_main_check_returns_status_code(tmp_path, monkeypatch, capsys):
    target = scaffold("Dark mode toggle", out=tmp_path)

    monkeypatch.chdir(tmp_path)
    assert main(["--check", str(target)]) == 0
    assert "OK" in capsys.readouterr().out

    (target / "tasks.md").unlink()
    assert main(["--check", str(target)]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_main_without_idea_is_a_usage_error():
    with pytest.raises(SystemExit) as excinfo:
        main([])
    assert excinfo.value.code == 2


def test_main_name_override(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["whatever", "--name", "custom-name"]) == 0
    assert (tmp_path / "specs" / "custom-name" / "design.md").is_file()
    assert not Path(tmp_path / "specs" / "whatever").exists()
