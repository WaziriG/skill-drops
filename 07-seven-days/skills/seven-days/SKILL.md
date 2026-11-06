---
name: seven-days
description: Measure one week of your own Claude Code use from the session logs already on your computer. Reports sessions, active hours, streams of work, tokens and a leverage estimate (hours of agent work per hour of your attention), with the method stated plainly. Read-only, local, no internet, uploads nothing. Use when someone asks "how much am I actually using Claude Code", "measure my week", "what is my leverage", or "seven days". Trigger: /seven-days
---

# /seven-days

People who use Claude Code every day usually can't say what it is worth to them. They guess. The answer is already on their computer: Claude Code keeps a log of every session, with a timestamp on every message. This skill reads those logs and turns one week into a few honest numbers.

You run one script, then explain what it found in plain language. You never guess a number. Every number you give comes from the script's output.

## What this skill will never do

- Change, move or delete anything in `~/.claude/projects/` (the script opens the logs read-only)
- Connect to the internet, upload or send anything
- Save a file, unless the user asks for one
- Quote the user's own prompts back to anyone but the user

## Usage

```
/seven-days                 # the last 7 days, ending today
/seven-days 14              # a longer window
/seven-days ending 2026-03-08
/seven-days themes          # also sort the week's sessions into themes (private)
```

## Step 1: Run the script

The script sits beside this file. Run it with Python 3:

```
python3 ~/.claude/skills/seven-days/seven_days.py
```

Options, if the user asked for them:

- `--days 14` for a different window length
- `--end YYYY-MM-DD` to end the window on another day
- `--prompts` for the themes step (Step 4)
- `--save <file>` only if the user asked to keep a copy, and only into a folder they name

If the logs live somewhere else, add `--projects-dir <path>`.

If `python3` is missing, stop and tell the user: on a Mac, typing `python3` in Terminal offers to install it (Apple's free developer tools, a few minutes). On Windows, install Python from python.org. Then run again.

If the script says it found no activity, tell the user plainly. Most likely they have used Claude Code for less than a week, or their logs were cleared. Suggest `--days 14` or trying again after a week of use.

Do not read the log files yourself. They are large and full of private text. The script is the only thing that reads them.

## Step 2: Give the readout

Show the user this, filled from the script output only:

```
YOUR WEEK ON THE TERMINAL  (<start> to <end>)

<wall-hours> h of your attention  x  <leverage> leverage  =  <agent-hours> h of agent work

Streams of work: <total>  (<sessions> sessions you started + <sub-agent runs> sub-agent runs)
Active days: <n> of 7
Prompts you typed: <n>     Actions the agent took: <tool calls>
```

Then the day-by-day table from the script, unchanged.

## Step 3: Explain it in plain words

Write three short paragraphs. No jargon.

1. **What the leverage number means.** Leverage is hours of agent work divided by hours of your attention. 1.0x means the assistant only worked while you watched. 2.0x means two hours of work came back for each hour you spent. Say where theirs sits.
2. **The method, said simply.** "Every message in your logs has a time on it. When messages in one session are 15 minutes apart or less, that counts as working time. Longer pauses count as breaks. Each session is counted on its own, so two sessions running side by side count twice: that is agent-hours. Lay all of them on one clock and count overlaps once: that is your hours."
3. **What it cannot see.** Wall-hours are a floor on their time, not their whole day: thinking, reading, calls and work away from the terminal are not in the logs. A session that ended cleanly may not have done its job well. Claude Code keeps about 30 days of logs by default, so this can measure the last month, not the last year.

Then give the **three most interesting things the numbers say about how they work**, including one that is not flattering. Use the day table: busy days and quiet days, which days had the most parallel work, whether most work happens in one session at a time. Each point must point at a number in the output.

End with one question: "What would you want this number to look like in a month, and which one chore would get you there?"

## Step 4: Themes (only when the user asked for themes)

Run the script with `--prompts`. It lists the first prompt the user typed in each session. Group them into four to seven themes (for example: customer email, bookkeeping, website, planning) and give a count for each. Show only theme names and counts. Do not repeat the prompts themselves in your answer, and never put them in a saved file.

Say this once: "The raw list quotes your own words: names, numbers and private matters. Keep it to yourself. If you share your week, share the counts."

## Step 5: If they want to share it

Offer a short version they can paste anywhere: the headline line, streams, active days and the method in one sentence. No prompts, no project folder names, no client names. Remind them that a folder name can be a client's name.

## Make it yours

- Change `GAP_MINUTES` at the top of `seven_days.py` if 15 minutes feels wrong for how you work. Say so when you share a number, because it changes the result.
- Run it every Friday and keep the headline line in a note. The direction over four weeks tells you more than any one week.

## Credit

The way this reads Claude Code's logs (the usage fields, telling a typed prompt from machine bookkeeping, and counting each streamed reply once) is adapted from Nate Herk's [token-dashboard](https://github.com/nateherkai/token-dashboard), MIT, Copyright (c) 2026 Nathan Herkelman. His tool is about cost. This one is about time and leverage.
