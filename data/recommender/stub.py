"""Hour-one stub: realistic SA Chipotle + H-E-B pair, same return shape as engine."""

from __future__ import annotations

import math
from typing import Any

from .schema import DEFAULT_RADIUS_MILES, with_tax


def _distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 3959
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.asin(math.sqrt(a))


def stub_recommend(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
    radius_miles: float = DEFAULT_RADIUS_MILES,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return a fixed-but-realistic pair when it fits budget; else None sides."""
    _ = goal, radius_miles

    chipotle = {
        "type": "restaurant",
        "name": "Chipotle - Downtown",
        "chain": "Chipotle",
        "address": "733 E Houston St, San Antonio, TX 78205",
        "order": "Chicken bowl — white rice, pinto beans, fajita veggies, salsa, NO cheese/sour cream",
        "price": 9.25,
        "price_with_tax": with_tax(9.25),
        "calories": 520,
        "protein_g": 42.0,
        "carbs_g": 58.0,
        "fat_g": 12.0,
        "lat": 29.4267,
        "lng": -98.4847,
    }
    chipotle["distance_miles"] = round(_distance(lat, lng, chipotle["lat"], chipotle["lng"]), 1)

    heb = {
        "type": "grocery",
        "store": "H-E-B - Alamo Heights",
        "store_chain": "H-E-B",
        "address": "300 W Olmos Dr, San Antonio, TX 78212",
        "items": [
            "H-E-B dozen large eggs ($2.89)",
            "Fresh spinach 10oz ($2.49)",
            "H-E-B black beans 15oz ($0.89)",
        ],
        "recipe": "Scramble 3 eggs with spinach. Heat black beans. Makes 4 servings — ~$1.57/meal, 5 min.",
        "prep_minutes": 5,
        "price": 1.57,
        "price_with_tax": with_tax(1.57),
        "calories": 380,
        "protein_g": 28.0,
        "carbs_g": 22.0,
        "fat_g": 18.0,
        "lat": 29.4712,
        "lng": -98.4891,
    }
    heb["distance_miles"] = round(_distance(lat, lng, heb["lat"], heb["lng"]), 1)

    restaurant = chipotle if chipotle["price_with_tax"] <= budget else None
    grocery = heb if heb["price_with_tax"] <= budget else None
    return restaurant, grocery
