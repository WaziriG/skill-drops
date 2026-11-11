#!/bin/zsh
# memguard.sh: run during big copies. Every 30 s, if macOS's icon service (iconservicesagent)
# passes 1.5 GB it is stopped; macOS restarts it clean. A runaway icon service can eat all
# memory in minutes during big media copies and freeze the computer.
# Usage: zsh scripts/memguard.sh &     (stop it with: kill %1, or close the terminal)
LIMIT_MB=${LIMIT_MB:-1500}
while true; do
  top -l 1 -o mem -stats pid,command,mem -n 40 | awk -v lim="$LIMIT_MB" '$2 ~ /^iconservicesag/ {m=$3; u=substr(m,length(m)); v=m+0; if(u=="G")v*=1024; else if(u=="K")v/=1024; if(v>lim) print $1, int(v)}' |
  while read pid mb; do
    if kill -9 "$pid" 2>/dev/null; then r=stopped; else r="could not stop (owned by the system; needs an admin)"; fi
    echo "$(date '+%F %T') icon service pid $pid at ${mb} MB: $r"
    osascript -e "display notification \"Icon service at ${mb} MB: $r\" with title \"Memory guard\"" 2>/dev/null
  done
  sleep 30
done
