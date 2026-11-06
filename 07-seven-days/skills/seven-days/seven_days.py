#!/usr/bin/env python3
"""Seven Days on the Terminal: measure one week of your own Claude Code use.

Reads the session logs Claude Code keeps on your own computer
(~/.claude/projects/*/*.jsonl, plus the subagents/ folders inside them)
and prints sessions, active hours, streams of work and a leverage estimate.

What it will never do:
  - write, move or delete anything in your logs (it opens them read-only)
  - connect to the internet (it imports nothing that can)
  - save a file, unless you pass --save <path>

Standard library only. Python 3.8 or newer.

Parts of the log reading (the usage fields, the prompt-text check, and
counting each streamed reply once by its message id) are adapted from
Nate Herk's token-dashboard (MIT, Copyright (c) 2026 Nathan Herkelman):
https://github.com/nateherkai/token-dashboard
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

GAP_MINUTES = 15          # a pause longer than this counts as a break
TIMED_TYPES = {"user", "assistant", "system"}


# ---------------------------------------------------------------- reading

def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def usage_of(rec):
    u = (rec.get("message") or {}).get("usage") or {}
    return {
        "input": int(u.get("input_tokens") or 0),
        "output": int(u.get("output_tokens") or 0),
        "cache_write": int(u.get("cache_creation_input_tokens") or 0),
        "cache_read": int(u.get("cache_read_input_tokens") or 0),
    }


def human_prompt(rec):
    """Return the text of a real typed prompt, or None for machine bookkeeping."""
    if rec.get("type") != "user" or rec.get("isMeta") or rec.get("isCompactSummary"):
        return None
    content = (rec.get("message") or {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        text = "".join(b.get("text", "") for b in content
                       if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    text = text.strip()
    if not text or text.startswith("<") or text.startswith("Caveat:"):
        return None
    return text


def read_stream(path, start, end):
    """One log file = one stream. Returns its events inside the window."""
    stream = {"times": [], "replies": {}, "tools": set(), "prompts": [],
              "has_user": False, "has_assistant": False}
    try:
        fh = open(path, "r", encoding="utf-8", errors="replace")
    except OSError:
        return None
    with fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if not isinstance(rec, dict) or rec.get("type") not in TIMED_TYPES:
                continue
            ts = parse_time(rec.get("timestamp"))
            if ts is None or ts < start or ts >= end:
                continue
            stream["times"].append(ts)
            if rec["type"] == "assistant":
                stream["has_assistant"] = True
                msg = rec.get("message") or {}
                # Claude Code writes a streaming reply to disk more than once.
                # Keep the last copy of each message id so it is counted once.
                key = msg.get("id") or rec.get("uuid") or id(rec)
                stream["replies"][key] = {"model": msg.get("model"), "usage": usage_of(rec)}
                for block in msg.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        stream["tools"].add(block.get("id") or (key, len(stream["tools"])))
            else:
                text = human_prompt(rec)
                if text is not None:
                    stream["has_user"] = True
                    stream["prompts"].append((ts, text))
    stream["times"].sort()
    return stream


def active_intervals(times, gap):
    """Split a stream's timestamps into busy stretches separated by breaks."""
    out = []
    for t in times:
        if out and t - out[-1][1] <= gap:
            out[-1][1] = t
        else:
            out.append([t, t])
    return out


def union_hours(intervals):
    total, cur_s, cur_e = 0.0, None, None
    for s, e in sorted(intervals):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += (cur_e - cur_s).total_seconds()
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += (cur_e - cur_s).total_seconds()
    return total / 3600


def local_midnight(day):
    """Midnight at the start of this day, in your own time zone (daylight saving included)."""
    return datetime.combine(day, datetime.min.time()).astimezone()


def split_by_day(intervals):
    """Cut intervals at local midnight so each day gets its own share."""
    by_day = defaultdict(list)
    for s, e in intervals:
        s, e = s.astimezone(), e.astimezone()
        while s.date() < e.date():
            midnight = local_midnight(s.date() + timedelta(days=1))
            by_day[s.date()].append((s, midnight))
            s = midnight
        by_day[s.date()].append((s, e))
    return by_day


# ---------------------------------------------------------------- report

def fmt_tokens(n):
    for unit, size in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= size:
            return "%.2f%s" % (n / size, unit)
    return str(n)


def build_report(root, days, end_date, show_prompts):
    end_local = local_midnight(end_date + timedelta(days=1))
    start_local = local_midnight(end_date - timedelta(days=days - 1))
    start, end = start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)
    gap = timedelta(minutes=GAP_MINUTES)

    files = sorted(Path(root).expanduser().glob("**/*.jsonl"))
    sessions, subagents, all_intervals = 0, 0, []
    agent_hours_by_day = defaultdict(float)
    replies, tools, prompts, models = 0, 0, 0, Counter()
    tok = Counter()
    first_prompts = []
    logs_read = 0

    for path in files:
        s = read_stream(path, start, end)
        if s is None:
            continue
        logs_read += 1
        if not (s["has_user"] or s["has_assistant"]) or not s["times"]:
            continue
        if not s["has_assistant"]:
            continue
        is_sub = "subagents" in path.parts
        if is_sub:
            subagents += 1
        elif s["has_user"]:
            sessions += 1
        else:
            continue
        iv = active_intervals(s["times"], gap)
        all_intervals.extend(iv)
        for day, parts in split_by_day(iv).items():
            agent_hours_by_day[day] += sum((e - b).total_seconds() for b, e in parts) / 3600
        replies += len(s["replies"])
        tools += len(s["tools"])
        if not is_sub:
            prompts += len(s["prompts"])
            if s["prompts"]:
                first_prompts.append(min(s["prompts"]))
        for r in s["replies"].values():
            if r["model"] and r["model"] != "<synthetic>":
                models[r["model"]] += 1
            tok.update(r["usage"])

    wall_by_day = {d: union_hours(p) for d, p in split_by_day(all_intervals).items()}
    agent_h = sum(agent_hours_by_day.values())
    wall_h = sum(wall_by_day.values())
    lev = (agent_h / wall_h) if wall_h else 0.0
    active_days = sum(1 for d in wall_by_day if wall_by_day[d] > 0)
    processed = sum(tok.values())

    L = []
    L.append("SEVEN DAYS ON THE TERMINAL")
    L.append("Window: %s to %s (%d days, your local time)" % (
        start_local.date(), end_date, days))
    L.append("Logs read: %d files under %s (read-only, nothing sent anywhere)" % (logs_read, root))
    L.append("")
    if not all_intervals:
        L.append("No Claude Code activity found in this window.")
        L.append("Check the folder, or try a longer window with --days 14.")
        return "\n".join(L)
    L.append("HEADLINE")
    L.append("  Your hours at the keyboard (wall-hours):  %6.1f h" % wall_h)
    L.append("  Hours of agent work (agent-hours):        %6.1f h" % agent_h)
    L.append("  Leverage (agent-hours / wall-hours):      %6.2fx" % lev)
    L.append("")
    L.append("STREAMS OF WORK")
    L.append("  Sessions you started:     %d" % sessions)
    L.append("  Sub-agent runs:           %d" % subagents)
    L.append("  Streams in total:         %d" % (sessions + subagents))
    L.append("  Active days:              %d of %d" % (active_days, days))
    L.append("  Prompts you typed:        %d" % prompts)
    L.append("  Replies from the agent:   %d" % replies)
    L.append("  Tool calls (actions):     %d" % tools)
    L.append("")
    L.append("TOKENS")
    L.append("  Processed (all four kinds): %s" % fmt_tokens(processed))
    L.append("  Generated (output only):    %s" % fmt_tokens(tok["output"]))
    if processed:
        L.append("  Share that is cache reads:  %d%%" % round(100 * tok["cache_read"] / processed))
    L.append("")
    L.append("BY DAY            wall-h   agent-h   leverage")
    d = start_local.date()
    while d <= end_date:
        w, a = wall_by_day.get(d, 0.0), agent_hours_by_day.get(d, 0.0)
        L.append("  %s %s  %6.1f    %6.1f    %s" % (
            d.strftime("%a"), d, w, a, ("%.2fx" % (a / w)) if w else "  -"))
        d += timedelta(days=1)
    L.append("")
    if models:
        L.append("MODELS (agent replies)")
        for m, n in models.most_common():
            L.append("  %-34s %d" % (m, n))
        L.append("")
    L.append("METHOD")
    L.append("  Agent-hours: inside each stream, add up the time between events when the")
    L.append("    pause is %d minutes or less. Longer pauses are breaks. Streams are added" % GAP_MINUTES)
    L.append("    separately, so two terminals running at once count twice.")
    L.append("  Wall-hours: the same busy stretches laid on one clock, overlaps counted once.")
    L.append("  Leverage: agent-hours divided by wall-hours. Above 1.0x means work ran in parallel.")
    L.append("  Streams: sessions with at least one prompt you typed and one reply, plus")
    L.append("    sub-agent runs. A stream ending cleanly does not prove the task succeeded.")
    L.append("  Tokens: each streamed reply counted once by its message id.")
    L.append("  Limits: Claude Code keeps about 30 days of logs by default. Wall-hours are a")
    L.append("    floor on your time: reading, thinking and calls away from the terminal are")
    L.append("    not in the logs.")
    if show_prompts:
        L.append("")
        L.append("FIRST PROMPT OF EACH SESSION (private: for sorting into themes, never for sharing)")
        for ts, text in sorted(first_prompts):
            one = " ".join(text.split())
            L.append("  %s  %s" % (ts.astimezone().strftime("%a %H:%M"),
                                    one[:110] + ("..." if len(one) > 110 else "")))
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Measure one week of your own Claude Code use.")
    p.add_argument("--days", type=int, default=7, help="length of the window (default 7)")
    p.add_argument("--end", help="last day of the window, YYYY-MM-DD (default today)")
    p.add_argument("--projects-dir", default=os.environ.get("CLAUDE_PROJECTS_DIR", "~/.claude/projects"),
                   help="where Claude Code keeps its logs (default ~/.claude/projects)")
    p.add_argument("--prompts", action="store_true",
                   help="also list the first prompt of each session (stays on your screen)")
    p.add_argument("--save", help="write the report to this file as well as the screen")
    a = p.parse_args(argv)
    end_date = (datetime.strptime(a.end, "%Y-%m-%d").date() if a.end
                else datetime.now().astimezone().date())
    root = str(Path(a.projects_dir).expanduser())
    if not Path(root).is_dir():
        print("No Claude Code logs found at %s. Run a few sessions first." % root)
        return 1
    report = build_report(root, max(1, a.days), end_date, a.prompts)
    print(report)
    if a.save:
        with open(a.save, "w", encoding="utf-8") as fh:
            fh.write(report + "\n")
        print("\nSaved a copy to %s" % a.save)
    return 0


if __name__ == "__main__":
    sys.exit(main())
