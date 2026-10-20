#!/bin/bash
# Relationship Memory: weekly run, for launchd or cron. Edit the five settings, then test by hand once:
#   bash ~/.relationship-memory/bin/run_weekly.sh
# Mail is read-only. Owner columns are never written.
set -euo pipefail

STORE="excel"                                   # excel | csv | notion | airtable
PEOPLE="$HOME/Documents/People.xlsx"            # Excel/CSV only: the spine file
ME="you@yourfirm.example"                       # your address(es), comma-separated
IMAP_HOST="imap.gmail.com"                      # leave as is for Gmail / Google Workspace
IMAP_USER="you@yourfirm.example"

HOME_DIR="$HOME/.relationship-memory"
DAY="$(date +%Y-%m-%d)"
mkdir -p "$HOME_DIR/reports" "$HOME_DIR/exports"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

if [ "$STORE" = "excel" ] || [ "$STORE" = "csv" ]; then
  # App password comes from the macOS Keychain, only for this run. Never stored in a file.
  INBOX_PASSWORD="$(security find-generic-password -s relationship-memory-imap -a "$IMAP_USER" -w)"
  export INBOX_PASSWORD
  python3 "$HOME_DIR/bin/inbox_enrich.py" --people "$PEOPLE" \
    --imap-host "$IMAP_HOST" --imap-user "$IMAP_USER" --me "$ME" --search-link gmail \
    --summarize --report "$HOME_DIR/reports/weekly-$DAY.md" --apply
else
  # Notion or Airtable: Claude runs the skill headless and writes through the connector.
  # Replace mcp__YOUR_STORE_SERVER with the connector's server name from `claude mcp list`.
  claude -p "Use the relationship-memory-weekly skill in --apply mode. Save the report to $HOME_DIR/reports/weekly-$DAY.md." \
    --allowedTools "Bash(python3:*),Bash(security find-generic-password:*),Read,Write,mcp__YOUR_STORE_SERVER" \
    > "$HOME_DIR/reports/weekly-$DAY-claude.log" 2>&1
fi
