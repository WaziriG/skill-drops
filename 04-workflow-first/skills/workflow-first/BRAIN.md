# Workflow-First BRAIN.md
## The Methodology Behind the Skill

---

## The Core Principle

**Defense before Offense.**

You cannot automate what you cannot describe. You cannot describe what only one person understands. And most businesses have far more of the second kind than they know.

The failure mode in AI implementation is not technical. It is organizational. The tool gets built. It hits the real workflow. The real workflow is nothing like what was described. The tool breaks, or worse, silently produces wrong outputs that nobody catches because nobody knew what "right" looked like either.

Workflow-First exists to close that gap before a single line of automation is written.

The job is not to critique how a business operates. The job is to make the invisible visible: to take what lives in three people's heads and put it on a page where a system can use it.

---

## The 5 Automation Readiness Criteria (ARC)

Score each 1–10. A workflow scoring below 6 on any criterion is not automation-ready in that area.

### 1. Describability
*Can the person doing the work explain it step by step to a stranger?*
- 1–3: "It depends" / "you just kind of know" / "I'll show you" — entirely tacit
- 4–6: Can describe the general shape but not the branch conditions
- 7–10: Can write it out as a numbered list that someone else could follow exactly

### 2. Consistency
*Does the same input reliably produce the same output, regardless of who runs it?*
- 1–3: Different people do it differently; same person does it differently each time
- 4–6: Mostly consistent with occasional deviations that "make sense in context"
- 7–10: Fully repeatable — same inputs, same outputs, no judgment calls

### 3. Boundary Clarity
*Is it obvious where this workflow starts and ends, and who hands off to whom?*
- 1–3: Blurry starts/ends; handoffs happen informally or "when it feels right"
- 4–6: Defined start and end, but handoff conditions are fuzzy
- 7–10: Clear trigger, clear output, clear owner, clear recipient at every step

### 4. Exception Handling
*Are the edge cases documented, or do they live in one expert's head?*
- 1–3: Exceptions handled by one person who "just knows" — total tribal knowledge
- 4–6: Some exceptions documented, major ones still person-dependent
- 7–10: Exception paths are written out and known to multiple people

### 5. Data Availability
*Does the information needed at each step exist in a system, or does someone have to find/create it?*
- 1–3: Key inputs live in email threads, memory, or one person's files
- 4–6: Some data is structured, some requires manual gathering
- 7–10: All required inputs exist in accessible, structured form at the moment they're needed

---

## The Interview Protocol

Three phases. Never skip Phase 1 to get to Phase 3.

### Phase 1 — Surface (What They Think They Have)

Open questions. Let them talk. Your job is to listen for confidence versus hesitation.

1. Walk me through this process start to finish — what triggers it, what ends it?
2. Who owns each step?
3. How long does each step take?
4. Where does this process live right now — docs, email, someone's head?
5. When it goes wrong, what usually broke?

**Listen for:** Hedging language ("usually," "typically," "it depends," "we're working on that"), passive voice ("it gets sent"), and unnamed actors ("someone checks").

---

### Phase 2 — Dig (What's Actually Happening)

Go back through each step and challenge the surface answer.

1. You said [X happens] — who specifically does that, and where exactly do they get the information they need?
2. What happens if [Y is missing or wrong] at this step?
3. If [key person] were out for two weeks, how would this step get done?
4. Has this process changed in the last 12 months? What changed and why?
5. What's the part of this process that you'd be most nervous about someone else running?

**Listen for:** Pauses before answering, answers that start with a person's name, "we'd have to figure it out," any step where the answer is "call [person]."

---

### Phase 3 — Expose the Gaps (What Needs to Exist Before Automation)

Surface the delta between what was described and what would need to be true for a system to run it.

1. If I handed this process to a new employee with zero context, what would they get stuck on first?
2. What judgment calls happen in this process that aren't written down anywhere?
3. Are there any steps where the output is "it looks right" rather than a specific measurable thing?
4. Who would you ask if you got stuck? Is that person always available?
5. What's the one thing in this process that only works because of [specific person]?

---

## Workflow Map Output Format

When producing a workflow map, use this structure:

```
WORKFLOW: [Name]
OWNER: [Role or person]
TRIGGER: [What starts this workflow]
OUTCOME: [What a successful completion looks like]
FREQUENCY: [How often / volume]

STEPS:
1. [Step name]
   - Input: [What is needed]
   - Action: [What happens]
   - Output: [What is produced]
   - Owner: [Who does it]
   - Tool/System: [Where it happens]
   - Duration: [How long]
   - Exception: [What to do if it breaks]

[repeat for each step]

HANDOFFS:
- [Step X] → [Step Y]: [trigger for handoff, format of handoff]

TRIBAL KNOWLEDGE FLAGS:
- [Step #]: [What lives in someone's head that isn't written down]

AUTOMATION READINESS SCORE:
- Describability: [X/10]
- Consistency: [X/10]
- Boundary Clarity: [X/10]
- Exception Handling: [X/10]
- Data Availability: [X/10]
- OVERALL ARS: [average/10]
```

---

## Gap Analysis Framework

After mapping, identify gaps in this order of priority:

### Tier 1 — Blockers (automation will fail without these)
- Undocumented decision logic ("use judgment here")
- Missing data sources (inputs that exist in email/memory only)
- Single-person dependencies with no backup

### Tier 2 — Risks (automation will drift without these)
- Inconsistent naming conventions across steps
- Handoff conditions that are time-based rather than state-based
- Exception paths that aren't documented

### Tier 3 — Optimizations (automation works but isn't clean)
- Redundant steps that exist for historical reasons
- Manual data entry that could be eliminated
- Approval steps that serve no current function

---

## The Readiness Brief (for `/workflow-first brief`)

One page. Three sections:

**What We Found**
2–3 sentences on what was described vs. what the interview surfaced. Name the gap without naming a villain.

**What Needs to Exist Before We Build**
A numbered list of Tier 1 blockers only — the things that must be resolved before any automation begins. Be specific. Not "document the process" but "write out the decision logic for [step X] including the three exceptions the office manager currently handles from memory."

**Recommended Next Step**
One concrete action. Who does it, what they produce, and when it needs to be done before the build timeline is at risk.

---

## The Core Metaphor (use when explaining this to a team)

*"You don't teach a new employee by having them watch someone experienced do the job for ten years and hoping they absorb it. You write a manual. AI is the same, except it has no patience for ambiguity and no way to ask a follow-up question at 2pm on a Tuesday. Everything that lives in someone's head has to live on a page first. That's what we're doing here."*

---

## Where this fits

`interview` produces the raw workflow map → `gap` turns it into a requirements list → `brief` turns that into one page you can hand to whoever builds the automation, inside your team or outside it.
