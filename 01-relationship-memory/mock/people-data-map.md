# People Data Map (DEMO)

*Demo map for the invented people in this kit. Paths are relative to the kit folder. Tools read this file; they never hard-code tables.*

Owner: Alex Rivera (invented)  ·  Store: CSV  ·  Updated: 2026-10-01

## Where people live

| Table | Role | Location | Has Can Help With? | Warmth-sorted view | Links to People via |
|---|---|---|---|---|---|
| People | Spine | `mock/sample-run/people-spine-enriched.csv` | Yes | sort by Warmth (a number in this file) | n/a |
| Inbox Discoveries | Review queue | `mock/sample-run/people-spine-enriched-discoveries.csv` | No | n/a | Promote → new People row |
| LinkedIn connections | Feeder | `mock/linkedin-feeder.csv` | No | n/a | "In Spine" column, or Email/Name match |

## Inbox

Type: .mbox export (`mock/mock-inbox.mbox`)  ·  My addresses: alex@yourfirm.example

## Store notes

CSV: Warmth and Follow-up Status are values computed on the day of the run.

## Owner columns (never written by automation)

Name, Email, Other Emails, Company, Role / Title, Segment, Priority, Know Them?, Can Help With, Notes, Next Step. Follow-up Cadence once it has a value. Open Loops is append-only: the run adds dated lines and never removes one.
