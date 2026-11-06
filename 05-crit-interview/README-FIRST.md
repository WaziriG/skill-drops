# CRIT: make the AI interview you first

You ask AI a question and it answers right away. The answer is fine, and it is generic, because it answers the question you typed. The one you needed answered sits one level down, in things only you know.

`/crit` changes the order. Before any task that matters, it walks you through four steps:

- **Context.** You tell it what is going on in paragraphs, the way you would tell a smart friend, and you paste in the real email, the real numbers, the real plan. It plays the situation back to you so you can correct it.
- **Role.** It proposes a specific expert to be for this problem (not "a consultant", but someone whose background changes how they would see it). You can swap it.
- **Interview.** It asks you questions, one at a time, before it tells you anything. Three is usual, five at most. Each one builds on your last answer.
- **Task.** It restates the job in one line: what gets made, for whom, where it lands. You confirm.

Then it either does the work right there, or hands you a ready prompt that carries everything you worked out, to paste into any AI (Claude, ChatGPT, Gemini) or save for later.

It needs no accounts and no keys. It never sends anything, and it only reads files you point it to.

**The method is Geoff Woods'**, from his book *The AI-Driven Leader*. This skill is my own write-up of how I run it day to day. If it helps you, read the book.

**Where it came from.** I heard Geoff walk through CRIT on a livestream in July. That evening I wrote the four steps into the instructions every one of my Claude Code sessions reads before it does anything else, and they have run at the top of my working sessions since. On September 22 I used it to prepare for a first call with a partner's head of technology. Written down, the context, role and interview came to one decision: listen first. No offer on the first call, only questions, and a single useful follow-up within two days.

**The story behind it:** [The Interview](https://wazirigaruba.com/the-interview)

## What you need

- Claude Code
- One decision, plan or problem you have been putting off
- Ten minutes

## 1. Install the skill (one minute)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it, open the `05-crit-interview` folder, and copy `skills/crit` into `~/.claude/skills/`:

```
cp -R skills/crit ~/.claude/skills/
```

Restart Claude Code if it was already open.

## 2. See a finished run (two minutes)

Open `sample-run/SAMPLE-RUN.md`. It follows an invented cleaning company owner whose biggest office client wants 15 percent off. Watch for the second interview question: it is the one that turns a price fight into a different conversation.

## 3. Run it on something real (ten minutes)

Open Claude Code and type:

```
/crit
```

Then describe what you are working on. Pick something real: a price you need to set, a hire, a hard email, a client who is drifting. Answer its questions honestly and briefly. The questions that make you pause are the ones doing the work.

If the job is quick and mechanical, it will tell you so and just do it. Not everything needs an interview.

## Make it yours

The whole skill is one markdown file of plain instructions: `skills/crit/SKILL.md`. Open it. You can change the default number of questions, add the kinds of experts you like it to play, or add a rule your business always follows. When you find yourself correcting it the same way twice, put that correction in the file.

## What it will not do

- Send, post, schedule, buy or delete anything
- Open your email, calendar or accounts
- Read files you did not point it to
- Save anything unless you ask (it offers a one-page brief only for work that spans more than one sitting)
- Make the decision for you

## What's in this folder

| Path | What it is |
|---|---|
| `skills/crit/` | The skill: one `SKILL.md`. Copy the folder into `~/.claude/skills/`. |
| `sample-run/SAMPLE-RUN.md` | A full run with an invented operator, from context to the email she sent. |
| `LICENSE` | MIT. Use it, change it, share it. The CRIT method itself belongs to Geoff Woods; credit him when you teach it. |

Every person and business in this folder is invented.

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
