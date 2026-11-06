# Workflow First: start here

Most automation fails before anyone writes a line of it. A team describes how a job gets done, someone builds the automation, and then it meets the job as it is actually done. The real version has a step nobody mentioned, a call one person makes from memory, and a status that lives on a sticky note. The tool breaks, or worse, it quietly gets things wrong and nobody notices, because nobody had written down what right looks like.

`/workflow-first` closes that gap before you build. It interviews you, one question at a time, about one workflow. It listens for "usually," "it depends" and "she just knows." Then it hands you three things:

- **a workflow map:** every step, who owns it, where the information comes from, and what happens when it breaks
- **an Automation Readiness Score:** 1 to 10 on five criteria, with the reason for each
- **a gap list:** what must be written down or set up before any automation will hold, and the one next action

**It builds nothing, connects nothing and needs no accounts.** That is on purpose. You can't automate what you can't describe.

**The story behind it:** [Then the Room Started Talking](https://wazirigaruba.com/the-room-started-talking). Twenty-nine founders briefed an agent on how they actually work, and found out the build was the conversation.

## What you need

- Claude Code
- One workflow you would like to hand to an AI someday: order intake, scheduling, invoicing, client onboarding, anything you repeat
- Twenty minutes, and ideally the person who does that work every day

## 1. Install the skill (one minute)

On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it and open the `04-workflow-first` folder. Copy the `skills/workflow-first` folder into `~/.claude/skills/`:

```
cp -R skills/workflow-first ~/.claude/skills/
```

## 2. See a finished run (two minutes)

Open `SAMPLE-RUN.md`. It follows an invented framing-shop owner who wanted an assistant to text customers when their frames were ready. The interview found that "ready" meant "sitting on a shelf," which no system could see. Her score was 3.8 out of 10, and the next action was a two-week spreadsheet, not a build.

## 3. Run it on your own workflow (fifteen minutes)

Open Claude Code and type:

```
/workflow-first
```

It asks which workflow you want to map, then asks one question at a time. Answer the way you would explain the job to a new hire on day one. If you have notes or a call transcript about the workflow, paste them in instead:

```
/workflow-first map <paste your notes>
```

## 4. Do the next action before you build

Every run ends with one task: usually something to write down or one place to start tracking a status. Do it, then run `/workflow-first score` again. When every criterion is 6 or higher, the workflow is ready to automate.

## Other modes

| Command | What it does |
|---|---|
| `/workflow-first interview <context>` | The full interview |
| `/workflow-first map <notes>` | Turns messy notes or a transcript into a workflow map |
| `/workflow-first score <workflow>` | The readiness score with reasons |
| `/workflow-first gap <map>` | What must exist before automation |
| `/workflow-first brief <context>` | One page you can hand to your team or whoever builds it |

## What it will not do

- Build, connect or schedule any automation
- Recommend a specific automation product
- Ask for passwords, keys or access to your accounts
- Judge the people doing the work. The gap between the stated process and the real one is in every business.

## Make it yours

The whole skill is two markdown files of plain instructions: `SKILL.md` (how the advisor behaves) and `BRAIN.md` (the interview questions, the five criteria and how they're scored). Open them. If your business has a question every workflow should face, add it to the interview in `BRAIN.md`.

## What's in this folder

| Path | What it is |
|---|---|
| `skills/workflow-first/` | The skill: `SKILL.md` and `BRAIN.md`. Copy the folder into `~/.claude/skills/`. |
| `SAMPLE-RUN.md` | A full worked run on an invented framing shop. |
| `LICENSE` | MIT. Use it, change it, share it. |

— Waz · [wazirigaruba.com](https://wazirigaruba.com)
