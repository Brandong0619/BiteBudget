# Data + Model (Person A)

San Antonio curated meals, deterministic recommender, and eval fixtures.

| Path | Purpose |
|------|---------|
| `datasets/` | `locations.json`, `meals.json`, `eval_cases.json` |
| `recommender/` | `recommend()` stub + engine (API-compatible dicts) |
| `scripts/validate_data.py` | Local validation (no Supabase) |
| `PROGRESS.md` | What changed + directory layout |

Wire-up instructions for Person B: [`recommender/HANDOFF.md`](recommender/HANDOFF.md).
