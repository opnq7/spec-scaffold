"""Tests for the ANSI helper."""

import io

import pytest

from spec_scaffold.console import paint, supports_color


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)


def test_non_tty_stream_disables_colour(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr("sys.stdout", stream)
    assert supports_color() is False
    assert paint("created", "green") == "created"


def test_force_color_wins(monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert paint("created", "green") == "\x1b[32mcreated\x1b[0m"


def test_no_color_wins_over_tty(monkeypatch):
    class FakeTty(io.StringIO):
        def isatty(self):
            return True

    stream = FakeTty()
    monkeypatch.setattr("sys.stdout", stream)
    assert supports_color() is True

    monkeypatch.setenv("NO_COLOR", "1")
    assert supports_color() is False
    assert paint("created", "green") == "created"


def test_explicit_enabled_beats_detection():
    assert paint("x", "red", enabled=True) == "\x1b[31mx\x1b[0m"
    assert paint("x", "red", enabled=False) == "x"


def test_unknown_colour_is_a_no_op():
    assert paint("x", "chartreuse", enabled=True) == "x"
