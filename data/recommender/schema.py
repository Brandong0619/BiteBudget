"""Shared schema helpers and constants for the recommender."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

Goal = Literal["gain_muscle", "lose_weight", "maintain"]
MealType = Literal["restaurant", "grocery"]

TAX_RATE = 0.0825
DEFAULT_RADIUS_MILES = 5.0
DEFAULT_LAT = 29.4241
DEFAULT_LNG = -98.4936

DATA_DIR = Path(__file__).resolve().parents[1] / "datasets"
REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_MEAL_FIELDS = (
    "location_chain",
    "type",
    "order",
    "price",
    "calories",
    "protein_g",
    "carbs_g",
    "fat_g",
    "goals",
)

REQUIRED_LOCATION_FIELDS = ("name", "chain", "type", "address", "lat", "lng")


def with_tax(price: float) -> float:
    return round(price * (1 + TAX_RATE), 2)


def spend_price(meal: dict[str, Any]) -> float:
    if meal.get("per_serving_price") is not None:
        return float(meal["per_serving_price"])
    return float(meal["price"])
