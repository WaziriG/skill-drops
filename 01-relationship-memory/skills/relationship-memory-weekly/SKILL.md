---
name: relationship-memory-weekly
description: The weekly learning run for Relationship Memory (kit 1.1). Reads the inbox read-only, adds new mail since Inbox Checked to each person's stored email history (never resets it), proposes Suggested Can Help With lines for people the owner has not described yet, and lists new people (2+ emails each way, not in the spine) for one-click promotion. Store-agnostic (Notion, Airtable, Excel, Google Sheets, CSV) via the People Data Map. Never writes owner columns (including Next Step). Modes: --dry-run (print proposed changes, write nothing), --apply (write without asking; for schedules), --full (recheck everyone), --promote (move ticked discoveries into People). Trigger: /relationship-memory-weekly
---

# /relationship-memory-weekly

Once a week, the system learns from the inbox so the owner does not have to remember who they talked to, about what, and who is waiting on them.

Setup must have run first. If `~/.relationship-memory/people-data-map.md` or `config.json` is missing, stop and suggest `/relationship-memory-setup`.

## Rules

- **Mail is read-only.** No sending, deleting, moving, labeling or marking as read. With the Gmail connector, use only its search and read tools.
- **Owner columns are never written:** Name, Email, Other Emails, Company, Role / Title, Segment, Priority, Know Them?, Can Help With, Notes, **Next Step**. The script refuses to produce them; do not add them by hand either. Next Step holds the owner's own rules ("PAUSED", "No outreach", "No action until..."): read it, respect it, never write it.
- **Follow-up Cadence is set once.** The script proposes one only when it is blank, using the store's own option names when it is a select. Never overwrite a cadence that has a value.
- **Open Loops only grows.** New loops arrive as dated lines added to the existing text. Never delete or replace a loop.
- **Formulas are never written.** Warmth and Follow-up Status come back under `computed` in the changes file; they are for the report only.
- **Incremental means add, not replace.** See "How incremental runs work" below.
- **Suggestions are suggestions.** Suggested Can Help With is written only to its own column, and only for people whose Can Help With is blank. The owner accepts it by writing Can Help With in their own words.
- **New people are proposed, not added.** They go to Inbox Discoveries. Only a ticked Promote moves someone into People, and Know Them? stays blank.
- **Private stays private.** The report goes to the owner only. Never paste one person's Relationship Context or Open Loops into anything another person will see.
- **Dry run means nothing is written** to the store, the files or anywhere else except `~/.relationship-memory/reports/` and `exports/`.

## Modes

| Invocation | Behavior |
|---|---|
| `/relationship-memory-weekly` | Run, show the report, ask "Write these changes?" and write only on yes |
| `--dry-run` | Run, show the report, write nothing |
| `--apply` | Run and write history columns, suggestions and discoveries without asking (scheduled use) |
| `--full` | Recompute everyone from all the mail the source can see (first run, or after fixing an address) |
| `--promote` | Move ticked Inbox Discoveries rows into People, then stop |

## How incremental runs work

Every run after the first is incremental. For a person who has stored history and an Inbox Checked date, the script reads only mail dated after Inbox Checked (or after the stored Last Email, if later). It then:
- **adds** those messages to Emails Exchanged and Email Threads (never resets them);
- keeps the earlier **First Email**;
- sets Last Email From = **Them** only when the latest message is from one of their addresses with the owner in To, and **Me** only when the owner wrote to them. Mail they were only cc'd on, or that someone else sent, counts toward volume and never toward who wrote last, so it never creates a false "Reply owed";
- keeps **Relationship Context** word for word and adds a dated line for what is new;
- adds new **Open Loops** as dated lines, skipping duplicates;
- leaves anyone with no new mail untouched.

With `--full`, counts are recomputed from everything the source can see. Even then, a person with stored history is never zeroed because the run found no mail for them; the report lists them under "Stored history kept".

## Steps

### 1. Read the map

Read `~/.relationship-memory/people-data-map.md` and `config.json`. The People row tells you where the spine lives; feeder rows are used only to label new people. Read the store notes for that store in the setup skill's references (`../relationship-memory-setup/references/<store>.md`) if anything is unclear.

### 2. Export the spine

- **Excel or CSV**: nothing to export; use the file path.
- **Notion or Airtable**: read every People row through the connector, keep the row or page ID as `id`, and save all columns as JSON to `~/.relationship-memory/exports/people-<date>.json`. Export select values as their option names (a cadence of `Monthly` stays `Monthly`). Include Next Step, Open Loops and Relationship Context exactly as stored: the script needs them to merge rather than overwrite. In Notion, formula columns (Warmth, Follow-up Status) are unreadable and are not needed: the script recomputes them.
- **Google Sheets**: see `sheets-excel.md`.
- Export each feeder that has an Email column the same way (Name, Email only is enough).

### 3. Get the mail

- **IMAP**: nothing to do here; the script connects. Read the app password from the Keychain into `INBOX_PASSWORD` for the run only:
  `INBOX_PASSWORD="$(security find-generic-password -s relationship-memory-imap -a <user> -w)"`
- **.mbox**: check the file's date. If it is older than the last Inbox Checked, tell the owner a fresh export is needed and stop.
- **Gmail connector**: for each spine person with an email (and any Other Emails), search `from:<addr> OR to:<addr> OR cc:<addr>` (on the first run or with `--full`, all time; otherwise `after:<Inbox Checked>`), and read each thread's messages. Keep To and Cc separate in the JSON: the script needs them apart to tell who wrote to whom. Also search `in:sent after:<today minus 120 days>` and `in:inbox after:<same>` for discovery. Write every message once to `~/.relationship-memory/exports/messages-<date>.json` as `{"id","date":"YYYY-MM-DD","from","to","cc","subject","text"}` with the body trimmed to 700 characters. Read only; never open a draft or change a label.

### 4. Run the script (always a dry run first)

```
python3 ~/.relationship-memory/bin/inbox_enrich.py --config ~/.relationship-memory/config.json \
  --people <spine file or export> --feeder <feeder export> \
  <--mbox PATH | --imap-host HOST --imap-user USER | --messages-json PATH> \
  --me <addresses> --owner "<owner name>" --search-link <gmail|none> \
  --summarize --model <summary_model> \
  --out ~/.relationship-memory/exports/changes-<date>.json \
  --report ~/.relationship-memory/reports/weekly-<date>.md
```
`--config` supplies the owner's addresses, the cadence option names (when Follow-up Cadence is a select) and any column renames (`column_map`). Add `--full` if asked. The first run on a large spine takes a while: summaries run four at a time.

### 5. Show the owner the report

Lead with what needs a human:
1. **Replies owed** (they wrote last within 60 days), oldest first. If a person's Next Step holds an owner rule (PAUSED, No outreach, no action until...), show it beside their name and do not suggest writing to them.
2. **New people** worth promoting, with counts and last subject.
3. **Suggested Can Help With** lines to accept or ignore.
4. **Check these**: people matched by name only (no email on file), where a wrong match is possible.
Then one line of totals. Do not paste the whole diff unless asked.

If `--dry-run`: stop here and say nothing was written.

### 6. Write (on yes, or with `--apply`)

- **Excel or CSV**: rerun the same command with `--apply`. A backup goes to `_archive/` first.
- **Notion or Airtable**: from `changes-<date>.json`, write each `updates[].fields` to the row with that `id`, and nothing else. Never write `updates[].computed` (Warmth, Follow-up Status are formulas in the store). A column missing from `fields` means leave it alone, never clear it. Open Loops and Relationship Context arrive with the earlier text already included: write them as given. If a person appears under `kept_without_change`, write nothing for them. Then add each `new_people` entry to Inbox Discoveries unless its Email is already there. Follow the batch sizes and date formats in the store notes.
- After writing, read back three updated rows and confirm the values landed. Report any row that failed, by name.

### 7. Promote (when asked, or at the start of each run if Promote boxes are ticked)

- **Excel or CSV**: `inbox_enrich.py --people <file> --promote`.
- **Notion or Airtable**: each ticked Discoveries row becomes a People row (Name, Email, Notes "Added from inbox discovery <date>"), Know Them? blank. Remove it from Discoveries.
Then tell the owner who was promoted and that Know Them? is theirs to set.

### 8. Close

Save the report (the script already wrote it) and end with three lines: replies owed count, suggestions waiting, new people waiting. If any summaries failed, say how many and that the next run fills only the gaps.

## The learning loop (Getting to know → Yes)

For people marked `Getting to know`, the next follow-up the owner sends should carry one natural question that draws out what they do and who they know. When the reply arrives, the weekly run proposes a Suggested Can Help With from their own words. The owner approves it, writes Can Help With, and changes Know Them? to Yes. The automation never makes that change.
