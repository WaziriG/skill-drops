# Seven Days on the Terminal: start here

Ask anyone who uses Claude Code every day what it is worth to them and you get a guess. "It saves me a lot of time." How much? Nobody knows, because nobody has measured it.

The measurements are already on your computer. Claude Code keeps a log of every session you run, and every message in it has a time on it. `/seven-days` reads one week of those logs and tells you:

- **your hours:** how long you were actually at the terminal
- **agent hours:** how long the assistant was working, with sessions running side by side counted separately
- **leverage:** agent hours divided by your hours, the number that says whether work is happening while you do something else
- **streams of work:** how many sessions you started, and how many helper runs the assistant started inside them
- **a day-by-day table**, tokens, and the plain method behind every number

It only reads. It does not change or delete your logs, it never connects to the internet, and it uploads nothing. You can check: the script, `skills/seven-days/seven_days.py`, imports nothing that can reach the network.

**Where it came from.** In July I measured one week of my own work this way: 2.49x leverage, 115 streams of work, read from 266 session logs. The story and the full method are here: [Seven Days on the Terminal](https://wazirigaruba.com/seven-days). This drop turns that method into something you can run on your own week.

## What you need (setup: about five minutes)

- Claude Code, the terminal or desktop app. The chat website does not keep these logs.
- At least a week of your own Claude Code use. Claude Code keeps about 30 days of logs by default.
- Python 3. Most Macs have it. To check, open Terminal and type `python3 --version`. If your Mac offers to install developer tools, say yes; it is free and takes a few minutes. On Windows, install Python from python.org.

## 1. Install the skill (one minute)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it, open the `07-seven-days` folder, and copy `skills/seven-days` into `~/.claude/skills/`:

```
cp -R skills/seven-days ~/.claude/skills/
```

Restart Claude Code if it was already open.

## 2. See a finished run (two minutes)

Open `sample-run/SAMPLE-RUN.md`. It follows an invented framing-shop owner through one week: what the script printed, and what Claude said back. **The numbers in it are invented.** It shows the shape of the result, not a target.

## 3. Run it on your own week (two minutes)

Open Claude Code anywhere and type:

```
/seven-days
```

You will see your hours, your agent hours, your leverage and a table of the last seven days, then three short paragraphs on what it means and three things the numbers say about how you work. One of them will not be flattering. That one is usually the most useful.

Want to know where the week went? Type `/seven-days themes`. It sorts your sessions into themes and shows counts only.

## Before you share your numbers

Share the headline and the method, not the raw output. Your prompts and your project folder names can carry client names, figures and private matters. The skill never repeats your prompts back except on your own screen, and only when you ask for themes.

## Make it yours

The skill is two files: `SKILL.md` (plain instructions) and `seven_days.py` (the counting). The one setting worth knowing is `GAP_MINUTES = 15` at the top of the script: a pause longer than that counts as a break. If you change it, say so when you share a number.

Run it every Friday and keep the headline line in a note. Four weeks of the same number tell you more than one week of any number.

## What it will not do

- Change, move or delete anything in your logs
- Connect to the internet or upload anything
- Save a file, unless you ask for one
- Guess a number that is not in your logs

## What's in this folder

| Path | What it is |
|---|---|
| `skills/seven-days/SKILL.md` | The skill: what Claude does with the numbers. |
| `skills/seven-days/seven_days.py` | The script that reads your logs, read-only. Standard Python, nothing to install. |
| `sample-run/SAMPLE-RUN.md` | A finished run on an invented week. Every number in it is invented. |
| `LICENSE` | MIT. Use it, change it, share it. It also carries Nate Herk's MIT notice. |

## Credit

The way the script reads Claude Code's logs is adapted from Nate Herk's [token-dashboard](https://github.com/nateherkai/token-dashboard) (MIT). His tool shows where your tokens go. This one measures your time and your leverage. Every person and business in this folder is invented.

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
