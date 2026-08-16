"""Database access + recommendation orchestration.

Local recommendations are provided by Person A's package under `data/recommender`.
Supabase RPC remains an optional override when configured.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from app.config import settings

# Person A package (repo_root/data)
_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
if str(_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(_DATA_DIR))

from recommender import recommend as data_recommend  # noqa: E402
from recommender.schema import TAX_RATE  # noqa: E402

__all__ = ["TAX_RATE", "fetch_recommendations", "get_supabase"]


def get_supabase():
    if not (settings.supabase_url and settings.supabase_key):
        return None
    try:
        from supabase import create_client
    except ImportError:
        return None
    return create_client(settings.supabase_url, settings.supabase_key)


def fetch_recommendations(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return best restaurant and grocery options within budget for the goal."""
    client = get_supabase()

    if client:
        try:
            result = client.rpc(
                "get_recommendations",
                {"p_budget": budget, "p_goal": goal, "p_lat": lat, "p_lng": lng},
            ).execute()
            if result.data:
                data = result.data
                return data.get("restaurant"), data.get("grocery")
        except Exception:
            pass

    return data_recommend(budget=budget, goal=goal, lat=lat, lng=lng)
