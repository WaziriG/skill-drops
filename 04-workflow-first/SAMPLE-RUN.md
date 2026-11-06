# Sample run: a framing shop's custom-order workflow

*An illustration, not a client record. The business and every name in it are invented. It shows what a full `/workflow-first` session looks like from the first question to the next action, so you know what you are getting before you run it on your own work.*

**The operator:** Tessa owns a custom framing shop with two counters and four staff. She wants an AI assistant to send customers order confirmations and "ready for pickup" messages, because the phone rings all day with "is my frame done yet?"

---

## The interview (one question at a time)

**Phase 1: Surface**

> **Advisor:** Walk me through a custom order from start to finish. What starts it, and what ends it?
>
> **Tessa:** Customer walks in with art. We pick a frame and mat together, write up the ticket, take a deposit. It goes to the back, Luis builds it, we call them when it's ready, they pay the balance and pick it up.

> **Advisor:** Where does the ticket live once it's written?
>
> **Tessa:** Paper ticket, clipped to the art. The price goes in the register. Luis keeps his own list of what's in the queue.

> **Advisor:** When it goes wrong, what usually broke?
>
> **Tessa:** Usually the glass. If we're out of museum glass, the order sits, and nobody tells the customer.

**Phase 2: Dig**

> **Advisor:** You said Luis builds it. How does he decide what to build next?
>
> **Tessa:** He just knows. Rush jobs, and anything that's been waiting too long. It depends on the week.

*Flag: "he just knows" and "it depends." The build order lives in one person's head.*

> **Advisor:** If Luis were out for two weeks, who would know which frames are waiting on glass?
>
> **Tessa:** ...Honestly, nobody. We'd have to go through the clips one by one.

> **Advisor:** How do you know a frame is ready to call about?
>
> **Tessa:** Luis puts it on the shelf by the front. Whoever's on the counter sees it and calls. Usually.

*Flag: the "ready" signal is a physical shelf, and the call depends on someone noticing.*

**Phase 3: Expose the gaps**

> **Advisor:** If a new hire ran the counter tomorrow with no context, where would they get stuck first?
>
> **Tessa:** Knowing what to tell someone who calls about an order that isn't on the shelf.

---

## The workflow map

```
WORKFLOW: Custom framing order
OWNER: Counter staff (intake, pickup); Luis (build)
TRIGGER: Customer brings in art for a custom frame
OUTCOME: Customer picks up a finished frame and pays the balance
FREQUENCY: About 40 orders a week across both counters

STEPS:
1. Design and quote
   - Input: the art, the customer's choices
   - Action: choose frame, mat and glass; price it
   - Output: paper ticket clipped to the art; price in the register
   - Owner: counter staff
   - Exception: none written down
2. Queue and build
   - Input: paper ticket, materials on hand
   - Action: Luis picks the next job and builds it
   - Output: finished frame on the front shelf
   - Owner: Luis
   - Exception: material out of stock; order waits, customer not told
3. Notify
   - Input: frame appears on the shelf
   - Action: whoever is on the counter calls the customer
   - Output: customer told it's ready
   - Owner: unclear
   - Exception: no one notices the shelf
4. Pickup and balance
   - Input: customer arrives
   - Action: find the frame, take the balance
   - Output: order closed

HANDOFFS:
- Step 1 → Step 2: the clipped ticket goes to the back (physical, no record)
- Step 2 → Step 3: the frame appears on the shelf (physical, no record)

TRIBAL KNOWLEDGE FLAGS:
- Step 2: build order and rush rules live in Luis's head
- Step 2: which orders are waiting on materials is known only by looking

AUTOMATION READINESS SCORE:
- Describability: 6/10  (Tessa can describe the shape; the build rules are tacit)
- Consistency: 4/10     (the call happens "usually," and depends on who is on the counter)
- Boundary Clarity: 5/10 (clear start and end; the step 3 owner is unnamed)
- Exception Handling: 2/10 (the most common failure, missing glass, has no path at all)
- Data Availability: 2/10 (order status exists only on paper and on a shelf)
- OVERALL ARS: 3.8/10
```

## The gap list

**Tier 1: Blockers (an automation will fail without these)**

1. **Order status does not exist anywhere a system can read it.** An assistant cannot send "your frame is ready" when "ready" means "sitting on a shelf." Each order needs a status (Quoted, In queue, Waiting on materials, Ready, Picked up) in one shared place. A spreadsheet is enough.
2. **The waiting-on-materials state has no owner.** Write down who marks an order as waiting and who tells the customer.
3. **The build order depends on one person.** Write Luis's rules down: what counts as a rush, how long is "too long."

**Tier 2: Risks**

- The ready-call is triggered by someone noticing, not by a change in status.

**Tier 3: Optimizations**

- The price is entered twice, on the ticket and in the register.

## The Tribal Knowledge Flag

Which orders are stuck waiting on glass. Only Luis knows, and only by looking. This is the first thing that would break the "ready for pickup" messages: the assistant would stay silent on exactly the orders customers call about most.

## Next action

Before anything gets automated: for two weeks, the counter writes each order into one shared sheet with a status column, and Luis changes the status when he starts, stalls or finishes a job. Luis spends thirty minutes writing his build-order rules on one page. After two weeks, run `/workflow-first score` again. If Data Availability and Exception Handling are both 6 or higher, the messages are ready to build.

**What Tessa noticed:** the automation she asked for was the easy part. The phone calls were a symptom of a status nobody could see.
