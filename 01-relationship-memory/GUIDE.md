# Relationship Memory Kit

## A setup guide for operators · Harlem Labs · Version 1.1 · October 2026

# What it does

Most people's networks live in three places that never talk to each other: a contact list, a LinkedIn connections list, and an inbox. The list knows names. The inbox knows the relationship. This kit joins them.

Once a week, a read-only pass over your inbox fills in, for every person you care about: how many emails you have exchanged, when it started, when it last moved, who wrote last, what you have talked about and worked on, what is still open, and when to follow up. From that it scores **Warmth** (0 to 100) and flags **replies you owe**.

You add one thing the inbox cannot know: a line, in your own words, on what each person **can help with**. Then you can ask Claude Code "who do I know who…" and get an answer ranked warmest first, quoting your own words, with who could introduce you. Ask it for introductions and it finds people in your network who should meet each other, then drafts the ask, one side at a time.

It works with the tools you already use: **Notion, Airtable, Excel or Google Sheets** for the people, and **Gmail, any IMAP mailbox, or an exported .mbox file** for the mail.

# What changed in 1.1

Version 1.1 (October 2, 2026) fixes five problems found when the kit ran against a real inbox and a real contact list. If you installed 1.0, copy the new `scripts/inbox_enrich.py` into `~/.relationship-memory/bin/` and the three skills into `~/.claude/skills/`. Your data needs no changes.

| What you might have seen in 1.0 | What 1.1 does |
|---|---|
| A weekly run reset a long history to a handful of emails, lost the First Email date, and rewrote Relationship Context from one week of mail | Weekly runs **add** new mail to the stored totals. The first email date stays. Relationship Context keeps every word and gains a dated line for what is new. |
| "Reply owed" for someone who was only copied on a message, or when a third party wrote last | **They wrote last** only when they wrote to you. **You wrote last** only when you wrote to them. Copies and third-party mail count toward volume, never toward who owes a reply. |
| Follow-up Cadence written as a number of days into a column that uses choices such as Monthly or Quarterly, or over a cadence you had set | The run uses your column's own choices, and it writes a cadence **only when the cell is blank**. |
| Next Step filled in by the automation | **Next Step is yours.** Write your plans and rules there ("Paused", "No outreach", "No action until January"). The run never writes it, and the other tools respect it. |
| Open Loops replaced on each run | Open Loops **only grows**: each new item is added on its own dated line, duplicates are skipped, and nothing is removed. Clear a loop yourself when it closes. |

Two smaller changes: Warmth and Follow-up Status are now kept apart from the columns written to Notion or Airtable, so they can never overwrite a formula; and a full recheck (`--full`) never zeroes a person whose history it could not find. The kit now ships with tests: `python3 -m unittest discover -s scripts/tests` runs 20 checks, one or more for each fix.

# What you need

| Item | Notes |
|---|---|
| A Mac or Linux machine with Python 3.9+ | `python3 --version` |
| Claude Code, signed in | It writes the summaries and runs the three skills |
| `openpyxl` | Only for Excel: `pip3 install openpyxl` |
| One people store | Notion or Airtable (with its connector added to Claude Code), Excel, or Google Sheets |
| One inbox | Gmail connector, IMAP with an app password, or an .mbox export |

# Twenty minutes to your first result

### 1. Unzip the kit (1 minute)

Unzip it anywhere and open a terminal in the `Relationship-Memory-Kit` folder.

### 2. Run the demo (2 minutes)

Everyone in it is invented. Nothing is written. The demo inbox is dated relative to the day it was built (October 1, 2026); to re-date it to today first, run `python3 mock/make_mock.py`.

```
python3 scripts/inbox_enrich.py --people mock/people-spine.csv \
  --feeder mock/linkedin-feeder.csv --mbox mock/mock-inbox.mbox \
  --me alex@yourfirm.example --search-link gmail
```

You should see about 29 people with history, 9 replies owed, and 3 new people found in the inbox. Open `mock/sample-run/run-report.txt` to see the same run with Claude's summaries switched on, and the two `who-knows` examples beside it.

### 3. Install the three skills (1 minute)

If you already have a skill named `who-knows`, rename ours first.

```
cp -R skills/relationship-memory-setup skills/relationship-memory-weekly skills/who-knows ~/.claude/skills/
```

### 4. Run setup in Claude Code (10 minutes)

From the kit folder, in Claude Code:

```
/relationship-memory-setup
```

It asks three questions, one at a time: where your people live, which inbox, and how to schedule the weekly run. Then it creates the columns and views in your store, writes your **People Data Map** to `~/.relationship-memory/`, and shows you how to store a mail app password in the macOS Keychain yourself. Claude never sees the password.

### 5. Load your people (3 minutes)

Bring a contacts export, your LinkedIn `Connections.csv`, or type the people who matter most. Start small: the 20 to 50 you would actually call.

### 6. First learning run, dry (2 minutes, longer on a big inbox)

```
/relationship-memory-weekly --dry-run --full
```

Nothing is written. Read the report: replies owed, new people, suggested lines. Then run it again without `--dry-run` and say yes to write.

### 7. Ask your first question (1 minute)

```
/who-knows someone who can get a company's books ready for a bank loan
```

# The columns

| You write these | The weekly run writes these |
|---|---|
| Name, Email, Company, Role / Title | Emails Exchanged, Email Threads |
| Segment, Priority (A, B, C) | First Email, Last Email, Last Email From |
| **Know Them?** (Yes / Getting to know / No) | Relationship Context (kept, with dated additions) |
| **Can Help With**, in your own words | Open Loops (added to, never cleared) |
| Notes | Follow-up Cadence (only if blank), Inbox Checked |
| **Next Step**: your plan or rule for this person | Mail Search Link, **Suggested Can Help With** |

Warmth, Warm Enough to Ask and Follow-up Status are formulas in your store. The full list, with types and formulas for each store, is in `skills/relationship-memory-setup/references/`.

# How Warmth and follow-up work

**Warmth** = email volume (4 points per email, up to 40) + recency (40 for an email today, falling to 0 after about a year) + 20 if they wrote last. **35 or more is warm enough to ask.** Below that, re-warm before asking for anything.

**Follow-up Status**, checked in this order:

| Status | Meaning |
|---|---|
| Reply owed | They wrote last, within the past 60 days |
| Dormant | Silent for more than three follow-up cycles: re-warm before any ask |
| Overdue | The follow-up date has passed |
| Due soon | Due within 14 days |
| On track | Not due yet |
| No email history | Nothing in the inbox yet |

The follow-up cadence starts from Priority (A every 30 days, B 60, C 90) and tightens to the rhythm you actually keep with that person, never under 14 days. Set it yourself and it sticks.

# Know Them? and Can Help With

These two columns are what make the answers trustworthy, so the automation never touches them.

- **Yes**: you know them well enough to ask. Only these people are ever suggested.
- **Getting to know**: in your pipeline, not yet known. Never suggested. Your next follow-up should carry one natural question about what they do. When they answer, the weekly run proposes a line; you approve it and switch them to Yes.
- **No**: never suggested, never flagged as a reply owed.

Write **Can Help With** the way you would describe the person to a friend: "Fractional CFO for service firms under $20M; clean books before a bank loan." The weekly run may propose a **Suggested Can Help With** for people you have not described yet. It sits in its own column until you accept it in your words.

# The weekly habit (ten minutes)

1. Open **Follow up now**. Answer the replies you owe first.
2. Open **Suggestions to review**. Accept or ignore.
3. Open **Inbox Discoveries**. Tick Promote for anyone who belongs in People. Set their Know Them? yourself.
4. Write **Can Help With** for five more people from **Write Can Help With** (warmest first).

# Introductions

```
/who-knows --intros
```
The run looks at what your people have told you they need (Open Loops, Next Step, recent context), matches it against everyone else's Can Help With, and proposes up to three introductions. For each it drafts two notes, **to be sent one at a time**: first to the person with the need, offering the intro and asking what they are comfortable sharing; then, only after they say yes, to the other side. Neither draft carries the other person's private context.

# What it will never do

- Send, delete, move, label or mark as read any email. IMAP folders are opened read-only and messages are fetched with a peek.
- Write Can Help With, Know Them?, Notes, Segment, Priority or Next Step, or replace a follow-up cadence you set.
- Delete or rewrite an open loop or the relationship history it has already recorded.
- Add a new person to your People table without your tick.
- Suggest anyone marked Getting to know, No, or left blank.
- Show one person another person's notes, email context or open loops.
- Store your mail password in a file. It lives in the macOS Keychain, and the script reads it only for the run.
- Send anything anywhere. Drafts are shown to you; you send them.

# For your IT lead: where the data goes

| Data | Where it goes |
|---|---|
| Mail headers and bodies | Read on your machine. Only counts, dates and the summaries below are written to your store. |
| Up to 15 recent messages per person, trimmed to 500 characters each | Sent to Claude through your own Claude Code account, only when summaries are on (`--summarize`), to write Relationship Context, Open Loops and the suggested line. Turn summaries off and no message text leaves the machine. |
| History columns | Written to your store (Notion or Airtable through their connectors; Excel and CSV on disk). |
| App password | macOS Keychain. Exported into the environment for one run only. |
| Backups | Excel and CSV: a dated copy in `_archive/` before every write. |

Microsoft 365 tenants usually disable password-based IMAP. The script supports OAuth (`--imap-oauth-env`); getting the token is a tenant admin task. An .mbox export is the zero-integration fallback.

# Troubleshooting

| Symptom | Fix |
|---|---|
| `Give your own address with --me` | Pass every address you send from, comma-separated. Without it the script cannot tell sent from received. |
| IMAP login fails | Use an app password, not your normal password. 2-step verification must be on. Workspace or Microsoft 365 admins may need to allow IMAP. |
| Everyone shows "No email history" | Wrong folder. Gmail needs `[Gmail]/All Mail` (the default for imap.gmail.com). Elsewhere, pass `--imap-folders "INBOX,Sent Items"`. |
| A person matched "by Name" | No email on file, so the match used their name. Check it, then add their email. |
| Summaries failed | Check `claude -p "hello"` works in the same terminal. The next run fills only the gaps. |
| Notion shows Warmth but Claude cannot read it | Expected. Formulas are not readable through the API. The skills read the "Warmest first" view in order instead. |
| Excel write fails or loses formatting | Close the workbook before the run. Keep charts and pivots in a separate workbook. |
| Scheduled run did nothing | Check `~/.relationship-memory/reports/launchd.err`. The Keychain is unavailable while the Mac is locked; schedule for a time you are usually logged in. |

# What is in the kit

| Path | What it is |
|---|---|
| `README-FIRST.md` | One page: what is here and what to open first |
| `skills/relationship-memory-setup/` | The setup skill, with the schema and per-store notes in `references/` |
| `skills/relationship-memory-weekly/` | The weekly learning run |
| `skills/who-knows/` | "Who do I know who…" plus `--intros` |
| `scripts/inbox_enrich.py` | The read-only inbox reader (IMAP, .mbox, or messages pulled by Claude) |
| `scripts/tests/` | Regression tests on invented data, one or more for each 1.1 fix |
| `scripts/scheduler/` | launchd template, crontab line, wrapper script, and notes for Claude Code routines and n8n |
| `mock/` | Invented people, an invented inbox, a demo People Data Map, and a sample run with summaries |
