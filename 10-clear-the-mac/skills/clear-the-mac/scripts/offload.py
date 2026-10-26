#!/usr/bin/env python3
"""offload.py — move big, rarely-used folders off a computer onto two external drives, safely.

The register (a CSV) is the single source of truth. Every row is one folder.
Nothing is ever deleted unless `clear --confirm` is run, and even then only for
folders whose every file is re-hashed and matched against BOTH drive copies.

Commands
  inventory ROOT [ROOT...] --register R.csv [--min-mb 250]   list big folders into the register
  copy      --register R.csv --drives A B [--root ~]          copy rows marked archive/pull-back to both drives, md5-verify
  check     --register R.csv --drives A B [--root ~]          re-hash the computer's files against the drive logs (read-only)
  clear     --register R.csv --drives A B [--root ~] --confirm  empty verified folders, leave a READ-ME, write the manifest
  pullback  "folder path" --register R.csv --drives A B [--root ~]  copy a cleared folder back and verify it
  status    --register R.csv                                  totals by stage

Stdlib only. Tested on macOS; works anywhere Python 3.8+ runs.
"""
import argparse, csv, datetime as dt, hashlib, os, shutil, sys, time

IGNORE = {".DS_Store", "Thumbs.db", "desktop.ini", "Icon\r", ".localized"}
MEDIA = {".mov", ".mp4", ".m4v", ".avi", ".mkv", ".mts", ".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff",
         ".raw", ".cr2", ".cr3", ".nef", ".arw", ".dng", ".psd", ".wav", ".mp3", ".m4a", ".aif", ".aiff", ".flac"}
FIELDS = ["id", "item", "path", "size_gb", "media_gb", "files", "last_changed", "suggested", "need",
          "stage", "on_drive_a", "on_drive_b", "verified_on", "cleared_on", "notes"]
MOVE_NEEDS = {"archive", "pull back"}
README = "READ-ME - moved to external drives.md"
OFFLOAD_DIR = "Mac-Offload"
TODAY = dt.date.today().isoformat()


def skip(name):
    return name in IGNORE or name.startswith("._")


def walk_files(top):
    for root, dirs, files in os.walk(top):
        dirs[:] = [d for d in dirs if not d.startswith(".Trash")]
        for name in files:
            if skip(name) or name == README:
                continue
            yield os.path.join(root, name)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def read_register(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def write_register(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def need_of(row):
    return row.get("need", "").strip().lower()


def rel_of(row, root):
    return os.path.relpath(os.path.expanduser(row["path"]), root)


def drive_target(drive, rel):
    return os.path.join(drive, OFFLOAD_DIR, rel)


def log_path(register, drive, rel):
    safe = "".join(c if c.isalnum() else "-" for c in rel).strip("-")[-120:]
    folder = os.path.join(os.path.dirname(os.path.abspath(register)), "offload-logs")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{os.path.basename(drive.rstrip('/'))}__{safe}.tsv")


def read_log(path):
    if not os.path.exists(path):
        return {}
    with open(path, newline="") as fh:
        return {r["relpath"]: r for r in csv.DictReader(fh, delimiter="\t") if r["status"] == "VERIFIED"}


# ---------- inventory ----------

def folder_stats(top):
    size = media = count = 0
    newest = 0.0
    for f in walk_files(top):
        try:
            st = os.lstat(f)
        except OSError:
            continue
        size += st.st_size
        count += 1
        newest = max(newest, st.st_mtime)
        if os.path.splitext(f)[1].lower() in MEDIA:
            media += st.st_size
    return size, media, count, newest


def pick_folders(top, min_bytes, depth=0, max_depth=4):
    """Emit folders >= min_bytes; split a big folder into its children when they hold most of it."""
    size, media, count, newest = folder_stats(top)
    if size < min_bytes:
        return []
    subs = [os.path.join(top, d) for d in sorted(os.listdir(top))
            if os.path.isdir(os.path.join(top, d)) and not os.path.islink(os.path.join(top, d)) and not d.startswith(".")]
    if depth < max_depth and size >= 4 * min_bytes and subs:
        sub_sizes = {s: folder_stats(s)[0] for s in subs}
        if sum(v for v in sub_sizes.values() if v >= min_bytes) >= 0.6 * size:
            out = []
            for s in subs:
                if sub_sizes[s] >= min_bytes:
                    out += pick_folders(s, min_bytes, depth + 1, max_depth)
            return out
    return [(top, size, media, count, newest)]


def suggest(newest):
    age_days = (time.time() - newest) / 86400 if newest else 9999
    if age_days > 365:
        return "archive"
    if age_days > 90:
        return "pull back"
    return "keep"


def cmd_inventory(a):
    rows = read_register(a.register)
    known = {os.path.expanduser(r["path"]) for r in rows}
    next_id = max([int(r["id"]) for r in rows if r.get("id", "").isdigit()] + [0]) + 1
    added = 0
    for root in a.roots:
        root = os.path.abspath(os.path.expanduser(root))
        for path, size, media, count, newest in pick_folders(root, a.min_mb * 1_000_000):
            if path in known:
                continue
            rows.append({"id": str(next_id), "item": os.path.basename(path), "path": path,
                         "size_gb": f"{size / 1e9:.2f}", "media_gb": f"{media / 1e9:.2f}", "files": str(count),
                         "last_changed": dt.date.fromtimestamp(newest).isoformat() if newest else "",
                         "suggested": suggest(newest), "need": "", "stage": "on computer",
                         "on_drive_a": "", "on_drive_b": "", "verified_on": "", "cleared_on": "", "notes": ""})
            next_id += 1
            added += 1
            print(f"  {size / 1e9:7.2f} GB  {suggest(newest):9s}  {path}")
    rows.sort(key=lambda r: -float(r["size_gb"] or 0))
    write_register(a.register, rows)
    print(f"{added} new rows -> {a.register}. Fill the 'need' column: keep / archive / pull back.")


# ---------- copy ----------

def copy_folder(src, dst, logfile):
    done = read_log(logfile)
    new = not os.path.exists(logfile)
    copied = same = failed = 0
    with open(logfile, "a", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        if new:
            w.writerow(["relpath", "bytes", "md5_src", "md5_dst", "status", "utc"])
        for f in walk_files(src):
            if os.path.islink(f):
                continue
            rel = os.path.relpath(f, src)
            target = os.path.join(dst, rel)
            src_hash = md5(f)
            if rel in done and done[rel]["md5_src"] == src_hash and os.path.exists(target):
                same += 1
                continue
            status, dst_hash = "FAILED", ""
            for _ in range(3):
                try:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.copy2(f, target)
                    dst_hash = md5(target)
                    if dst_hash == src_hash:
                        status = "VERIFIED"
                        break
                except OSError as e:
                    dst_hash = f"error: {e}"
            w.writerow([rel, os.path.getsize(f), src_hash, dst_hash, status,
                        dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")])
            fh.flush()
            if status == "VERIFIED":
                copied += 1
            else:
                failed += 1
                print(f"    FAILED {rel}: {dst_hash}")
    return copied, same, failed


def cmd_copy(a):
    rows = read_register(a.register)
    root = os.path.expanduser(a.root)
    for d in a.drives:
        if not os.path.isdir(d):
            sys.exit(f"Drive not mounted: {d}")
    for r in rows:
        if need_of(r) not in MOVE_NEEDS or r["stage"] not in ("on computer", "copying"):
            continue
        src, rel = os.path.expanduser(r["path"]), rel_of(r, root)
        r["stage"] = "copying"
        write_register(a.register, rows)
        ok = []
        for i, d in enumerate(a.drives):
            c, s, f = copy_folder(src, drive_target(d, rel), log_path(a.register, d, rel))
            print(f"  {os.path.basename(d.rstrip('/'))}: copied {c}  already identical {s}  FAILED {f}  {r['item']}")
            r["on_drive_a" if i == 0 else "on_drive_b"] = "yes" if f == 0 else ""
            ok.append(f == 0)
        if all(ok):
            r["stage"], r["verified_on"] = "verified on both", TODAY
        write_register(a.register, rows)


# ---------- check / clear ----------

def check_row(r, a, root):
    src, rel = os.path.expanduser(r["path"]), rel_of(r, root)
    logs = [read_log(log_path(a.register, d, rel)) for d in a.drives]
    problems, files, size = [], 0, 0
    if not os.path.isdir(src):
        return ["folder missing on computer"], 0, 0
    for f in walk_files(src):
        rel_f = os.path.relpath(f, src)
        if os.path.islink(f):
            problems.append(f"symlink not copied: {rel_f}")
            continue
        files += 1
        size += os.path.getsize(f)
        h = md5(f)
        for d, log in zip(a.drives, logs):
            entry = log.get(rel_f)
            target = os.path.join(drive_target(d, rel), rel_f)
            if not entry:
                problems.append(f"{os.path.basename(d)}: never copied {rel_f}")
            elif entry["md5_src"] != h:
                problems.append(f"{os.path.basename(d)}: changed since copy {rel_f}")
            elif not os.path.isfile(target) or os.path.getsize(target) != os.path.getsize(f):
                problems.append(f"{os.path.basename(d)}: missing on drive {rel_f}")
    return problems, files, size


def candidates(rows):
    return [r for r in rows if r["stage"] == "verified on both" and need_of(r) in MOVE_NEEDS]


def cmd_check(a):
    rows, root = read_register(a.register), os.path.expanduser(a.root)
    for r in candidates(rows):
        problems, files, size = check_row(r, a, root)
        print(("PASS " if not problems else "HOLD ") + f"{files:6d} files {size / 1e9:7.2f} GB  {r['path']}")
        for p in problems[:5]:
            print("       " + p)


def cmd_clear(a):
    if not a.confirm:
        sys.exit("clear deletes files from this computer. Re-run with --confirm once the owner has said so.")
    for d in a.drives:
        if not os.path.isdir(d):
            sys.exit(f"Drive not mounted: {d}")
    rows, root = read_register(a.register), os.path.expanduser(a.root)
    manifest_dir = os.path.join(os.path.dirname(os.path.abspath(a.register)), "manifests")
    os.makedirs(manifest_dir, exist_ok=True)
    manifest = os.path.join(manifest_dir, f"{TODAY}_offload-manifest.tsv")
    first = not os.path.exists(manifest)
    freed = 0
    with open(manifest, "a", newline="") as mf:
        w = csv.writer(mf, delimiter="\t")
        if first:
            w.writerow(["folder", "relpath", "bytes", "md5"] + [f"drive_{i + 1}" for i in range(len(a.drives))])
        for r in candidates(rows):
            problems, files, size = check_row(r, a, root)
            if problems:
                print(f"HOLD  {r['path']}  ({problems[0]})")
                continue
            src, rel = os.path.expanduser(r["path"]), rel_of(r, root)
            log = read_log(log_path(a.register, a.drives[0], rel))
            for rel_f, e in sorted(log.items()):
                w.writerow([r["path"], rel_f, e["bytes"], e["md5_src"]] +
                           [os.path.join(drive_target(d, rel), rel_f) for d in a.drives])
            for name in os.listdir(src):
                p = os.path.join(src, name)
                if os.path.isdir(p) and not os.path.islink(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            with open(os.path.join(src, README), "w") as fh:
                fh.write(f"# This folder was moved off this computer\n\nMoved {TODAY}. {files} files, "
                         f"{size / 1e9:.2f} GB, md5-verified on every drive below.\n\n" +
                         "".join(f"- {drive_target(d, rel)}\n" for d in a.drives) +
                         "\nTo bring it back, plug in either drive and run the pullback command, "
                         "or ask Claude to \"pull back\" this folder.\n")
            r["stage"], r["cleared_on"] = "removed from computer", TODAY
            write_register(a.register, rows)
            freed += size
            print(f"CLEARED {files} files {size / 1e9:.2f} GB  {r['path']}")
    if freed:
        for d in a.drives:
            os.makedirs(os.path.join(d, OFFLOAD_DIR), exist_ok=True)
            shutil.copy2(manifest, os.path.join(d, OFFLOAD_DIR, os.path.basename(manifest)))
    print(f"Freed {freed / 1e9:.2f} GB. Manifest: {manifest} (copied to each drive).")
    print("If free space does not rise, local snapshots (Time Machine) are still holding the files; they expire on their own.")


def cmd_pullback(a):
    rows, root = read_register(a.register), os.path.expanduser(a.root)
    target = os.path.abspath(os.path.expanduser(a.folder))
    row = next((r for r in rows if os.path.abspath(os.path.expanduser(r["path"])) == target), None)
    if not row:
        sys.exit("That folder is not in the register.")
    rel = rel_of(row, root)
    drive = next((d for d in a.drives if os.path.isdir(drive_target(d, rel))), None)
    if not drive:
        sys.exit("Neither drive has this folder mounted right now.")
    log = read_log(log_path(a.register, drive, rel))
    bad = 0
    for rel_f, e in log.items():
        src = os.path.join(drive_target(drive, rel), rel_f)
        dst = os.path.join(target, rel_f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        if md5(dst) != e["md5_src"]:
            bad += 1
            print(f"  MISMATCH {rel_f}")
    if bad == 0:
        readme = os.path.join(target, README)
        if os.path.exists(readme):
            os.remove(readme)
        row["stage"] = "pulled back"
        row["notes"] = (row.get("notes", "") + f" Pulled back {TODAY}.").strip()
        write_register(a.register, rows)
    print(f"Restored {len(log) - bad} of {len(log)} files from {drive}.")


def cmd_status(a):
    totals = {}
    for r in read_register(a.register):
        t = totals.setdefault(r["stage"] or "?", [0, 0.0])
        t[0] += 1
        t[1] += float(r["size_gb"] or 0)
    for stage, (n, gb) in sorted(totals.items()):
        print(f"{stage:24s} {n:4d} folders {gb:8.1f} GB")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("inventory"); s.add_argument("roots", nargs="+"); s.add_argument("--min-mb", type=int, default=250)
    for name in ("copy", "check", "clear", "pullback"):
        s = sub.add_parser(name)
        if name == "pullback":
            s.add_argument("folder")
        s.add_argument("--drives", nargs=2, required=True, metavar=("DRIVE_A", "DRIVE_B"))
        s.add_argument("--root", default="~", help="paths on the drives are stored relative to this (default: home)")
        if name == "clear":
            s.add_argument("--confirm", action="store_true")
    sub.add_parser("status")
    for s in sub.choices.values():
        s.add_argument("--register", required=True)
    a = p.parse_args()
    {"inventory": cmd_inventory, "copy": cmd_copy, "check": cmd_check, "clear": cmd_clear,
     "pullback": cmd_pullback, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
