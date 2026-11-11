---
name: clear-the-mac
description: "Free up a full computer drive safely by moving big, rarely-used folders onto two external hard drives, with every file checksum-verified on both before anything is deleted, a register that tracks where everything went, a READ-ME left in each emptied folder, and a dollar figure for what the freed space is worth. Use when someone says their disk is full, \"low on storage\", \"startup disk almost full\", \"my Mac is slow\", \"clear the Mac\", \"free up space\", \"offload to my hard drives\", or \"media register\". Trigger: /clear-the-mac"
---

# Clear the Mac

Most "my computer is full" problems are not a storage problem. They are a **tracking** problem: people keep everything on the laptop because they are afraid they will never find it again once it moves. This skill fixes the fear first, then moves the files.

**The promise to the owner:** every folder that leaves the computer exists, byte-for-byte, on **two** drives; you can see where it went from the folder itself; and nothing is deleted until you say the words.

Engine: `scripts/offload.py` (stdlib Python, no installs). Calculator: `scripts/savings.py`.

## The rules (never break these)

1. **Two copies or no move.** A folder is copied to two separate drives and every file is md5-checked on both.
2. **Nothing is deleted without the owner's explicit go** ("clear the Mac" or equivalent), given in this conversation for this batch.
3. **Re-check right before deleting.** `clear` re-hashes every file on the computer against the copy logs. A file that changed or appeared since the copy holds the whole folder back.
4. **Leave a trail.** Each emptied folder keeps its place and gets a READ-ME naming both drive paths. A manifest (every file, size, md5, both locations) is saved next to the register and on each drive.
5. **The owner decides what moves.** Claude suggests (by age and size); the owner fills the `need` column. Never move something marked `keep`.
6. **No drive that can't be trusted.** Don't use a drive that is read-only (NTFS on a Mac), failing a health check, or more than ~85% full. A network drive that is already nearly full is not a destination.

## Demo mode

If the user says "demo" (or `~/clear-the-mac-demo` exists and they want to practice), skip the interview. Use `~/clear-the-mac-demo/home` as `--root` and as the inventory folder, `~/clear-the-mac-demo/DRIVE_A` and `DRIVE_B` as the drives, `--min-mb 1`, and the register at `~/clear-the-mac-demo/register.csv`. Run every step and explain each one as it happens. Ask the user for the go before `clear`, exactly as you would for real. Finish by showing a READ-ME, then pulling one folder back.

## Step 0 — Interview (three questions, one at a time)

1. "Which two drives can we use, and roughly how much is free on each?" (Then check them yourself: `df -h`, `diskutil info`, filesystem type. Reject unusable ones under rule 6 and say why.)
2. "Where do you want to see the list of what moved — a spreadsheet file, Notion, Google Sheets, Airtable?" Default: the CSV register itself. If they pick a tool, mirror the register into it and keep both in step.
3. "Is anything off-limits — client records, legal or tax files, anything that must stay on this machine?" Write the answer into `notes` and default those rows to `keep`.

## Step 1 — Measure (show the owner the real problem)

- `df -h /` — free space and percent used.
- `sysctl vm.swapusage` and `memory_pressure` (macOS): a nearly-full disk starves swap, and a starved swap is what triggers "low memory" warnings. Say this plainly; it often explains the slowness better than RAM does.
- Biggest folders: `du -xhd 2 ~ 2>/dev/null | sort -h | tail -30`.
- Local snapshots: `tmutil listlocalsnapshots /` — these can hold deleted space for up to a day.

## Step 2 — Inventory into the register

```bash
python3 scripts/offload.py inventory ~/Desktop ~/Documents ~/Movies --register ~/offload/register.csv --min-mb 250
```

Each row: folder, size, how much of it is media, file count, last changed, and a **suggested** need (`archive` if untouched 12+ months, `pull back` if 3–12 months, `keep` if recent). Show the owner the top 20 by size and the total that `archive` + `pull back` would free.

## Step 3 — The owner decides

They fill `need` with `keep`, `archive` (rarely needed), or `pull back` (move it, but expect to want it back within ~90 days). Confirm the total before copying. If they want to change a row later, they just edit the cell.

## Step 4 — Copy and verify (safe; deletes nothing)

**Before a big copy (added 2026-11-11, after a copy froze and restarted the Mac):**
1. Start the memory guard in the background: `zsh scripts/memguard.sh &`. During big media copies macOS's icon service can balloon to tens of GB in minutes and freeze the computer; the guard stops it at 1.5 GB and macOS restarts it clean.
2. Close every Finder window that shows the destination drives. Browsing them while files land is what sets the icon service off.
3. Run big copies overnight or when no calls are planned, never during the owner's working day.
4. If an antivirus is installed, offer to exclude the external drives from real-time scanning for the copy; it re-reads every file.

```bash
python3 scripts/offload.py copy --register ~/offload/register.csv --drives "/Volumes/DRIVE_A" "/Volumes/DRIVE_B"
```

Run it in the background for big batches (USB hard drives do roughly 5–100 MB/s; tell the owner the estimate). Copies land at `<drive>/Mac-Offload/<same path as on the computer, relative to home>`. Rows with zero failures on both drives become `verified on both`. Re-running is safe: already-verified files are skipped.

## Step 5 — Check, then clear (only on the owner's word)

```bash
python3 scripts/offload.py check --register ... --drives ...           # read-only dry run
python3 scripts/offload.py clear --register ... --drives ... --confirm  # after the owner says go
```

Report every HOLD and why. Common holds: a file edited since the copy (re-run `copy`); Windows junk files (`Thumbs.db`, `desktop.ini`), which are ignored automatically; symlinks, which `copy` recreates on every drive (a folder holds only if a link is missing or differs; re-run `copy`); and **Locked files** (Finder's Locked flag): the folder is held whole rather than half-deleted. Unlock only with the owner's OK (`chflags nouchg <file>`), then re-run `clear`.

After clearing, `clear` rebuilds the day's manifest from the drive copy logs and prints `Manifest check: N folders, N files listed, 0 problems`. Report that line. Any PROBLEM line means stop and look before anything else is cleared.

**If free space doesn't rise after clearing**, local Time Machine snapshots are still holding the deleted files. They are released automatically within about a day, or when space runs low. Tell the owner; offer `sudo tmutil deletelocalsnapshots /` only if no backup is in progress.

## Step 6 — Pull back (any time)

```bash
python3 scripts/offload.py pullback "~/Desktop/Clients/Old Client" --register ... --drives ...
```

Copies from whichever drive is plugged in, verifies every file against the original checksum, removes the READ-ME, marks the row `pulled back`.

## Step 7 — What it was worth

```bash
python3 scripts/savings.py --freed-gb 64 --disk-gb 500 --drives-already-owned --tier-step-cost 400
```

Every price is an input with a labeled default; confirm current prices before quoting a number to anyone. Lead with the honest insight: **gigabytes on an external drive are cheap; the real money is in buying the next computer with the storage you actually need, not the storage your fear tells you to buy.** A 1 TB → 2 TB step at purchase typically costs a few hundred dollars; this system is what makes the smaller tier safe.

## Step 8 — Make it a habit (so it never fills up again)

Offer, don't impose:
- **A trigger, not a calendar:** when free space drops below a line the owner picks (e.g. 50 GB), run Step 2 for new folders only (`inventory` skips folders already in the register).
- **One drive leaves the house.** Two copies in the same room are one fire away from zero copies. Suggest keeping one drive at the office or with family and swapping monthly.
- **Run it by hand a few times before automating it.** Once it has worked several times, a scheduled job can run the inventory and send the owner the list.

## Output to the owner

A short report: space before → after, folders moved (count, GB), holds and why, where the register and manifest live, the savings table, and the one-line pull-back instruction. Plain language, no jargon.
