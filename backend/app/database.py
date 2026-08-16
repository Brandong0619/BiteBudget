import math
from typing import Any

from supabase import Client, create_client

from app.config import settings

# Texas combined sales tax in San Antonio (~8.25%)
TAX_RATE = 0.0825

# Curated MVP data for San Antonio pilot zone
# Prices are estimates based on typical SA menu pricing (Aug 2025)
LOCATIONS: list[dict[str, Any]] = [
    {
        "name": "Chipotle - Alamo Heights",
        "chain": "Chipotle",
        "type": "restaurant",
        "address": "4210 Broadway St, San Antonio, TX 78209",
        "lat": 29.4678,
        "lng": -98.4634,
    },
    {
        "name": "Chipotle - Downtown",
        "chain": "Chipotle",
        "type": "restaurant",
        "address": "733 E Houston St, San Antonio, TX 78205",
        "lat": 29.4267,
        "lng": -98.4847,
    },
    {
        "name": "Whataburger - St Mary's",
        "chain": "Whataburger",
        "type": "restaurant",
        "address": "2427 N St Mary's St, San Antonio, TX 78212",
        "lat": 29.4465,
        "lng": -98.4821,
    },
    {
        "name": "Panda Express - UTSA Loop",
        "chain": "Panda Express",
        "type": "restaurant",
        "address": "5706 UTSA Blvd, San Antonio, TX 78249",
        "lat": 29.5831,
        "lng": -98.6198,
    },
    {
        "name": "Torchy's Tacos - The Pearl",
        "chain": "Torchy's Tacos",
        "type": "restaurant",
        "address": "302 Pearl Pkwy, San Antonio, TX 78215",
        "lat": 29.4421,
        "lng": -98.4803,
    },
    {
        "name": "H-E-B - Alamo Heights",
        "chain": "H-E-B",
        "type": "grocery",
        "address": "300 W Olmos Dr, San Antonio, TX 78212",
        "lat": 29.4712,
        "lng": -98.4891,
    },
    {
        "name": "H-E-B - Southside",
        "chain": "H-E-B",
        "type": "grocery",
        "address": "4100 S New Braunfels Ave, San Antonio, TX 78223",
        "lat": 29.3856,
        "lng": -98.4612,
    },
    {
        "name": "H-E-B Plus - Bulverde",
        "chain": "H-E-B",
        "type": "grocery",
        "address": "2070 N Loop 1604 E, San Antonio, TX 78232",
        "lat": 29.6123,
        "lng": -98.4567,
    },
]

MEALS: list[dict[str, Any]] = [
    {
        "location_chain": "Chipotle",
        "type": "restaurant",
        "order": "Chicken bowl — white rice, pinto beans, fajita veggies, salsa, NO cheese/sour cream",
        "price": 9.25,
        "calories": 520,
        "protein_g": 42,
        "carbs_g": 58,
        "fat_g": 12,
        "goals": ["gain_muscle", "maintain"],
    },
    {
        "location_chain": "Chipotle",
        "type": "restaurant",
        "order": "Chicken salad — lettuce, black beans, fajita veggies, salsa, NO rice",
        "price": 9.25,
        "calories": 340,
        "protein_g": 38,
        "carbs_g": 22,
        "fat_g": 10,
        "goals": ["lose_weight", "maintain"],
    },
    {
        "location_chain": "Whataburger",
        "type": "restaurant",
        "order": "Grilled chicken sandwich — no mayo, add extra lettuce & tomato",
        "price": 6.49,
        "calories": 380,
        "protein_g": 32,
        "carbs_g": 38,
        "fat_g": 9,
        "goals": ["gain_muscle", "maintain", "lose_weight"],
    },
    {
        "location_chain": "Whataburger",
        "type": "restaurant",
        "order": "Whataburger Jr. — plain, no cheese, no mayo",
        "price": 4.29,
        "calories": 310,
        "protein_g": 16,
        "carbs_g": 28,
        "fat_g": 14,
        "goals": ["lose_weight", "maintain"],
    },
    {
        "location_chain": "Panda Express",
        "type": "restaurant",
        "order": "Bowl — grilled teriyaki chicken + super greens (no rice)",
        "price": 8.99,
        "calories": 360,
        "protein_g": 36,
        "carbs_g": 18,
        "fat_g": 14,
        "goals": ["lose_weight", "gain_muscle"],
    },
    {
        "location_chain": "Panda Express",
        "type": "restaurant",
        "order": "Plate — black pepper chicken + chow mein (half portion rice)",
        "price": 9.49,
        "calories": 680,
        "protein_g": 34,
        "carbs_g": 72,
        "fat_g": 22,
        "goals": ["gain_muscle"],
    },
    {
        "location_chain": "Torchy's Tacos",
        "type": "restaurant",
        "order": "Mr. Orange — corn tortilla, add grilled chicken, no queso",
        "price": 5.50,
        "calories": 420,
        "protein_g": 28,
        "carbs_g": 32,
        "fat_g": 18,
        "goals": ["gain_muscle", "maintain"],
    },
    {
        "location_chain": "H-E-B",
        "type": "grocery",
        "order": "Muscle Bowl — 1 dozen eggs + 1 bag spinach + 1 can black beans",
        "items": ["H-E-B dozen large eggs ($2.89)", "Fresh spinach 10oz ($2.49)", "H-E-B black beans 15oz ($0.89)"],
        "recipe": "Scramble 3 eggs with spinach. Heat black beans. Makes 4 servings — ~$1.57/meal, 5 min.",
        "prep_minutes": 5,
        "price": 6.27,
        "calories": 380,
        "protein_g": 28,
        "carbs_g": 22,
        "fat_g": 18,
        "goals": ["gain_muscle", "maintain"],
    },
    {
        "location_chain": "H-E-B",
        "type": "grocery",
        "order": "Protein Wrap Fix — rotisserie chicken + whole wheat tortillas + salsa",
        "items": ["H-E-B rotisserie chicken ($7.98)", "Whole wheat tortillas 8ct ($2.29)", "H-E-B salsa 16oz ($1.99)"],
        "recipe": "Shred chicken, wrap with salsa. Makes 4 wraps — ~$3.07/wrap, 3 min each.",
        "prep_minutes": 3,
        "price": 12.26,
        "calories": 320,
        "protein_g": 32,
        "carbs_g": 28,
        "fat_g": 8,
        "goals": ["gain_muscle", "maintain"],
        "per_serving_price": 3.07,
    },
    {
        "location_chain": "H-E-B",
        "type": "grocery",
        "order": "Budget Cut Bowl — canned tuna + microwave rice + frozen broccoli",
        "items": ["Chicken of the Sea tuna 5oz x2 ($1.98)", "H-E-B microwavable rice ($1.49)", "Frozen broccoli 12oz ($1.29)"],
        "recipe": "Microwave rice & broccoli, mix with tuna. Makes 2 bowls — ~$2.38/bowl, 5 min.",
        "prep_minutes": 5,
        "price": 4.76,
        "calories": 410,
        "protein_g": 32,
        "carbs_g": 48,
        "fat_g": 6,
        "goals": ["gain_muscle", "lose_weight", "maintain"],
        "per_serving_price": 2.38,
    },
    {
        "location_chain": "H-E-B",
        "type": "grocery",
        "order": "Light & Lean — Greek yogurt + banana + peanut butter",
        "items": ["H-E-B plain Greek yogurt 32oz ($3.99)", "Banana bunch ($0.69)", "H-E-B natural PB 16oz ($2.99)"],
        "recipe": "1 cup yogurt + 1 banana + 1 tbsp PB. Makes 4 servings — ~$1.92/meal, 2 min.",
        "prep_minutes": 2,
        "price": 7.67,
        "calories": 340,
        "protein_g": 22,
        "carbs_g": 38,
        "fat_g": 12,
        "goals": ["lose_weight", "maintain"],
        "per_serving_price": 1.92,
    },
]


def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 3959
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.asin(math.sqrt(a))


def with_tax(price: float) -> float:
    return round(price * (1 + TAX_RATE), 2)


def get_supabase() -> Client | None:
    if settings.supabase_url and settings.supabase_key:
        return create_client(settings.supabase_url, settings.supabase_key)
    return None


def fetch_recommendations(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
) -> tuple[dict | None, dict | None]:
    """Return best restaurant and grocery options within budget for the goal."""
    client = get_supabase()

    if client:
        try:
            result = client.rpc(
                "get_recommendations",
                {"p_budget": budget, "p_goal": goal, "p_lat": lat, "p_lng": lng},
            ).execute()
            if result.data:
                data = result.data
                return data.get("restaurant"), data.get("grocery")
        except Exception:
            pass

    return _local_recommendations(budget, goal, lat, lng)


def _local_recommendations(
    budget: float,
    goal: str,
    lat: float,
    lng: float,
) -> tuple[dict | None, dict | None]:
    restaurant_candidates: list[tuple[float, dict]] = []
    grocery_candidates: list[tuple[float, dict]] = []

    for meal in MEALS:
        if goal not in meal["goals"]:
            continue

        price = meal.get("per_serving_price", meal["price"])
        price_with_tax = with_tax(price)
        if price_with_tax > budget:
            continue

        matching_locations = [
            loc
            for loc in LOCATIONS
            if loc["chain"] == meal["location_chain"] and loc["type"] == meal["type"]
        ]

        for loc in matching_locations:
            dist = haversine_miles(lat, lng, loc["lat"], loc["lng"])
            entry = {
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
            }
            score = _score_option(meal, goal, dist, price_with_tax, budget)
            if meal["type"] == "restaurant":
                restaurant_candidates.append((score, entry))
            else:
                grocery_candidates.append((score, entry))

    restaurant = max(restaurant_candidates, key=lambda x: x[0])[1] if restaurant_candidates else None
    grocery = max(grocery_candidates, key=lambda x: x[0])[1] if grocery_candidates else None
    return restaurant, grocery


def _score_option(
    meal: dict,
    goal: str,
    distance: float,
    price_with_tax: float,
    budget: float,
) -> float:
    protein = meal["protein_g"]
    calories = meal["calories"]
    savings = budget - price_with_tax

    score = 0.0
    score += protein * 2
    score += savings * 3
    score -= distance * 5

    if goal == "lose_weight":
        score -= max(0, calories - 450) * 0.05
        score += protein * 1.5
    elif goal == "gain_muscle":
        score += protein * 3
        score += max(0, calories - 400) * 0.02

    if meal["type"] == "grocery":
        score += 8  # prefer savings when comparable

    return score
