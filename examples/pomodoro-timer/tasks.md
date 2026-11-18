# Tasks — pomodoro timer

> Ordered, independently shippable steps. A box is ticked only when the behaviour
> is there **and** the criterion it implements can be demonstrated.

## Phase 1 — Skeleton

- [x] One `index.html`, inline CSS, inline JS, no dependencies (AC-12)
- [x] Layout: mode buttons, SVG ring, `mm:ss` digits, three controls
- [x] `mm:ss` formatter with zero padding (AC-2)

## Phase 2 — Core behaviour

- [x] Start / pause / resume without losing the remaining time (AC-3)
- [x] Reset the current block (AC-1)
- [x] `work → short → work …` cycle, long break on the fourth tomato (AC-4)
- [x] Break completion returns to a fresh focus block (AC-5)
- [x] Four-dot cycle indicator and the session hint line
- [x] Duration inputs change the block length (AC-8, partially — see Phase 4)

## Phase 3 — Polish

- [x] Synthesised alarm with WebAudio, no audio file
- [x] Toast for each transition
- [x] Browser notification when permission is granted (AC-11, partially)
- [x] Space toggles start/pause, `R` resets (AC-9)
- [x] Progress ring driven by `timeLeft / totalTime`

## Phase 4 — Known gaps

Opened after writing the spec against the shipped file; each one is a criterion
that the current code does not meet.

- [ ] **AC-6 — clock drift.** `tick()` decrements a counter on a 1 s interval, so a
      backgrounded tab runs slow. Replace with `deadline = now + remaining*1000`
      and recompute on each tick.
- [ ] **AC-7 — persistence.** Durations live in a module-level `DEFAULTS` object
      and the tomato count in a local variable; both die on reload. Snapshot to
      `localStorage` after every transition.
- [ ] **AC-10 — skip counts a tomato.** The skip handler calls `finish()`, which
      increments the count for `work` blocks. Skipping a focus block must not
      credit one.
- [ ] **AC-11 — permission on load.** `Notification.requestPermission()` runs at
      parse time, before any gesture. Move it to the first start click.
- [ ] **Dead branch.** The `🎉 本轮完成` hint is unreachable: the fourth tomato
      resets the count to 0 before the hint is rendered. Pick one owner for the
      count and delete the other path.
- [ ] **AC-8 — settings while running.** The inputs apply on `change` (blur), and
      while running they silently do nothing. Either disable them during a block
      or apply on the next one and say so in the label.
- [ ] Add the timing tests from `design.md` (injected clock, background gap).
