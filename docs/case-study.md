# Case study: what a spec would have caught

The example in [`examples/pomodoro-timer/`](../examples/pomodoro-timer/) is a
complete spec for a real 577-line single-file Pomodoro timer — one of those
projects that a model writes in a single pass, that works well enough to keep, and
that nobody opens again.

The spec was written *afterwards*, on purpose. It is the document that would have
made the second session cheap, and reading it next to the code shows what it would
have forced into the open **before** the first line was written.

## What the app gets right

Mode switching, the SVG progress ring, the four-tomato cycle, synthesised audio,
toast messages and keyboard shortcuts all arrived in one pass and all work. This
is the part people mean when they say one-shot code is "good enough".

## Four decisions the spec makes explicit

Each one is a line of code that looks fine in isolation.

**1. How is time measured?** The timer decrements a counter once per second. That
is correct until the tab is backgrounded, at which point browsers throttle timers
to roughly one tick per minute — so a 25-minute block can take half an hour and
the number on screen is simply wrong. AC-6 says the remaining time must be within
one second of wall-clock, which rules out counting ticks and leaves one design:
store a deadline, recompute on every tick. You cannot write AC-6 and then write
`timeLeft--`.

**2. Does anything survive a reload?** Durations live in a module-level object and
the tomato count in a local variable; both are gone on refresh, and the inputs
snap back to 25/5/15. Nothing in a requirements document would have caught this —
but AC-7 ("restore the durations and the count") is a sentence someone has to
write, and once written, "where does it live" becomes a design question with an
obvious answer.

**3. What does *skip* mean?** The skip handler sets the time to zero and calls the
same `finish()` that a completed block calls, so skipping a focus block credits a
tomato. The app therefore rewards giving up. AC-10 splits "finished" from "skipped"
in one line; without it, the shortcut is indistinguishable from the achievement.

**4. When do you ask for notification permission?** At parse time, before any user
gesture — which browsers increasingly ignore, and which is the kind of thing that
gets a file-permission prompt denied forever on first contact. AC-11 makes the
alarm and toast the primary signal and the permission request a single, deliberate
event.

There is a fifth, quieter one: the "🎉 cycle complete" hint is unreachable, because
the fourth tomato resets the count to zero before the hint renders. Two pieces of
code both claim ownership of the same counter. A state-machine table — the kind
`design.md` asks for — makes that duplication visible on paper.

## What this says about the tool

The linter agrees the folder is complete, and that is the least interesting thing
about it:

```console
$ spec-scaffold --check examples/pomodoro-timer
OK  examples/pomodoro-timer looks like a complete spec
```

The value is not the headings. It is that a spec has to say *what "done" means*
for each behaviour, in a sentence short enough to check against the code. Four of
those sentences, written before the code, would have produced a better app in the
same number of passes.

## The honest caveat

This is a reconstruction. Writing the spec after the code is a diagnosis, not a
cure: it tells you what the first session should have asked, and it is why
`tasks.md` keeps the unmet criteria as open boxes instead of quietly ticking them.

If you have a one-shot project of your own, the cheapest version of this exercise
is:

```bash
spec-scaffold "your project, in a few words" -o specs
# then rewrite requirements.md from memory, and read the code against it
```

The gaps you find in the first twenty minutes are the ones that were never
decisions — they were defaults.
