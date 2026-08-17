# Handoff: Person A → Person B

## What to import

From the repo root (or with `PYTHONPATH` including the repo root):

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # adjust if needed
sys.path.insert(0, str(ROOT / "data"))

from recommender import recommend  # real engine
# from recommender import stub_recommend  # hour-one stub if needed
```

Suggested plug-in in `backend/app/database.py` inside `fetch_recommendations` (after Supabase attempt / as local path):

```python
from recommender import recommend
return recommend(
    budget=budget,
    goal=goal,
    lat=lat,
    lng=lng,
    radius_miles=settings.default_radius_miles,
)
```

Keep Pydantic models in `backend/app/models.py` as the HTTP contract. `recommend()` returns plain dicts matching `RestaurantOption` / `GroceryOption` field names.

## Contract

See [`../../shared/contracts/recommend_api.md`](../../shared/contracts/recommend_api.md).

```text
recommend(budget, goal, lat, lng, radius_miles=5.0)
  -> (restaurant_dict | None, grocery_dict | None)
```

- Tax: 8.25% applied inside the engine (`price_with_tax`)
- Strict filter: checkout `price` (full basket, not per-serving) with tax `<= budget`, and distance `<= radius_miles`
- `per_serving_price` on grocery JSON is recipe context only
- Goals: `gain_muscle` | `lose_weight` | `maintain`

## Datasets

- `data/datasets/locations.json`
- `data/datasets/meals.json` (≥150 curated combinations)
- `data/datasets/eval_cases.json`

Prices are SA estimates with `estimate_as_of` metadata. Always show a demo disclaimer.

## Stub → real

- Stub: `recommender.stub_recommend` (fixed Chipotle + H-E-B pair)
- Real (default export): `recommender.recommend`
- Debug (Person A / eval only): `recommender.recommend_with_debug` returns winners plus `top_restaurants` / `top_groceries` (top 3). Public `recommend()` API is unchanged for Person B.

## Non-goals for Person A

Expo, Mapbox UI, CORS, hosting, Supabase RPC — those stay with B/C.
