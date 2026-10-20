# Relationship Memory: the schema

Every store (Notion, Airtable, Google Sheets, Excel) gets the same column names, so the three skills and `inbox_enrich.py` work unchanged. Use these names exactly. Store-specific types and formulas are in `notion.md`, `airtable.md` and `sheets-excel.md`.

## The tables

| Table | Role | Required? |
|---|---|---|
| **People** (the spine) | One row per person you actually have a relationship with. Every tool reads this first. | Yes |
| **Inbox Discoveries** | New people the weekly run found (2+ emails each way, not in People). Tick **Promote** to move one into People. | Yes |
| Feeder tables (LinkedIn connections, business cards, prospects, event lists) | Wider lists. Used for unvetted leads and introducer paths. A feeder row can link to its People row. | Optional |

The **People Data Map** (`~/.relationship-memory/people-data-map.md`) lists every table, where it lives, and its role. Tools read the map; they never hard-code table IDs.

## People: owner columns (the automation never writes these)

| Column | Type | Notes |
|---|---|---|
| Name | title / text | |
| Email | email / text | Several addresses allowed, separated by `;` |
| Company | text | |
| Role / Title | text | |
| Segment | select | Your own groups. Defaults: Client, Partner, Prospect, Peer, Investor, Vendor, Not a Fit |
| Priority | select | A, B, C. Sets the default follow-up cadence (A 30 days, B 60, C 90) |
| **Know Them?** | select | `Yes` (can be suggested) · `Getting to know` (never suggested; the next follow-up asks one natural question about what they do) · `No` (never suggested, never "reply owed") |
| **Can Help With** | long text | **Written by the owner, in the owner's words.** The automation never writes, edits or "fixes" it. |
| Notes | long text | Private. Never quoted to anyone else. |
| **Next Step** | text | **The owner's.** Your plan or rule for this person: "Send the proposal Friday", "PAUSED", "No outreach", "No action until January". The automation never writes it, and other tools (who-knows, follow-up views) respect what it says. |
| Other Emails | text (optional) | Extra addresses for the same person, `;`-separated. Mail from any of them counts as theirs. |

## People: history columns (written by the weekly run)

| Column | Type | How it is filled |
|---|---|---|
| Emails Exchanged | number | Messages between you and this person (any direction, To or Cc). Incremental runs add to it. |
| Email Threads | number | Distinct subjects, ignoring Re:/Fwd:. Incremental runs add new subjects only (approximate). |
| First Email | date | Set once. An incremental run never moves it. |
| Last Email | date | The last message between the two of you (one of you writing to the other). Mail they were only copied on counts toward volume, not here. |
| Last Email From | select | `Them` only when the latest message is from one of their addresses with you in To. `Me` only when it is from you with them in To. Cc-only and third-party mail never set it. `No email yet` when there is none. |
| Relationship Context | long text | 2 to 3 sentences from Claude: how it started, what you talked about, what you worked on. Once written, later runs keep every word and add a dated line for what is new. |
| Open Loops | long text | **Append-only.** Each new loop is added on its own line with a date prefix (`2026-10-02: ...`). Duplicates are skipped. Nothing is ever deleted or replaced; clear a loop yourself when it closes. |
| Follow-up Cadence | number (days) or select | Written only when blank; a value you set is never replaced. Priority default, tightened to your natural rhythm, never under 14. As a select, use these option names: `Every 2 weeks` (14), `Monthly` (30), `Every 6 weeks` (42), `Quarterly` (90), `Twice a year` (182), and record them in `config.json` (see below). |
| Inbox Checked | date | Last time the run looked. The next run only re-reads people with mail since this date. |
| Mail Search Link | url | Opens the whole history in your mail client (Gmail; blank where the client has no search link) |
| **Suggested Can Help With** | long text | Claude's proposal from the emails. The owner accepts it by copying it into Can Help With, in their own words. |

## How the weekly run updates history (incremental mode)

The weekly run is incremental. For anyone who already has history and an Inbox Checked date, it reads only mail dated after Inbox Checked (or after the stored Last Email, if that is later), and:

- **adds** the new messages to Emails Exchanged and Email Threads, never resets them;
- keeps the earlier **First Email**;
- moves Last Email and Last Email From only when one of you wrote to the other;
- keeps **Relationship Context** and adds a dated line for what is new;
- **appends** to Open Loops;
- leaves anyone with no new mail exactly as they were.

`--full` recomputes everyone from all the mail the source can see. Use it for the first run, or after fixing a wrong email address. Even then, a person whose stored history is not zero is never zeroed because a run found no mail for them.

## People: computed columns (formulas in the store)

| Column | Rule |
|---|---|
| **Warmth** (0-100) | Volume `min(40, Emails Exchanged × 4)` + Recency `max(0, 40 − days since Last Email ÷ 9)` + `20` if Last Email From = Them. Rounded. |
| Warm Enough to Ask | `Yes` when Warmth ≥ 35, else `No`. A text helper, because some stores cannot filter a view on a formula number. |
| Follow-up Status | In this order: `No email history` (no Last Email) · `Reply owed` (they wrote last, within 60 days, and Know Them? is not No) · `Dormant` (silent more than 3 × cadence) · `Overdue` (Last Email + cadence has passed) · `Due soon` (due within 14 days) · `On track` |
| Next Follow-up | Last Email + Follow-up Cadence (optional, for calendar views) |

`inbox_enrich.py` computes Warmth and Follow-up Status itself too (for reports and the CSV route). In `--out` they sit under `computed`, apart from `fields`, and are never written to Notion or Airtable. If you change the formula in the store, change `warmth()` and `follow_up_status()` in the script to match.

## Inbox Discoveries

| Column | Type |
|---|---|
| Name | title / text |
| Email | email / text |
| Promote | checkbox (CSV/Excel: type `yes` or `x`) |
| Sent / Received | number, number |
| First Email / Last Email | date |
| Last Subject | text |
| Also In | text (for example "LinkedIn feeder") |
| Found On | date |

Promoting creates a People row with Name, Email and a note "Added from inbox discovery <date>". **Know Them?** stays blank: the owner decides.

## Feeder tables (minimum)

Name, Company, Role / Title, Email (if known), a profile link if there is one, Last Message Date (if the source has one), and optionally a relation to People and its own Can Help With. who-knows uses feeders only for unvetted leads (at most 3, whole-word matching, always with the last-message date) and for introducer paths.

## config.json settings the script reads (`--config`)

| Key | Example | Use |
|---|---|---|
| `my_addresses`, `owner_name`, `search_link`, `summary_model` | | Same as the command-line flags |
| `follow_up_cadence_options` | `{"Every 2 weeks": 14, "Monthly": 30, "Every 6 weeks": 42, "Quarterly": 90, "Twice a year": 182}` | Follow-up Cadence is a select: proposals use these option names, and the labels are read back as days |
| `column_map` | `{"Mail Search Link": "Gmail History"}` | Your table names a kit column differently |

Either key can sit at the top of `config.json` or inside the store's section (for example `"notion": {...}`).

## Select option names

No commas inside an option name (Notion splits on them). Keep the exact spellings above: `Yes`, `Getting to know`, `No`, `Me`, `Them`, `No email yet`.
