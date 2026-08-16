from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class HealthGoal(str, Enum):
    GAIN_MUSCLE = "gain_muscle"
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN = "maintain"


class RecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0, le=100, description="Max spend in USD including tax")
    goal: HealthGoal
    lat: float | None = None
    lng: float | None = None


class RestaurantOption(BaseModel):
    type: Literal["restaurant"] = "restaurant"
    name: str
    chain: str
    address: str
    distance_miles: float
    order: str
    price: float
    price_with_tax: float
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    lat: float
    lng: float


class GroceryOption(BaseModel):
    type: Literal["grocery"] = "grocery"
    store: str
    store_chain: str
    address: str
    distance_miles: float
    items: list[str]
    recipe: str
    prep_minutes: int
    price: float
    price_with_tax: float
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    lat: float
    lng: float


class RecommendationResponse(BaseModel):
    budget: float
    goal: HealthGoal
    tax_rate: float
    restaurant: RestaurantOption | None
    grocery: GroceryOption | None
    message: str | None = None
