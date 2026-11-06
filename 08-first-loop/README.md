# The Governor: design your first loop

Most people use AI by prompting it. That means every piece of work still costs a piece of you: you are the one who remembers to start it, the one who checks it, the one who carries what happened last time. The assistant never gets tired. Your attention does.

A loop changes who starts the work. It is a repeatable job an assistant does on a rhythm, with its rules written down, and every result waiting in one place for your yes.

`/first-loop` designs your first one. It asks you three questions at most about one task you redo by hand every week. Then it gives you a one-page spec:

- **the trigger:** when it runs
- **what the assistant does**, step by step, and the rules it follows
- **what it is never allowed to do:** send, post, pay, delete, and anything your answers add
- **the review queue:** the one place its drafts wait for you
- **how you will know it works** after one week, with a tally you can keep on a sticky note

It ends with the prompt for your first manual run.

**It installs nothing and schedules nothing.** That is on purpose. You don't automate a job you have never run by hand; you would only be making mistakes on a timer. Run it yourself for a week. If it passes, then you choose how to schedule it.

**The name:** in 1788 James Watt put a governor on his steam engine, two brass balls on a spinning shaft that opened and closed the valve on their own. It was the part that let the engine run without a man standing beside it with his hand on the valve. That is what a loop is for.

**The story behind it:** [Looping](https://wazirigaruba.com/looping). The week I stopped prompting my AI and built five loops that all report to one review queue.

## What you need

- Claude Code
- One task you redo every week
- Ten minutes for the interview, then one week of manual runs

## 1. Install the skill (one minute)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it and open the `08-first-loop` folder. Copy the `skills/first-loop` folder into `~/.claude/skills/`:

```
cp -R skills/first-loop ~/.claude/skills/
```

## 2. See a finished run (two minutes)

Open `SAMPLE-RUN.md`. It follows an invented dog-grooming shop owner through the three questions, the first-loop check, the spec, and the prompt she pastes each Monday.

## 3. Run it on your own task (ten minutes)

Open Claude Code and type:

```
/first-loop
```

It asks one question at a time. Pick something small and boring: follow-ups, review replies, a weekly report, tidying a spreadsheet. If your first idea is too big, it will say so and cut it down to a slice that passes.

## 4. Run it by hand for a week

Use the run prompt at the bottom of your spec, every time the trigger comes around. Keep the tally. At the end of the week, the spec tells you whether the loop passed, and what to fix if it did not.

## What it will not do

- Build, install, connect or schedule anything
- Recommend automation products
- Design a loop that sends, pays, posts or deletes without your yes
- Ask for passwords, keys or access to your accounts

## Make it yours

The whole skill is one markdown file of plain instructions: `skills/first-loop/SKILL.md`. Open it. If your business has a rule every loop should follow, add it to the "never allowed" list there, and every spec it writes will carry it.

## What's in this folder

| Path | What it is |
|---|---|
| `skills/first-loop/` | The skill. Copy the folder into `~/.claude/skills/`. |
| `SAMPLE-RUN.md` | A full example run with an invented operator. |
| `LICENSE` | MIT. Use it, change it, share it. |

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
