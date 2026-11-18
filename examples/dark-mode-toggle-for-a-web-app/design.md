# Design — dark mode toggle for a web app

> How the system meets `requirements.md`. One `specs/dark-mode-toggle-for-a-web-app/` folder = one change.

## Overview

The chosen approach in two or three sentences, plus the one alternative that was
rejected and why.

## Architecture

```
+-------------+      +-------------+      +-------------+
|   input     | ---> |   dark-mode-toggle-for-a-web-app     | ---> |   output    |
+-------------+      +-------------+      +-------------+
```

- **Module layout** — `<package>/` holds the entry point, `<package>/core.py`
  holds the pure logic, `tests/` mirrors it.

## Data Model

| Name | Type | Notes |
| --- | --- | --- |
| `id` | string | stable slug, unique per record |

## Error Handling

- Bad input: fail fast with a message that names the offending value.
- Missing files: report the path, never the traceback.

## Testing

- Unit tests for the pure functions.
- One end-to-end test that runs the CLI against a temp directory.
