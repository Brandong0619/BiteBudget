# BrokeBite

**Google Maps meets MyFitnessPal — for when you're broke.**

Tell the app how much cash you have and your health goal. Get two options in San Antonio:

1. **Restaurant** — exact order, price with tax, macros
2. **H-E-B grocery fix** — 3-ingredient shopping list, 5-min recipe, half the price

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite (JavaScript) |
| Backend | Python + FastAPI |
| Database | Supabase + PostgreSQL |
| Maps | Google Maps Platform (Phase 2) |
| Hosting | Vercel (frontend) · Render/Railway (backend) · Supabase (DB) |

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
copy .env.example .env

uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
copy .env.example .env

npm run dev
```

App: http://localhost:5173

### 3. Supabase (optional for MVP)

The app works out of the box with curated in-memory data. To use Supabase:

1. Create a project at [supabase.com](https://supabase.com)
2. Run `supabase/schema.sql` then `supabase/seed.sql` in the SQL Editor
3. Add `SUPABASE_URL` and `SUPABASE_KEY` to `backend/.env`

## MVP scope (San Antonio)

- **Restaurants:** Chipotle, Whataburger, Panda Express, Torchy's
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

- [ ] Google Maps embed + directions links
- [ ] Real-time menu pricing via crowdsourcing
- [ ] User accounts + saved budgets
- [ ] Expand beyond San Antonio
