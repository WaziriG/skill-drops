# Relationship Memory Kit 1.1: read this first

**What it is.** A way to give your contact list a memory. A weekly, read-only pass over your inbox records how warm each relationship is, what you have talked about, what is still open, and who is waiting on a reply. You add one line per person on what they can help with, in your words. Then Claude Code can answer "who do I know who…" and suggest introductions worth making.

**Open first:** `GUIDE.pdf` (the same text is in `GUIDE.md`). About 20 minutes to a first result.

**Fastest proof it works** (two minutes, invented people only, writes nothing):
```
python3 scripts/inbox_enrich.py --people mock/people-spine.csv --feeder mock/linkedin-feeder.csv \
  --mbox mock/mock-inbox.mbox --me alex@yourfirm.example --search-link gmail
```

## What is in the box

| Folder | Contents |
|---|---|
| `GUIDE.pdf` / `GUIDE.md` | Setup guide: steps, columns, the weekly habit, what it will never do, troubleshooting |
| `skills/` | Three Claude Code skills: `relationship-memory-setup`, `relationship-memory-weekly`, `who-knows`. Copy them into `~/.claude/skills/`. |
| `skills/relationship-memory-setup/references/` | The column schema and notes for Notion, Airtable, and Excel or Google Sheets |
| `scripts/inbox_enrich.py` | The inbox reader. Read-only. Works with IMAP, an .mbox export, or messages pulled through a Gmail connector |
| `scripts/tests/` | Tests on invented data: `python3 -m unittest discover -s scripts/tests` |
| `scripts/scheduler/` | Weekly scheduling: launchd template, crontab line, wrapper script, Claude Code routine and n8n notes |
| `mock/` | Demo data: 30 invented people, 40 invented LinkedIn rows, an invented inbox, a demo People Data Map, and a sample run (`mock/sample-run/`) |

## Three promises

1. Mail is only ever read. Nothing is sent, moved, labeled or marked read.
2. The columns you write (Can Help With, Know Them?, Notes, Segment, Priority, Next Step) are never written by the automation. A follow-up cadence you set is never replaced, and open loops are only ever added to.
3. Every person in `mock/` is invented. Your real data stays in your own store and on your own machine.

## What changed in 1.1

Version 1.1 (October 2, 2026) fixes five problems found on a real inbox. Upgrading from 1.0: copy `scripts/inbox_enrich.py` into `~/.relationship-memory/bin/` and the skills into `~/.claude/skills/`. Your data needs no changes.

1. Weekly runs add new mail to each person's stored history instead of replacing it. The first email date and the relationship summary are kept; new context is added as a dated line.
2. "Reply owed" now means the person wrote to you. Mail they were only copied on, or that someone else sent, no longer counts as their last word.
3. Follow-up Cadence uses your column's own choices (Monthly, Quarterly and so on) and is written only when blank.
4. Next Step belongs to you. The automation never writes it, so you can record plans and rules there ("Paused", "No outreach").
5. Open Loops only grows: new items are added with a date, and nothing is deleted.

Full notes are in `GUIDE.pdf`, section "What changed in 1.1".
