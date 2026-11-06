---
name: nurture-starter
description: A small, hand-run prospect nurture system. Sets up a short list of the people you want to stay close to (in a CSV, Excel, Google Sheets, Airtable or Notion), then, whenever you paste in public news about them (an announcement, a post, a job change), decides whether it is a real reason to write, drafts one value-first note per person for you to review, and logs it. Never sends anything, never opens LinkedIn, never asks for keys or passwords. Use when someone says "set up my prospect list", "who should I reach out to", "draft a touch for", "here's some news about my prospects", or "who's due". Trigger: /nurture-starter
---

# /nurture-starter

Long sales cycles are lost in the quiet stretches. The person you met in spring is in the middle of something big by autumn: a new location, a new hire, a new boss. If you say nothing, it reads as indifference. If you send "just checking in", it reads as need. What works is a short note, sent when something real has happened, that gives them something before it asks for anything.

This skill does the thinking part of that by hand, with you in the loop every time:

1. **Setup**: a short list of people, with the few fields that decide whether a note is any good.
2. **Run**: you paste in what you have seen about them. It decides who has a real reason for a note today, drafts one note per person, and shows you all of it before anything is saved.
3. **Log**: after you approve, it records the touch and sets the next date.

## The rules (never broken, whatever the user asks)

- **Never send anything.** No email, no message, no post, no connection request. The user copies the note and sends it themselves.
- **Never open LinkedIn**, log in to anything, or use anyone's session or cookies. If the user pastes a LinkedIn link, ask them to paste the text of the post instead.
- **Never search for people on your own.** Work only from what the user pastes. If they paste a link to a public news page and ask you to read it, you may read that one page.
- **Never ask for an API key, password or token.** If the user has already connected Notion, Airtable or Google Sheets to Claude, you may use that connection, and you ask before every write.
- **Never invent.** No made-up news, quotes, dates, meetings, prices, offers or promises. If a note needs something the user has not given you (a link, a date, an attachment), ask for it, or leave the note out.
- **Silence beats a weak reason.** "No note today" is a good result. Say why in one line.

## Usage

```
/nurture-starter setup     # first time: build the list
/nurture-starter           # paste in news about your people; get drafts to review
/nurture-starter due       # who is due a note, even without news
/nurture-starter log       # record what you actually sent, and any replies
```

---

## Setup

Ask **one question at a time**, three at most.

1. **"Where do you want to keep the list? A CSV file in this folder (the simplest), Excel, Google Sheets, Airtable or Notion."** If they are unsure, recommend the CSV. It works everywhere and can be imported into any of the others later.
2. **"Who are the first five to ten people you want to stay close to?"** Name, organization and role are enough to start. Fewer is better than more. Ten people watched well beats fifty watched badly.
3. **"For each one: why are you watching them, and what could you give them that they would value?"** Help them make each answer specific. "Potential client" is too vague. "Opening a second office next year; we cleaned their first one" is usable. These two fields decide the quality of every draft, so spend the time here.

Then build the list with these columns, in this order:

| Column | What goes in it |
|---|---|
| Name | The person |
| Organization | Where they work. Used to check that news is about the right person. |
| Role | Their job title |
| Relationship | Prospect, Past customer, Referral source or Ally |
| Stage | Aware, Talking, Proposal out, Deciding, Customer or Not now |
| Why I'm watching | One or two specific sentences, in the user's words |
| What I can give | Something useful to them: a checklist, an introduction, a short how-to, an article you wrote, a lesson you learned |
| Last touch | Date of the last note the user actually sent |
| Last touch summary | One line: what it said |
| Next touch | The date they are next due a note |
| Notes | Anything else |

And a second table, **Touch log**:

| Column | What goes in it |
|---|---|
| Date | When the draft was made |
| Name | Who it is for |
| Signal | What happened, in one line, with the source and its date |
| Why now | Why this is a real reason to write today |
| Channel | Email, LinkedIn message, Text or Phone |
| Draft | The note |
| Status | Draft, Sent, Edited and sent, or Skipped |
| Reply | What came back, if anything |

**How to build it in each store:**

- **CSV** (default): copy `templates/prospects.csv` and `templates/touch-log.csv` from this skill's folder into a `nurture/` folder where the user is working, then add their people to `nurture/prospects.csv`.
- **Excel**: do the CSV steps, then tell the user to open the files in Excel. If they save as `.xlsx`, you can only read and update it if Python with `openpyxl` is available; otherwise ask them to keep it saved as CSV.
- **Google Sheets**: make the CSVs, then tell them: File, Import, Upload, one tab each. On later runs, either use their connected Google Sheets (if they have one) or ask them to paste the rows, and give back the new rows ready to paste.
- **Airtable**: make the CSVs, then tell them: add a table, choose "Import a CSV". Set Stage and Relationship to single select, and the three date columns to date.
- **Notion**: make the CSVs, then tell them: Import, CSV, which creates a database. Set the same field types. If Notion is already connected to Claude, offer to create the database there instead, and ask before writing.

Finish with: the file paths or table names, the number of people, and which rows still have a vague **Why I'm watching** or an empty **What I can give**. Those rows will produce weak notes until they are filled.

---

## Run (the main job)

The user pastes whatever they have seen: news headlines, the text of a post, a note that someone changed jobs, a line from a newsletter. Messy is fine. One line per item is ideal: `Name: what happened (source, date)`.

### Step 1: Read the list and the log

Load the prospect list and the touch log. If you cannot find them, ask where they are, or run setup.

### Step 2: Check every signal before you use it

For each pasted item, in order, and stop at the first failure:

1. **Is it the right person?** Match on name **and** organization or city. A name alone is not enough: the same name turns up on strangers' news. If you cannot tell, mark it "Check: may be someone else" and draft nothing.
2. **Is it recent?** It should be from the last 30 days. Old pages often look new. If there is no date, ask. If it is older, no note, and say how old.
3. **Is it about them, or just near them?** A company award they had nothing to do with is weak. A move, a launch, a hire, a new role, a published opinion, a problem they named in public: those are real.
4. **Is there already an open draft for them?** If the touch log has a Draft for this person that was never sent or skipped, do not write another. Point to the existing one.
5. **Did they just hear from the user?** If Last touch is inside the last 14 days, a new note needs a strong reason. Say so.
6. **Is this the right moment?** If the post is about a loss, a layoff, a complaint or a hard week, a sales note reads as opportunistic. Suggest a plain human word or nothing at all. The one exception: for a past customer, a plain offer to help with the exact thing you already do for them is fine. No pitch, no prices, two or three lines.

### Step 3: Draft one note per person who passes

At most one note per person per run. Each note:

- **Opens with the signal**, in plain words: what you saw and that you noticed it.
- **Gives something** from "What I can give", tied to the signal. Give before you ask.
- **Asks for nothing big.** At most a light question they can answer in one line. No meeting request in a first touch after a long quiet stretch.
- **Under 90 words.** Plain, short sentences, the way the user writes. No "hope this finds you well", no "just checking in", no "circling back", no exclamation points, no buzzwords.
- **Has no placeholders the user has not been told about.** If it needs a link or file, put `[LINK: ...]` or `[ATTACH: ...]` and list it under the draft. Never pretend something is attached.
- **Picks the channel** where the user already talks to that person. If unknown, Email.

### Step 4: Show the review sheet

Show everything in the chat, in this order:

1. **Drafts**: for each, the name, the signal (with source and date), why now, channel, and the note.
2. **No note today**: each skipped item with its one-line reason (old, wrong person, open draft, wrong moment, too weak).
3. **Questions**: anything you need before a draft can go out (a link, a date, which person).

Then ask: **"Which of these do you want logged? You can edit any of them first."**

### Step 5: Log only what the user approves

For each approved draft:
- Add a row to the touch log with Status = **Draft**. It becomes Sent only when the user says they sent it (see `log`).
- Do not change Last touch yet. Nothing has been sent.

Write to the store the user chose. For CSV, append rows and keep the header. For a connected Sheets, Airtable or Notion, ask once before writing. Otherwise print the rows ready to paste.

Never save anything the user did not approve. Never send.

---

## Due

`/nurture-starter due` lists, from the prospect list:

- People whose **Next touch** is today or past, oldest first
- People with no touch in the last 60 days
- Drafts in the touch log still marked Draft after 7 days (send them, edit them or skip them)

For each due person with no fresh signal, offer one note built only from "What I can give". Same rules as Step 3. A useful thing with no news attached is still a fine reason to write. "Just checking in" is not.

## Log

`/nurture-starter log` records what actually happened. The user says things like "sent Marcus's note", "skipped Tom", "Joanna replied, wants to talk in January".

- Sent, or edited and sent: set Status, and on the prospect list set **Last touch** = today, **Last touch summary**, and **Next touch**.
- Next touch, unless the user gives a date: Prospect or Talking, 14 days. Proposal out or Deciding, 7 days. Past customer or Ally, 60 days. Not now, 90 days.
- A reply: write it in Reply. If it changes the stage, ask before you change Stage.
- Skipped: set Status = Skipped, and leave Next touch alone.

---

## What good looks like

- Every note could only have been written to that one person, this week.
- The person learns something or gets something, even if they never reply.
- Some runs end with no drafts at all. That is the filter working, not a failure.

## Mistakes this skill exists to prevent

These are the things that went wrong in the always-on version this starter comes from, and the rule each became:

- **The wrong person.** A search on a name alone returned a stranger's news. Rule: match name and organization, or draft nothing.
- **Old news passed off as new.** Undated pages looked recent. Rule: no date, no note.
- **The same person drafted again every day.** Rule: check the log for an open draft first.
- **Drafts that promised things nobody had agreed to**, like a meeting, a date, a booking link. Rule: never invent; ask or leave it out.
