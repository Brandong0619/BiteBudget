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
    *,
    best_restaurant_tax: float | None = None,
) -> float:
    protein = float(meal["protein_g"])
    calories = int(meal["calories"])
    savings = budget - price_with_tax

    score = 0.0
    score += protein * 2.0
    score += savings * 2.0
    score -= distance * 4.0
    score += 8.0 * (protein / max(price_with_tax, 0.5))

    if goal == "gain_muscle":
        score += protein * 4.0
        score += 0.03 * max(0, calories - 400)
    elif goal == "lose_weight":
        score += protein * 2.5
        score -= 0.12 * max(0, calories - 450)
        if calories <= 400:
            score += 12.0

    if meal["type"] == "grocery":
        score += 6.0
        if best_restaurant_tax is not None and price_with_tax <= 0.60 * best_restaurant_tax:
            score += 10.0

    return score


def _debug_row(score: float, entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "score": round(score, 3),
        "order": entry.get("order", ""),
        "items": entry.get("items", []),
        "chain": entry.get("chain") or entry.get("store_chain"),
        "price_with_tax": entry["price_with_tax"],
        "protein_g": entry["protein_g"],
        "calories": entry["calories"],
        "distance_miles": entry["distance_miles"],
    }


def _build_entry(meal: dict[str, Any], loc: dict[str, Any], dist: float, price: float, price_with_tax: float) -> dict[str, Any]:
    return {
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
        "type": meal["type"],
    }


def recommend_with_debug(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
    radius_miles: float = DEFAULT_RADIUS_MILES,
) -> dict[str, Any]:
    """Return winners plus top-3 candidate debug lists."""
    restaurant_candidates: list[tuple[float, dict[str, Any]]] = []
    grocery_candidates: list[tuple[float, dict[str, Any]]] = []

    locations = load_locations()
    meals = load_meals()

    # Pass 1: restaurants
    for meal in meals:
        if meal["type"] != "restaurant" or goal not in meal["goals"]:
            continue
        price = spend_price(meal)
        price_with_tax = with_tax(price)
        if price_with_tax > budget:
            continue
        matching = [
            loc for loc in locations
            if loc["chain"] == meal["location_chain"] and loc["type"] == "restaurant"
        ]
        for loc in matching:
            dist = haversine_miles(lat, lng, loc["lat"], loc["lng"])
            if dist > radius_miles:
                continue
            entry = _build_entry(meal, loc, dist, price, price_with_tax)
            score = score_option(meal, goal, dist, price_with_tax, budget)
            restaurant_candidates.append((score, entry))

    best_restaurant_tax = None
    if restaurant_candidates:
        best_restaurant_tax = max(restaurant_candidates, key=lambda x: x[0])[1]["price_with_tax"]

    # Pass 2: groceries (relative savings vs best restaurant)
    for meal in meals:
        if meal["type"] != "grocery" or goal not in meal["goals"]:
            continue
        price = spend_price(meal)
        price_with_tax = with_tax(price)
        if price_with_tax > budget:
            continue
        matching = [
            loc for loc in locations
            if loc["chain"] == meal["location_chain"] and loc["type"] == "grocery"
        ]
        for loc in matching:
            dist = haversine_miles(lat, lng, loc["lat"], loc["lng"])
            if dist > radius_miles:
                continue
            entry = _build_entry(meal, loc, dist, price, price_with_tax)
            score = score_option(
                meal, goal, dist, price_with_tax, budget,
                best_restaurant_tax=best_restaurant_tax,
            )
            grocery_candidates.append((score, entry))

    restaurant_candidates.sort(key=lambda x: x[0], reverse=True)
    grocery_candidates.sort(key=lambda x: x[0], reverse=True)

    restaurant = restaurant_candidates[0][1] if restaurant_candidates else None
    grocery = grocery_candidates[0][1] if grocery_candidates else None

    return {
        "restaurant": restaurant,
        "grocery": grocery,
        "top_restaurants": [_debug_row(s, e) for s, e in restaurant_candidates[:3]],
        "top_groceries": [_debug_row(s, e) for s, e in grocery_candidates[:3]],
    }


def recommend(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
    radius_miles: float = DEFAULT_RADIUS_MILES,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return best restaurant and grocery options within budget for the goal."""
    result = recommend_with_debug(budget, goal, lat, lng, radius_miles)
    return result["restaurant"], result["grocery"]
