"""Dataset quality gates."""

from __future__ import annotations

from collections import Counter

from recommender.load import load_locations, load_meals
from recommender.schema import spend_price, with_tax

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
LOCAL_PRICE_FIELDS = ("price_source", "price_confidence", "price_checked_on")
LOCAL_PRICE_SOURCES = {"official_menu", "official_pdf", "fallback_public"}
LOCAL_PRICE_CONFIDENCE = {"high", "medium"}


def test_meal_and_grocery_counts():
    meals = load_meals()
    grocery = [m for m in meals if m["type"] == "grocery"]
    assert len(meals) >= 150
    assert len(grocery) >= 50
    assert all(m["location_chain"] == "H-E-B" for m in grocery)


def test_all_restaurant_chains_present():
    meals = load_meals()
    chains = {m["location_chain"] for m in meals if m["type"] == "restaurant"}
    assert EXPECTED_CHAINS <= chains
    assert LOCAL_CHAINS <= chains


def test_local_chain_price_metadata():
    meals = load_meals()
    local = [
        m for m in meals
        if m["type"] == "restaurant" and m["location_chain"] in LOCAL_CHAINS
    ]
    assert local, "expected local chain meals"
    for m in local:
        for field in LOCAL_PRICE_FIELDS:
            assert m.get(field), f"{m['location_chain']} missing {field} on {m['order'][:40]}"
        assert m["price_source"] in LOCAL_PRICE_SOURCES
        assert m["price_confidence"] in LOCAL_PRICE_CONFIDENCE
        assert m["price_checked_on"]


def test_no_duplicate_orders():
    meals = load_meals()
    keys = [m["order"].casefold().strip() for m in meals]
    dupes = [k for k, n in Counter(keys).items() if n > 1]
    assert dupes == []


def test_no_weak_variants():
    meals = load_meals()
    bad = []
    for m in meals:
        order = m["order"].casefold()
        if any(p in order for p in WEAK_PATTERNS):
            bad.append(m["order"])
    assert bad == []


def test_locations_load():
    locs = load_locations()
    assert len(locs) >= 20


def test_pitch_wow_bands():
    meals = load_meals()
    wow = [m for m in meals if m.get("pitch_wow")]
    assert wow, "expected pitch_wow meals"

    def under(band: float, mtype: str) -> int:
        n = 0
        for m in wow:
            if m["type"] != mtype:
                continue
            if with_tax(spend_price(m)) <= band:
                n += 1
        return n

    for band in (5.0, 8.0, 12.0):
        assert under(band, "restaurant") >= 2, f"need >=2 wow restaurants under ${band}"
        assert under(band, "grocery") >= 2, f"need >=2 wow groceries under ${band}"


def test_grocery_has_items_and_recipe():
    for m in load_meals():
        if m["type"] != "grocery":
            continue
        assert m.get("items")
        assert m.get("recipe")
