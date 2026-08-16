#!/usr/bin/env python3
"""Validate datasets and run eval_cases against the real recommender."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recommender import recommend  # noqa: E402
from recommender.load import load_locations, load_meals, validate_locations, validate_meals  # noqa: E402
from recommender.schema import TAX_RATE  # noqa: E402


def main() -> int:
    locations = load_locations()
    meals = load_meals()

    errors = validate_locations(locations) + validate_meals(meals)
    if len(meals) < 150:
        errors.append(f"Need >= 150 meals, found {len(meals)}")

    chains = {m["location_chain"] for m in meals if m["type"] == "restaurant"}
    expected = {
        "Chipotle",
        "Whataburger",
        "Panda Express",
        "Torchy's Tacos",
        "McDonald's",
        "Taco Cabana",
        "Chick-fil-A",
        "Subway",
    }
    missing = expected - chains
    if missing:
        errors.append(f"Missing restaurant chains: {sorted(missing)}")

    grocery = [m for m in meals if m["type"] == "grocery"]
    if not grocery or any(m["location_chain"] != "H-E-B" for m in grocery):
        errors.append("Grocery meals must be H-E-B only")

    eval_path = ROOT / "datasets" / "eval_cases.json"
    cases = json.loads(eval_path.read_text(encoding="utf-8"))["cases"]
    for case in cases:
        restaurant, grocery_opt = recommend(
            budget=case["budget"],
            goal=case["goal"],
            lat=case["lat"],
            lng=case["lng"],
            radius_miles=case.get("radius_miles", 5.0),
        )
        expect = case["expect"]
        options = [o for o in (restaurant, grocery_opt) if o]
        if expect.get("at_least_one") and not options:
            errors.append(f"{case['id']}: expected at least one option")
        for opt in options:
            if opt["price_with_tax"] > expect["max_price_with_tax"] + 1e-6:
                errors.append(
                    f"{case['id']}: price_with_tax {opt['price_with_tax']} exceeds budget"
                )
            if opt["distance_miles"] > expect["max_distance_miles"] + 1e-6:
                errors.append(
                    f"{case['id']}: distance {opt['distance_miles']} exceeds radius"
                )
        if restaurant and "min_protein_if_restaurant" in expect:
            if restaurant["protein_g"] < expect["min_protein_if_restaurant"]:
                errors.append(f"{case['id']}: restaurant protein too low")
        if restaurant and "max_calories_if_restaurant" in expect:
            if restaurant["calories"] > expect["max_calories_if_restaurant"]:
                errors.append(f"{case['id']}: restaurant calories too high for lose_weight signal")

    print(f"locations={len(locations)} meals={len(meals)} tax_rate={TAX_RATE}")
    if errors:
        print(f"FAILED ({len(errors)} issues):")
        for e in errors[:40]:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(cases)} eval cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
