# Scheduling the weekly run

Pick one. Whatever runs it, the scheduled run **applies history columns only**. Suggestions and new people wait in the store for you. Mail is read-only either way.

First copy the files into place:
```
mkdir -p ~/.relationship-memory/bin ~/.relationship-memory/reports
cp scripts/inbox_enrich.py scripts/scheduler/run_weekly.sh ~/.relationship-memory/bin/
```
Edit the five settings at the top of `run_weekly.sh`, then run it once by hand before scheduling it.

## Option 1: Claude Code scheduled routine (simplest if you live in Claude Code)

Ask Claude Code: "Schedule `/relationship-memory-weekly --apply` every Monday at 7am" (the built-in `/schedule` command). Routines run as cloud agents, so they can use cloud connectors (Notion, Airtable, Gmail) but **cannot see files or the Keychain on your Mac**. Use this route with the Gmail connector and a Notion or Airtable store. For IMAP, Excel or a local .mbox, use launchd or cron.

## Option 2: launchd on a Mac (recommended for IMAP and Excel)

```
sed "s/YOUR_USERNAME/$(whoami)/g" scripts/scheduler/com.relationship-memory.weekly.plist.template \
  > ~/Library/LaunchAgents/com.relationship-memory.weekly.plist
launchctl load ~/Library/LaunchAgents/com.relationship-memory.weekly.plist
launchctl start com.relationship-memory.weekly        # run once now to test
```
Logs land in `~/.relationship-memory/reports/`. A Mac asleep at the scheduled time runs the job when it wakes. To stop it: `launchctl unload` the same path.

## Option 3: cron (Linux, or a Mac if you prefer)

Add the line in `crontab.txt` with `crontab -e`. On a Linux server there is no Keychain: put the app password in a root-readable file or a secrets manager and export `INBOX_PASSWORD` from it in `run_weekly.sh`.

## Option 4: n8n

1. **Schedule Trigger**: weekly, Monday 07:00.
2. **Execute Command** node (self-hosted n8n only; n8n Cloud has no shell): `bash ~/.relationship-memory/bin/run_weekly.sh`. The n8n host needs Python 3, the script, and the password available as an environment variable (n8n credentials or the host's secret store), not in the workflow JSON.
3. Optional: **Read Binary File** on `~/.relationship-memory/reports/weekly-{{$today.format('yyyy-MM-dd')}}.md`, then send yourself the summary in Slack, Teams, email or Telegram. Send it only to yourself: the report contains private context about other people.

Keep the logic in the script and the skills, not in n8n nodes, so the same run works from any scheduler.
