# Vet a Tool: start here

Every week someone asks you to connect a new AI tool to your inbox, your contacts or your clients. Most people decide from the vendor's homepage. That is backwards: once you read the marketing first, the marketing becomes your requirements.

`/vet-a-tool` runs the check in the right order. It asks you five questions, one at a time, about the job and the data. It works out your non-negotiables from your answers. Only then does it look at what the vendor has actually written down. You get a verdict you can file: permissible, permissible with a written limit, or not permissible, plus a list of what is still unknown.

It never states a vendor's terms from memory. Terms change and differ by plan. If nobody has looked something up, the honest answer is "unknown," and for your most sensitive data, unknown counts as a No.

**The story behind it:** [One Link Deeper](https://wazirigaruba.com/one-link-deeper). An AI introduction service asked me twice for a list of people from my network. When I finally checked its policies, the real answers were one link below the page labeled Privacy.

## What you need

- Claude Code
- One tool you are using, or about to start using
- Twenty minutes

## 1. Install the skill (one minute)

Copy the `skills/vet-a-tool` folder into `~/.claude/skills/`:

```
cp -R skills/vet-a-tool ~/.claude/skills/
```

## 2. See a finished run (two minutes)

Open `sample-run/boardy-2026-10-21.md`. It is my own run on Boardy, with the vendor's exact words quoted, the date I read them, and the verdict. Your verdict will differ, because it depends on your data and your obligations, not the tool alone.

## 3. Run it on a tool you already use (fifteen minutes)

Pick one you already rely on: the notetaker on your calls, the AI inside your email, the assistant that reads your documents. Then type:

```
/vet-a-tool <the tool's name>
```

Answer one question at a time. When it asks what you found on the vendor's site, you can either look yourself or ask Claude Code to read the pages for you. If it reads them, check that every claim it reports is a quote, with the page and its "last updated" date. A summary is not a quote.

## 4. File the verdict

Save the verdict block with the date somewhere you will find it again. That becomes your approved-tools list. File the Nos too, with the reason. An exclusion with no recorded reason gets argued again in six months.

## The same check, without Claude

`skills/vet-a-tool/WORKSHEET.md` is the same filter on paper, about twenty minutes with a pen. The skill saves you the lookups and the drafting. The judgment is still yours.

## Make it yours

The whole skill is two markdown files of plain instructions: `SKILL.md` (the interview) and `BRAIN.md` (the reasoning behind it). Open them. If your industry has a rule the five lanes miss, add it to `BRAIN.md`. And once you see how this one is built, you can write one for any decision you make over and over.

## What it will not do

- Tell you whether you are legally a "covered institution," a "business associate" or a "controller"
- Interpret your contracts or a regulation
- Rank tools or name a "best" one

Those questions belong to a lawyer or a compliance professional. Knowing which questions aren't yours to answer is part of the job.

## What's in this folder

| Path | What it is |
|---|---|
| `skills/vet-a-tool/` | The skill: `SKILL.md`, `BRAIN.md`, and the paper `WORKSHEET.md`. Copy the folder into `~/.claude/skills/`. |
| `sample-run/` | A real, dated run on Boardy, quoting the vendor's own policies. |

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
