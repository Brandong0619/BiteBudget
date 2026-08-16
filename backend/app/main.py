from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import TAX_RATE, fetch_recommendations
from app.models import (
    GroceryOption,
    HealthGoal,
    RecommendationRequest,
    RecommendationResponse,
    RestaurantOption,
)

app = FastAPI(
    title="BiteBudget API",
    description="Budget-conscious meal recommendations for San Antonio",
    version="0.1.0",
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "city": "San Antonio, TX"}


@app.get("/api/goals")
def list_goals():
    return [
        {"id": "gain_muscle", "label": "Gain muscle", "description": "High protein, calorie-dense options"},
        {"id": "lose_weight", "label": "Lose weight", "description": "Lower calorie, high protein picks"},
        {"id": "maintain", "label": "Maintain", "description": "Balanced macros within your budget"},
    ]


@app.post("/api/recommendations", response_model=RecommendationResponse)
def get_recommendations(body: RecommendationRequest):
    lat = body.lat if body.lat is not None else settings.default_lat
    lng = body.lng if body.lng is not None else settings.default_lng

    restaurant_raw, grocery_raw = fetch_recommendations(
        budget=body.budget,
        goal=body.goal.value,
        lat=lat,
        lng=lng,
    )

    restaurant = RestaurantOption(**restaurant_raw) if restaurant_raw else None
    grocery = GroceryOption(**grocery_raw) if grocery_raw else None

    message = None
    if not restaurant and not grocery:
        message = (
            f"No options found under ${body.budget:.2f} (incl. tax) for your goal. "
            "Try raising your budget or switching goals."
        )
    elif not restaurant:
        message = "No restaurant orders fit your budget — but H-E-B has you covered below."
    elif not grocery:
        message = "No H-E-B combo under budget nearby — restaurant option below works."

    return RecommendationResponse(
        budget=body.budget,
        goal=body.goal,
        tax_rate=TAX_RATE,
        restaurant=restaurant,
        grocery=grocery,
        message=message,
    )
