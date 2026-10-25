# Tracker – working conventions (for the AI agent)

Personal health, food and fitness tracker. Data must stay in plain Markdown and CSV so it is
readable without any tooling.

**First:** if `profile.md` or this file still contains `{{`, setup is unfinished. Follow the
setup guide in `README.md` (section 2) before anything else.

## Rules
- At the start of every conversation, check the current date and time in the user's timezone
  (`TZ={{TIMEZONE}} date`). Use it to work out "today", what's done, and what's next. Never
  assume the date.
- Dates: ISO `YYYY-MM-DD`. Durations in minutes, distances in km, elevation in metres, pace
  as `mm:ss/km`, weight in kg (convert if the user uses imperial, but store metric).
- CSVs: keep the header row exactly as-is; append rows in date order; quote any field
  containing commas. **Leave unknown values empty, never invent them.**
- `sport` values: `run`, `walk`, `hike`, `trail`, `bike`, `swim`, `strength`, `mobility`,
  `sport`, `rest`, `other` (add new ones here if needed).
- `focus` values (which goal a session serves): `general` plus one short key per goal or
  event in `plans/goals.md` (e.g. `5k`, `fatloss`, `trip`).
- **Workouts:** when the user reports one, append to `data/training_log.csv`, and set the
  matching `data/plan.csv` row's status. Screenshots from a watch/app are fine: read the
  numbers off them.
- **Body:** weight/HR/HRV/sleep → `data/body_metrics.csv`; smart-scale details →
  `data/body_composition.csv`. Weight is judged on the **weekly average** of morning,
  same-conditions readings, never a single day.
- **Food:** when the user reports food, append to `data/food_log.csv` with estimated kcal +
  protein and state the estimate basis in `notes`. Estimate **conservatively**: use the
  user's weights or labels when given, otherwise the upper end of the range for
  restaurant/takeaway food (oil, sauces, rice/noodle portions). Reuse values from
  `data/food_reference.csv` for repeat items and add new labelled items there. After
  logging, compare the day's running total with the targets in `profile.md` and give one
  practical suggestion for the rest of the day.
- **Plan:** `data/plan.csv` is the source of truth; `plans/plan.md` mirrors it. For
  "what's today/this week?", read `data/plan.csv` and adapt to recent logs, sleep, pain and
  how the user feels. When a planned session is done, skipped or changed, set its `status`
  (`done`, `skipped`, `moved`) and run `python3 scripts/render_plan.py`. For a moved session,
  keep the old row as `moved` and add a new `planned` row on the new date.
- **Deviations:** every skipped, moved, shortened or late session also gets a row in
  `data/deviations.csv` (days pushed + reason; ask if not given). Every ~3 weeks, summarise
  patterns in `plans/deviations.md`, decide one fix per pattern, and use them when scheduling.
  A bad day should get a 10–20 min minimum session instead of zero, where safe.
- **Pain:** when the user mentions pain/niggles, append to `data/niggles.csv` (0–10, when it
  hurts) and update `plans/injuries.md`. Apply the traffic-light rule there when choosing or
  adjusting sessions. After long or hard sessions, ask about tracked issues. Not medical
  advice: red flags or anything not settling in 2–3 weeks → recommend a doctor/physio.
- **Plan changes** (goals, phases, targets, big schedule changes) go in the change log in
  `plans/goals.md` with the date and reason.
- Write day-level detail about 2 weeks ahead from the week-level outline in `plans/plan.md`.
- Event-specific facts (dates, logistics, goals, results) go in `events/<event>.md`.
- Be honest and specific: name trade-offs, flag unrealistic targets, prefer a smaller
  sustainable change over a perfect plan.
- Commit and push after every update with a short message, e.g.
  `log: 2026-03-02 run 5k`, `food: 2026-03-02 lunch`, `plan: move Sat long run to Sun`.
  {{BRANCHING: e.g. "Work directly on main." or "Use a branch per change."}}
