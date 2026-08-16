"""Real recommender: strict budget/goal/radius filter + goal-aware scoring."""

from __future__ import annotations

import math
from typing import Any

from .load import load_locations, load_meals
from .schema import DEFAULT_RADIUS_MILES, spend_price, with_tax


def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 3959
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.asin(math.sqrt(a))


def score_option(
    meal: dict[str, Any],
    goal: str,
    distance: float,
    price_with_tax: float,
    budget: float,
) -> float:
    protein = float(meal["protein_g"])
    calories = int(meal["calories"])
    savings = budget - price_with_tax

    score = 0.0
    score += protein * 2
    score += savings * 3
    score -= distance * 5

    if goal == "lose_weight":
        score -= max(0, calories - 450) * 0.05
        score += protein * 1.5
    elif goal == "gain_muscle":
        score += protein * 3
        score += max(0, calories - 400) * 0.02

    if meal["type"] == "grocery":
        score += 8

    return score


def recommend(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
    radius_miles: float = DEFAULT_RADIUS_MILES,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return best restaurant and grocery options within budget for the goal."""
    restaurant_candidates: list[tuple[float, dict[str, Any]]] = []
    grocery_candidates: list[tuple[float, dict[str, Any]]] = []

    locations = load_locations()
    meals = load_meals()

    for meal in meals:
        if goal not in meal["goals"]:
            continue

        price = spend_price(meal)
        price_with_tax = with_tax(price)
        if price_with_tax > budget:
            continue

        matching_locations = [
            loc
            for loc in locations
            if loc["chain"] == meal["location_chain"] and loc["type"] == meal["type"]
        ]

        for loc in matching_locations:
            dist = haversine_miles(lat, lng, loc["lat"], loc["lng"])
            if dist > radius_miles:
                continue

            entry: dict[str, Any] = {
                "name": loc["name"],
                "chain": loc["chain"],
                "store": loc["name"],
                "store_chain": loc["chain"],
                "address": loc["address"],
                "distance_miles": round(dist, 1),
                "order": meal["order"],
                "items": meal.get("items", []),
                "recipe": meal.get("recipe", ""),
                "prep_minutes": meal.get("prep_minutes", 0),
                "price": round(price, 2),
                "price_with_tax": price_with_tax,
                "calories": meal["calories"],
                "protein_g": meal["protein_g"],
                "carbs_g": meal["carbs_g"],
                "fat_g": meal["fat_g"],
                "lat": loc["lat"],
                "lng": loc["lng"],
            }
            score = score_option(meal, goal, dist, price_with_tax, budget)
            if meal["type"] == "restaurant":
                entry["type"] = "restaurant"
                restaurant_candidates.append((score, entry))
            else:
                entry["type"] = "grocery"
                grocery_candidates.append((score, entry))

    restaurant = max(restaurant_candidates, key=lambda x: x[0])[1] if restaurant_candidates else None
    grocery = max(grocery_candidates, key=lambda x: x[0])[1] if grocery_candidates else None
    return restaurant, grocery
