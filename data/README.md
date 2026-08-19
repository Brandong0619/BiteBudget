# Data + Model (Person A)

San Antonio curated meals, deterministic recommender, and eval fixtures.

| Path | Purpose |
|------|---------|
| `datasets/` | `locations.json`, `meals.json`, `eval_cases.json` |
| `recommender/` | `recommend()` stub + engine (API-compatible dicts) |
| `scripts/validate_data.py` | Local validation (no Supabase) |
| `tools/debug_ui.py` | Local web UI for custom + eval-case debug runs |

Wire-up instructions for Person B: [`recommender/HANDOFF.md`](recommender/HANDOFF.md).


## Quick debug UI

```bash
python3 data/tools/debug_ui.py
# open http://127.0.0.1:8099
```

This helps validate budget/radius/goal behavior quickly with top-3 debug output.
