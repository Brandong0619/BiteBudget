# BrokeBite

**Google Maps meets MyFitnessPal — for when you're broke.**

Tell the app how much cash you have and your health goal. Get two options in San Antonio:

1. **Restaurant** — exact order, price with tax, macros
2. **H-E-B grocery fix** — 3-ingredient shopping list, 5-min recipe, half the price

## Directory layout

| Folder | Role | Owns |
|--------|------|------|
| `shared/` | All | Cross-role contracts and constants (no secrets) |
| `data/` | Person A — Data + Model | Datasets, recommender, eval, progress |
| `backend/` | Person B — Backend + Integration | FastAPI (unchanged location) |
| `supabase/` | Person B | Schema / seed (repo root) |
| `frontend/` | Person C — Frontend + Narrative | Vite UI + `expo/` and `narrative/` placeholders |

See [`shared/docs/team_roles.md`](shared/docs/team_roles.md) and [`data/PROGRESS.md`](data/PROGRESS.md).

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite (JavaScript); Expo planned |
| Backend | Python + FastAPI |
| Data / model | Curated JSON + deterministic scorer in `data/` |
| Database | Supabase + PostgreSQL (optional) |
| Maps | Mapbox preferred (Phase 2) |
| Hosting | Vercel (frontend) · Render/Railway (backend) · Supabase (DB) |

## Quick start

### 1. Backend (Person B)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

To use Person A's recommender, follow [`data/recommender/HANDOFF.md`](data/recommender/HANDOFF.md).

### 2. Frontend (Person C)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: http://localhost:5173

### 3. Data + model (Person A)

```bash
cd data
python scripts/validate_data.py
```

### 4. Supabase (optional for MVP)

The app works with curated data under `data/datasets/`. To use Supabase:

1. Create a project at [supabase.com](https://supabase.com)
2. Run `supabase/schema.sql` then `supabase/seed.sql` in the SQL Editor
3. Add `SUPABASE_URL` and `SUPABASE_KEY` to `backend/.env` (never commit real keys)

## MVP scope (San Antonio)

- **Restaurants:** Chipotle, Whataburger, Panda Express, Torchy's, McDonald's, Taco Cabana, Chick-fil-A, Subway
- **Grocery:** H-E-B only
- **Tax:** 8.25% Bexar County rate applied automatically
- **Goals:** Gain muscle · Lose weight · Maintain

## Deploy

**Frontend (Vercel)**
- Root: `frontend`
- Build: `npm run build`
- Output: `dist`
- Env: `VITE_API_URL=https://your-api.onrender.com`

**Backend (Render / Railway)**
- Root: `backend`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Env: `SUPABASE_URL`, `SUPABASE_KEY`, `CORS_ORIGINS`

## Roadmap

- [ ] Mapbox embed + directions links
- [ ] Expo mobile client
- [ ] Real-time menu pricing via crowdsourcing
- [ ] User accounts + saved budgets
- [ ] Expand beyond San Antonio
