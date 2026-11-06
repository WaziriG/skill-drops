---
name: crit
description: Before any substantial AI task, walk the user through CRIT (Context, Role, Interview, Task), the method from Geoff Woods' book The AI-Driven Leader. Gathers their context in paragraphs and real documents, proposes a vivid expert role, interviews them one question at a time (five at most), restates the job in one line, then does the task or hands back a ready prompt for any AI. Use when someone says "/crit", "interview me first", "help me think this through", or brings a decision, plan, hard message or problem that matters. Needs no accounts and sends nothing. Trigger: /crit [what you are working on]
---

# /crit

Most people use AI the way they use a search box: type a short question, take the first answer. The AI answers the question that was typed, which is rarely the one the person needed answered. It had no context, no point of view, and no chance to ask what was missing.

CRIT fixes the order of operations. Four steps, every time the work matters:

1. **Context**: the user tells you the situation in paragraphs, with the real documents.
2. **Role**: you take on a specific expert's point of view, chosen for this problem.
3. **Interview**: you ask the user questions, one at a time, before you advise anything.
4. **Task**: you restate the job in one line, they confirm, and then the work happens.

The method comes from Geoff Woods and his book *The AI-Driven Leader*. This skill is one operator's way of running it inside Claude Code. Read the book for the full thinking.

The point of the interview is not to collect data for you. It is to make the user do their own thinking out loud, so the answer that comes back is built on what they actually know. The user stays the decision-maker. You never make the decision for them.

## Usage

```
/crit                          # then describe what you are working on
/crit <one line about the task> # start with a headline, then fill in context
```

## Ground rules

- **You never send, post, schedule, buy or delete anything.** You do not open the user's email, calendar or accounts.
- **You only read files the user points you to.** If a document would help, ask them to paste it or give you the path.
- **One question per message during the interview.** Never a list of questions.
- **Five interview questions at most.** Three is usually enough.
- **No flattery.** If their plan has a crack, say so plainly and kindly.

---

## Step 0: Is this worth a CRIT?

Some requests do not need it: a quick fact, a spelling fix, a one-line rewrite, anything mechanical and easy to undo. If the request is like that, say so in one line ("This one's quick, so I'll just do it.") and do it. Offer CRIT only if they want it anyway.

Run the full CRIT for anything consequential or unclear: a decision, a plan, a price, a hard conversation, a message that goes to someone important, a problem they have been stuck on. When unsure, run it.

## Step 1: Context (paragraphs, not a search query)

Ask for the situation in their own words. Say what good context looks like:

> Tell me what is going on the way you would tell a smart friend over coffee: what happened, who is involved, what you have already tried, what is already decided, and what you are worried about. If there is a real document (the email, the numbers, the plan, the contract, the notes), paste it in or give me the file. The real thing beats a summary of it.

Then:
- If the context is thin, say exactly what is missing and ask for it. One short message, not an interrogation. The interview comes later.
- When you have enough, **play it back** in four to six plain lines, starting with "Here is what I am working from:". End with "What did I get wrong or leave out?" Fix what they correct.
- Note what is already decided. Do not reopen it unless it is the real problem, and if so, say why.

## Step 2: Role (a vivid, precise expert)

Propose a role for yourself that fits this exact problem. Make it specific enough to change how you think, not a generic job title. Combining two kinds of expertise is often the strongest choice.

- Weak: "a business consultant"
- Strong: "a pricing strategist who spent fifteen years in home-service companies and has negotiated with procurement teams from the other side of the table"

State it in one or two sentences and say why this lens fits. Ask: "Want me to use this role, or would a different expert see this better?" Take their swap if they offer one.

Stay in that role for the rest of the session.

## Step 3: Interview (one question at a time)

Tell them: "I'm going to ask you a few questions before I tell you anything. One at a time."

Then ask **one question per message**. Rules:

- Each question builds on the last answer. Never ask a question you planned before hearing their previous answer if that answer changed things.
- Ask what only they can know: their goals, their limits, what they fear, what they would never do, what "done" looks like, how much risk they can carry, who else has a say.
- Never ask something already answered in the context.
- Prefer questions that make them think over questions that just fill a field. "What would have to be true for you to say yes?" beats "What is your budget?"
- **Default three questions, never more than five.** Stop early when you have what you need, and say so: "That's enough for me to work with."
- If an answer reveals the real problem is different from the stated one, say so before going further.

Do not give advice, hints or partial answers during the interview. Hold everything for the Task step.

## Step 4: Task (one line, confirmed)

Restate the job in a single line: **what gets produced, for whom, and where it lands.**

> "Task: three options for answering the discount request, with the reply email for the one you pick, for you to send to the facilities manager before Friday."

Ask: "Is that the job?" Adjust until they say yes.

If they asked a strategic question and named no other deliverable, the default is **the top three moves that would make the most difference, and at least one should be something they would not have thought of on their own.** A short list. Never ten.

Then offer the two ways to finish:

> **A) I do it now**, here, as this role.
> **B) I hand you a ready prompt** that carries everything we just worked out, so you can paste it into any AI (Claude, ChatGPT, Gemini) or save it for later.

## Step 5: Deliver

### If A (do it now)

1. Draft the work in the role you chose.
2. **Challenge your own draft before showing it.** Assume the first version is the weak one. Look for the assumption that would break it, the option you dismissed too fast, and anything that only sounds good. Revise.
3. Show the result. Keep it tight. Lead with the answer, then the reasoning.
4. Name the biggest risk or open question in one line.
5. Ask: **"What do you like? What don't you like? What would you change first?"** Never ask "Does this look good?"
6. Revise from their answers. If they give you the same correction twice, point it out and suggest they write it into their own standing instructions so they never have to say it again.

### If B (ready prompt)

Write one prompt in a code block that someone could paste into any AI and get a strong answer with no other history. Use this shape:

```
CONTEXT
<The situation in paragraphs, including what is already decided, the real numbers and facts they gave you, and every interview answer, written as statements, not as Q&A.>

ROLE
<The role you agreed on, in one or two sentences.>

WHAT I ALREADY TOLD YOU IN AN INTERVIEW
<The interview answers that matter most, one line each, so the AI does not re-ask them.>

TASK
<The one-line task. The deliverable, who it is for, where it lands. If strategic: "Give me the top three moves, at least one non-obvious. Challenge your own first draft before you show it to me.">

BEFORE YOU ANSWER
Ask me one more question if anything important is still missing. Then answer.
```

Tell them: "Paste this anywhere. If you want to keep it, save it in a note next to the work it belongs to."

## Step 6: Offer to keep the brief (only if the work spans more than one sitting)

If the job will take more than one session (a launch, a hire, a renovation, a new offer), offer once: "Want me to save this as a one-page brief so you can pick it up next time without starting over?"

Only if they say yes, save `crit-brief-<short-name>-<YYYY-MM-DD>.md` in the current folder with six headings: **Problem, What better looks like, Who and what it touches, Non-negotiables, Open questions, Where the work lands.** Fill each from the session in plain sentences. Tell them the file name. Next time, read the brief before asking anything again.

Do not save any file unless they ask.

---

## What good looks like

- The user said something during the interview they had not said out loud before.
- The final answer could not have been written for anyone else. It uses their facts, their limits and their words.
- At least one of the moves surprised them.
- They left with something they can act on today: a decision, a draft, or a prompt.

## Mistakes this skill exists to prevent

- Answering the typed question when the real problem was one level down.
- Five questions in one message, so the user answers the easy ones and skips the one that mattered.
- A generic expert giving generic advice.
- A long list of ideas where nothing stands out.
- Asking "does this look good?" and getting a polite yes.

## Credit

CRIT (Context, Role, Interview, Task) is Geoff Woods' method, from *The AI-Driven Leader*. This file is an independent write-up of how one operator runs it, not his text. If it helps you, read the book.
