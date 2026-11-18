# Design — pomodoro timer

> How the system meets `requirements.md`. One `index.html` = one change; the spec
> folder exists so the next change is a diff against these decisions, not a guess.

## Overview

One HTML file: markup, inline CSS and inline JS, no dependencies and no build
step. The interesting decision is **how time is measured**. The shipped version
counts ticks (`setInterval(tick, 1000)` decrementing a counter), which is the
obvious approach and the wrong one: browsers throttle background timers to about
one tick per minute, so a 25-minute block can run for half an hour and the number
on screen is a lie. This design derives the remaining time from a stored
`deadline` timestamp instead, which makes backgrounding, sleep and a slow frame
irrelevant.

## Architecture

```
+--------------------+        +----------------------+        +---------------+
|  mode buttons      | -----> |  state machine       | -----> |  renderer     |
|  play / reset/skip |        |  mode, deadline,     |        |  digits, ring, |
|  duration inputs   |        |  remaining, count    |        |  dots, labels |
+--------------------+        +----------+-----------+        +---------------+
                                         |
                              +----------+-----------+
                              |  storage (localStorage) |
                              |  durations, count, date |
                              +-------------------------+
```

- **One state object**, mutated only by named transitions (`start`, `pause`,
  `reset`, `skip`, `finish`, `setMode`, `setDurations`).
- **The renderer is pure**: it reads the state and writes the DOM. No transition
  reads the DOM to decide what to do next.
- **Storage is a snapshot**, written after every transition, read once at boot.

## Timing

| Concern | Decision |
| --- | --- |
| Source of truth | `deadline = Date.now() + remaining * 1000` while running |
| Display tick | `setInterval(200)` recomputes `remaining = ceil((deadline - now)/1000)` |
| Drift | impossible: each tick recomputes, it does not decrement |
| Background | nothing special — the next tick after focus returns shows the truth |
| Auto-finish | `remaining <= 0` → `finish()`, once, guarded by a flag |

A 200 ms tick is used only so the displayed second changes close to the real one;
it costs nothing and it keeps the digits from visibly lagging.

## State machine

| From | Event | To | Side effects |
| --- | --- | --- | --- |
| `idle` | `start` | `running` | set `deadline`, persist |
| `running` | `pause` | `paused` | freeze `remaining`, clear interval |
| `paused` | `start` | `running` | recompute `deadline` |
| `running` | `reset` | `idle` | `remaining = duration(mode)` |
| `running` | `finish` (remaining ≤ 0) | next block | alarm, `count++` only if `mode == work`, toast |
| any | `skip` | next block | **no** `count++` |
| any | `setMode` | `idle` | stops the clock, loads that duration |

`finish` is a single function that decides the next mode: `work` → `short`
(→ `long` when `count == 4`), `short`/`long` → `work`, and it resets `count` to 0
**only** when the long break has been completed.

## Data Model

| Key | Type | Notes |
| --- | --- | --- |
| `pomodoro.durations` | `{work, short, long}` (seconds) | default 25 / 5 / 15 |
| `pomodoro.count` | integer 0–4 | tomatoes in the current cycle |
| `pomodoro.date` | `YYYY-MM-DD` | lets a daily reset be added without a migration |

In memory: `mode`, `remaining`, `deadline | null`, `running`, `count`.

## Error Handling

- **`localStorage` unavailable** (private mode, `file://` in some browsers,
  quota): catch on read and write, fall back to in-memory defaults, never block
  the timer.
- **WebAudio blocked until a user gesture**: create the `AudioContext` lazily on
  the first play/skip click, and resume it if it is `suspended`.
- **`Notification` denied or missing**: the alarm and the toast are the primary
  signal; notification is a bonus and its permission is requested once, on first
  start, never on load.
- **`new Notification({icon})` needs a URL**, not an emoji; omit the icon.

## Testing

- **Timing**: inject the clock (`now()`), then assert `remaining` after simulated
  jumps — 0 s, 1 s, 25 min, and a 10-minute gap standing in for a backgrounded tab.
- **Transitions**: table-driven over the state machine above; the skip case asserts
  `count` is unchanged.
- **Persistence**: fake storage, reload, assert durations and count survive.
- **Manual**: alarm audible, space/R work with focus on the page, reload restores.

No test framework is in the shipped file; the timing tests are the ones worth
adding first because they are the regression that a human cannot see by clicking.

## Rejected alternatives

- **Counting ticks** (what shipped): simpler to read, silently wrong in background
  tabs. Rejected by AC-6.
- **`requestAnimationFrame` for the clock**: pauses when not rendering, which is
  the same bug wearing a different hat.
- **A framework and a build step**: 14 KB of HTML does not need a toolchain; the
  cost is a `node_modules` for anyone who wants to change a colour.
