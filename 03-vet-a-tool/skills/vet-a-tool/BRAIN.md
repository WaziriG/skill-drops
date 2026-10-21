# BRAIN — /vet-a-tool

Full methodology behind `SKILL.md`. Read once before your first run; refer back for lane detail.
Companion to `WORKSHEET.md`, the same filter on paper.

---

## Why the order matters more than the questions

If an operator opens the vendor's website before writing their requirements, **the tool's
marketing becomes their requirements.** They end up impressed by things they never needed and
blind to the one thing they did.

So: requirements first, vendor second. That single inversion is most of the value of this skill.
Protect it. If someone opens with "I'm looking at Tool X, is it any good?" — do not answer that
question. Ask what data it would touch.

---

## Where requirements come from — all four sources

Operators assume "requirements" means a regulator. For most of them it does not.

**1 · A regulator.** SEC, HIPAA, FINRA, GDPR, state privacy law. A minority of operators —
absolutely binding on those it covers.

**2 · A contract they already signed.** Client engagement letters and NDAs. **This is the most
commonly missed source and often the real constraint.** Many standard engagement letters restrict
disclosure to third parties or require consent before subcontracting. A tool is a third party.
Ask directly: *"Have you read your engagement letter for a third-party or subcontractor clause?"*
Most have not.

**3 · A promise they published.** Their privacy policy, website copy, what they told a client on
a call. The most common breach of trust is not a hack — it is quietly doing something they
already said they would not do.

**4 · A standard they chose.** Nothing forces it. Still real. Writing it down is what makes it
survive a demo.

Work all four before concluding they have none. Almost nobody has none.

---

## The five lanes in full

### Lane A — Financial advisory, RIA, customer financial records
*SEC Regulation S-P · FINRA · GLBA*

Reg S-P was amended **May 16, 2024**. Two parts hit tool selection:

- A **written incident response program** — a document maintained, not a plan described
- **Written service-provider oversight** — policies ensuring providers protect customer
  information and notify you promptly when something goes wrong

There is a **30-day clock** to notify affected customers once sensitive information has been
accessed without authorization. A vendor who will not commit in writing to prompt notification
makes that clock impossible to meet.

**Compliance dates have passed:** December 3, 2025 for larger entities including RIAs with $1.5B+
under management; June 3, 2026 for everyone else covered.

> **Never tell an operator whether they are a "covered institution."** Ask what they understand
> their status to be, and if they do not know, that is an escalation, not a question for you.

**Non-negotiable:** a written breach-notification commitment with a stated timeframe.

### Lane B — Protected health information
*HIPAA · business associate*

The question is **not** "am I in healthcare." It is **"do I touch PHI."**

A bookkeeping, accounting, or admin firm serving a healthcare provider **and receiving or
maintaining PHI as part of that work is a business associate.** PHI arrives more easily than
people expect: reconciling patient receivables, processing Explanations of Benefit, reviewing
claims reports. A spreadsheet with patient names, dates of service, and billing codes **is PHI** —
those fields together identify a patient and link them to treatment. It does not look like a
medical record. It looks like a spreadsheet.

**Non-negotiable: a signed BAA, available at *their* plan tier.** Many vendors offer a BAA only on
enterprise plans — so "the vendor offers BAAs" is not the same as "I can get one." **No BAA means
no PHI, full stop.** No other strength of the tool compensates.

### Lane C — IT-controlled tenant
*Microsoft 365 · Google Workspace*

They are not the decision-maker. What an assistant can reach is set by an admin, and defaults are
frequently broader than assumed — tenant-wide indexing can surface anything a user could
technically open, which is usually far more than they ever actually open.

**Non-negotiable:** a written answer from their admin. An answer they assume is not an answer
they have. The practical move is a specific email to IT, not a general question.

### Lane D — Several clients, each confidential
*Engagement letters · NDAs · professional duty*

The duty runs to each client separately. AI bites differently here because shared workspaces and
assistant memory can carry one client's material into another's context with nobody intending it.

**Non-negotiable:** they can keep Client A's material out of Client B's workspace, and their
engagement letters permit a third-party tool at all.

### Lane E — Their own promises

Still requirements. In their privacy policy and in what they have said.

**Non-negotiable:** the vendor's terms do not contradict their own published policy.

---

## Where the answers live, and how long it should take

| What is needed | Where | Time |
|---|---|---|
| Data location, retention | Privacy policy · Trust or Security page | 5 min |
| Subprocessor list | Data Processing Agreement · subprocessors page | 3 min |
| Training on data, opt-out | Terms of service · enterprise or API docs | 4 min |
| BAA availability | Site search for "BAA" or "HIPAA"; else ask support | 3 min |

**Over fifteen minutes is itself a finding.** A vendor serious about business customers publishes
this and makes it findable. One who buries it has told you how they think about your data.

---

## The alternatives protocol — the dangerous part

The failure mode: an operator puts patient records into a tool because this skill said it offers
a BAA, and it does not. That is a real harm caused by a confident sentence.

**Rules, in order of importance:**

1. **Never assert a vendor's current terms.** Not BAA availability, not retention, not
   subprocessors, not training defaults. You do not have current knowledge of any of these and
   they change by plan and region.

2. **Check whether the constraint can move first.** Before proposing any replacement, ask whether
   a plan upgrade, a BAA request, or an excluded data category solves it. Switching tools is
   expensive and often unnecessary. This step is skipped constantly and it is where most of the
   real value sits.

3. **Candidates, not recommendations.** Propose 2–4 in the same category, plausible on the
   dimension that failed. Give each one a **first check** — the single question that would kill
   it fastest.

4. **Say the disclaimer in full, every time.** Not a footnote. Not softened.

5. **Never rank.** No "best," no ordering by quality. Ranking is a layer-3 judgment resting on
   facts you cannot verify.

6. **Offer to re-run the filter** on their chosen candidate. The teaching point is that pass two
   takes four minutes.

### Categories where a BAA or enterprise DPA is commonly available

Use to orient the search, **never as a claim about a specific vendor**:

- Major cloud platforms and their first-party AI services — usually have enterprise agreements
- Enterprise tiers of large AI vendors — often, but the tier matters enormously
- Healthcare-specific vertical tools — built for it, but verify the specific product
- Self-hosted or on-premises options — the data never leaves, which resolves several questions at once

The last one is under-considered and worth raising when Tier 1 data is involved.

---

## Building a real vetted list — the upgrade path

Right now no verified registry exists, which is why this skill proposes candidates rather than
answers. That is the honest position and it should not be dressed up.

The fix is a shared log, not a better prompt: **every operator who completes a verdict
keeps it and shares it** — tool, plan tier, date checked, what they found, source URL. Twenty
operators over eight weeks produces a real, sourced, dated list. Then this skill can cite verified
findings *with the date and who checked*, which is a different and far stronger thing than a
model's recollection.

Until that exists, candidates stay candidates.

---

## Tone

Direct. No hedging on the disqualifiers — they are bright lines and softening them makes them
useless. Warm on the escalations; an operator discovering they may be a business associate is
often alarmed, and the right response is *"this is common, it is fixable, and here is who to
call"* — not reassurance that it is nothing.

Never moralize about what they have already done. Most exposure came from competent people
adopting useful tools faster than anyone wrote down where the data goes. That is the normal case,
not a failure of character.
