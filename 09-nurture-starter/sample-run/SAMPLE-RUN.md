# Sample run: a cleaning company owner and four people she wants to stay close to

Every person and business here is invented. The list this run used is `sample-prospects.csv` and the pasted news is `sample-signals.txt`, both in this folder, so you can run the same thing and compare.

Renee Castillo runs Castillo Commercial Cleaning. She set up her list on a Monday morning with `/nurture-starter setup`, chose a CSV, and added four people. The run below is the following Friday, November 6.

**What Renee typed:**

```
/nurture-starter
```

Then she pasted the four lines in `sample-signals.txt`.

---

## 1. The checks

| # | Person | Right person? | Recent? | About them? | Open draft? | Result |
|---|---|---|---|---|---|---|
| 1 | Marcus Hale | Yes: Northgate Medical matches | Nov 2, 4 days | Yes: a second location | No | Draft |
| 2 | Tom Albrecht | Yes: Riverside Charter matches | Oct 30, 7 days | Yes: hiring the role he does himself today | No | Draft |
| 3 | Joanna Pruitt | Can't tell yet | ? | ? | No | Question: that is a LinkedIn link. I don't open LinkedIn. Paste the text of the post and its date. |
| 4 | Owen Reyes | **No**: this Owen Reyes is a high school coach. Yours is an office manager at Bluefin Architects. | | | | No note |

**Renee pasted Joanna's post:** "Long week. Two tenants moved out with no notice and our maintenance lead is out sick. Grateful for a team that keeps showing up." (Nov 4)

Joanna is a past customer, the post is a hard week, and move-out cleans are exactly what Renee did for her. So: a short offer of help, no pitch, no prices.

---

## 2. The review sheet

### Drafts

**Marcus Hale**, Northgate Medical Offices
Signal: second location opening in March on Fifth Street (City Business Journal, Nov 2)
Why now: a new suite has to be cleaned to a medical standard before patients arrive, and his current contract ends in April, a month after the opening.
Channel: Email

```
Subject: Your Fifth Street opening

Marcus,

I saw Northgate is opening on Fifth Street in March. Congratulations.

Before our first medical client opened, we wrote a one-page checklist for getting a suite ready for patients: exam rooms, waiting area, what inspectors look at. I've attached it. Use it with whoever does the work.

When is the space handed over to you?

Renee
```
To attach: `[ATTACH: medical suite opening checklist]`

**Tom Albrecht**, Riverside Charter School
Signal: job posting for a facilities coordinator (school website, Oct 30)
Why now: he has been doing facilities himself, and a new coordinator starts with a blank calendar.
Channel: Email

```
Subject: For your new facilities coordinator

Tom,

I saw Riverside is hiring a facilities coordinator. That should take a lot off your plate.

Here is the summer deep-clean calendar we use with schools: what gets done in June, July and August so classrooms are ready for the first week. It might save your new hire a few weeks of guessing.

Renee
```
To attach: `[ATTACH: school summer deep-clean calendar]`
Note: his Next touch was August 7, so he was three months overdue. This note covers it.

**Joanna Pruitt**, Pruitt & Sons Property Group
Signal: post about two no-notice move-outs and a sick maintenance lead (her post, Nov 4)
Why now: she is short-handed on exactly the work you have done for her.
Channel: Text (you've texted her before)

```
Joanna, saw your post. Sounds like a week. If those two units need a move-out clean, we can get a crew there this week. No need to reply if you've got it covered.
```

### No note today

- **Owen Reyes**: the news is about a different Owen Reyes (a high school coach). Nothing drafted.

### Questions

1. Marcus and Tom: do you have both attachments ready to send?
2. Joanna: can you really get a crew there this week? If not, change "this week" to a day you can keep.

**Renee's answers:** "Both files are ready. Yes, Wednesday or Thursday works for Joanna. Log all three."

---

## 3. What was logged

Three rows added to `nurture/touch-log.csv`, each with Status = **Draft**. Last touch on the prospect list was not changed, because nothing had been sent yet.

```
2026-11-06,Marcus Hale,"Second location opening in March, Fifth Street (City Business Journal, Nov 2)","New suite needs medical-standard cleaning; current contract ends April",Email,"<the note above>",Draft,
2026-11-06,Tom Albrecht,"Hiring a facilities coordinator (school website, Oct 30)","He does facilities himself; new hire starts with a blank calendar",Email,"<the note above>",Draft,
2026-11-06,Joanna Pruitt,"Post: two no-notice move-outs, maintenance lead out (Nov 4)","Short-handed on the work we already do for her",Text,"<the note above>",Draft,
```

---

## 4. Due check

**Renee typed:** `/nurture-starter due`

- **Owen Reyes**: Next touch was November 1. No real news this week, so here is a note built from what you can give him:

```
Subject: After-hours cleaning, how we do it

Owen,

You mentioned you need a cleaner who can come in after 7pm. Here's a one-page outline of how our evening crews work: arrival times, who holds the keys, and how we lock up and report back. Keep it for when you're ready to compare.

Renee
```
To attach: `[ATTACH: after-hours schedule and key handling]`

- **Drafts older than 7 days**: none.

**Renee:** "Log Owen's too." One more row added to the touch log, Status = Draft.

---

## 5. A week later

**Renee typed:** `/nurture-starter log` and said: "Sent Marcus and Tom by email Monday. Texted Joanna. Joanna replied, they used us Thursday for both units. Skipped Owen for now."

- Marcus and Tom: Status = Sent. Last touch = Nov 9. Next touch = Nov 23 (Talking and Aware prospects, 14 days).
- Joanna: Status = Sent. Reply = "Booked both units for Thursday." Last touch = Nov 9. Next touch = Jan 8 (past customer, 60 days). It asked before changing anything else.
- Owen: Status = Skipped. Next touch left at Nov 1, so he shows up in the next due check.

Nothing was sent by the skill. Renee sent every note herself.
