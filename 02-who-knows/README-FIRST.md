# Who Knows: start here

Someone asks you "who do you know who…?" You answer from memory, and memory hands you the last person you talked to, not the right one.

`/who-knows` answers that question from your own notes. You keep a short table of people you would actually ask, with one or two sentences each, in your own words, on what they can help with. Then you ask Claude Code in plain English and it answers from that table. It quotes your words back to you, ranks the people you trust most first, names who could introduce you, and tells you plainly when nobody fits.

It is read-only. It never writes to your table, and it never sends anything. Every draft it writes is for you to read.

**Already installed Drop 1 (Relationship Memory)?** You have this skill and it already reads your inbox for warmth. Skip to "Get more out of it" at the bottom.

## What you need

- Claude Code
- About fifteen minutes and ten people you know well

## 1. Install the skill (one minute)

Copy the `skills/who-knows` folder into `~/.claude/skills/`:

```
cp -R skills/who-knows ~/.claude/skills/
```

If you already have a skill named `who-knows`, rename one of them first.

## 2. Run the demo (two minutes)

Open Claude Code in this folder and type:

```
/who-knows --map demo/people-data-map.md someone who can get our books ready for a bank loan
```

The demo table has 30 invented people. You should see one strong match and one partial, with the demo owner's own words quoted as the reason, a "Could introduce you" line, and a short "Gaps" line. Nothing touches your data. Compare with `demo/sample-run/who-knows-example.txt`.

Try a second one:

```
/who-knows --map demo/people-data-map.md --intros
```

That asks the reverse question: who in this network should meet whom? It reads the needs people have told you about and matches them against everyone else's strengths. Every introduction is drafted one side at a time, so nobody is introduced before they agree. Compare with `demo/sample-run/who-knows-intros-example.txt`.

## 3. Make your own table (ten minutes)

1. Copy `starter/people.csv` somewhere you keep your files and open it in Excel, Numbers or Google Sheets.
2. Add ten people you would actually call. For each one, fill in:
   - **Know Them?**: `Yes` if you would ask them for a favor today. `Getting to know` if not yet. Only `Yes` people are ever suggested.
   - **Can Help With**: one or two sentences, in your own words. "Fractional CFO for service firms; good at getting books ready for a bank" beats "finance." This column is what makes the answers good.
   - **Priority**: A, B or C. With no inbox history, this is how the skill ranks people.
   - **Open Loops** (optional): anything they have asked you for, one dated line each. `--intros` reads this column.
   - **Next Step** (optional): write `PAUSED` here and the skill will never draft a note to that person.
3. Delete the example row and save it as CSV.
4. Put the map where the skill looks for it. If `~/.relationship-memory/people-data-map.md` already exists, you set up the full kit earlier: don't overwrite it, just add your table to it.

```
mkdir -p ~/.relationship-memory
cp starter/people-data-map.md ~/.relationship-memory/people-data-map.md
```

5. Open `~/.relationship-memory/people-data-map.md` and replace `/full/path/to/people.csv` with the real path to your file, and `YOUR NAME` with your name.

## 4. Ask

```
/who-knows someone who can review a vendor contract before I sign it
```

If the answer is "no strong match," that is the skill working. It tells you where your network is thin.

## Get more out of it

- **Write Can Help With as you go.** After every good conversation, add a sentence. Ten honest entries beat two hundred blank rows.
- **Run `--intros` once a week.** It finds people in your table whose needs match someone else's strengths, and drafts the first note for you to send.
- **Add warmth.** The full Relationship Memory kit (Drop 1) reads your inbox once a week, read-only, and ranks people by how recently and how often you actually talk. https://github.com/WaziriG/skill-drops/tree/main/01-relationship-memory

## What's in this folder

| Path | What it is |
|---|---|
| `skills/who-knows/` | The skill. Copy it into `~/.claude/skills/`. |
| `demo/` | 30 invented people, a demo map, and `sample-run/` with the answers the demo should give. |
| `starter/` | A blank table and a map template for your own people. |

Every person in `demo/` is invented. Any resemblance to a real person or company is accidental.

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
