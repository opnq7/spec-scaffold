"""spec-scaffold — turn a one-line idea into a Kiro-style spec folder.

The public surface is small on purpose: :func:`scaffold` writes the files,
:func:`slugify` names the folder, :func:`lint_spec` checks an existing one, and
:func:`main` is what the ``spec-scaffold`` console script calls.
"""

__version__ = "0.2.0"

from .cli import main, scaffold, slugify  # noqa: E402
from .lint import lint_spec  # noqa: E402

__all__ = ["__version__", "lint_spec", "main", "scaffold", "slugify"]
