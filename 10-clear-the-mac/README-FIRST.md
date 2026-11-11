# Clear the Mac: start here

My MacBook Pro had 11 GB free on a 500 GB disk, and it kept telling me memory was low. The real cause was the disk. macOS uses spare disk space when memory fills up, and there wasn't any left.

The files stayed on the laptop for a reason you'll probably recognize. Once something moves to an external drive, it might as well be gone: you don't know what went where, or whether the copy is any good. So the fix had to be tracking first and moving second.

`/clear-the-mac` lists your big folders and lets you decide what moves. It copies each approved folder to **two** drives and fingerprint-checks every file on both. It deletes nothing until you say so, and it checks every file again right before it does. Each emptied folder keeps a READ-ME saying where its files went, and one sentence brings a folder back.

My first run moved 64 GB in an afternoon plus one night of copying. The Mac went from **11 GB to 71 GB free**, and nothing was lost. The numbers are in `sample-run/2026-10-25-first-run.md`.

## What you need

- Claude Code on a Mac (any computer with Python 3.8+ works)
- Two external drives your computer can write to. On a Mac, an NTFS drive is read-only and won't work.
- About fifteen minutes of decisions. The copying runs on its own.

## 1. Install the skill (one minute)

```
cp -R skills/clear-the-mac ~/.claude/skills/
```

## 2. Watch it on pretend files first (five minutes)

```
bash demo/make-demo.sh
```

That builds a pretend computer and two pretend drives in `~/clear-the-mac-demo`. Then open Claude Code and type:

```
/clear-the-mac demo
```

You'll see the whole cycle: list, decide, copy, check, clear, pull back. It all happens on files that don't matter.

## 3. Run it for real

```
/clear-the-mac
```

Claude asks three questions: which drives, where you want to see the list (a spreadsheet, Notion, Google Sheets or Airtable), and whether anything is off-limits. Then it shows what's taking up your space and suggests what to move. You decide.

## The rules it keeps

- **Two copies or no move.** Every file is checked on both drives.
- **Nothing is deleted until you say so,** and every file is checked again right before.
- **A trail stays behind:** a READ-ME in each emptied folder, plus a manifest of every file.
- **Anything you mark *keep* is never touched.**

## What it's worth

```
python3 skills/clear-the-mac/scripts/savings.py --freed-gb 64 --drives-already-owned --tier-step-cost 400
```

Every price in the calculator is an input, so put in your own. Here's what I found: the gigabytes themselves are cheap, since two drive copies cost about 7× less than built-in storage. The real saving is buying your next computer with the storage you actually need and putting that money into memory. That's where the slowness was coming from.

## If your free space doesn't go up right away

Time Machine keeps local snapshots that can hold deleted files for up to a day. Mine released on their own a few hours later.

## Make it a habit

- **Use a trigger, not a calendar.** When free space drops below a line you pick, run it again. It only lists folders that are new since last time.
- **Keep one drive somewhere else.** Two copies in the same room are one fire away from zero copies.

## What's in this folder

- `skills/clear-the-mac/`: the skill (`SKILL.md`) and two scripts that use only standard Python, with nothing to install
- `demo/make-demo.sh`: the pretend computer
- `sample-run/`: my first run, with the real numbers
- `CLEAR-THE-MAC-GUIDE.pdf`: a one-page version to share

## What's new in v1.1 (2026-11-11)
- `scripts/memguard.sh`: run it during big copies. It stops macOS's icon service if it balloons, which can otherwise freeze the computer mid-copy.
- Folders containing Locked files are held whole instead of being half-deleted.
- Symlinks are recreated on both drives, so folders that contain them can be cleared.
- After every clear, the manifest is rebuilt from the drive copy logs and checked, so the file list is always complete.
