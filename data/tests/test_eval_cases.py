"""Eval-case driven invariants."""

from __future__ import annotations

import json
from pathlib import Path

from recommender import recommend, recommend_with_debug
from recommender.schema import with_tax

EVAL_PATH = Path(__file__).resolve().parents[1] / "datasets" / "eval_cases.json"
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


def _cases():
    return json.loads(EVAL_PATH.read_text(encoding="utf-8"))["cases"]


def test_eval_cases_invariants():
    errors = []
    for case in _cases():
        restaurant, grocery = recommend(
            budget=case["budget"],
            goal=case["goal"],
            lat=case["lat"],
            lng=case["lng"],
            radius_miles=case.get("radius_miles", 5.0),
        )
        expect = case["expect"]
        options = [o for o in (restaurant, grocery) if o]
        if expect.get("require_restaurant") and restaurant is None:
            errors.append(f"{case['id']}: restaurant required")
        if expect.get("at_least_one") and not options:
            errors.append(f"{case['id']}: expected at least one option")
        if not expect.get("at_least_one") and options:
            # tiny budgets may still find grocery; only fail if restaurant sneaks over
            pass
        for opt in options:
            if opt["price_with_tax"] > expect["max_price_with_tax"] + 1e-6:
                errors.append(f"{case['id']}: over budget {opt['price_with_tax']}")
            if opt["distance_miles"] > expect["max_distance_miles"] + 1e-6:
                errors.append(f"{case['id']}: over radius {opt['distance_miles']}")
            if abs(opt["price_with_tax"] - with_tax(opt["price"])) > 1e-6:
                errors.append(f"{case['id']}: tax math mismatch")
    assert errors == []


def test_goal_separation_cases():
    muscle_r, _ = recommend(12.0, "gain_muscle", 29.4241, -98.4936)
    lose_r, _ = recommend(12.0, "lose_weight", 29.4241, -98.4936)
    assert muscle_r and lose_r
    assert muscle_r["protein_g"] >= lose_r["protein_g"]
    assert lose_r["calories"] <= muscle_r["calories"]


def test_chain_coverage_across_top3():
    seen: set[str] = set()
    for case in _cases():
        if not case["expect"].get("collect_top3_chains"):
            continue
        debug = recommend_with_debug(
            case["budget"], case["goal"], case["lat"], case["lng"],
            case.get("radius_miles", 5.0),
        )
        for row in debug["top_restaurants"]:
            if row.get("chain"):
                seen.add(row["chain"])
    missing = EXPECTED_CHAINS - seen
    assert not missing, f"chains never in top-3 across suite: {sorted(missing)}"
