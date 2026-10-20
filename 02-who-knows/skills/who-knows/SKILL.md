---
name: who-knows
description: Answer "Who do I know who…?" from the owner's own people tables, and (with --intros) find introductions worth making. Reads the People Data Map to find the tables, matches the ask against Can Help With entries the owner wrote (meaning, not keywords), suggests only people marked Know Them? = Yes, ranks warmest first, quotes the owner's own words, adds timing nudges, introducers, a "Not yet" section, up to three unvetted feeder leads, and the gaps. --intros matches one person's needs against everyone else's Can Help With and drafts double-opt-in notes, one side at a time. Read-only. Works on a full Relationship Memory setup or on a simple starter table with no email history. Trigger: /who-knows <the ask> | /who-knows --intros [name] | /who-knows --map <path> <the ask>
---

# /who-knows

A good answer is **warmest first**, carries **the real why in the owner's words**, shows **who could introduce them**, and lists **only people the owner would actually ask**.

## Rules

- **Read-only.** This skill never writes to any table, and never sends anything. Drafts are shown to the owner, nothing more.
- **Can Help With is the owner's voice.** Quote it; never paraphrase it into a claim the owner did not make; never fill it in. If an entry looks like a dictation slip, flag it, don't fix it. Suggested Can Help With is *not* the owner's voice and is never used as a reason to suggest someone.
- **Know Them? decides who can be an answer:**
  - `Yes`: can be an answer.
  - `Getting to know`: never an answer. May appear in "Not yet" with one question to ask in the next follow-up.
  - `No`: never shown.
  - Blank: not decided yet. Not an answer.
- **No match is a valid answer.** Say so plainly and name the gap. Never stretch a weak match to fill the list.
- **Confidentiality.** Output stays with the owner. Never draft anything to one person that reveals another person's Relationship Context, Open Loops or Notes.
- **Next Step is the owner's rule.** If it says PAUSED, No outreach, or no action until a date, the person may still be named as an answer, but never draft a note to them or propose them for an introduction; show the rule beside their name.

## 1. Read the map

Read `~/.relationship-memory/people-data-map.md`. If the ask starts with `--map <path>`, read that file instead (this is how the demo runs without touching your own map). Relative paths inside a map resolve from the map's own folder. Every table in "Where people live" is a candidate; answers come only from tables with a Can Help With column. Feeders without it supply unvetted leads and introducer paths only. If the map is missing, stop and point the owner to `README-FIRST.md` in this drop (the fifteen-minute starter) or to `/relationship-memory-setup` if they have the full kit.

## 2. Pull the rows, warmest first

Keep for each row: Name, Know Them?, Can Help With, Role / Title, Company, Relationship Context, Open Loops, Next Step, Last Email, Last Email From, Follow-up Status, Mail Search Link, and any link to a feeder or spine row.

How to get the warmth order depends on the store (see the map's store notes):
- **Notion**: Warmth is a formula and **cannot be read through the API**. Read the "Warmest first" view in order and treat **row position as the rank** (1 = warmest). Page through until there are no more rows.
- **Airtable, Excel, CSV, Google Sheets**: read Warmth directly and sort descending.
- If Warmth is missing anywhere, compute it: `min(40, Emails Exchanged × 4) + max(0, 40 − days since Last Email ÷ 9) + (20 if Last Email From = Them)`.

**Starter tables (no email history).** If the table has no Warmth, Emails Exchanged or Last Email columns, do not compute warmth and never call anyone "cooler". Rank by Priority (A, B, C, then blank), then by the order the owner listed them, and show `priority <A/B/C>` where the warmth rank would go. Leave out the last-email part of the answer line and the timing nudges that depend on email. Once, at the end, mention that the full Relationship Memory kit adds warmth from the owner's inbox.

Warm enough to ask = Warmth 35 or more. People under 35 can still be answers, but say "cooler; re-warm before asking".

## 3. Match (forward mode)

Read the ask, then read every eligible row's **Can Help With** first. Use Role / Title and Relationship Context only as support. Match on meaning: "someone who can sort out our books before a bank meeting" matches "Fractional CFO work … getting ready for a bank loan".

- **Strong**: Can Help With says it directly.
- **Partial**: adjacent, or only Role / Context supports it.
- Drop anything weaker.

**Introducers.** Some people are a path, not the answer. Look for Can Help With entries about connecting people ("makes introductions generously"), Relationship Context that records who introduced whom, and community or event hosts.

**Not yet.** If a `Getting to know` person's Role or Context suggests they might fit, note them with one natural question for the next follow-up.

**Unvetted leads from feeders** (rows without Can Help With): a keyword pass over Name, Company and Role / Title.
- **Whole words only.** A substring match on "ETA" (search fund) also hits "Meta". Use word boundaries.
- **Show at most 3**, labeled unvetted.
- **Always show the last-message date.** An old warm score overstates people who have been silent for years.
- If a feeder row is linked to (or matches by email) a People row, use the People row instead.

## 4. Rank

Strong before Partial; within each, warmest first. Then two timing nudges that move a person up without changing their tier:
- **Reply owed** (they wrote last, recently): "you owe them a reply; ask inside that reply."
- **Open loop pending**: mention it, so the ask doesn't land on top of an unanswered thread.

## 5. Answer in this shape (forward mode)

```
WHO KNOWS: <the ask in one line>

Ask these
1. <Name>, <Role> at <Company> · Strong · warmth #<rank> of <N> (<score if readable>) · last email <date> (<Me/Them>)
   Why: "<owner's Can Help With, quoted, trimmed to the relevant clause>"
   Timing: <reply owed / open loop: … / nothing pending>
   <Mail Search Link>
(at most 5)

Could introduce you
- <Name>: <why they are a path, one line>

Not yet (getting to know)
- <Name>: might fit because <Role/Context>. Next follow-up, ask: "<one natural question>"

Worth a look (unvetted, from <feeder>)
- <Name>, <Role> at <Company>, last message <date>. Write their Can Help With if they belong in answers.

Gaps: <what the network does not cover>
```
Leave out empty sections. If nothing is Strong, start with "No strong match" before any Partials.

## 6. Introductions mode (`--intros [name]`)

The reverse question: **who in my network should meet whom?**

1. **Pick the people with needs.** With a name: that person only. Without: every `Know Them? = Yes` person whose Open Loops, Next Step or Relationship Context (last 90 days) states a need: a hire, a referral, an advisor, capital, a customer.
2. **State each need in one line, privately**, from those columns. This line is for the owner only.
3. **Match the need against everyone else's Can Help With** (Know Them? = Yes, not the same person), exactly as in forward mode: Strong or Partial, warmest first.
4. **Propose at most 3 introductions per run**, best first. For each:
   ```
   INTRO: <Person with the need> ↔ <Person who can help>
   Need (private, for you): <one line>
   Why them: "<helper's Can Help With, quoted>"
   Warmth: <both ranks>; timing: <reply owed / open loop>
   ```
5. **Draft double-opt-in notes, one side at a time, in the owner's voice:**
   - **First, to the person with the need.** Offer the intro, describe the helper only by what is public (role, company, what they do), and ask: would you like the introduction, and what are you comfortable with me sharing?
   - **Second, to the helper, only after the first person says yes.** Ask whether they are open to it, sharing only what the first person approved. No private context, no quotes from email, nothing from Notes.
   - Never send both at once, never cc both on a first note, and never put one person's Relationship Context, Open Loops or Notes in the other's draft.
6. If a match depends on a reply the owner owes, say so: the intro offer can go inside that reply.

## 7. If the ask is standing

If the need will last (a hire, a partner, an investor), offer to note it in whatever list the owner keeps for open asks. Write nothing without a yes.
