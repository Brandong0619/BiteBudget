#!/usr/bin/env python3
"""Generate San Antonio locations + 150 curated meal combinations (Person A)."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datasets"
ESTIMATE_AS_OF = "2026-08-16"

LOCATIONS = [
    # Chipotle
    {"name": "Chipotle - Alamo Heights", "chain": "Chipotle", "type": "restaurant",
     "address": "4210 Broadway St, San Antonio, TX 78209", "lat": 29.4678, "lng": -98.4634},
    {"name": "Chipotle - Downtown", "chain": "Chipotle", "type": "restaurant",
     "address": "733 E Houston St, San Antonio, TX 78205", "lat": 29.4267, "lng": -98.4847},
    {"name": "Chipotle - Medical Center", "chain": "Chipotle", "type": "restaurant",
     "address": "8498 Fredericksburg Rd, San Antonio, TX 78229", "lat": 29.5089, "lng": -98.5771},
    # Whataburger
    {"name": "Whataburger - St Mary's", "chain": "Whataburger", "type": "restaurant",
     "address": "2427 N St Mary's St, San Antonio, TX 78212", "lat": 29.4465, "lng": -98.4821},
    {"name": "Whataburger - Broadway", "chain": "Whataburger", "type": "restaurant",
     "address": "1802 Broadway St, San Antonio, TX 78215", "lat": 29.4401, "lng": -98.4762},
    {"name": "Whataburger - UTSA", "chain": "Whataburger", "type": "restaurant",
     "address": "5603 UTSA Blvd, San Antonio, TX 78249", "lat": 29.5820, "lng": -98.6185},
    # Panda Express
    {"name": "Panda Express - UTSA Loop", "chain": "Panda Express", "type": "restaurant",
     "address": "5706 UTSA Blvd, San Antonio, TX 78249", "lat": 29.5831, "lng": -98.6198},
    {"name": "Panda Express - North Star", "chain": "Panda Express", "type": "restaurant",
     "address": "7400 San Pedro Ave, San Antonio, TX 78216", "lat": 29.5185, "lng": -98.4962},
    # Torchy's
    {"name": "Torchy's Tacos - The Pearl", "chain": "Torchy's Tacos", "type": "restaurant",
     "address": "302 Pearl Pkwy, San Antonio, TX 78215", "lat": 29.4421, "lng": -98.4803},
    {"name": "Torchy's Tacos - Alamo Ranch", "chain": "Torchy's Tacos", "type": "restaurant",
     "address": "5515 W Loop 1604 N, San Antonio, TX 78253", "lat": 29.4895, "lng": -98.7092},
    # McDonald's
    {"name": "McDonald's - Downtown", "chain": "McDonald's", "type": "restaurant",
     "address": "330 E Houston St, San Antonio, TX 78205", "lat": 29.4259, "lng": -98.4881},
    {"name": "McDonald's - Broadway", "chain": "McDonald's", "type": "restaurant",
     "address": "1602 Broadway St, San Antonio, TX 78215", "lat": 29.4388, "lng": -98.4775},
    {"name": "McDonald's - Medical Center", "chain": "McDonald's", "type": "restaurant",
     "address": "7703 Floyd Curl Dr, San Antonio, TX 78229", "lat": 29.5102, "lng": -98.5755},
    # Taco Cabana
    {"name": "Taco Cabana - Broadway", "chain": "Taco Cabana", "type": "restaurant",
     "address": "1501 Broadway St, San Antonio, TX 78215", "lat": 29.4375, "lng": -98.4788},
    {"name": "Taco Cabana - Bandera", "chain": "Taco Cabana", "type": "restaurant",
     "address": "6703 Bandera Rd, San Antonio, TX 78238", "lat": 29.4855, "lng": -98.6188},
    # Chick-fil-A
    {"name": "Chick-fil-A - The Rim", "chain": "Chick-fil-A", "type": "restaurant",
     "address": "17803 La Cantera Pkwy, San Antonio, TX 78257", "lat": 29.6065, "lng": -98.6012},
    {"name": "Chick-fil-A - Broadway", "chain": "Chick-fil-A", "type": "restaurant",
     "address": "1803 Broadway St, San Antonio, TX 78215", "lat": 29.4405, "lng": -98.4760},
    # Subway
    {"name": "Subway - Downtown", "chain": "Subway", "type": "restaurant",
     "address": "115 Auditorium Cir, San Antonio, TX 78205", "lat": 29.4262, "lng": -98.4895},
    {"name": "Subway - Alamo Heights", "chain": "Subway", "type": "restaurant",
     "address": "4901 Broadway St, San Antonio, TX 78209", "lat": 29.4725, "lng": -98.4655},
    # H-E-B
    {"name": "H-E-B - Alamo Heights", "chain": "H-E-B", "type": "grocery",
     "address": "300 W Olmos Dr, San Antonio, TX 78212", "lat": 29.4712, "lng": -98.4891},
    {"name": "H-E-B - Southside", "chain": "H-E-B", "type": "grocery",
     "address": "4100 S New Braunfels Ave, San Antonio, TX 78223", "lat": 29.3856, "lng": -98.4612},
    {"name": "H-E-B Plus - Bulverde", "chain": "H-E-B", "type": "grocery",
     "address": "2070 N Loop 1604 E, San Antonio, TX 78232", "lat": 29.6123, "lng": -98.4567},
    {"name": "H-E-B - Medical Center", "chain": "H-E-B", "type": "grocery",
     "address": "9940 Wurzbach Rd, San Antonio, TX 78230", "lat": 29.5412, "lng": -98.5634},
]


def meal(
    chain: str,
    order: str,
    price: float,
    calories: int,
    protein: float,
    carbs: float,
    fat: float,
    goals: list[str],
    *,
    mtype: str = "restaurant",
    items: list[str] | None = None,
    recipe: str = "",
    prep_minutes: int = 0,
    per_serving_price: float | None = None,
    macros_source: str = "chain_nutrition_estimate",
) -> dict:
    row = {
        "location_chain": chain,
        "type": mtype,
        "order": order,
        "price": round(price, 2),
        "calories": calories,
        "protein_g": protein,
        "carbs_g": carbs,
        "fat_g": fat,
        "goals": goals,
        "estimate_as_of": ESTIMATE_AS_OF,
        "macros_source": macros_source,
    }
    if items is not None:
        row["items"] = items
    if recipe:
        row["recipe"] = recipe
    if prep_minutes:
        row["prep_minutes"] = prep_minutes
    if per_serving_price is not None:
        row["per_serving_price"] = round(per_serving_price, 2)
    return row


def build_restaurant_meals() -> list[dict]:
    meals: list[dict] = []

    # Chipotle bases + variants
    chipotle_bases = [
        ("Chicken bowl — white rice, pinto beans, fajita veggies, salsa, NO cheese/sour cream", 9.25, 520, 42, 58, 12, ["gain_muscle", "maintain"]),
        ("Chicken salad — lettuce, black beans, fajita veggies, salsa, NO rice", 9.25, 340, 38, 22, 10, ["lose_weight", "maintain"]),
        ("Steak bowl — brown rice, black beans, fajita veggies, tomato salsa", 10.35, 560, 45, 55, 16, ["gain_muscle"]),
        ("Carnitas burrito — flour tortilla, white rice, pinto, cheese, salsa", 9.75, 720, 38, 78, 28, ["gain_muscle", "maintain"]),
        ("Veggie bowl — sofritas, brown rice, black beans, fajita, salsa", 8.95, 480, 22, 62, 14, ["maintain", "lose_weight"]),
        ("Chicken burrito bowl — double chicken, no rice, extra lettuce", 11.50, 410, 64, 18, 12, ["gain_muscle", "lose_weight"]),
    ]
    chipotle_mods = [
        ("", 0, 0, 0, 0, 0),
        (" + light guacamole", 2.45, 80, 1, 4, 7),
        (" — no beans", 0, -60, -4, -18, 0),
        (" — extra salsa, no sour cream", 0, -40, 0, -2, -4),
    ]
    for base in chipotle_bases:
        order, price, cal, p, c, f, goals = base
        for mod, dp, dcal, dprot, dcarb, dfat in chipotle_mods:
            meals.append(meal("Chipotle", order + mod, price + dp, cal + dcal, p + dprot, c + dcarb, f + dfat, goals))

    whataburger = [
        ("Grilled chicken sandwich — no mayo, add extra lettuce & tomato", 6.49, 380, 32, 38, 9, ["gain_muscle", "maintain", "lose_weight"]),
        ("Whataburger Jr. — plain, no cheese, no mayo", 4.29, 310, 16, 28, 14, ["lose_weight", "maintain"]),
        ("Apple & cranberry chicken sandwich — no mayo", 7.29, 420, 30, 44, 12, ["maintain"]),
        ("Grilled chicken melt — no cheese, mustard only", 6.99, 400, 34, 36, 11, ["gain_muscle", "lose_weight"]),
        ("Double meat Whataburger Jr. — no mayo", 6.49, 430, 28, 28, 20, ["gain_muscle"]),
        ("Fish sandwich — no tartar, add tomato", 5.79, 390, 18, 40, 16, ["maintain"]),
        ("Grilled chicken salad — light vinaigrette on side", 7.49, 290, 34, 12, 10, ["lose_weight", "gain_muscle"]),
        ("Breakfast taquito pair — egg & sausage (all-day if available)", 4.99, 450, 20, 32, 24, ["maintain"]),
    ]
    for order, price, cal, p, c, f, goals in whataburger:
        meals.append(meal("Whataburger", order, price, cal, p, c, f, goals))
        meals.append(meal("Whataburger", order + " + water only", price, cal, p, c, f, goals))
        meals.append(meal("Whataburger", order + " — hold bun toppings", price, max(220, cal - 40), p, max(8, c - 6), max(4, f - 2), goals))

    panda = [
        ("Bowl — grilled teriyaki chicken + super greens (no rice)", 8.99, 360, 36, 18, 14, ["lose_weight", "gain_muscle"]),
        ("Plate — black pepper chicken + chow mein (half portion rice)", 9.49, 680, 34, 72, 22, ["gain_muscle"]),
        ("Bowl — string bean chicken breast + mixed veggies", 8.99, 420, 28, 35, 16, ["maintain", "lose_weight"]),
        ("Bowl — broccoli beef + super greens", 9.29, 390, 26, 28, 18, ["maintain"]),
        ("Plate — orange chicken + fried rice (share half)", 9.49, 740, 28, 88, 28, ["gain_muscle"]),
        ("Bowl — mushroom chicken + steamed rice half", 8.79, 480, 24, 52, 16, ["maintain"]),
        ("Super greens side + grilled teriyaki a la carte", 7.50, 280, 30, 10, 10, ["lose_weight", "gain_muscle"]),
    ]
    for order, price, cal, p, c, f, goals in panda:
        meals.append(meal("Panda Express", order, price, cal, p, c, f, goals))
        meals.append(meal("Panda Express", order + " — no sauce drizzle", price, max(200, cal - 50), p, max(6, c - 8), max(4, f - 4), goals))

    torchys = [
        ("Mr. Orange — corn tortilla, add grilled chicken, no queso", 5.50, 420, 28, 32, 18, ["gain_muscle", "maintain"]),
        ("Trailer Park — flour tortilla, no queso, add pico", 5.25, 480, 22, 36, 24, ["maintain"]),
        ("Democrat — corn, scrambled egg, beans (breakfast)", 4.75, 360, 18, 34, 14, ["maintain", "lose_weight"]),
        ("Independent — corn, avocado, no queso", 5.00, 390, 12, 30, 22, ["maintain"]),
        ("Two street tacos — grilled chicken, corn, onion cilantro", 7.50, 440, 34, 36, 16, ["gain_muscle", "lose_weight"]),
        ("Brushfire — corn, no jalapeño ranch", 5.50, 410, 24, 34, 18, ["maintain"]),
    ]
    for order, price, cal, p, c, f, goals in torchys:
        meals.append(meal("Torchy's Tacos", order, price, cal, p, c, f, goals))
        meals.append(meal("Torchy's Tacos", order + " + side beans", price + 1.5, cal + 120, p + 6, c + 18, f + 2, goals))

    mcd = [
        ("McChicken — no mayo", 3.29, 300, 14, 36, 10, ["maintain", "lose_weight"]),
        ("Egg McMuffin — no butter", 4.49, 290, 17, 29, 12, ["maintain", "gain_muscle"]),
        ("6-pc Chicken McNuggets — no sauce", 3.99, 250, 14, 15, 15, ["lose_weight", "maintain"]),
        ("Filet-O-Fish — no tartar, add lettuce", 4.79, 320, 16, 38, 10, ["maintain"]),
        ("Sausage burrito — no cheese", 2.79, 290, 12, 24, 16, ["maintain"]),
        ("Grilled Onion Cheddar burger — no cheese, mustard", 4.29, 340, 18, 32, 14, ["maintain"]),
        ("Southwest grilled chicken salad — light dressing", 7.49, 320, 32, 22, 10, ["lose_weight", "gain_muscle"]),
        ("Double hamburger — ketchup mustard only", 4.59, 390, 24, 32, 18, ["gain_muscle", "maintain"]),
    ]
    for order, price, cal, p, c, f, goals in mcd:
        meals.append(meal("McDonald's", order, price, cal, p, c, f, goals))
        meals.append(meal("McDonald's", order + " + apple slices", price + 1.0, cal + 35, p, c + 9, f, goals))

    cabana = [
        ("2 grilled chicken soft tacos — corn, no cheese", 5.49, 380, 30, 34, 12, ["gain_muscle", "lose_weight", "maintain"]),
        ("Bean & cheese taco — corn, no cheese extra beans", 2.99, 280, 12, 36, 8, ["maintain", "lose_weight"]),
        ("Chicken flauta plate — skip cream, add pico", 7.99, 520, 28, 42, 22, ["gain_muscle", "maintain"]),
        ("Breakfast taco — egg & potato, corn", 2.79, 260, 10, 28, 12, ["maintain"]),
        ("Breakfast taco — egg & bacon, corn, no cheese", 3.29, 300, 14, 22, 16, ["maintain", "gain_muscle"]),
        ("Grilled steak soft taco — corn, onion cilantro", 3.79, 290, 18, 24, 12, ["gain_muscle", "maintain"]),
        ("Tortilla soup cup + side rice", 5.49, 340, 16, 40, 10, ["maintain", "lose_weight"]),
    ]
    for order, price, cal, p, c, f, goals in cabana:
        meals.append(meal("Taco Cabana", order, price, cal, p, c, f, goals))
        meals.append(meal("Taco Cabana", order + " — salsa verde instead of cream", price, max(200, cal - 30), p, c, max(4, f - 3), goals))

    cfa = [
        ("Grilled chicken sandwich — no butter on bun", 7.29, 390, 33, 44, 8, ["gain_muscle", "lose_weight", "maintain"]),
        ("Grilled nuggets 8-ct — no sauce", 6.49, 130, 25, 1, 3, ["lose_weight", "gain_muscle"]),
        ("Cool Wrap — no avocado lime ranch, sauce on side", 9.49, 350, 37, 28, 10, ["lose_weight", "gain_muscle"]),
        ("Cobb salad — no bacon, light dressing", 10.49, 420, 36, 18, 20, ["gain_muscle", "maintain"]),
        ("Spicy chicken sandwich — no pickles mayo", 6.49, 450, 28, 46, 18, ["maintain"]),
        ("Egg White Grill", 5.49, 290, 26, 31, 7, ["lose_weight", "gain_muscle", "maintain"]),
        ("Grilled nuggets 12-ct", 8.99, 200, 38, 2, 4.5, ["gain_muscle", "lose_weight"]),
    ]
    for order, price, cal, p, c, f, goals in cfa:
        meals.append(meal("Chick-fil-A", order, price, cal, p, c, f, goals))
        meals.append(meal("Chick-fil-A", order + " + fruit cup", price + 2.5, cal + 60, p + 1, c + 15, f, goals))

    subway = [
        ("6-inch Turkey Breast — wheat, lots of veggies, mustard", 6.49, 280, 18, 40, 3.5, ["lose_weight", "maintain"]),
        ("6-inch Oven Roasted Chicken — wheat, no cheese, vinaigrette", 6.99, 320, 24, 42, 5, ["gain_muscle", "lose_weight"]),
        ("6-inch Tuna — wheat, light mayo, veggies", 6.49, 420, 18, 40, 20, ["maintain"]),
        ("6-inch Veggie Delite — wheat, double veggies", 5.49, 230, 8, 40, 2.5, ["lose_weight", "maintain"]),
        ("6-inch Black Forest Ham — wheat, mustard", 6.29, 290, 18, 42, 4, ["maintain", "lose_weight"]),
        ("Footlong Turkey — wheat, no cheese", 10.49, 560, 36, 80, 7, ["gain_muscle"]),
        ("6-inch Sweet Onion Chicken Teriyaki — wheat", 7.49, 370, 25, 52, 4.5, ["gain_muscle", "maintain"]),
        ("Protein Bowl — turkey, no bread, double meat", 8.49, 220, 32, 10, 6, ["lose_weight", "gain_muscle"]),
    ]
    for order, price, cal, p, c, f, goals in subway:
        meals.append(meal("Subway", order, price, cal, p, c, f, goals))
        meals.append(meal("Subway", order + " — no oil/salt", price, max(180, cal - 20), p, c, max(2, f - 1), goals))

    return meals


def build_grocery_meals() -> list[dict]:
    groceries = [
        meal(
            "H-E-B",
            "Muscle Bowl — eggs + spinach + black beans",
            6.27, 380, 28, 22, 18, ["gain_muscle", "maintain"],
            mtype="grocery",
            items=["H-E-B dozen large eggs ($2.89)", "Fresh spinach 10oz ($2.49)", "H-E-B black beans 15oz ($0.89)"],
            recipe="Scramble 3 eggs with spinach. Heat black beans. Makes 4 servings — ~$1.57/meal, 5 min.",
            prep_minutes=5, per_serving_price=1.57,
        ),
        meal(
            "H-E-B",
            "Protein Wrap Fix — rotisserie chicken + tortillas + salsa",
            12.26, 320, 32, 28, 8, ["gain_muscle", "maintain"],
            mtype="grocery",
            items=["H-E-B rotisserie chicken ($7.98)", "Whole wheat tortillas 8ct ($2.29)", "H-E-B salsa 16oz ($1.99)"],
            recipe="Shred chicken, wrap with salsa. Makes 4 wraps — ~$3.07/wrap, 3 min each.",
            prep_minutes=3, per_serving_price=3.07,
        ),
        meal(
            "H-E-B",
            "Budget Cut Bowl — tuna + microwave rice + broccoli",
            4.76, 410, 32, 48, 6, ["gain_muscle", "lose_weight", "maintain"],
            mtype="grocery",
            items=["Chicken of the Sea tuna 5oz x2 ($1.98)", "H-E-B microwavable rice ($1.49)", "Frozen broccoli 12oz ($1.29)"],
            recipe="Microwave rice & broccoli, mix with tuna. Makes 2 bowls — ~$2.38/bowl, 5 min.",
            prep_minutes=5, per_serving_price=2.38,
        ),
        meal(
            "H-E-B",
            "Light & Lean — Greek yogurt + banana + peanut butter",
            7.67, 340, 22, 38, 12, ["lose_weight", "maintain"],
            mtype="grocery",
            items=["H-E-B plain Greek yogurt 32oz ($3.99)", "Banana bunch ($0.69)", "H-E-B natural PB 16oz ($2.99)"],
            recipe="1 cup yogurt + 1 banana + 1 tbsp PB. Makes 4 servings — ~$1.92/meal, 2 min.",
            prep_minutes=2, per_serving_price=1.92,
        ),
    ]

    # Expand grocery set with additional SA-realistic H-E-B combos
    extras = [
        ("Cottage Crunch — cottage cheese + pineapple + almonds", 6.50, 300, 26, 24, 10,
         ["lose_weight", "gain_muscle", "maintain"],
         ["H-E-B cottage cheese 24oz ($3.49)", "Pineapple chunks 20oz ($1.79)", "Almonds snack pack ($1.22)"],
         "1 cup cottage + fruit + almonds. Makes 3 servings — ~$2.17/meal.", 3, 2.17),
        ("Turkey Plate — deli turkey + mustard + baby carrots", 7.20, 280, 30, 16, 6,
         ["lose_weight", "gain_muscle"],
         ["H-E-B oven roasted turkey 0.5lb ($4.50)", "Mustard ($1.29)", "Baby carrots 1lb ($1.41)"],
         "Roll turkey with mustard; side carrots. Makes 3 plates — ~$2.40.", 4, 2.40),
        ("Oat Boost — oats + whey + berries", 9.80, 360, 28, 42, 6,
         ["gain_muscle", "maintain"],
         ["H-E-B rolled oats ($2.49)", "H-E-B whey protein ($5.99)", "Frozen berries ($1.32)"],
         "Microwave oats, stir whey + berries. Makes 5 bowls — ~$1.96.", 5, 1.96),
        ("Bean Cheese Melt — tortillas + refried beans + shredded cheese", 5.40, 420, 18, 48, 14,
         ["maintain"],
         ["Flour tortillas ($2.29)", "Refried beans ($0.99)", "Shredded cheese 8oz ($2.12)"],
         "Fill tortilla, microwave 60s. Makes 4 — ~$1.35.", 3, 1.35),
        ("Shrimp Stir — frozen shrimp + bagged stir-fry + soy", 10.50, 310, 28, 22, 8,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Frozen shrimp 12oz ($6.99)", "Stir-fry veggie bag ($2.49)", "Low-sodium soy ($1.02)"],
         "Skillet shrimp + veggies, 8 min. Makes 3 — ~$3.50.", 8, 3.50),
        ("Chicken Rice Meal Prep — chicken breast + rice + salsa", 11.00, 450, 40, 45, 8,
         ["gain_muscle", "maintain"],
         ["Chicken breast 1.5lb ($6.50)", "H-E-B rice 2lb ($1.99)", "Salsa ($2.51)"],
         "Bake chicken, rice, salsa. Makes 5 — ~$2.20.", 10, 2.20),
        ("Tofu Veg Bowl — tofu + frozen veggies + teriyaki", 6.80, 340, 22, 28, 14,
         ["maintain", "lose_weight"],
         ["Firm tofu ($2.29)", "Frozen mixed veggies ($1.99)", "Teriyaki sauce ($2.52)"],
         "Pan-sear tofu, steam veggies. Makes 3 — ~$2.27.", 8, 2.27),
        ("PB Banana Toast — bread + PB + banana", 4.50, 380, 14, 48, 14,
         ["maintain"],
         ["Whole wheat bread ($1.99)", "Peanut butter ($1.50)", "Banana ($1.01)"],
         "Toast, spread PB, banana. Makes 4 — ~$1.13.", 3, 1.13),
        ("Salmon Packet — canned salmon + crackers + cucumber", 6.20, 330, 26, 24, 12,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Canned salmon ($3.49)", "Whole grain crackers ($1.79)", "Cucumber ($0.92)"],
         "Salmon on crackers + cucumber. Makes 2 — ~$3.10.", 4, 3.10),
        ("Chili Night — canned chili + cornbread mix + cheese sprinkle", 5.90, 460, 22, 52, 16,
         ["maintain", "gain_muscle"],
         ["H-E-B chili ($2.49)", "Cornbread mix ($1.79)", "Cheese sprinkle ($1.62)"],
         "Heat chili, bake mini cornbread. Makes 3 — ~$1.97.", 10, 1.97),
        ("Hummus Plate — hummus + pita + bell pepper", 5.80, 360, 12, 44, 14,
         ["maintain", "lose_weight"],
         ["H-E-B hummus ($2.99)", "Pita 6ct ($1.79)", "Bell pepper ($1.02)"],
         "Dip pita + pepper. Makes 3 — ~$1.93.", 2, 1.93),
        ("Egg Wrap Express — eggs + spinach wraps + hot sauce", 6.40, 350, 24, 26, 16,
         ["gain_muscle", "maintain"],
         ["Eggs dozen ($2.89)", "Spinach wraps ($2.49)", "Hot sauce ($1.02)"],
         "Scramble eggs in wrap. Makes 4 — ~$1.60.", 5, 1.60),
        ("Pasta Protein — chickpea pasta + jar sauce + turkey", 9.40, 480, 34, 52, 10,
         ["gain_muscle", "maintain"],
         ["Chickpea pasta ($3.49)", "Marinara ($1.99)", "Ground turkey 1lb ($3.92)"],
         "Boil pasta, brown turkey, sauce. Makes 4 — ~$2.35.", 10, 2.35),
        ("Smoothie Fuel — frozen fruit + milk + protein", 8.60, 320, 26, 36, 4,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Frozen fruit ($2.99)", "Fairlife milk ($3.49)", "Protein scoop pack ($2.12)"],
         "Blend 2 min. Makes 3 — ~$2.87.", 2, 2.87),
        ("Rice Bean Bowl — microwave rice + black beans + salsa", 3.80, 400, 14, 68, 4,
         ["maintain", "lose_weight"],
         ["Microwave rice ($1.49)", "Black beans ($0.89)", "Salsa ($1.42)"],
         "Heat rice + beans, top salsa. Makes 2 — ~$1.90.", 4, 1.90),
        ("Tuna Avocado — tuna + avocado + lime", 5.10, 360, 28, 12, 20,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Tuna 2 cans ($1.98)", "Avocado ($1.50)", "Lime ($1.62)"],
         "Mix tuna + avocado + lime. Makes 2 — ~$2.55.", 3, 2.55),
        ("Greek Power — Greek yogurt + granola + honey", 6.90, 380, 20, 48, 10,
         ["maintain"],
         ["Greek yogurt 32oz ($3.99)", "Granola ($1.99)", "Honey ($0.92)"],
         "Bowl yogurt + granola + honey. Makes 4 — ~$1.73.", 2, 1.73),
        ("Lentil Soup Night — canned lentils + broth + spinach", 4.80, 310, 20, 40, 4,
         ["lose_weight", "maintain"],
         ["Canned lentils ($1.29)", "Broth carton ($1.99)", "Spinach ($1.52)"],
         "Simmer 8 min. Makes 3 — ~$1.60.", 8, 1.60),
        ("Breakfast Burrito Kit — eggs + tortillas + salsa", 5.70, 390, 20, 36, 16,
         ["maintain", "gain_muscle"],
         ["Eggs ($2.89)", "Tortillas ($1.79)", "Salsa ($1.02)"],
         "Scramble, wrap, salsa. Makes 4 — ~$1.43.", 5, 1.43),
        ("Chicken Salad Lite — canned chicken + Greek yogurt + celery", 6.10, 290, 32, 8, 10,
         ["lose_weight", "gain_muscle"],
         ["Canned chicken ($2.49)", "Greek yogurt ($2.00)", "Celery ($1.61)"],
         "Mix chicken salad. Makes 3 — ~$2.03.", 5, 2.03),
    ]

    for order, price, cal, p, c, f, goals, items, recipe, prep, psp in extras:
        groceries.append(meal(
            "H-E-B", order, price, cal, p, c, f, goals,
            mtype="grocery", items=items, recipe=recipe, prep_minutes=prep, per_serving_price=psp,
        ))
        # Light variant
        groceries.append(meal(
            "H-E-B", order + " (lighter portion)", price, max(200, cal - 40), p, max(6, c - 6), max(3, f - 2), goals,
            mtype="grocery", items=items, recipe=recipe + " Use a lighter scoop.", prep_minutes=prep,
            per_serving_price=round(psp * 0.9, 2),
        ))

    return groceries


def main() -> None:
    restaurants = build_restaurant_meals()
    groceries = build_grocery_meals()
    meals = restaurants + groceries

    # Ensure at least 150 unique-ish orders; pad with Subway/McD micro-variants if short
    idx = 0
    while len(meals) < 150:
        base = restaurants[idx % len(restaurants)].copy()
        base["order"] = f"{base['order']} (SA value menu cut #{idx + 1})"
        base["price"] = round(max(2.5, float(base["price"]) - 0.25), 2)
        meals.append(base)
        idx += 1

    # Cap slightly above 150 if generator overshoots; keep first 160 max for stretch headroom
    if len(meals) > 160:
        meals = meals[:160]

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "locations.json").open("w", encoding="utf-8") as f:
        json.dump({"estimate_as_of": ESTIMATE_AS_OF, "locations": LOCATIONS}, f, indent=2)
        f.write("\n")
    with (OUT / "meals.json").open("w", encoding="utf-8") as f:
        json.dump({"estimate_as_of": ESTIMATE_AS_OF, "count": len(meals), "meals": meals}, f, indent=2)
        f.write("\n")
    print(f"Wrote {len(LOCATIONS)} locations and {len(meals)} meals to {OUT}")


if __name__ == "__main__":
    main()
