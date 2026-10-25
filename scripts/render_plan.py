"""Re-render the day-level tables in plans/plan.md from data/plan.csv.

Usage: python3 scripts/render_plan.py
Overwrites everything between <!-- PLAN:START --> and <!-- PLAN:END --> in plans/plan.md.
Week 1 starts on the Monday of the earliest date in data/plan.csv.
"""
import csv
import datetime as dt
from collections import defaultdict

MD = "plans/plan.md"
START, END = "<!-- PLAN:START -->", "<!-- PLAN:END -->"
MARK = {"done": " ✅", "skipped": " ❌", "moved": " ↪ moved", "planned": ""}

rows = list(csv.DictReader(open("data/plan.csv", encoding="utf-8")))
out = []
if rows:
    first = min(dt.date.fromisoformat(r["date"]) for r in rows)
    w1 = first - dt.timedelta(days=first.weekday())
    byweek = defaultdict(list)
    for r in rows:
        byweek[int(r["week"])].append(r)
    for wk in sorted(byweek):
        rs = byweek[wk]
        mon = w1 + dt.timedelta(7 * (wk - 1))
        sun = mon + dt.timedelta(6)
        hrs = sum(int(r["duration_min"] or 0) for r in rs if r["status"] in ("planned", "done")) / 60
        out.append(f"### Week {wk}: {mon:%d %b} – {sun:%d %b %Y} · Phase {rs[0]['block']} · ~{hrs:.1f} h\n")
        out.append("| Date | Day | Sessions | Nutrition |\n|---|---|---|---|")
        for date in sorted(dict.fromkeys(r["date"] for r in rs)):
            ds = [r for r in rs if r["date"] == date]
            sess = "<br>".join(
                (f"~~{r['slot']}: {r['session']}~~" if r["status"] == "moved" else f"{r['slot']}: **{r['session']}**")
                + (f" {r['duration_min']}′" if r["duration_min"] else "")
                + MARK.get(r["status"], f" ({r['status']})")
                for r in ds
            )
            nut = next((r for r in ds if r["status"] in ("planned", "done")), ds[0])["nutrition"]
            out.append(f"| {date[5:]} | {ds[0]['day']} | {sess} | {nut} |")
        out.append("")

s = open(MD, encoding="utf-8").read()
a, b = s.index(START) + len(START), s.index(END)
open(MD, "w", encoding="utf-8").write(s[:a] + "\n" + "\n".join(out) + s[b:])
print("rendered", len(rows), "rows")
