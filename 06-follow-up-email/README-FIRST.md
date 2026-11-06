# Follow-Up Email: start here

You end a good call with four promises: a price sheet, a few photos, an introduction, a date for the next step. By the time you sit down to write the follow-up, you remember three. The other person remembers all four.

`/follow-up-email` reads your call notes or transcript and does two things. First it lists every promise made on the call, by you and by them, with their words beside each one. Then it drafts a short follow-up email that delivers each of your promises or puts a date on it. It asks you at most three questions in between, such as whether you have a link or what date you can commit to.

It never sends anything. It does not open your email, your calendar or your files. You read the draft, attach what needs attaching, and send it yourself.

**Where it came from.** I use a bigger version of this in my own work, one that also finds the files on my computer. On September 17 it turned a call with an old classmate into one follow-up that carried every file I had promised, and said plainly which introduction I was still checking before I made it. This drop is the small version: the part anyone can run.

## What you need

- Claude Code
- Notes from one call. Typed bullets, a transcript from a recording app, or an AI notetaker's summary all work.
- Two minutes for the first run

## 1. Install the skill (one minute)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it, open the `06-follow-up-email` folder, and copy `skills/follow-up-email` into `~/.claude/skills/`:

```
cp -R skills/follow-up-email ~/.claude/skills/
```

Restart Claude Code if it was already open.

## 2. The two-minute first run

Open Claude Code in this folder and type:

```
/follow-up-email sample-run/sample-call-notes.txt
```

Those are invented notes from a bakery owner's call with a new wholesale lead. You will see a table of six promises, two flags (something said in confidence, and a budget number said loosely), and up to three questions. Answer them, or say "just draft it". Then compare what you get with `sample-run/SAMPLE-RUN.md`.

## 3. Run it on your last real call

Paste your notes after the command, or give it the file:

```
/follow-up-email
```

Read the promise list before you read the draft. If the list is missing something you remember saying, tell it. The list is the part that protects you.

## It works for a job search too

The same thing happens after an interview or a networking coffee: you said you would send something, and so did they. An invented example:

> Jordan Lee has a twenty-minute call with Priya Raman, a hiring manager at a regional health company. Jordan offers to send a one-page summary of a scheduling project and says, "I could send you the deck from my talk last spring." Priya says she will forward the job description and mention Jordan to her director. Jordan also says, "you should talk to my old manager, Sam, he hired for this exact role."

`/follow-up-email` lists five promises. Three are Jordan's: the summary, the deck, and the introduction to Sam, which it marks **Check first**. Two are Priya's. The draft thanks Priya for one specific thing she said, attaches the summary and the deck, says Jordan is checking with Sam and will connect them by a named day, and restates Priya's two promises once, without pushing. It comes in under 150 words, the night of the call.

## Make it yours

The whole skill is one markdown file of plain instructions, `skills/follow-up-email/SKILL.md`. Open it. Change the word limit, add phrases you never want in an email, or add a line about how you sign off. When you find yourself making the same correction to a draft twice, put that correction in the file.

## What it will not do

- Send, schedule or save anything to your email
- Make up a promise that is not in your notes
- Repeat a number or anything confidential from the call unless you confirm it

## What's in this folder

| Path | What it is |
|---|---|
| `skills/follow-up-email/` | The skill: one `SKILL.md`. Copy the folder into `~/.claude/skills/`. |
| `sample-run/sample-call-notes.txt` | Invented call notes for your first run. |
| `sample-run/SAMPLE-RUN.md` | The finished run on those notes: promise list, questions, draft, checklist. |
| `LICENSE` | MIT. Use it, change it, share it. |

Every person and business in this folder is invented.

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
