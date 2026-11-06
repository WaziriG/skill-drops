# Sample run: one invented week

**This is a sample. Every number below is invented** to show what you will see. Theo and his shop are invented too. Your numbers will be different, and that is the point.

Theo runs a two-person picture-framing shop. He has used Claude Code for about a month, mostly for customer emails, his price list and the shop's website. He wanted to know if it was worth the hours he was putting in.

**What Theo typed:**

```
/seven-days
```

---

## What the script printed

```
SEVEN DAYS ON THE TERMINAL
Window: 2026-11-02 to 2026-11-08 (7 days, your local time)
Logs read: 64 files under ~/.claude/projects (read-only, nothing sent anywhere)

HEADLINE
  Your hours at the keyboard (wall-hours):     9.4 h
  Hours of agent work (agent-hours):          15.3 h
  Leverage (agent-hours / wall-hours):        1.63x

STREAMS OF WORK
  Sessions you started:     21
  Sub-agent runs:           6
  Streams in total:         27
  Active days:              6 of 7
  Prompts you typed:        148
  Replies from the agent:   1204
  Tool calls (actions):     1377

TOKENS
  Processed (all four kinds): 212.40M
  Generated (output only):    1.08M
  Share that is cache reads:  93%

BY DAY            wall-h   agent-h   leverage
  Mon 2026-11-02     2.1       3.8    1.81x
  Tue 2026-11-03     1.6       2.2    1.38x
  Wed 2026-11-04     0.0       0.0      -
  Thu 2026-11-05     2.4       4.6    1.92x
  Fri 2026-11-06     1.8       2.9    1.61x
  Sat 2026-11-07     0.9       1.0    1.11x
  Sun 2026-11-08     0.6       0.8    1.33x

MODELS (agent replies)
  (your model names and reply counts appear here)

METHOD
  (the method notes, the same on every run)
```

---

## What Claude said back

```
YOUR WEEK ON THE TERMINAL  (Nov 2 to Nov 8)

9.4 h of your attention  x  1.63 leverage  =  15.3 h of agent work

Streams of work: 27  (21 sessions you started + 6 sub-agent runs)
Active days: 6 of 7
Prompts you typed: 148     Actions the agent took: 1,377
```

**What 1.63x means.** For every hour you spent at the terminal, about an hour and forty minutes of work came back. Above 1.0x means something was working while you were doing something else.

**How it was measured.** Every message in your logs has a time on it. When messages in one session are 15 minutes apart or less, that counts as working time; longer pauses count as breaks. Each session is counted on its own, so two running side by side count twice. Lay them all on one clock and count overlaps once, and you get your 9.4 hours.

**What it can't see.** The 9.4 hours is a floor. Time you spent reading a draft, on the phone, or thinking in the car is not in the logs. And a session that ended cleanly may still have done a poor job.

**Three things the numbers say:**

1. Your best days were Monday and Thursday, both above 1.8x. Those were the days you had two sessions going at once.
2. Saturday ran at 1.11x: almost all of it was one session at a time, with you watching.
3. The unflattering one: Wednesday is zero. A six-day habit with a hole in the middle usually means the work that day was done by hand, the old way.

What would you want this number to look like in a month, and which one chore would get you there?

---

Nothing was uploaded and no file was saved. Theo copied the headline line into a note so he can compare next Friday.
