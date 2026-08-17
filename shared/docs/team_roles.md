# Team roles

| Folder | Role | Owns |
|--------|------|------|
| `data/` | Person A — Data + Model | Datasets, recommender stub/engine, eval, progress notes |
| `backend/` + `supabase/` | Person B — Backend + Integration | FastAPI, deploy, CORS, Supabase wiring, demo URL |
| `frontend/` | Person C — Frontend + Narrative | Vite UI, future Expo app, demo script, Section 4, slides |
| `shared/` | All | Frozen contracts and constants only |

## Non-goals by role

- **Person A** does not own Expo, Mapbox UI, CORS, hosting, or Supabase RPC deploy.
- **Person B** does not curate the meal JSON or tune scoring weights (consumes `data/recommender`).
- **Person C** does not change the recommend contract without updating `shared/contracts/`.
