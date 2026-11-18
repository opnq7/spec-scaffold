# Requirements — pomodoro timer

## Overview

A Pomodoro timer that needs no install, no account and no network: one
`index.html`, opened from disk. It is for people who want the 25/5 rhythm without
another app on their machine — and it has to keep working while the tab is in the
background, which is exactly when a focus tool is most needed.

This spec was written after the app, as a worked example. `tasks.md` records which
criteria the shipped version actually meets.

## Goals

- Start a focus block in one click, from a file that needs no server.
- Cycle focus → short break → focus …, with a long break every fourth tomato.
- Track wall-clock time, not interval ticks, so a backgrounded tab does not drift.
- Remember the durations and the current cycle's tomato count across reloads.

## Non-goals

- Accounts, sync, teams, or any network request.
- Sound files or a build step; the alarm is synthesised with WebAudio.
- Task lists or time tracking against projects.

## User Stories

- **US-1** — As someone about to start deep work, I want the timer running in one
  click, so that I do not spend the first five minutes configuring it.
- **US-2** — As a user in a focus block, I want to see how much of it is left at a
  glance, so that I can decide whether to start one more thing.
- **US-3** — As a user whose block ended while I was in another tab, I want an
  alarm and a notification, so that I notice without watching the screen.
- **US-4** — As a user with a 50-minute cadence, I want to change the durations
  once and have them stick.
- **US-5** — As a keyboard user, I want space to start or pause and `R` to reset,
  so that I never have to aim at a small button.
- **US-6** — As a user who has finished four tomatoes, I want a long break offered
  automatically, so that I do not have to keep the cycle in my head.

## Acceptance Criteria

- **AC-1** — WHEN the page loads, THE SYSTEM SHALL show the focus duration and the
  label `准备开始`, with the timer stopped.
- **AC-2** — WHEN the user starts the timer, THE SYSTEM SHALL count down once per
  second and render `mm:ss` with zero-padded minutes and seconds.
- **AC-3** — WHEN the user pauses and later starts again, THE SYSTEM SHALL resume
  from the remaining time, not from the top of the block.
- **AC-4** — WHEN a focus block reaches zero, THE SYSTEM SHALL play the alarm, mark
  one tomato done, and switch to the short break — or to the long break when that
  was the fourth tomato.
- **AC-5** — WHEN a break reaches zero, THE SYSTEM SHALL play the alarm and return
  to a fresh focus block.
- **AC-6** — WHEN the tab has been in the background for any period, THE SYSTEM
  SHALL report the remaining time within one second of wall-clock elapsed time.
- **AC-7** — WHEN the user reloads the page, THE SYSTEM SHALL restore the three
  durations and the tomato count of the current cycle.
- **AC-8** — WHEN the user changes a duration while the timer is stopped, THE
  SYSTEM SHALL apply it to the current block; while running, to the next block.
- **AC-9** — WHEN the user presses space, THE SYSTEM SHALL toggle start and pause;
  WHEN the user presses `R`, THE SYSTEM SHALL reset the current block.
- **AC-10** — WHEN the user skips a break, THE SYSTEM SHALL move to the next focus
  block; WHEN the user skips a focus block, THE SYSTEM SHALL NOT count it as a
  completed tomato.
- **AC-11** — WHEN notification permission is denied or unavailable, THE SYSTEM
  SHALL still play the alarm and show the in-page toast, and SHALL NOT ask for
  permission again on every load.
- **AC-12** — WHEN the page is opened from the filesystem with no network, THE
  SYSTEM SHALL function fully.

## Out of Scope

- Statistics beyond the current cycle's four dots.
- Mobile-specific layout beyond a responsive single column.
- Themes, localisation, or a settings screen beyond three number inputs.

## Open Questions

- [ ] Does the tomato count belong to a *day* or to a *cycle*? The spec says cycle;
      a daily reset would need a stored date next to it.
- [ ] After the machine sleeps mid-block, should the alarm fire late or should the
      block be treated as finished? AC-6 covers elapsed time, not missed audio.
