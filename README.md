# RaceTrack Template

A personal **health, food and fitness tracker that you run by chatting with an AI agent**
(built for Claude Code; any agent that can read and write files and run Python works).

You tell the agent what you did, ate, weighed or felt. The agent logs it in plain CSV and
Markdown in this repo, keeps your plan up to date, tells you what to do today, and spots
patterns, for example "I skip morning sessions" or "my protein is always low before dinner".
There is no app or database: the repo is the backend and the chat is the UI.

It works for:
- **General health:** move more, eat better, lose or gain weight, sleep, consistency.
- **Fitness goals:** first 5K, get stronger, a hiking trip, a sports season.
- **Events and races,** optionally: marathon, triathlon, trail race, fight, competition.

> **Make your copy private.** Once you use it, this repo will contain health data (weight,
> food, injuries, schedule). Click **Use this template**, then choose **Private**.

---

## 1. Quick start (for the human)

1. Click **Use this template** → create a **private** repo.
2. Open it with your AI agent (e.g. Claude Code on the web or in a terminal).
3. Say: **"Set up this tracker for me."** The agent follows section 2 below and interviews
   you. It takes about 15–30 minutes, and you can do it over several chats.
4. After that, just talk to it daily:
   - "What's the plan today?"
   - "Did 30 min easy run, felt good" / "Had chicken rice for lunch" / "Weighed 72.4"
   - "My knee hurts a bit, 3/10" / "Can't train today, work is crazy"
   - "How did this week go?"

---

## 2. Setup guide (for the AI agent: read this fully before starting)

You are setting this repo up for a new user. Everything below marked `{{…}}` is a blank to
fill, and every CSV row whose `notes` starts with `EXAMPLE` is sample data to delete.
**While any `{{` remains in `profile.md` or `CLAUDE.md`, setup is not finished:** continue
it before doing anything else.

### How to run the interview
- Ask **a few questions at a time** (3–5), in plain language, and accept "don't know / skip".
  Never invent values: leave unknowns empty (`""` in CSV) and note them as TBC.
- After each group, **write the answers into the files immediately** and commit, so nothing
  is lost if the chat ends.
- Adapt to the person. Skip the event questions for someone with no events. Skip pace/HR
  zones for someone who just wants to walk more. Don't overwhelm a beginner.
- Be honest about unrealistic goals (e.g. >1 kg/week fat loss, a marathon in 6 weeks from
  zero) and propose a safer version. Record their original wish and the agreed goal.
- This is not medical advice. If they mention chest pain, fainting, pregnancy, an eating
  disorder history, diabetes or other conditions, recommend checking with a doctor and plan
  conservatively.

### Interview order → where answers go

| # | Ask about | Write to |
|---|---|---|
| 1 | Name or nickname, **timezone** (e.g. `Asia/Singapore`, `Europe/London`), units (metric/imperial) | `profile.md`; replace `{{TIMEZONE}}` in `CLAUDE.md` |
| 2 | Main goals (1–3), in their words, and why. For each: what does success look like, and by when? | `plans/goals.md` |
| 3 | Events with dates (races, trips, competitions, a wedding…), if any | `plans/goals.md` key dates, one file per event in `events/` (copy `events/_template.md`) |
| 4 | Current activity: what they do now, how often, how long; longest/hardest recent effort; past events/PBs | `profile.md` background; optional monthly rows in `data/history.csv`; `events/past-results.md` |
| 5 | Body: height, current weight (and how measured), target weight if any, body-composition device if any | `profile.md`; first row in `data/body_metrics.csv` (and `data/body_composition.csv`) |
| 6 | Schedule: work hours, which days are busy, best time slots, fixed commitments, travel coming up, how many hours/week they can realistically train | `profile.md` availability |
| 7 | Equipment and places: gym access, pool, bike/trainer, home weights, routes, watch/apps | `profile.md` equipment |
| 8 | Injuries, pain, conditions; anything that hurts during or after activity | `plans/injuries.md` (one section per issue) + rows in `data/niggles.csv` |
| 9 | Food: typical day of eating, foods they eat often, dislikes/restrictions (halal, vegetarian, allergies), cooking vs eating out, drinks/alcohol | `profile.md` nutrition; frequent items → `data/food_reference.csv` |
| 10 | Preferences: what they enjoy or hate, how strict or relaxed the coaching should be, how detailed food logging should be (full kcal + protein vs just protein vs off) | `profile.md` preferences; adjust rules in `CLAUDE.md` |

### Then build the plan
1. Set targets in `profile.md`: training zones only if relevant (HR/pace/power), a daily
   **calorie and protein** range (or "not tracking calories"), and a sleep target.
2. Write `plans/goals.md`: the goals, key dates, and phases (e.g. *Build habit → Build →
   Peak/Event → Recover*). Keep it short.
3. Fill `plans/framework.md` "Choices for this user" (sessions/week, hard days, strength
   days, rest day, deficit or not).
4. Fill the **session library** in `plans/plan.md` with the 4–8 session types this person
   will actually use.
5. Write **2–4 weeks day by day** in `data/plan.csv` (one row per session), then a
   week-level outline for later weeks in `plans/plan.md`. Start easier than you think;
   week 1 should feel easy.
6. Run `python3 scripts/render_plan.py` to rebuild the tables in `plans/plan.md`.
7. **Delete every `EXAMPLE` row** in `data/*.csv` (keep the header rows). Delete the example
   issue in `plans/injuries.md` and the example event file if unused.
8. Replace this README's title with something personal if they like, and confirm that no
   `{{` is left: `grep -rn "{{" --include=*.md .`
9. Commit and push: `setup: initial profile and plan`.

---

## 3. File map

```
README.md                  this guide
CLAUDE.md                  rules the agent follows in every chat (read every time)
profile.md                 who the user is: goals, schedule, body, targets, equipment, food, preferences
plans/goals.md             goals, key dates, phases, change log of plan decisions
plans/framework.md         training/health principles + choices for this user
plans/plan.md              readable plan: session library, day tables (rendered), later weeks
plans/injuries.md          pain rules (traffic light) + active issues
plans/deviations.md        patterns in missed/moved sessions and what we changed
events/                    optional: one file per event/race, past-results.md
injuries/                  optional: detailed write-ups of bigger injuries
data/plan.csv              every planned session (source of truth for the plan)
data/training_log.csv      every session actually done
data/deviations.csv        every skipped / moved / shortened / late session + reason
data/food_log.csv          meals with estimated kcal + protein
data/food_reference.csv    the user's usual foods with kcal + protein (labels, weighed portions)
data/body_metrics.csv      weight, resting HR, HRV, sleep
data/body_composition.csv  smart-scale readings (optional)
data/niggles.csv           pain/niggle check-ins (0–10)
data/weekly_summary.csv    weekly totals + notes
data/history.csv           optional baseline history (e.g. monthly totals before starting)
scripts/render_plan.py     rebuilds the day tables in plans/plan.md from data/plan.csv
```

Everything is plain Markdown and CSV: readable on GitHub, editable by hand, no tooling needed
except Python 3 for the one render script.

## 4. Why it works

- **The plan is data,** so the agent always knows what's next and what was missed.
- **Every deviation is logged with a reason.** After a few weeks, patterns show ("busy days
  become zero days", "evening sessions slip") and the plan changes to fit the person's
  real life.
- **Food is logged with estimates and a stated basis,** and reused from your own reference
  list, so numbers get more accurate over time.
- **Pain is scored and gated by a simple traffic-light rule,** so small niggles don't become
  injuries.
