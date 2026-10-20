# People Data Map

*The one place every tool looks to find out where people live. Update it whenever a table is added, moved or retired. Tools read this file; they never hard-code table IDs.*

Owner: <name>  ·  Store: <Notion | Airtable | Excel | Google Sheets | CSV>  ·  Updated: <YYYY-MM-DD>

## Where people live

| Table | Role | Location (ID, URL or file path) | Has Can Help With? | Warmth-sorted view | Links to People via |
|---|---|---|---|---|---|
| People | Spine | <data source ID / base+table ID / file path + sheet> | Yes | <view ID or "sort by Warmth"> | n/a |
| Inbox Discoveries | Review queue | <location> | No | n/a | Promote → new People row |
| <LinkedIn connections> | Feeder | <location> | <Yes/No> | <view or n/a> | <relation name, or "Email match"> |
| <Business cards> | Feeder | <location> | <Yes/No> | <view or n/a> | <relation name> |

## Inbox

Type: <IMAP host / .mbox path / Gmail connector>  ·  My addresses: <list>  ·  Folders: <default>

## Schedule

<Claude Code routine | launchd | cron | n8n>, <day and time>. Reports: `~/.relationship-memory/reports/`.

## Store notes

<Anything specific to this setup: for Notion, "Warmth is a formula; read the Warmest first view in order and treat row position as rank." For Airtable, "formula values are readable." For Excel, "close the workbook before a run.">

## Owner columns (never written by automation)

Name, Email, Other Emails, Company, Role / Title, Segment, Priority, Know Them?, Can Help With, Notes, Next Step. Follow-up Cadence once it has a value. Open Loops is append-only: the run adds dated lines and never removes one.
