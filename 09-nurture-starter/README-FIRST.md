# Nurture Starter: start here

You met someone good in the spring. By the autumn they have opened a new location, hired a new manager, changed jobs. You meant to stay in touch. Now the only note you can think of is "just checking in", and you know how that reads.

`/nurture-starter` keeps a short list of the people you want to stay close to and helps you write to them when something real has happened. You paste in what you have seen: a headline, the text of a post, a job change. It checks each item (is it the right person, is it recent, is it actually about them), drafts one short note per person that gives them something useful before it asks for anything, and shows you every draft. You decide. It logs what you approve, and tells you who is due a note next.

It never sends anything. It never opens LinkedIn or logs in to anything. It never searches for people on its own, and it never asks for a key or a password.

**Where it came from.** I run a bigger version of this every day. It searches the news for each person on my list, checks what it finds, and emails me one digest with drafts waiting for my review. I showed it at an AI showcase on October 15, and it is still running: on November 5 it read through 60 people and drafted 6 notes for me to review. The always-on version needs a workflow tool and three accounts with keys. This drop is the part anyone can run today, by hand. `GROWS-INTO.md` shows the rest.

The longer kit, with the five things that broke in mine: [wazirigaruba.com/kits](https://wazirigaruba.com/kits)

## What you need

- Claude Code
- Five to ten people you want to stay close to: prospects, past customers, people who send you referrals
- One place to keep the list: a CSV file (simplest), Excel, Google Sheets, Airtable or Notion

## Setup checklist (about 45 minutes, most of it thinking)

| Step | Time | What you do |
|---|---|---|
| 1. Install the skill | 2 minutes | Copy the folder (below) and restart Claude Code |
| 2. Try the sample | 5 minutes | Run it on the invented list in `sample-run/` |
| 3. Make your list | 2 minutes for a CSV; about 10 for Excel, Google Sheets, Airtable or Notion | Type `/nurture-starter setup` and pick where the list lives. For anything but the CSV, it makes the file and tells you how to import it. |
| 4. Fill in your people | 20 to 30 minutes | For each person: why you are watching them, and what you could give them. This is the real work. Vague answers make vague notes. |
| 5. First real run | 10 minutes | Paste in whatever you have seen about them this month |
| Then, once a week | About 15 minutes | Paste the week's news, run `/nurture-starter due`, send the notes you like |

## 1. Install the skill (two minutes)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it, open the `09-nurture-starter` folder, and copy `skills/nurture-starter` into `~/.claude/skills/`:

```
cp -R skills/nurture-starter ~/.claude/skills/
```

Restart Claude Code if it was already open.

## 2. The five-minute first run

Open Claude Code in this folder and type:

```
/nurture-starter
```

Tell it the list is `sample-run/sample-prospects.csv`, then paste the four lines from `sample-run/sample-signals.txt`. You will see two drafts, one question about a LinkedIn link it refuses to open, and one "no note": the news is about a different person with the same name. Compare with `sample-run/SAMPLE-RUN.md`.

## 3. Set up your own list

```
/nurture-starter setup
```

It asks three questions, one at a time: where the list should live, who is on it, and for each person, why you are watching them and what you could give them.

## 4. Use it weekly

```
/nurture-starter          # paste news about your people, get drafts to review
/nurture-starter due      # who is due a note, even with no news
/nurture-starter log      # "sent Marcus's note", "Joanna replied"
```

Where to find news worth pasting: their company's news page, a local business journal, a newsletter they write, posts they publish (copy the text, not the link), a job change you heard about. One line each is enough: `Name: what happened (source, date)`.

## Make it yours

The whole skill is one markdown file of plain instructions, `skills/nurture-starter/SKILL.md`. Open it. Change the word limit, add phrases you never want in a note, or change how many days until each person is due again. When you make the same edit to a draft twice, put that edit in the file.

## What it will not do

- Send, schedule or post anything
- Open LinkedIn, use your login, or search for people on its own
- Ask for an API key, password or token
- Make up news, quotes, dates, meetings or offers
- Write a note when there is no real reason to

## What's in this folder

| Path | What it is |
|---|---|
| `skills/nurture-starter/` | The skill: `SKILL.md` and two blank CSV templates. Copy the folder into `~/.claude/skills/`. |
| `sample-run/sample-prospects.csv` | An invented list of four people for your first run |
| `sample-run/sample-signals.txt` | Invented news to paste in |
| `sample-run/SAMPLE-RUN.md` | The finished run: checks, drafts, the log, the due list, and a week later |
| `GROWS-INTO.md` | The always-on version: what it needs, what it costs in time, and what broke in mine |
| `LICENSE` | MIT. Use it, change it, share it. |

Every person and business in this folder is invented.

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
