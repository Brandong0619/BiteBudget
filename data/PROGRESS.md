# Data + Model progress (Person A)

## 2026-08-16

### Directory layout
- `shared/` — cross-role contracts and constants (all)
- `data/` — Person A: datasets, recommender, eval, this PROGRESS file
- `backend/` — Person B: FastAPI (unchanged location)
- `supabase/` — Person B: schema/seed (repo root)
- `frontend/` — Person C: Vite UI + `expo/` and `narrative/` placeholders

### What changed
- Added `shared/` contracts (`recommend_api.md`, goals, constants) and team role docs
- Added `data/recommender` with stub + real filter/score engine (`recommend()`)
- Migrated and expanded curated SA data to `data/datasets/` (**23 locations**, **160 meals** across 8 restaurant chains + H-E-B)
- Added `data/scripts/generate_datasets.py`, `validate_data.py`, and `eval_cases.json` (16 cases passing)
- Thin backend adapter: `backend/app/database.py` calls Person A’s `recommend()` when Supabase RPC is unavailable
- Hardened root `.gitignore` for secrets, venv, Expo/Node build artifacts
- Expanded `frontend/expo/` and `frontend/narrative/` placeholders for Person C
- Updated root README with directory layout index
- Pushed to `ayu_test`
