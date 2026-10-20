# Store notes: Notion

Use the Notion connector (MCP) in Claude Code. Column names and meanings are in `schema.md`; this file covers only what is different about Notion.

## Gotchas we learned the hard way

1. **Formula values cannot be read through the Notion API or MCP.** A row read returns an opaque formula reference, not the number, and SQL-style queries cannot see it either. So:
   - Build a view **sorted by Warmth, descending** ("Warmest first"). Read the view in order and **treat row position as the warmth rank** (1 = warmest).
   - Never try to read Warmth or Follow-up Status as numbers or text. When a skill needs the value, it recomputes it from Emails Exchanged, Last Email, Last Email From and Follow-up Cadence with the rule in `schema.md`.
2. **Views cannot filter a formula numerically.** That is why the schema has the text helper **Warm Enough to Ask** (`Yes`/`No`). Filter on that, not on Warmth ≥ 35.
3. **Select option names cannot contain commas.** Notion splits on them. Keep `Getting to know`, never "Getting to know, maybe".
4. **Add relations after the tables exist.** Creating a relation inline while creating a database fails often. Create People and the feeder first, then add the relation with an *update* on the existing data source.
5. **Databases hold data sources.** Writes target the data source (its address starts with `collection:` followed by an ID), not the database page. Record both in the People Data Map.
6. **The connector only sees pages shared with it.** Create everything under one parent page the connector can reach.
7. **Dates go in as plain ISO dates** (`2026-09-14`). Some connector versions want expanded keys such as `date:Last Email:start` plus `date:Last Email:is_datetime: 0`. Read the tool's schema before the first write.
8. **Go slowly.** Notion allows about three requests a second. Update in batches and pause between them on large runs.

## Property types

| Column | Notion type |
|---|---|
| Name | Title |
| Email | Email (one address) or Text (several, `;`-separated) |
| Company, Role / Title, Next Step | Text (Next Step is an owner column) |
| Segment, Priority, Know Them?, Last Email From | Select |
| Can Help With, Notes, Relationship Context, Open Loops, Suggested Can Help With | Text |
| Emails Exchanged, Email Threads | Number |
| Follow-up Cadence | Number (days), or Select with `Every 2 weeks`, `Monthly`, `Every 6 weeks`, `Quarterly`, `Twice a year` (record the options in `config.json`; see `schema.md`) |
| First Email, Last Email, Inbox Checked | Date |
| Mail Search Link | URL |
| Warmth, Warm Enough to Ask, Follow-up Status | Formula |

## Formulas (Notion formula syntax)

**Warmth**
```
if(empty(prop("Emails Exchanged")) or prop("Emails Exchanged") == 0, 0,
  round(min(40, prop("Emails Exchanged") * 4)
    + if(empty(prop("Last Email")), 0, max(0, 40 - dateBetween(now(), prop("Last Email"), "days") / 9))
    + if(prop("Last Email From") == "Them", 20, 0)))
```

**Warm Enough to Ask**
```
if(prop("Warmth") >= 35, "Yes", "No")
```

**Follow-up Status**
```
lets(d, dateBetween(now(), prop("Last Email"), "days"),
     c, if(empty(prop("Follow-up Cadence")), 90, prop("Follow-up Cadence")),
  if(empty(prop("Last Email")), "No email history",
  if(prop("Last Email From") == "Them" and d <= 60 and prop("Know Them?") != "No", "Reply owed",
  if(d > 3 * c, "Dormant",
  if(d > c, "Overdue",
  if(c - d <= 14, "Due soon", "On track"))))))
```

If Follow-up Cadence is a Select, replace the `c` line with:
```
     c, ifs(prop("Follow-up Cadence") == "Every 2 weeks", 14, prop("Follow-up Cadence") == "Monthly", 30,
            prop("Follow-up Cadence") == "Every 6 weeks", 42, prop("Follow-up Cadence") == "Twice a year", 182, 90),
```

If the connector will not create a formula property, create the column as Text, then ask the owner to change its type to Formula and paste the formula (two minutes in the Notion UI).

## Views to create on People

| View | Filter | Sort |
|---|---|---|
| Warmest first | Know Them? = Yes | Warmth descending |
| Write Can Help With | Know Them? = Yes and Can Help With is empty | Warmth descending |
| Follow up now | Follow-up Status is Reply owed, Overdue or Due soon | Last Email ascending |
| Suggestions to review | Suggested Can Help With is not empty | Warmth descending |
| Getting to know | Know Them? = Getting to know | Last Email descending |

On **Inbox Discoveries**: a "To review" view (Promote unchecked, Last Email descending).

## Reading and writing in the weekly run

- **Export the spine** by reading the "Warmest first" view and an unfiltered view (for people who are not Yes), keeping each page ID. Save as JSON with an `id` column, then pass it to `inbox_enrich.py --people`.
- **Write back** by page ID from the `updates` list in `changes.json`. Write only the keys in `fields`; the script guarantees none of them is an owner column. Never write anything under `computed` (Warmth, Follow-up Status): they are formulas in Notion and recalculate on their own.
- **Never write Next Step, Can Help With, Know Them?, Notes, or any column not in `fields`.** Next Step holds the owner's own rules ("PAUSED", "No outreach", "No action until..."), and other tools read them.
- **A key that is missing from `fields` means "leave it alone"**, never "clear it". On an incremental run the script leaves out First Email, and often Relationship Context, Last Email and Last Email From, on purpose.
- **Open Loops and Relationship Context arrive complete.** The value in `fields` already holds every earlier line plus the new dated one; write it as given, and never write a shorter value over a longer one.
- **Follow-up Cadence** appears only when the stored value was blank, already as one of the select's option names.
- If a column has a different name in your table (for example "Gmail History" for Mail Search Link), put it in `column_map` in `config.json`; the script reads and writes the store's name.
- **New people** go into Inbox Discoveries as new pages. Before adding, check by Email that the row is not already there.
- **Promote**: for each Discoveries row with Promote ticked, create a People page (Name, Email, Notes "Added from inbox discovery <date>"), leave Know Them? blank, then delete the Discoveries row or untick it and add "Promoted" to its title.
