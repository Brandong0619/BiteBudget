"""Scorer behavior tests."""

from __future__ import annotations

from recommender import recommend, recommend_with_debug
from recommender.load import load_meals
from recommender.schema import spend_price, with_tax


DOWNTOWN = (29.4241, -98.4936)


def test_muscle_vs_lose_weight_diverge():
    lat, lng = DOWNTOWN
    muscle_r, _ = recommend(12.0, "gain_muscle", lat, lng)
    lose_r, _ = recommend(12.0, "lose_weight", lat, lng)
    assert muscle_r is not None and lose_r is not None
    assert muscle_r["protein_g"] >= lose_r["protein_g"]
    assert lose_r["calories"] <= muscle_r["calories"]


def test_strict_budget_and_tax_math():
    lat, lng = DOWNTOWN
    for budget in (5.0, 8.0, 12.0):
        for goal in ("gain_muscle", "lose_weight", "maintain"):
            r, g = recommend(budget, goal, lat, lng)
            for opt in (r, g):
                if not opt:
                    continue
                assert opt["price_with_tax"] <= budget + 1e-6
                assert abs(opt["price_with_tax"] - with_tax(opt["price"])) < 1e-6


def test_recommend_with_debug_top3_shape():
    debug = recommend_with_debug(12.0, "gain_muscle", *DOWNTOWN)
    assert "restaurant" in debug and "grocery" in debug
    assert len(debug["top_restaurants"]) <= 3
    assert len(debug["top_groceries"]) <= 3
    if debug["top_restaurants"]:
        row = debug["top_restaurants"][0]
        for key in ("score", "chain", "price_with_tax", "protein_g", "calories", "distance_miles"):
            assert key in row


def test_protein_per_dollar_prefers_efficient_picks():
    """High protein cheap picks should appear in top-3 for muscle goal."""
    debug = recommend_with_debug(8.0, "gain_muscle", *DOWNTOWN)
    assert debug["top_restaurants"] or debug["top_groceries"]
    best = (debug["top_restaurants"] or debug["top_groceries"])[0]
    assert best["protein_g"] / max(best["price_with_tax"], 0.5) >= 2.0


def test_grocery_budget_uses_checkout_price_not_per_serving():
    """A multi-serve H-E-B pack cannot sneak in under budget via per_serving_price."""
    meals = load_meals()
    bulky = [
        m
        for m in meals
        if m["type"] == "grocery"
        and m.get("per_serving_price") is not None
        and float(m["price"]) >= 10
        and with_tax(float(m["price"])) > 5
        and with_tax(float(m["per_serving_price"])) <= 5
    ]
    assert bulky, "need a grocery pack that's cheap per serving but expensive at checkout"
    assert all(spend_price(m) == float(m["price"]) for m in bulky)

    _, grocery = recommend(5.0, "gain_muscle", *DOWNTOWN)
    if grocery:
        assert grocery["price_with_tax"] <= 5 + 1e-6
        assert grocery["price"] < 10
