"""Load and lightly validate curated San Antonio datasets."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from .schema import DATA_DIR, REQUIRED_LOCATION_FIELDS, REQUIRED_MEAL_FIELDS


def _read_json(name: str) -> Any:
    path = DATA_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_locations(locations: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for i, loc in enumerate(locations):
        for field in REQUIRED_LOCATION_FIELDS:
            if field not in loc:
                errors.append(f"locations[{i}] missing {field}")
    return errors


def validate_meals(meals: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for i, meal in enumerate(meals):
        for field in REQUIRED_MEAL_FIELDS:
            if field not in meal:
                errors.append(f"meals[{i}] missing {field}")
                continue
        if meal.get("type") == "grocery":
            if not meal.get("items"):
                errors.append(f"meals[{i}] grocery missing items")
            if not meal.get("recipe"):
                errors.append(f"meals[{i}] grocery missing recipe")
        goals = meal.get("goals") or []
        if not goals:
            errors.append(f"meals[{i}] goals empty")
    return errors


@lru_cache(maxsize=1)
def load_locations() -> list[dict[str, Any]]:
    data = _read_json("locations.json")
    locations = data["locations"] if isinstance(data, dict) else data
    errors = validate_locations(locations)
    if errors:
        raise ValueError("Invalid locations.json:\n" + "\n".join(errors[:20]))
    return locations


@lru_cache(maxsize=1)
def load_meals() -> list[dict[str, Any]]:
    data = _read_json("meals.json")
    meals = data["meals"] if isinstance(data, dict) else data
    errors = validate_meals(meals)
    if errors:
        raise ValueError("Invalid meals.json:\n" + "\n".join(errors[:20]))
    return meals


def reload_datasets() -> None:
    load_locations.cache_clear()
    load_meals.cache_clear()
