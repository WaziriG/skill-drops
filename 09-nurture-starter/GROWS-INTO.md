# What it grows into: the always-on version

The starter is run by hand. You paste the news, you read every draft, you send every note. That is on purpose. Run it by hand for a month first. You will learn which people deserve a place on the list, what a good "Why I'm watching" line looks like, and which kinds of news are worth a note. If you automate before you know that, you only get weak notes faster.

The version I run myself does the same job on a schedule. Here is the shape of it, so you can see where the starter is heading.

## The shape

```
Every day, on a timer
  -> read the prospect list
  -> for each person, search recent public news (name + organization)
  -> a model checks each result: right person? recent? a real reason to write?
  -> if yes: write the signal and a draft note into a review queue
  -> send one digest email: each person's news, and the drafts waiting
You
  -> read the digest, edit or skip each draft, send the good ones yourself
```

The rules do not change when it runs on its own. It still never sends. Drafts still wait for your yes.

## What it needs that the starter does not

| Piece | What it does | Typical choice |
|---|---|---|
| A scheduler | Runs the job every day | n8n (cloud or self-hosted), or any workflow tool you already use |
| A news search API | Finds recent public news about each person | A web search API with a "news only" option |
| A model API | Checks the news and drafts the note | Claude, through your own API key |
| A connection to your list | Reads people, writes signals and drafts | The Notion, Airtable or Google Sheets connector in your workflow tool |
| A way to reach you | The daily digest | An email node sending to you only |

Each of those needs its own account and key. That is why this drop is the hand-run starter.

## Honest time and cost

These are estimates, not promises.

- **Build:** an afternoon if you have built a workflow before; a weekend if you have not.
- **Tuning:** about two weeks of reading the digest every day and fixing what it gets wrong.
- **Running cost:** one search and one model call per person per day. Keep the list short, and add a cap on how many people it checks per run.

## What broke in mine, and the rule each became

Every rule in the starter's "Mistakes this skill exists to prevent" came from the always-on version:

- A search on a name alone returned a stranger's news. Search name plus organization, and have the model confirm it is the same person.
- Undated pages came back as if they were new. Ask the search for news only, and drop anything without a date.
- The same people got a new draft every day. Check the review queue for an open draft before writing another.
- Drafts invented meetings, dates and booking links. Tell the model it may only use facts in front of it, and leave anything missing as a visible placeholder.
- The digest ran twice and sent two emails a day. Check that it sends one, and read a week of them before you trust it.

## When you are ready

Keep your list in the same columns the starter uses. The always-on version reads the same fields, and the touch log becomes the review queue. Nothing you set up now is wasted.
