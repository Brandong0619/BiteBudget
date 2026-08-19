#!/usr/bin/env python3
"""Validate datasets and run eval_cases against the real recommender."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recommender import recommend, recommend_with_debug  # noqa: E402
from recommender.load import load_locations, load_meals, reload_datasets, validate_locations, validate_meals  # noqa: E402
from recommender.schema import TAX_RATE, spend_price, with_tax  # noqa: E402

WEAK_PATTERNS = ("value menu cut", "+ water only", "(lighter portion)")
EXPECTED_CHAINS = {
    "Chipotle",
    "Whataburger",
    "Panda Express",
    "Torchy's Tacos",
    "McDonald's",
    "Taco Cabana",
    "Chick-fil-A",
    "Subway",
}
LOCAL_CHAINS = {
    "Pasha Mediterranean",
    "Kababchi",
}


def main() -> int:
    reload_datasets()
    locations = load_locations()
    meals = load_meals()

    errors = validate_locations(locations) + validate_meals(meals)
    if len(meals) < 150:
        errors.append(f"Need >= 150 meals, found {len(meals)}")

    grocery = [m for m in meals if m["type"] == "grocery"]
    if len(grocery) < 50:
        errors.append(f"Need >= 50 grocery meals, found {len(grocery)}")
    if not grocery or any(m["location_chain"] != "H-E-B" for m in grocery):
        errors.append("Grocery meals must be H-E-B only")

    chains = {m["location_chain"] for m in meals if m["type"] == "restaurant"}
    missing = EXPECTED_CHAINS - chains
    if missing:
        errors.append(f"Missing restaurant chains: {sorted(missing)}")
    missing_local = LOCAL_CHAINS - chains
    if missing_local:
        errors.append(f"Missing local restaurant chains: {sorted(missing_local)}")

    for m in meals:
        if m["type"] != "restaurant" or m["location_chain"] not in LOCAL_CHAINS:
            continue
        for field in ("price_source", "price_confidence", "price_checked_on"):
            if not m.get(field):
                errors.append(f"Local meal missing {field}: {m['order'][:50]}")

    orders = [m["order"].casefold().strip() for m in meals]
    dupes = [k for k, n in Counter(orders).items() if n > 1]
    if dupes:
        errors.append(f"Duplicate orders: {dupes[:5]}")

    for m in meals:
        order = m["order"].casefold()
        if any(p in order for p in WEAK_PATTERNS):
            errors.append(f"Weak variant: {m['order']}")

    eval_path = ROOT / "datasets" / "eval_cases.json"
    cases = json.loads(eval_path.read_text(encoding="utf-8"))["cases"]
    top3_chains: set[str] = set()

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
        if not expect.get("at_least_one") and options:
            errors.append(f"{case['id']}: expected no options, got {len(options)}")
        if expect.get("require_restaurant") and restaurant is None:
            errors.append(f"{case['id']}: restaurant required")
        for opt in options:
            if opt["price_with_tax"] > expect["max_price_with_tax"] + 1e-6:
                errors.append(f"{case['id']}: over budget")
            if opt["distance_miles"] > expect["max_distance_miles"] + 1e-6:
                errors.append(f"{case['id']}: over radius")
            if abs(opt["price_with_tax"] - with_tax(opt["price"])) > 1e-6:
                errors.append(f"{case['id']}: tax math mismatch for {opt.get('order')}")

        if expect.get("collect_top3_chains"):
            debug = recommend_with_debug(
                case["budget"], case["goal"], case["lat"], case["lng"],
                case.get("radius_miles", 5.0),
            )
            for row in debug["top_restaurants"]:
                if row.get("chain"):
                    top3_chains.add(row["chain"])

        required_local = expect.get("require_local_chain_top3")
        if required_local:
            debug = recommend_with_debug(
                case["budget"], case["goal"], case["lat"], case["lng"],
                case.get("radius_miles", 5.0),
            )
            top_chains = {row.get("chain") for row in debug["top_restaurants"]}
            if required_local not in top_chains:
                errors.append(
                    f"{case['id']}: expected {required_local} in top-3, got {sorted(top_chains)}"
                )

    missing_top3 = EXPECTED_CHAINS - top3_chains
    if missing_top3:
        errors.append(f"Chains never in top-3 across suite: {sorted(missing_top3)}")

    muscle_r, _ = recommend(12.0, "gain_muscle", 29.4241, -98.4936)
    lose_r, _ = recommend(12.0, "lose_weight", 29.4241, -98.4936)
    if not muscle_r or not lose_r:
        errors.append("goal separation: missing restaurant picks")
    elif muscle_r["protein_g"] < lose_r["protein_g"]:
        errors.append("goal separation: muscle protein should be >= lose_weight")
    elif lose_r["calories"] > muscle_r["calories"]:
        errors.append("goal separation: lose_weight calories should be <= muscle")

    wow = [m for m in meals if m.get("pitch_wow")]
    for band in (5.0, 8.0, 12.0):
        for mtype in ("restaurant", "grocery"):
            n = sum(
                1
                for m in wow
                if m["type"] == mtype and with_tax(spend_price(m)) <= band
            )
            if n < 2:
                errors.append(f"pitch_wow {mtype} under ${band}: need >=2 got {n}")

    print(f"locations={len(locations)} meals={len(meals)} grocery={len(grocery)} tax_rate={TAX_RATE}")
    if errors:
        print(f"FAILED ({len(errors)} issues):")
        for e in errors[:50]:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(cases)} eval cases + quality gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
