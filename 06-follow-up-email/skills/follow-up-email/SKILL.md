---
name: follow-up-email
description: Turn call notes or a transcript into a list of every promise made on the call, then a short follow-up email that delivers or dates each one. Use after a sales call, a client call, an interview or a networking conversation, when someone pastes notes and says "draft the follow-up", "what did I promise", or "write the follow-up email". Never sends anything. Trigger: /follow-up-email
---

# /follow-up-email

Most follow-ups fail in one of two ways. They go out late, or they go out on time and forget one of the things you said you would send. The other person remembers what you promised. This skill makes sure you do too.

You do two things, in this order:

1. **List every promise made on the call**, by either side.
2. **Draft a short follow-up email** that delivers each promise you made, or puts a date on it.

You never send anything. You never open the user's email, calendar or files unless they ask you to. The user reads the draft, fills the gaps and sends it themselves.

## Usage

```
/follow-up-email                     # then paste the notes or transcript
/follow-up-email <path to a file>    # read notes or a transcript from a file
```

The notes can be anything: a typed summary, bullet points, a recording app's transcript, an AI notetaker's summary, or a few lines written from memory in the car.

---

## Step 1: Work out who is who

Find the **sender** (the user, who will send the email) and the **recipient** (the person the email goes to). Use names from the notes.

If the transcript has several speakers and you cannot tell which one is the user, ask one question: "Which speaker are you?" Otherwise do not ask; start.

If there are several other people on the call, the email goes to the main one. Say who you picked, so the user can correct it.

## Step 2: List every promise

Read the whole thing, start to end. A promise is anything someone said they would do, send, check, introduce, decide or schedule. Look for:

- "I'll send you...", "I can get you...", "let me share..."
- "I'll introduce you to...", "you should meet..."
- "I'll check with...", "let me find out..."
- "by Friday", "tomorrow", "next week", "before the board meeting"
- Soft offers: "I could send you the recording", "happy to share the deck". Count these. The other person heard them as promises.
- Promises the **other person** made: "I'll send you the job description", "I'll talk to my partner".

Show the list as a table before anything else:

| # | Who promised | What | Their words (or closest line in the notes) | Deadline said | Status |
|---|---|---|---|---|---|

Status is one of:
- **Ready**: the user can include it now (a file, a link, an answer).
- **Needs a date**: it is not ready, so the email gives a specific date.
- **Check first**: it involves a third person (an introduction, a favour, someone else's time). The user should ask that person before promising them in writing.
- **Theirs**: the other person owns it. The email restates it lightly, once.

Rules for the list:
- Only promises that are in the notes. Never add one because it "would make sense".
- Quote the words when the notes have them. If the notes are a summary, say "from the summary" instead of inventing a quote.
- If the notes are too thin to tell what was promised, say so plainly and ask the user to add what they remember.
- Flag anything the other person said was confidential. It does not go in the email.
- Flag any number said on the call (a price, a salary, a headcount, a date). Do not repeat it in the email unless the user confirms it.

## Step 3: Ask once, then draft

Ask **one message** with only the questions you need, at most three. Typical ones:

- "Promise 2, the price sheet: do you have a link, or is it an attachment?"
- "Promise 4 is not ready. What date can you commit to?"
- "Promise 5 is an introduction. Have you checked with that person?"

If the user says "just draft it", skip the questions and use placeholders: `[LINK: price sheet]`, `[ATTACH: proposal]`, `[DATE]`.

## Step 4: Draft the email

Structure:

```
Subject: <plain, specific: what is inside, not "Following up">

<First name>,

<One sentence that names one specific thing they said on the call. Not "great to connect".>

<Each of the sender's promises, in the order that matters to the recipient:
 delivered (link or attachment), or dated ("I'll have the revised quote to you by Thursday the 12th").
 One line each. Group them under short labels only if there are more than four.>

<Introductions marked Check first: "I'm checking with <name> first and will connect you by <date>.">

<Their promises, restated once, lightly: "And when you have the job description, send it my way.">

<One next step, with an owner and a time.>

<Sign-off with the sender's first name>
```

Rules:
- **Under 150 words** in the body. If it runs longer, cut the framing, not the promises.
- Every one of the sender's promises appears: delivered or dated. None dropped, none vague. "Soon" is not a date.
- Never say something is attached or linked unless the user confirmed it. Otherwise use a placeholder.
- Write the way the sender talks in the notes. Plain words, short sentences.
- No "hope this finds you well", "just circling back", "per our conversation", "touching base". No exclamation points. No buzzwords.
- Nothing confidential, no unconfirmed numbers, nothing about third parties beyond what the recipient already knows.

## Step 5: The send checklist

After the draft, show a short checklist:

- [ ] Placeholders to fill (list each one)
- [ ] Attachments to drag in (list each one)
- [ ] Dates you just committed to: put each on your calendar now
- [ ] Introductions to check with the third person before you send
- [ ] Send it today. A follow-up sent within a day reads as care. One sent a week later reads as a reminder.

## Step 6: Stop

Show the promise list, the draft and the checklist in the chat. Do not save a file unless the user asks; if they do, save it as `follow-up-<recipient-first-name>-<date>.md` in the current folder. Do not send, schedule or open anything.

---

## What good looks like

- The recipient could check the email against their own memory of the call and find nothing missing.
- Every open item has a date the sender can keep.
- It reads like a person wrote it the same afternoon.

## Mistakes this skill exists to prevent

- Promising an introduction in writing before asking the person being introduced.
- Sending the "main" file and forgetting the small one offered in passing ("I could send you the recording").
- Repeating a number said loosely on a call as if it were an offer.
- A follow-up so long the one real next step gets lost.
