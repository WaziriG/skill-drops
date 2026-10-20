"""Regression tests for inbox_enrich.py 1.1. Invented people and addresses only.

Run from the kit folder:  python3 -m unittest discover -s scripts/tests -v
"""
import csv, datetime as dt, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
SCRIPT = KIT / "scripts" / "inbox_enrich.py"
sys.path.insert(0, str(SCRIPT.parent))
import inbox_enrich as ie  # noqa: E402

ME = {"alex@yourfirm.example"}
TODAY = ie.TODAY
D = lambda n: (TODAY - dt.timedelta(days=n))
OPTS = {"full": False, "template": "", "cadence_options": ie.DEFAULT_CADENCE_OPTIONS, "cadence_select": False}
SELECT_OPTS = {**OPTS, "cadence_select": True}


def msg(i, days_ago, sender, to, cc=(), subject="Project update", text="Hello."):
    return {"id": f"m{i}", "date": D(days_ago), "ts": D(days_ago).isoformat(), "seq": i,
            "from": ("", sender), "to": [("", a) for a in to], "cc": [("", a) for a in cc], "subject": subject, "text": text}


def person(row, i=0):
    return ie.to_person(row, i)


def run(rows, records, opts=OPTS, summarizer=None):
    people = [person(r, i) for i, r in enumerate(rows)]
    by_addr, by_name = ie.index_mail(records)
    found = {p["index"]: ie.match(p, by_addr, by_name) for p in people}
    changes, failed = ie.build_changes(people, found, ME, opts, summarizer)
    return {c["name"]: c for c in changes}


def stored(**kw):
    base = {"Name": "Jordan Vale", "Email": "jordan@valeworks.example", "Know Them?": "Yes"}
    base.update(kw)
    return base


JORDAN = "jordan@valeworks.example"
OTHER = "pat@thirdparty.example"


class IncrementalKeepsHistory(unittest.TestCase):
    """Bug 1: an incremental run treated a partial window as the whole history."""

    def test_adds_new_mail_to_stored_totals(self):
        row = stored(**{"Emails Exchanged": "318", "Email Threads": "120", "First Email": "2019-04-02",
                        "Last Email": D(10).isoformat(), "Last Email From": "Me", "Inbox Checked": D(7).isoformat(),
                        "Relationship Context": "Long-running partner since 2019."})
        new = [msg(1, 5, JORDAN, ["alex@yourfirm.example"], subject="New idea"), msg(2, 3, "alex@yourfirm.example", [JORDAN], subject="Re: New idea")]
        c = run([row], new)["Jordan Vale"]
        f = c["fields"]
        self.assertEqual(c["mode"], "incremental")
        self.assertEqual(f["Emails Exchanged"], 320)
        self.assertEqual(f["Email Threads"], 121)
        self.assertNotIn("First Email", f)                # the earlier First Email is kept
        self.assertNotIn("Relationship Context", f)       # no summary: stored context untouched
        self.assertEqual(f["Last Email"], D(3).isoformat())
        self.assertEqual(f["Last Email From"], "Me")

    def test_no_new_mail_changes_nothing(self):
        row = stored(**{"Emails Exchanged": "204", "Last Email": D(40).isoformat(), "Last Email From": "Them",
                        "Inbox Checked": D(7).isoformat(), "Relationship Context": "Board member."})
        self.assertEqual(run([row], []), {})
        old_only = [msg(1, 40, JORDAN, ["alex@yourfirm.example"])]
        self.assertEqual(run([row], old_only), {})

    def test_full_run_with_no_mail_never_zeroes_stored_history(self):
        row = stored(**{"Emails Exchanged": "204", "Last Email": D(40).isoformat(), "Inbox Checked": D(7).isoformat()})
        c = run([row], [], {**OPTS, "full": True})["Jordan Vale"]
        self.assertEqual(c["kind"], "kept")
        self.assertEqual(c["fields"], {})

    def test_context_merges_instead_of_rewriting(self):
        row = stored(**{"Emails Exchanged": "50", "Last Email": D(20).isoformat(), "Last Email From": "Me",
                        "Inbox Checked": D(14).isoformat(), "Relationship Context": "Worked together on the 2024 launch."})
        summarizer = lambda p, msgs, existing, cutoff: {"whats_new": "Asked about a second project.", "open_loops": "None"}
        f = run([row], [msg(1, 2, JORDAN, ["alex@yourfirm.example"])], summarizer=summarizer)["Jordan Vale"]["fields"]
        self.assertTrue(f["Relationship Context"].startswith("Worked together on the 2024 launch."))
        self.assertTrue(f["Relationship Context"].endswith(f"{TODAY.isoformat()}: Asked about a second project."))

    def test_split_runs_equal_one_full_run_on_mock_inbox(self):
        """Full run on mail up to day X, then an incremental run on everything, must land on the full-run totals."""
        rows, _ = ie.read_table(KIT / "mock" / "people-spine.csv", None)
        records = ie.load_mbox(KIT / "mock" / "mock-inbox.mbox")
        cut = D(20)
        first = run([dict(r) for r in rows], [r for r in records if r["date"] <= cut], {**OPTS, "full": True})
        staged = []
        for r in rows:
            r = dict(r)
            c = first.get(r["Name"])
            if c:
                r.update(c["fields"])
                r["Inbox Checked"] = cut.isoformat()
            staged.append(r)
        incremental = run(staged, records)
        full = run([dict(r) for r in rows], records, {**OPTS, "full": True})
        checked = 0
        for i, r in enumerate(staged):
            name = r["Name"]
            merged = dict(r)
            if name in incremental:
                merged.update(incremental[name]["fields"])
            want = full[name]["fields"]
            for col in ("Emails Exchanged", "First Email", "Last Email", "Last Email From"):
                self.assertEqual(str(merged.get(col, "")), str(want.get(col, "")), f"{name}: {col}")
            checked += 1
        self.assertEqual(checked, 30)


class LastWordIsBetweenTwoPeople(unittest.TestCase):
    """Bug 2: cc-only and third-party mail set Last Email From = Them."""

    def setUp(self):
        self.base = [msg(1, 30, JORDAN, ["alex@yourfirm.example"]), msg(2, 25, "alex@yourfirm.example", [JORDAN])]

    def test_cc_only_message_does_not_flip_last_from(self):
        mail = self.base + [msg(3, 4, OTHER, ["alex@yourfirm.example"], cc=[JORDAN])]
        c = run([stored()], mail)["Jordan Vale"]
        self.assertEqual(c["fields"]["Emails Exchanged"], 3)      # still counts toward volume
        self.assertEqual(c["fields"]["Last Email From"], "Me")
        self.assertEqual(c["fields"]["Last Email"], D(25).isoformat())
        self.assertNotEqual(c["computed"]["Follow-up Status"], "Reply owed")

    def test_person_writing_to_someone_else_is_not_them(self):
        mail = self.base + [msg(3, 4, JORDAN, [OTHER], cc=["alex@yourfirm.example"])]
        self.assertEqual(run([stored()], mail)["Jordan Vale"]["fields"]["Last Email From"], "Me")

    def test_owner_cc_to_person_is_not_me(self):
        mail = [msg(1, 10, JORDAN, ["alex@yourfirm.example"]), msg(2, 4, "alex@yourfirm.example", [OTHER], cc=[JORDAN])]
        self.assertEqual(run([stored()], mail)["Jordan Vale"]["fields"]["Last Email From"], "Them")

    def test_incremental_third_party_only_keeps_stored_last_from(self):
        row = stored(**{"Emails Exchanged": "12", "Last Email": D(20).isoformat(), "Last Email From": "Me",
                        "Inbox Checked": D(14).isoformat()})
        f = run([row], [msg(9, 3, OTHER, ["alex@yourfirm.example"], cc=[JORDAN])])["Jordan Vale"]["fields"]
        self.assertEqual(f["Emails Exchanged"], 13)
        self.assertNotIn("Last Email From", f)
        self.assertNotIn("Last Email", f)

    def test_know_them_no_is_never_reply_owed(self):
        mail = [msg(1, 3, JORDAN, ["alex@yourfirm.example"])]
        self.assertEqual(run([stored()], mail)["Jordan Vale"]["computed"]["Follow-up Status"], "Reply owed")
        self.assertNotEqual(run([stored(**{"Know Them?": "No"})], mail)["Jordan Vale"]["computed"]["Follow-up Status"], "Reply owed")


class OwnerColumnsStayTheOwners(unittest.TestCase):
    """Bugs 3 and 4: cadence written as a number over a select; Next Step written by automation."""

    mail = [msg(1, 30, JORDAN, ["alex@yourfirm.example"]), msg(2, 3, "alex@yourfirm.example", [JORDAN])]

    def test_existing_cadence_is_untouched(self):
        for value in ("Monthly", "45", "Twice a year"):
            f = run([stored(**{"Follow-up Cadence": value})], self.mail, SELECT_OPTS)["Jordan Vale"]["fields"]
            self.assertNotIn("Follow-up Cadence", f, value)

    def test_blank_cadence_uses_store_option_names(self):
        f = run([stored(Priority="A")], self.mail, SELECT_OPTS)["Jordan Vale"]["fields"]
        self.assertEqual(f["Follow-up Cadence"], "Monthly")
        self.assertIn(f["Follow-up Cadence"], ie.DEFAULT_CADENCE_OPTIONS)
        self.assertEqual(run([stored(Priority="A")], self.mail)["Jordan Vale"]["fields"]["Follow-up Cadence"], 30)

    def test_label_cadence_drives_status(self):
        c = run([stored(**{"Follow-up Cadence": "Every 2 weeks"})], [msg(1, 20, "alex@yourfirm.example", [JORDAN])], SELECT_OPTS)
        self.assertEqual(c["Jordan Vale"]["computed"]["Follow-up Status"], "Overdue")

    def test_next_step_is_never_written(self):
        summarizer = lambda p, msgs, existing, cutoff: {"relationship_context": "Met at a dinner.", "open_loops": "Send the deck.",
                                                       "next_step": "Email them now.", "suggested_can_help_with": ""}
        row = stored(**{"Next Step": "PAUSED until January. No outreach."})
        c = run([row], self.mail, summarizer=summarizer)["Jordan Vale"]
        self.assertNotIn("Next Step", c["fields"])
        self.assertIn("Next Step", ie.OWNER_COLS)
        self.assertNotIn("Next Step", ie.MACHINE_COLS)

    def test_formulas_are_kept_out_of_fields(self):
        c = run([stored()], self.mail)["Jordan Vale"]
        self.assertFalse(set(c["fields"]) & set(ie.FORMULA_COLS))
        self.assertEqual(set(c["computed"]), set(ie.FORMULA_COLS))


class OpenLoopsOnlyGrow(unittest.TestCase):
    """Bug 5: Open Loops was replaced on every run."""

    def row(self):
        return stored(**{"Emails Exchanged": "8", "Last Email": D(20).isoformat(), "Last Email From": "Me",
                         "Inbox Checked": D(14).isoformat(), "Relationship Context": "Peer.",
                         "Open Loops": "2026-09-01: You promised to send the pricing note."})

    def loops(self, new_loop):
        s = lambda p, msgs, existing, cutoff: {"whats_new": "", "open_loops": new_loop}
        return run([self.row()], [msg(1, 2, JORDAN, ["alex@yourfirm.example"])], summarizer=s)["Jordan Vale"]["fields"].get("Open Loops")

    def test_appends_with_date_prefix(self):
        value = self.loops("They asked for two intro names.")
        self.assertTrue(value.startswith("2026-09-01: You promised to send the pricing note.\n"))
        self.assertTrue(value.endswith(f"{TODAY.isoformat()}: They asked for two intro names."))

    def test_duplicate_and_none_change_nothing(self):
        self.assertIsNone(self.loops("You promised to send the pricing note."))
        self.assertIsNone(self.loops("None"))


class CommandLine(unittest.TestCase):
    """End to end through the CLI on a CSV spine: full run, then a connector-style incremental run."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def cli(self, *args):
        out = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout

    def write_msgs(self, name, msgs):
        path = self.tmp / name
        path.write_text(json.dumps([{"id": m["id"], "date": m["date"].isoformat(), "from": m["from"][1],
                                     "to": ", ".join(a for _, a in m["to"]), "cc": ", ".join(a for _, a in m["cc"]),
                                     "subject": m["subject"], "text": m["text"]} for m in msgs]))
        return path

    def test_incremental_after_full_keeps_totals_and_owner_columns(self):
        spine = self.tmp / "people.csv"
        shutil.copy(KIT / "mock" / "people-spine.csv", spine)
        rows, head = ie.read_table(spine, None)
        rows[0]["Next Step"] = "No outreach until the board meeting."
        rows[0]["Follow-up Cadence"] = "45"
        with open(spine, "w", newline="") as fh:
            w = csv.DictWriter(fh, head)
            w.writeheader()
            w.writerows(rows)
        self.cli("--people", str(spine), "--mbox", str(KIT / "mock" / "mock-inbox.mbox"), "--me", "alex@yourfirm.example", "--apply")
        after_full = {r["Name"]: r for r in ie.read_table(spine, None)[0]}
        avery = after_full["Avery Calderwood"]
        self.assertEqual(avery["Next Step"], "No outreach until the board meeting.")
        self.assertEqual(avery["Follow-up Cadence"], "45")
        # the next weekly run: the connector returns only mail since Inbox Checked
        week = [msg(1, 0, "avery@ashgrovecapital.example", ["alex@yourfirm.example"], subject="Quick one"),
                msg(2, 0, "alex@yourfirm.example", ["avery@ashgrovecapital.example"], subject="Re: Quick one"),
                msg(3, 0, OTHER, ["alex@yourfirm.example"], cc=["avery@ashgrovecapital.example"], subject="Fwd: intro")]
        rows, head = ie.read_table(spine, None)
        for r in rows:  # pretend the full run happened yesterday
            if r["Inbox Checked"]:
                r["Inbox Checked"] = D(1).isoformat()
        with open(spine, "w", newline="") as fh:
            w = csv.DictWriter(fh, head)
            w.writeheader()
            w.writerows(rows)
        out_json = self.tmp / "changes.json"
        self.cli("--people", str(spine), "--messages-json", str(self.write_msgs("week.json", week)), "--me", "alex@yourfirm.example",
                 "--out", str(out_json), "--apply")
        after = {r["Name"]: r for r in ie.read_table(spine, None)[0]}
        a = after["Avery Calderwood"]
        self.assertEqual(int(a["Emails Exchanged"]), int(avery["Emails Exchanged"]) + 3)
        self.assertEqual(a["First Email"], avery["First Email"])
        self.assertEqual(a["Relationship Context"], avery["Relationship Context"])
        self.assertEqual(a["Last Email From"], "Me")
        self.assertEqual(a["Next Step"], "No outreach until the board meeting.")
        self.assertEqual(a["Follow-up Cadence"], "45")
        for name, r in after.items():  # nobody without new mail lost history
            if name != "Avery Calderwood":
                self.assertEqual(r["Emails Exchanged"], after_full[name]["Emails Exchanged"], name)
        changes = json.loads(out_json.read_text())
        self.assertEqual([u["name"] for u in changes["updates"]], ["Avery Calderwood"])
        for u in changes["updates"]:
            self.assertFalse(set(u["fields"]) & (set(ie.FORMULA_COLS) | set(ie.OWNER_COLS)))

    def test_demo_numbers(self):
        out = self.cli("--people", str(KIT / "mock" / "people-spine.csv"), "--feeder", str(KIT / "mock" / "linkedin-feeder.csv"),
                       "--mbox", str(KIT / "mock" / "mock-inbox.mbox"), "--me", "alex@yourfirm.example", "--search-link", "gmail")
        self.assertIn("History updated: 29", out)
        self.assertIn("Replies owed: 9", out)
        self.assertIn("NEW PEOPLE (2+ emails each way, not in the spine): 3", out)

    def test_column_map_and_cadence_select_from_config(self):
        spine = self.tmp / "people.json"
        spine.write_text(json.dumps([{"id": "p1", "Name": "Jordan Vale", "Email": JORDAN, "Know Them?": "Yes", "Priority": "B",
                                      "Follow-up Cadence": "", "Gmail History": ""}]))
        cfg = self.tmp / "config.json"
        cfg.write_text(json.dumps({"my_addresses": ["alex@yourfirm.example"], "store": "notion", "search_link": "gmail",
                                   "notion": {"column_map": {"Mail Search Link": "Gmail History"},
                                              "follow_up_cadence_is_select": ie.DEFAULT_CADENCE_OPTIONS}}))
        out_json = self.tmp / "changes.json"
        self.cli("--people", str(spine), "--config", str(cfg), "--out", str(out_json),
                 "--messages-json", str(self.write_msgs("m.json", [msg(1, 5, JORDAN, ["alex@yourfirm.example"])])))
        f = json.loads(out_json.read_text())["updates"][0]["fields"]
        self.assertIn("Gmail History", f)
        self.assertNotIn("Mail Search Link", f)
        self.assertEqual(f["Follow-up Cadence"], "Every 6 weeks")


if __name__ == "__main__":
    unittest.main()
