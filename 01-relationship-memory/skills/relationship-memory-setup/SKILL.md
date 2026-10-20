---
name: relationship-memory-setup
description: Set up a Relationship Memory system in the user's own tools. Asks three questions at most (where their people live: Notion, Airtable, Google Sheets or Excel; which inbox: Gmail through a connector, IMAP, or an .mbox export; how the weekly run is scheduled: a Claude Code routine, cron/launchd, or n8n), proves the kit on invented demo data, creates the People, Inbox Discoveries and optional feeder columns and views in their store, writes their People Data Map, and runs the first dry run. Trigger: /relationship-memory-setup
---

# /relationship-memory-setup

Builds a memory of the user's relationships in the store they already use. Three parts: a **People** spine with history columns filled from email, a weekly learning run (`/relationship-memory-weekly`), and `/who-knows` to ask "who do I know who…".

Kit files this skill relies on (find the kit folder first: the folder holding `scripts/inbox_enrich.py` and `mock/`; ask the user for its path if it is not the current directory):
- `references/schema.md`: every column, type and formula rule. Read it before creating anything.
- `references/notion.md`, `references/airtable.md`, `references/sheets-excel.md`: store-specific steps and gotchas. Read only the one for the user's store.
- `references/people-data-map-template.md`: the map you will fill in.

## Rules

- **Read-only on mail, always.** Never send, delete, move, label or mark mail as read. The script opens IMAP folders read-only and fetches with BODY.PEEK.
- **Never handle the user's mail password.** For IMAP, the user stores an app password in the macOS Keychain themselves (step 5). Do not ask them to paste it into the chat.
- **Owner columns are the owner's.** Never write Can Help With, Know Them?, Notes, Segment, Priority or **Next Step** (the owner's own plan or rule, such as "PAUSED" or "No outreach"). A Follow-up Cadence the owner set is never replaced. Can Help With may get a *Suggested* line next to it, never an edit. Open Loops is append-only.
- **Demo first.** Prove the kit on `mock/` before touching real data.
- **Add, don't rebuild.** If the user already has a people table, add the missing columns to it. Never delete or rename their existing columns.
- **One question at a time**, three at most. Each answer shapes the next.

## Steps

### 1. Interview (three questions, one at a time)

1. "Where do your people live today: **Notion, Airtable, Google Sheets or Excel**? Is there an existing table I should add columns to, or should I create a new one?" (If the answer names more than one place, the busiest becomes the spine and the others become feeders.)
2. "Which inbox should it learn from: **Gmail or Google Workspace through the Gmail connector**, **any mailbox over IMAP** (Gmail, Microsoft 365, iCloud, Fastmail), or **an exported .mbox file**? And which addresses are yours?" (Microsoft 365 tenants usually block password IMAP; offer IMAP with an OAuth token or an .mbox export.)
3. "How should the weekly run be scheduled: **a Claude Code scheduled routine**, **cron or launchd on this Mac**, or **n8n**? Which day and time?"

Restate the plan in one line and get a yes before building.

### 2. Check the machine

- `python3 --version` (3.9+) and `python3 -c "import openpyxl"` (install with `pip3 install openpyxl` if missing; only needed for Excel).
- `claude --version` (the summaries call `claude -p`).
- For Notion or Airtable: confirm the connector is available in this session by listing its tools. If it is not, stop and tell the user how to add it (Claude Code: `/mcp`).

### 3. Prove it on the demo data (two minutes)

```
python3 scripts/inbox_enrich.py --people mock/people-spine.csv --feeder mock/linkedin-feeder.csv \
  --mbox mock/mock-inbox.mbox --me alex@yourfirm.example --search-link gmail
```
Expect about 29 people updated, 9 replies owed and 3 new people (Gideon Ashcombe, Tobias Kettering, Marguerite Lowell). Show the user the summary lines, not the whole report. Everyone in the demo is invented.

### 4. Create the store

Create `~/.relationship-memory/` with `bin/`, `exports/` and `reports/`, and copy `scripts/inbox_enrich.py` into `bin/`. (Optional proof the copy is sound: `python3 -m unittest discover -s scripts/tests` from the kit folder; every test should pass.)

Then follow the store file:
- **Notion** (`references/notion.md`): under one parent page the connector can see, create People (or add the columns to their existing table), Inbox Discoveries, and the formulas and views. Add any feeder relation *after* both tables exist.
- **Airtable** (`references/airtable.md`): create the plain fields with the connector, then hand the user the three formulas and five views to add by hand. Formula fields and views cannot be created through the API.
- **Excel** (`references/sheets-excel.md`): copy `mock/People.xlsx` to where the user wants it, clear the demo rows, or point at their workbook. The script adds missing columns on the first `--apply`.
- **Google Sheets**: explain the two routes in `references/sheets-excel.md` and let the user pick.

Do not import or invent any people. The user brings their own (a LinkedIn connections export, a contacts export, or rows typed by hand). Offer to load a CSV they provide.

### 5. Connect the inbox

- **IMAP**: the user creates an app password with their provider, then stores it themselves. Ask them to run this in their own terminal (in Claude Code they can prefix it with `!`):
  `security add-generic-password -s relationship-memory-imap -a <their address> -w`
  It prompts for the password without echoing it. The scheduler reads it from the Keychain at run time.
- **Microsoft 365 with OAuth**: the script accepts `--imap-oauth-env NAME`, the name of an environment variable holding an access token with the IMAP.AccessAsUser.All scope. Getting that token is the tenant admin's job; say so plainly.
- **.mbox**: record the path. Remind them that an export is a snapshot; a weekly run needs a fresh export each week, so IMAP is better for the schedule.
- **Gmail connector**: no password. The weekly skill pulls messages through the connector and writes them to a JSON file for the script (`--messages-json`). Slower on big inboxes; fine for a spine of a few hundred.

### 6. Write the People Data Map

Fill `references/people-data-map-template.md` and save it as `~/.relationship-memory/people-data-map.md`, plus `~/.relationship-memory/config.json`:
```json
{"owner_name": "", "my_addresses": [], "store": "notion|airtable|excel|sheets|csv",
 "inbox": {"type": "imap|mbox|gmail-connector", "host": "", "user": "", "folders": [], "mbox_path": "",
           "keychain_service": "relationship-memory-imap", "oauth_env": ""},
 "search_link": "gmail|none", "summary_model": "sonnet", "schedule": {"how": "", "when": ""},
 "follow_up_cadence_options": {"Every 2 weeks": 14, "Monthly": 30, "Every 6 weeks": 42, "Quarterly": 90, "Twice a year": 182},
 "column_map": {}}
```
Keep `follow_up_cadence_options` only if Follow-up Cadence is a select in their store (drop it when it is a number of days). Use `column_map` when their existing table names a kit column differently, for example `{"Mail Search Link": "Gmail History"}`. The weekly run passes this file to the script with `--config`.
For Notion, also create a "People Data Map" page with the same table, so the user can see it in Notion. The local file stays the one the tools read.

### 7. First real run, dry

Run `/relationship-memory-weekly --dry-run --full`. Walk the user through the report: replies owed, suggested Can Help With lines, new people. Nothing is written. Then ask whether to apply.

### 8. Schedule it

Use `scripts/scheduler/SCHEDULING.md`: a Claude Code routine, the launchd template, a crontab line, or an n8n Schedule Trigger. The scheduled run applies history columns only; suggestions and new people wait in the store for the owner.

### 9. Hand over

Tell the user, in plain words:
- the one weekly habit: open "Suggestions to review" and "Inbox Discoveries", accept or ignore, and write **Can Help With** for the warmest people first (view "Write Can Help With");
- how to ask: `/who-knows <the ask>`, and `/who-knows --intros` for introductions;
- where the map and reports live (`~/.relationship-memory/`).
