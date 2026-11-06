# Sample run: a dog-grooming shop's Monday reviews

An example of `/first-loop`, so you can see what you get before you run it. **Renata and her shop are invented.** The shape of the run is real: three questions, a first-loop check, the one-page spec, and the run prompt.

## The interview

**Q1. The task.**
> "What's one thing you redo by hand every week, or every day, that you wish would just be drafted for you? Walk me through the last time you did it."

**Renata:** "Monday mornings I reply to the weekend's online reviews for both shops. I open the review sites, read each one, write a reply, and paste it in. The bad ones take forever because I rewrite them three times. Maybe 45 minutes most weeks, longer after a holiday."

**Q2. The stakes.**
> "If an assistant did this and got it wrong, what's the worst that could happen, and who would see the mistake?"

**Renata:** "Everyone. Reviews are public. If it promised a refund, or got a dog's name wrong, or argued with someone, that sits there forever. And I never discuss a dog's health in public."

**Q3. The gate.**
> "Where do you already look every day? And have you ever done this task start to finish with an AI helping, even once?"

**Renata:** "My email. I've used ChatGPT to fix one angry reply, but never the whole batch."

## The first-loop check

| Test | Result |
|---|---|
| Recurring | Pass. Every Monday. |
| Writable | Pass. Her rules came out in the interview: thank by name, mention the dog, never promise money, never discuss health, take complaints offline. |
| Draftable | Pass. The reply can wait as a draft. Posting stays with Renata. |
| Recoverable | Pass, because nothing is posted without her. If it posted on its own, this would fail. |

Good first loop. One narrowing: complaints of three stars or below get a short holding draft that moves the conversation to phone or email, never a full public reply.

## The spec

```
FIRST LOOP SPEC: Monday review replies
Owner: Renata          Date: (run date)          Stage: 1 of 3 (manual)

THE CHORE TODAY
Every Monday, Renata reads the weekend's reviews for both shops and writes each reply
by hand. About 45 minutes; longer after holidays.

1. TRIGGER
When it runs: Monday, 8:00 am.
Stage 1: Renata starts it by hand at 8:00 by pasting the run prompt below.

2. WHERE IT FINDS ITS WORK
The weekend's new reviews. For now, Renata copies them into one email to herself
(reviewer name, stars, text, which shop) and pastes that in.

3. WHAT THE ASSISTANT DOES
1. Read each review and note the shop, stars, reviewer, and dog's name if given.
2. Four or five stars: draft a two-sentence thank-you that mentions the dog by name.
3. Three stars or below: draft a short, warm holding reply that invites them to call
   or email the shop, with no details discussed in public.
4. Put all drafts in one list, five-star first, complaints last.
Rules it follows: warm and short; use the reviewer's first name only; never mention
price, refunds or discounts; never discuss a dog's health or behaviour; never argue.

4. CHECK BEFORE YOU SEE IT
- Every name and dog's name matches the review word for word
- Anything unclear (no dog's name, mixed review, a reply that might sound defensive)
  is marked FLAG instead of guessed
- No reply is longer than three sentences

5. NEVER ALLOWED
- Send, post or publish anything
- Pay, refund, book or cancel anything
- Delete or edit anything outside the review queue
- Promise money, a discount or a free service
- Mention a dog's health, injury or behaviour
- Reply to a review it has not seen in full

6. THE REVIEW QUEUE
Everything lands in: one email draft to Renata, subject "Review replies - (date)".
Each item shows: the review, the draft reply, and why it chose that tone.
Renata approves as is, edits then approves, or rejects with one line on why.
She posts the approved replies herself.

7. MEMORY
After each run, the assistant adds one line at the bottom of the draft:
date, how many reviews, how many flagged, anything to do differently next time.
The next run reads last week's line first.

8. HOW YOU WILL KNOW, AFTER ONE WEEK
Run it this Monday, plus once midweek on any new reviews (2 runs). Tally:
- Time per run, start to finish, against the old way: ____ vs 45 min
- Approved as is ____ / edited ____ / rejected ____
- Times it did something on the never-allowed list: must be 0
- Did Renata open the draft every time it filled? yes / no
It passes when: never-allowed stays at 0, at least half the replies are approved as is
or with light edits, and Renata would be annoyed if it stopped.
If it fails: fix the rules in step 3, or shrink the job to five-star replies only.

9. WHAT COMES NEXT (only after week one passes)
Stage 2: save the run prompt as a template so Monday starts with one paste.
Stage 3: have the new reviews collected and the draft built on a schedule, with a tool
Renata chooses. The review queue and the never-allowed list stay exactly as they are.
Posting stays with Renata.
```

## The run prompt (what Renata pastes each Monday)

```
You are drafting replies to my shop's online reviews. Below are this weekend's reviews.
Read last week's memory line first if I include it.

For each review: note the shop, stars, reviewer's first name, and dog's name.
Four or five stars: a two-sentence thank-you that mentions the dog by name.
Three stars or below: a short, warm reply inviting them to call or email the shop.
Discuss no details in public.

Rules: warm and short, three sentences at most. First names only. Check every name
against the review. Mark anything unclear FLAG instead of guessing.

Never: send, post or publish anything. Pay, refund, book or cancel anything. Delete or
edit anything outside this list. Promise money, a discount or a free service. Mention a
dog's health, injury or behaviour.

Put everything in one list: the review, the draft, and one line on why you chose that
tone. Five-star first, complaints last. Do not send, post, pay or delete anything.
When you are done, add the memory line: date, how many reviews, how many flagged,
anything to do differently next time.
```

## Renata's next step

Run it by hand on next Monday's reviews, post the approved replies herself, and keep the tally on a sticky note. A schedule comes up only after the week passes. That order is the whole point.
