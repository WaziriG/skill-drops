# Store notes: Airtable

Use the Airtable connector (MCP) in Claude Code. Column names and meanings are in `schema.md`; this file covers only what is different about Airtable.

## Gotchas

1. **Formula fields and views cannot be created through the API.** Create the plain fields with the connector, then give the owner the three formulas below to paste (Field type → Formula) and the view list to click together. Budget five minutes for this.
2. **Formula values can be read** through the API, unlike Notion. Read Warmth directly and sort on it.
3. **Write at most 10 records per request**, about 5 requests a second.
4. **New select options need `typecast: true`** on the write, or the write fails when the run sets a value the field has not seen.
5. **Select option names: no commas.** Not an Airtable limit, but the kit keeps one rule across stores.
6. **Linked records**: a feeder table links to People with a "Link to another record" field. Create both tables first, then add the link field.
7. **Next Step is the owner's** (the run never writes it), and **Open Loops is append-only**: write the value from `fields` as given, since it already holds the earlier lines. Write only `fields`, never `computed`.
8. If Follow-up Cadence is a single select, record its options in `config.json` (`follow_up_cadence_options`); the run proposes a cadence only when the field is blank.
9. A personal access token, if you use one outside the connector, needs `data.records:read`, `data.records:write` and `schema.bases:read`, scoped to this one base.

## Field types

| Column | Airtable type |
|---|---|
| Name | Single line text (primary field) |
| Email | Email (one address) or Single line text (several) |
| Company, Role / Title, Next Step | Single line text |
| Segment, Priority, Know Them?, Last Email From | Single select |
| Can Help With, Notes, Relationship Context, Open Loops, Suggested Can Help With | Long text |
| Emails Exchanged, Email Threads, Follow-up Cadence | Number (integer) |
| First Email, Last Email, Inbox Checked | Date (ISO) |
| Mail Search Link | URL |
| Warmth, Warm Enough to Ask, Follow-up Status | Formula |

## Formulas (paste as written)

**Warmth**
```
IF({Emails Exchanged},
  ROUND(MIN(40, {Emails Exchanged} * 4)
    + IF({Last Email}, MAX(0, 40 - DATETIME_DIFF(TODAY(), {Last Email}, 'days') / 9), 0)
    + IF({Last Email From} = "Them", 20, 0), 0),
  0)
```

**Warm Enough to Ask**
```
IF({Warmth} >= 35, "Yes", "No")
```

**Follow-up Status**
```
IF(NOT({Last Email}), "No email history",
IF(AND({Last Email From} = "Them", DATETIME_DIFF(TODAY(), {Last Email}, 'days') <= 60, {Know Them?} != "No"), "Reply owed",
IF(DATETIME_DIFF(TODAY(), {Last Email}, 'days') > 3 * IF({Follow-up Cadence}, {Follow-up Cadence}, 90), "Dormant",
IF(DATETIME_DIFF(TODAY(), {Last Email}, 'days') > IF({Follow-up Cadence}, {Follow-up Cadence}, 90), "Overdue",
IF(IF({Follow-up Cadence}, {Follow-up Cadence}, 90) - DATETIME_DIFF(TODAY(), {Last Email}, 'days') <= 14, "Due soon", "On track")))))
```

## Views (create by hand)

Same five as Notion: Warmest first, Write Can Help With, Follow up now, Suggestions to review, Getting to know. On Inbox Discoveries: To review (Promote unchecked).

## Reading and writing in the weekly run

- **Export the spine** with the connector's list-records tool (all fields, every page of results), keep each record ID as `id`, save as JSON and pass it to `inbox_enrich.py --people`.
- **Write back** by record ID from `changes.json`, 10 at a time, `typecast: true`. Skip Warmth and Follow-up Status (formulas).
- **New people**: create rows in Inbox Discoveries, skipping any Email already there.
- **Promote**: ticked Discoveries rows become People rows (Name, Email, Notes), Know Them? left blank; then delete the Discoveries row.
