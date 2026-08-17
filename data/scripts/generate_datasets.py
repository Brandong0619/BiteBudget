#!/usr/bin/env python3
"""Generate cleaned San Antonio locations + curated meals (Person A v2).

Spot-checks use free public sources (Aug 2026): Chipotle/Whataburger/CFA nutrition
pages and menu price aggregators; H-E-B-style grocery estimates.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datasets"
ESTIMATE_AS_OF = "2026-08-16"

LOCATIONS = [
    {"name": "Chipotle - Alamo Heights", "chain": "Chipotle", "type": "restaurant",
     "address": "4210 Broadway St, San Antonio, TX 78209", "lat": 29.4678, "lng": -98.4634},
    {"name": "Chipotle - Downtown", "chain": "Chipotle", "type": "restaurant",
     "address": "733 E Houston St, San Antonio, TX 78205", "lat": 29.4267, "lng": -98.4847},
    {"name": "Chipotle - Medical Center", "chain": "Chipotle", "type": "restaurant",
     "address": "8498 Fredericksburg Rd, San Antonio, TX 78229", "lat": 29.5089, "lng": -98.5771},
    {"name": "Whataburger - St Mary's", "chain": "Whataburger", "type": "restaurant",
     "address": "2427 N St Mary's St, San Antonio, TX 78212", "lat": 29.4465, "lng": -98.4821},
    {"name": "Whataburger - Broadway", "chain": "Whataburger", "type": "restaurant",
     "address": "1802 Broadway St, San Antonio, TX 78215", "lat": 29.4401, "lng": -98.4762},
    {"name": "Whataburger - UTSA", "chain": "Whataburger", "type": "restaurant",
     "address": "5603 UTSA Blvd, San Antonio, TX 78249", "lat": 29.5820, "lng": -98.6185},
    {"name": "Panda Express - UTSA Loop", "chain": "Panda Express", "type": "restaurant",
     "address": "5706 UTSA Blvd, San Antonio, TX 78249", "lat": 29.5831, "lng": -98.6198},
    {"name": "Panda Express - North Star", "chain": "Panda Express", "type": "restaurant",
     "address": "7400 San Pedro Ave, San Antonio, TX 78216", "lat": 29.5185, "lng": -98.4962},
    {"name": "Torchy's Tacos - The Pearl", "chain": "Torchy's Tacos", "type": "restaurant",
     "address": "302 Pearl Pkwy, San Antonio, TX 78215", "lat": 29.4421, "lng": -98.4803},
    {"name": "Torchy's Tacos - Alamo Ranch", "chain": "Torchy's Tacos", "type": "restaurant",
     "address": "5515 W Loop 1604 N, San Antonio, TX 78253", "lat": 29.4895, "lng": -98.7092},
    {"name": "McDonald's - Downtown", "chain": "McDonald's", "type": "restaurant",
     "address": "330 E Houston St, San Antonio, TX 78205", "lat": 29.4259, "lng": -98.4881},
    {"name": "McDonald's - Broadway", "chain": "McDonald's", "type": "restaurant",
     "address": "1602 Broadway St, San Antonio, TX 78215", "lat": 29.4388, "lng": -98.4775},
    {"name": "McDonald's - Medical Center", "chain": "McDonald's", "type": "restaurant",
     "address": "7703 Floyd Curl Dr, San Antonio, TX 78229", "lat": 29.5102, "lng": -98.5755},
    {"name": "Taco Cabana - Broadway", "chain": "Taco Cabana", "type": "restaurant",
     "address": "1501 Broadway St, San Antonio, TX 78215", "lat": 29.4375, "lng": -98.4788},
    {"name": "Taco Cabana - Bandera", "chain": "Taco Cabana", "type": "restaurant",
     "address": "6703 Bandera Rd, San Antonio, TX 78238", "lat": 29.4855, "lng": -98.6188},
    {"name": "Chick-fil-A - The Rim", "chain": "Chick-fil-A", "type": "restaurant",
     "address": "17803 La Cantera Pkwy, San Antonio, TX 78257", "lat": 29.6065, "lng": -98.6012},
    {"name": "Chick-fil-A - Broadway", "chain": "Chick-fil-A", "type": "restaurant",
     "address": "1803 Broadway St, San Antonio, TX 78215", "lat": 29.4405, "lng": -98.4760},
    {"name": "Subway - Downtown", "chain": "Subway", "type": "restaurant",
     "address": "115 Auditorium Cir, San Antonio, TX 78205", "lat": 29.4262, "lng": -98.4895},
    {"name": "Subway - Alamo Heights", "chain": "Subway", "type": "restaurant",
     "address": "4901 Broadway St, San Antonio, TX 78209", "lat": 29.4725, "lng": -98.4655},
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
    pitch_wow: bool = False,
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
    if pitch_wow:
        row["pitch_wow"] = True
    return row


def build_restaurant_meals() -> list[dict]:
    meals: list[dict] = []

    # Pitch-spot-checked Chipotle (public 2026 avg bowl ~$9.80; lean build macros)
    chipotle = [
        ("Chicken bowl — white rice, pinto, fajita, salsa, NO cheese/sour cream", 9.80, 520, 42, 58, 12,
         ["gain_muscle", "maintain"], True),
        ("Chicken salad — lettuce, black beans, fajita, salsa, NO rice", 9.80, 340, 38, 22, 10,
         ["lose_weight", "maintain"], True),
        ("Double chicken bowl — no rice, beans, fajita, salsa, lettuce", 12.50, 450, 64, 28, 14,
         ["gain_muscle", "lose_weight"], True),
        ("Steak bowl — brown rice, black beans, fajita, tomato salsa", 11.50, 540, 42, 52, 16,
         ["gain_muscle"], False),
        ("Carnitas burrito — flour, white rice, pinto, cheese, salsa", 10.50, 720, 38, 78, 28,
         ["gain_muscle", "maintain"], False),
        ("Sofritas bowl — brown rice, black beans, fajita, salsa", 9.80, 470, 20, 60, 14,
         ["maintain", "lose_weight"], False),
        ("Chicken tacos x3 — corn, chicken, salsa, lettuce", 10.50, 480, 39, 42, 14,
         ["gain_muscle", "maintain"], False),
        ("Barbacoa bowl — white rice, pinto, salsa, no cheese", 11.50, 560, 40, 58, 16,
         ["gain_muscle", "maintain"], False),
        ("Chicken bowl — brown rice, black beans, tomato salsa only", 9.80, 500, 40, 55, 11,
         ["gain_muscle", "lose_weight", "maintain"], False),
        ("Veggie bowl — sofritas, no rice, extra lettuce + salsa", 9.80, 280, 16, 24, 12,
         ["lose_weight", "maintain"], False),
        ("Chicken burrito — no cheese, no sour cream, extra veggies", 9.80, 650, 40, 80, 16,
         ["gain_muscle", "maintain"], False),
        ("Steak salad — no rice, beans, fajita, salsa", 11.50, 360, 36, 24, 12,
         ["lose_weight", "gain_muscle"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in chipotle:
        meals.append(meal("Chipotle", order, price, cal, p, c, f, goals,
                          macros_source="chipotle_public_nutrition_2026", pitch_wow=wow))

    # Pitch-spot-checked Whataburger (~$6.59 grilled chicken; 430 cal / ~30g protein)
    whataburger = [
        ("Grilled chicken sandwich — no mayo, extra lettuce & tomato", 6.59, 390, 30, 40, 10,
         ["gain_muscle", "maintain", "lose_weight"], True),
        ("Whataburger Jr. — plain, no cheese, no mayo", 4.29, 310, 16, 28, 14,
         ["lose_weight", "maintain"], True),
        ("Grilled chicken salad — dressing on the side", 7.49, 290, 34, 12, 10,
         ["lose_weight", "gain_muscle"], True),
        ("Double meat Whataburger Jr. — no mayo", 6.49, 430, 28, 28, 20,
         ["gain_muscle"], False),
        ("Fish sandwich — no tartar, add tomato", 5.79, 390, 18, 40, 16,
         ["maintain"], False),
        ("Apple & cranberry chicken sandwich — no mayo", 7.29, 420, 30, 44, 12,
         ["maintain"], False),
        ("Grilled chicken melt — mustard only, no cheese", 6.99, 380, 34, 36, 10,
         ["gain_muscle", "lose_weight"], False),
        ("Breakfast taquito pair — egg & sausage", 4.99, 450, 20, 32, 24,
         ["maintain"], False),
        ("Whatachick'n sandwich — no mayo", 5.99, 480, 27, 46, 18,
         ["maintain"], False),
        ("Chicken fajita taco", 4.99, 420, 22, 38, 16,
         ["maintain", "gain_muscle"], False),
        ("Jr. + side garden salad — light dressing", 6.50, 360, 18, 30, 14,
         ["lose_weight", "maintain"], False),
        ("Grilled chicken sandwich — mustard only", 6.59, 400, 30, 42, 11,
         ["gain_muscle", "lose_weight", "maintain"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in whataburger:
        meals.append(meal("Whataburger", order, price, cal, p, c, f, goals,
                          macros_source="whataburger_public_nutrition_2026", pitch_wow=wow))

    panda = [
        ("Bowl — grilled teriyaki chicken + super greens (no rice)", 8.99, 360, 36, 18, 14,
         ["lose_weight", "gain_muscle"], True),
        ("Plate — black pepper chicken + chow mein half rice", 9.49, 680, 34, 72, 22,
         ["gain_muscle"], False),
        ("Bowl — string bean chicken + mixed veggies", 8.99, 420, 28, 35, 16,
         ["maintain", "lose_weight"], False),
        ("Bowl — broccoli beef + super greens", 9.29, 390, 26, 28, 18,
         ["maintain"], False),
        ("Plate — orange chicken + fried rice (share half)", 9.49, 740, 28, 88, 28,
         ["gain_muscle"], False),
        ("Bowl — mushroom chicken + half steamed rice", 8.79, 480, 24, 52, 16,
         ["maintain"], False),
        ("A la carte grilled teriyaki + super greens", 7.50, 280, 30, 10, 10,
         ["lose_weight", "gain_muscle"], True),
        ("Bowl — honey walnut shrimp + veggies (no rice)", 10.49, 520, 18, 40, 28,
         ["maintain"], False),
        ("Bowl — kung pao chicken + super greens", 8.99, 400, 26, 30, 16,
         ["maintain", "lose_weight"], False),
        ("Plate — grilled teriyaki + broccoli beef + rice half", 11.49, 720, 42, 70, 22,
         ["gain_muscle"], False),
        ("Bowl — black pepper chicken + mixed veggies", 8.99, 410, 28, 32, 16,
         ["gain_muscle", "maintain"], False),
        ("Side chow mein + grilled chicken a la carte", 8.50, 500, 28, 55, 16,
         ["maintain"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in panda:
        meals.append(meal("Panda Express", order, price, cal, p, c, f, goals, pitch_wow=wow))

    torchys = [
        ("Mr. Orange — corn, add grilled chicken, no queso", 5.50, 420, 28, 32, 18,
         ["gain_muscle", "maintain"], True),
        ("Two street tacos — grilled chicken, corn, onion cilantro", 7.50, 440, 34, 36, 16,
         ["gain_muscle", "lose_weight"], True),
        ("Trailer Park — flour, no queso, add pico", 5.25, 480, 22, 36, 24,
         ["maintain"], False),
        ("Democrat — corn, egg, beans (breakfast)", 4.75, 360, 18, 34, 14,
         ["maintain", "lose_weight"], False),
        ("Independent — corn, avocado, no queso", 5.00, 390, 12, 30, 22,
         ["maintain"], False),
        ("Brushfire — corn, no jalapeño ranch", 5.50, 410, 24, 34, 18,
         ["maintain"], False),
        ("Two bean & cheese street tacos — corn", 4.50, 380, 14, 44, 14,
         ["maintain"], True),
        ("Soft taco — grilled chicken, corn, pico only", 4.25, 280, 22, 24, 10,
         ["lose_weight", "gain_muscle", "maintain"], False),
        ("Breakfast taco — egg & potato, corn", 3.75, 300, 12, 32, 12,
         ["maintain"], False),
        ("Two soft tacos — barbacoa, corn, onion cilantro", 8.00, 460, 30, 34, 20,
         ["gain_muscle", "maintain"], False),
        ("Mr. Orange + side beans", 7.00, 540, 34, 50, 20,
         ["gain_muscle", "maintain"], False),
        ("Veggie taco — corn, beans, pico, no queso", 3.95, 260, 10, 36, 8,
         ["lose_weight", "maintain"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in torchys:
        meals.append(meal("Torchy's Tacos", order, price, cal, p, c, f, goals, pitch_wow=wow))

    mcd = [
        ("McChicken — no mayo", 3.29, 300, 14, 36, 10, ["maintain", "lose_weight"], True),
        ("Egg McMuffin — no butter", 4.49, 290, 17, 29, 12, ["maintain", "gain_muscle"], True),
        ("6-pc Chicken McNuggets — no sauce", 3.99, 250, 14, 15, 15, ["lose_weight", "maintain"], True),
        ("Filet-O-Fish — no tartar, add lettuce", 4.79, 320, 16, 38, 10, ["maintain"], False),
        ("Sausage burrito — no cheese", 2.79, 290, 12, 24, 16, ["maintain"], True),
        ("Southwest grilled chicken salad — light dressing", 7.49, 320, 32, 22, 10,
         ["lose_weight", "gain_muscle"], False),
        ("Double hamburger — ketchup mustard only", 4.59, 390, 24, 32, 18,
         ["gain_muscle", "maintain"], False),
        ("McDouble — no cheese, mustard ketchup", 3.79, 350, 18, 32, 14, ["maintain"], False),
        ("4-pc McNuggets — no sauce", 2.99, 170, 9, 10, 10, ["lose_weight", "maintain"], False),
        ("Egg White Delight McMuffin", 4.79, 250, 17, 28, 8, ["lose_weight", "maintain"], False),
        ("Bacon ranch grilled chicken salad — light", 7.99, 320, 34, 14, 12,
         ["lose_weight", "gain_muscle"], False),
        ("Hamburger — plain", 2.49, 250, 12, 30, 9, ["maintain"], True),
    ]
    for order, price, cal, p, c, f, goals, wow in mcd:
        meals.append(meal("McDonald's", order, price, cal, p, c, f, goals, pitch_wow=wow))

    cabana = [
        ("2 grilled chicken soft tacos — corn, no cheese", 5.49, 380, 30, 34, 12,
         ["gain_muscle", "lose_weight", "maintain"], True),
        ("Bean & cheese taco — corn, extra beans no cheese", 2.99, 280, 12, 36, 8,
         ["maintain", "lose_weight"], True),
        ("Breakfast taco — egg & potato, corn", 2.79, 260, 10, 28, 12, ["maintain"], True),
        ("Breakfast taco — egg & bacon, corn, no cheese", 3.29, 300, 14, 22, 16,
         ["maintain", "gain_muscle"], False),
        ("Grilled steak soft taco — corn, onion cilantro", 3.79, 290, 18, 24, 12,
         ["gain_muscle", "maintain"], False),
        ("Chicken flauta plate — skip cream, add pico", 7.99, 520, 28, 42, 22,
         ["gain_muscle", "maintain"], False),
        ("Tortilla soup cup + side rice", 5.49, 340, 16, 40, 10,
         ["maintain", "lose_weight"], False),
        ("3 breakfast tacos — egg & bean, corn", 7.50, 540, 24, 60, 20, ["maintain"], False),
        ("Grilled chicken soft taco — corn, pico only", 2.99, 220, 18, 18, 8,
         ["lose_weight", "gain_muscle"], False),
        ("Steak & egg breakfast taco — corn", 3.49, 310, 16, 24, 14, ["maintain", "gain_muscle"], False),
        ("2 soft tacos — ground beef, corn, lettuce tomato", 5.49, 420, 24, 36, 18, ["maintain"], False),
        ("Chicken tortilla soup bowl", 6.49, 380, 22, 36, 12, ["maintain", "lose_weight"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in cabana:
        meals.append(meal("Taco Cabana", order, price, cal, p, c, f, goals, pitch_wow=wow))

    # Pitch-spot-checked CFA (official grilled sandwich 390 cal / 28g protein; ~$6.49–7.29)
    cfa = [
        ("Grilled chicken sandwich — no butter on bun", 6.79, 390, 28, 45, 11,
         ["gain_muscle", "lose_weight", "maintain"], True),
        ("Grilled nuggets 8-ct — no sauce", 6.49, 130, 25, 1, 3,
         ["lose_weight", "gain_muscle"], True),
        ("Grilled nuggets 12-ct — no sauce", 8.99, 200, 38, 2, 4.5,
         ["gain_muscle", "lose_weight"], True),
        ("Cool Wrap — sauce on the side", 9.49, 350, 37, 28, 10,
         ["lose_weight", "gain_muscle"], False),
        ("Cobb salad — no bacon, light dressing", 10.49, 420, 36, 18, 20,
         ["gain_muscle", "maintain"], False),
        ("Egg White Grill", 5.49, 290, 26, 31, 7,
         ["lose_weight", "gain_muscle", "maintain"], True),
        ("Spicy chicken sandwich — no pickles mayo", 6.49, 450, 28, 46, 18,
         ["maintain"], False),
        ("Grilled chicken club — no cheese bacon light", 9.29, 430, 36, 42, 12,
         ["gain_muscle", "maintain"], False),
        ("Market salad — grilled filet, light vinaigrette", 10.19, 340, 28, 28, 12,
         ["lose_weight", "maintain"], False),
        ("Chick-n-Minis 4-ct", 4.79, 360, 16, 36, 14, ["maintain"], False),
        ("Grilled nuggets 8-ct + fruit cup", 8.99, 190, 26, 16, 3,
         ["lose_weight", "gain_muscle"], False),
        ("Spicy southwest salad — no creamy dressing", 10.49, 380, 30, 28, 14,
         ["lose_weight", "maintain"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in cfa:
        meals.append(meal("Chick-fil-A", order, price, cal, p, c, f, goals,
                          macros_source="chickfila_public_nutrition_2026", pitch_wow=wow))

    subway = [
        ("6-inch Turkey Breast — wheat, veggies, mustard", 6.49, 280, 18, 40, 3.5,
         ["lose_weight", "maintain"], False),
        ("6-inch Oven Roasted Chicken — wheat, no cheese, vinaigrette", 6.99, 320, 24, 42, 5,
         ["gain_muscle", "lose_weight"], True),
        ("Protein Bowl — turkey, no bread, double meat", 8.49, 220, 32, 10, 6,
         ["lose_weight", "gain_muscle"], True),
        ("6-inch Tuna — wheat, light mayo, veggies", 6.49, 420, 18, 40, 20, ["maintain"], False),
        ("6-inch Veggie Delite — wheat, double veggies", 5.49, 230, 8, 40, 2.5,
         ["lose_weight", "maintain"], False),
        ("6-inch Black Forest Ham — wheat, mustard", 6.29, 290, 18, 42, 4,
         ["maintain", "lose_weight"], False),
        ("Footlong Turkey — wheat, no cheese", 10.49, 560, 36, 80, 7, ["gain_muscle"], False),
        ("6-inch Sweet Onion Chicken Teriyaki — wheat", 7.49, 370, 25, 52, 4.5,
         ["gain_muscle", "maintain"], False),
        ("6-inch Rotisserie-Style Chicken — wheat, no cheese", 7.29, 310, 26, 40, 5,
         ["gain_muscle", "lose_weight", "maintain"], False),
        ("Footlong Oven Roasted Chicken — wheat, veggies", 11.49, 640, 48, 84, 10,
         ["gain_muscle"], True),
        ("6-inch B.L.T. — wheat, light mayo", 5.99, 340, 14, 38, 14, ["maintain"], False),
        ("Protein Bowl — chicken, spinach, vinaigrette", 8.49, 200, 30, 8, 5,
         ["lose_weight", "gain_muscle"], False),
    ]
    for order, price, cal, p, c, f, goals, wow in subway:
        meals.append(meal("Subway", order, price, cal, p, c, f, goals, pitch_wow=wow))

    return meals


def build_grocery_meals() -> list[dict]:
    """~55–65 distinct H-E-B 3-ingredient fixes (no lighter-portion clones)."""
    rows: list[tuple] = [
        ("Muscle Bowl — eggs + spinach + black beans", 6.27, 380, 28, 22, 18,
         ["gain_muscle", "maintain"],
         ["H-E-B dozen large eggs ($2.89)", "Fresh spinach 10oz ($2.49)", "H-E-B black beans 15oz ($0.89)"],
         "Scramble 3 eggs with spinach; heat beans. 4 servings ~$1.57.", 5, 1.57, True),
        ("Protein Wrap Fix — rotisserie + tortillas + salsa", 12.26, 320, 32, 28, 8,
         ["gain_muscle", "maintain"],
         ["H-E-B rotisserie chicken ($7.98)", "Whole wheat tortillas 8ct ($2.29)", "H-E-B salsa 16oz ($1.99)"],
         "Shred chicken, wrap with salsa. 4 wraps ~$3.07.", 3, 3.07, True),
        ("Budget Cut Bowl — tuna + mic rice + broccoli", 4.76, 410, 32, 48, 6,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Tuna 5oz x2 ($1.98)", "H-E-B microwavable rice ($1.49)", "Frozen broccoli 12oz ($1.29)"],
         "Microwave rice & broccoli, mix tuna. 2 bowls ~$2.38.", 5, 2.38, True),
        ("Light & Lean — Greek yogurt + banana + PB", 7.67, 340, 22, 38, 12,
         ["lose_weight", "maintain"],
         ["H-E-B plain Greek yogurt 32oz ($3.99)", "Banana ($0.69)", "H-E-B natural PB ($2.99)"],
         "Yogurt + banana + 1 tbsp PB. 4 servings ~$1.92.", 2, 1.92, True),
        ("Cottage Crunch — cottage + pineapple + almonds", 6.50, 300, 26, 24, 10,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Cottage cheese 24oz ($3.49)", "Pineapple chunks ($1.79)", "Almonds ($1.22)"],
         "1 cup cottage + fruit + almonds. 3 servings ~$2.17.", 3, 2.17, False),
        ("Turkey Plate — deli turkey + mustard + carrots", 7.20, 280, 30, 16, 6,
         ["lose_weight", "gain_muscle"],
         ["Oven roasted turkey 0.5lb ($4.50)", "Mustard ($1.29)", "Baby carrots ($1.41)"],
         "Roll turkey; side carrots. 3 plates ~$2.40.", 4, 2.40, True),
        ("Oat Boost — oats + whey + berries", 9.80, 360, 28, 42, 6,
         ["gain_muscle", "maintain"],
         ["Rolled oats ($2.49)", "Whey protein ($5.99)", "Frozen berries ($1.32)"],
         "Microwave oats; stir whey + berries. 5 bowls ~$1.96.", 5, 1.96, False),
        ("Bean Cheese Melt — tortillas + refried + cheese", 5.40, 420, 18, 48, 14,
         ["maintain"],
         ["Flour tortillas ($2.29)", "Refried beans ($0.99)", "Shredded cheese ($2.12)"],
         "Fill tortilla; microwave 60s. 4 ~$1.35.", 3, 1.35, False),
        ("Shrimp Stir — shrimp + stir-fry veg + soy", 10.50, 310, 28, 22, 8,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Frozen shrimp 12oz ($6.99)", "Stir-fry bag ($2.49)", "Low-sodium soy ($1.02)"],
         "Skillet 8 min. 3 servings ~$3.50.", 8, 3.50, False),
        ("Chicken Rice Meal Prep — breast + rice + salsa", 11.00, 450, 40, 45, 8,
         ["gain_muscle", "maintain"],
         ["Chicken breast 1.5lb ($6.50)", "Rice 2lb ($1.99)", "Salsa ($2.51)"],
         "Bake chicken + rice. 5 servings ~$2.20.", 10, 2.20, True),
        ("Tofu Veg Bowl — tofu + frozen veg + teriyaki", 6.80, 340, 22, 28, 14,
         ["maintain", "lose_weight"],
         ["Firm tofu ($2.29)", "Frozen mixed veggies ($1.99)", "Teriyaki ($2.52)"],
         "Pan-sear tofu; steam veggies. 3 ~$2.27.", 8, 2.27, False),
        ("PB Banana Toast — bread + PB + banana", 4.50, 380, 14, 48, 14,
         ["maintain"],
         ["Whole wheat bread ($1.99)", "Peanut butter ($1.50)", "Banana ($1.01)"],
         "Toast + PB + banana. 4 ~$1.13.", 3, 1.13, True),
        ("Salmon Packet — canned salmon + crackers + cucumber", 6.20, 330, 26, 24, 12,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Canned salmon ($3.49)", "Crackers ($1.79)", "Cucumber ($0.92)"],
         "Salmon on crackers + cucumber. 2 ~$3.10.", 4, 3.10, False),
        ("Chili Night — chili + cornbread + cheese", 5.90, 460, 22, 52, 16,
         ["maintain", "gain_muscle"],
         ["H-E-B chili ($2.49)", "Cornbread mix ($1.79)", "Cheese ($1.62)"],
         "Heat chili; bake mini cornbread. 3 ~$1.97.", 10, 1.97, False),
        ("Hummus Plate — hummus + pita + pepper", 5.80, 360, 12, 44, 14,
         ["maintain", "lose_weight"],
         ["Hummus ($2.99)", "Pita 6ct ($1.79)", "Bell pepper ($1.02)"],
         "Dip pita + pepper. 3 ~$1.93.", 2, 1.93, False),
        ("Egg Wrap Express — eggs + wraps + hot sauce", 6.40, 350, 24, 26, 16,
         ["gain_muscle", "maintain"],
         ["Eggs dozen ($2.89)", "Spinach wraps ($2.49)", "Hot sauce ($1.02)"],
         "Scramble in wrap. 4 ~$1.60.", 5, 1.60, False),
        ("Pasta Protein — chickpea pasta + sauce + turkey", 9.40, 480, 34, 52, 10,
         ["gain_muscle", "maintain"],
         ["Chickpea pasta ($3.49)", "Marinara ($1.99)", "Ground turkey ($3.92)"],
         "Boil pasta; brown turkey. 4 ~$2.35.", 10, 2.35, False),
        ("Smoothie Fuel — fruit + milk + protein", 8.60, 320, 26, 36, 4,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Frozen fruit ($2.99)", "Fairlife milk ($3.49)", "Protein pack ($2.12)"],
         "Blend 2 min. 3 ~$2.87.", 2, 2.87, False),
        ("Rice Bean Bowl — mic rice + beans + salsa", 3.80, 400, 14, 68, 4,
         ["maintain", "lose_weight"],
         ["Microwave rice ($1.49)", "Black beans ($0.89)", "Salsa ($1.42)"],
         "Heat rice + beans. 2 ~$1.90.", 4, 1.90, True),
        ("Tuna Avocado — tuna + avocado + lime", 5.10, 360, 28, 12, 20,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Tuna 2 cans ($1.98)", "Avocado ($1.50)", "Lime ($1.62)"],
         "Mix tuna + avocado + lime. 2 ~$2.55.", 3, 2.55, True),
        ("Greek Power — yogurt + granola + honey", 6.90, 380, 20, 48, 10,
         ["maintain"],
         ["Greek yogurt ($3.99)", "Granola ($1.99)", "Honey ($0.92)"],
         "Bowl yogurt mix. 4 ~$1.73.", 2, 1.73, False),
        ("Lentil Soup Night — lentils + broth + spinach", 4.80, 310, 20, 40, 4,
         ["lose_weight", "maintain"],
         ["Canned lentils ($1.29)", "Broth ($1.99)", "Spinach ($1.52)"],
         "Simmer 8 min. 3 ~$1.60.", 8, 1.60, False),
        ("Breakfast Burrito Kit — eggs + tortillas + salsa", 5.70, 390, 20, 36, 16,
         ["maintain", "gain_muscle"],
         ["Eggs ($2.89)", "Tortillas ($1.79)", "Salsa ($1.02)"],
         "Scramble wrap. 4 ~$1.43.", 5, 1.43, False),
        ("Chicken Salad Lite — canned chicken + yogurt + celery", 6.10, 290, 32, 8, 10,
         ["lose_weight", "gain_muscle"],
         ["Canned chicken ($2.49)", "Greek yogurt ($2.00)", "Celery ($1.61)"],
         "Mix chicken salad. 3 ~$2.03.", 5, 2.03, True),
        ("Queso Potato — microwave potato + turkey chili + cheese", 5.50, 420, 22, 48, 12,
         ["maintain", "gain_muscle"],
         ["Russet potatoes 5lb ($2.49)", "Turkey chili ($1.99)", "Cheese ($1.02)"],
         "Microwave potato; top chili. 4 ~$1.38.", 8, 1.38, False),
        ("Edamame Rice — frozen edamame + rice + soy", 4.90, 360, 20, 48, 8,
         ["maintain", "lose_weight"],
         ["Frozen edamame ($2.29)", "Microwave rice ($1.49)", "Soy sauce ($1.12)"],
         "Heat + mix. 2 ~$2.45.", 5, 2.45, False),
        ("Sardine Toast — sardines + bread + mustard", 4.20, 340, 24, 28, 14,
         ["gain_muscle", "maintain"],
         ["Sardines ($1.79)", "Whole wheat bread ($1.49)", "Mustard ($0.92)"],
         "Toast + sardines. 2 ~$2.10.", 3, 2.10, False),
        ("Black Bean Tacos — tortillas + black beans + salsa", 4.10, 380, 16, 58, 8,
         ["maintain", "lose_weight"],
         ["Corn tortillas ($1.49)", "Black beans ($0.89)", "Salsa ($1.72)"],
         "Warm fillings. 3 ~$1.37.", 5, 1.37, True),
        ("Protein Nacho Lite — chips + turkey + salsa", 6.80, 400, 26, 36, 16,
         ["maintain", "gain_muscle"],
         ["Tortilla chips ($2.29)", "Deli turkey ($2.99)", "Salsa ($1.52)"],
         "Bake chips + turkey. 3 ~$2.27.", 8, 2.27, False),
        ("Kimchi Eggs — eggs + kimchi + rice", 5.60, 390, 22, 40, 14,
         ["maintain", "gain_muscle"],
         ["Eggs ($2.89)", "Kimchi ($1.79)", "Microwave rice ($0.92)"],
         "Scramble with kimchi over rice. 3 ~$1.87.", 6, 1.87, False),
        ("Caprese Snack — mozzarella + tomato + basil", 5.90, 320, 18, 10, 22,
         ["lose_weight", "maintain"],
         ["Fresh mozzarella ($3.49)", "Tomatoes ($1.49)", "Basil ($0.92)"],
         "Slice + plate. 2 ~$2.95.", 3, 2.95, False),
        ("Peanut Noodle — noodles + PB + soy chili", 4.40, 450, 16, 58, 16,
         ["maintain"],
         ["Ramen/noodles ($1.29)", "Peanut butter ($1.50)", "Soy + chili ($1.61)"],
         "Boil noodles; sauce. 2 ~$2.20.", 8, 2.20, False),
        ("Chickpea Salad — chickpeas + cucumber + lemon", 3.90, 300, 14, 40, 8,
         ["lose_weight", "maintain"],
         ["Chickpeas can ($0.99)", "Cucumber ($0.99)", "Lemon ($1.92)"],
         "Drain + toss. 2 ~$1.95.", 4, 1.95, False),
        ("Breakfast Parfait Stack — yogurt + cereal + berries", 6.20, 350, 18, 52, 6,
         ["maintain", "lose_weight"],
         ["Greek yogurt ($3.49)", "High-protein cereal ($1.79)", "Berries ($0.92)"],
         "Layer parfait. 3 ~$2.07.", 2, 2.07, False),
        ("Sheet-Pan Sausage — chicken sausage + potatoes + peppers", 9.20, 420, 26, 36, 18,
         ["maintain", "gain_muscle"],
         ["Chicken sausage ($4.99)", "Potatoes ($2.00)", "Peppers ($2.21)"],
         "Roast 10 min leftover-friendly. 4 ~$2.30.", 10, 2.30, False),
        ("Tuna Rice Cake Stack — tuna + rice cakes + hot sauce", 3.60, 280, 24, 28, 6,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Tuna can ($0.99)", "Rice cakes ($1.79)", "Hot sauce ($0.82)"],
         "Stack tuna on cakes. 2 ~$1.80.", 2, 1.80, True),
        ("Whey Coffee Shake — whey + milk + instant coffee", 7.40, 250, 30, 16, 4,
         ["gain_muscle", "lose_weight"],
         ["Whey scoop pack ($3.49)", "Fairlife milk ($2.99)", "Instant coffee ($0.92)"],
         "Shake 1 min. 2 ~$3.70.", 1, 3.70, False),
        ("Veggie Omelette Kit — eggs + frozen peppers + cheese", 5.30, 340, 24, 10, 22,
         ["gain_muscle", "maintain"],
         ["Eggs ($2.89)", "Frozen peppers ($1.49)", "Cheese ($0.92)"],
         "Omelette 5 min. 3 ~$1.77.", 5, 1.77, False),
        ("BBQ Chicken Sweet Potato — rotisserie bits + sweet potato + BBQ", 8.50, 400, 30, 42, 10,
         ["gain_muscle", "maintain"],
         ["Rotisserie leftovers/pack ($5.49)", "Sweet potatoes ($1.99)", "BBQ sauce ($1.02)"],
         "Microwave potato; top chicken. 3 ~$2.83.", 8, 2.83, False),
        ("Pinto Breakfast — pinto beans + eggs + tortilla", 4.00, 360, 18, 40, 12,
         ["maintain", "gain_muscle"],
         ["Pinto beans ($0.89)", "Eggs ($1.89)", "Tortillas ($1.22)"],
         "Heat beans; fry egg. 2 ~$2.00.", 6, 2.00, True),
        ("Apple Turkey Rollups — turkey + apple + mustard", 5.00, 260, 24, 20, 6,
         ["lose_weight", "gain_muscle", "maintain"],
         ["Deli turkey ($2.99)", "Apples ($1.29)", "Mustard ($0.72)"],
         "Roll turkey around apple. 2 ~$2.50.", 3, 2.50, True),
        ("Microwave Mac Protein — chickpea mac + tuna + peas", 6.40, 440, 32, 48, 10,
         ["gain_muscle", "maintain"],
         ["Chickpea mac ($2.99)", "Tuna ($0.99)", "Frozen peas ($2.42)"],
         "Microwave mac; mix tuna/peas. 2 ~$3.20.", 6, 3.20, False),
        ("Guac Egg Toast — toast + egg + guacamole cup", 5.80, 380, 16, 28, 22,
         ["maintain"],
         ["Bread ($1.49)", "Eggs ($1.89)", "Guac cup ($2.42)"],
         "Toast + fried egg + guac. 2 ~$2.90.", 5, 2.90, False),
        ("Citrus Chicken — canned chicken + orange + spinach", 5.40, 300, 30, 18, 8,
         ["lose_weight", "gain_muscle"],
         ["Canned chicken ($2.49)", "Orange ($1.00)", "Spinach ($1.91)"],
         "Toss chicken + citrus over spinach. 2 ~$2.70.", 4, 2.70, False),
        ("Spicy Bean Bowl — beans + microwave rice + salsa verde", 3.50, 390, 14, 66, 4,
         ["maintain", "lose_weight"],
         ["Black beans ($0.89)", "Microwave rice ($1.49)", "Salsa verde ($1.12)"],
         "Heat + mix. 2 ~$1.75.", 4, 1.75, True),
        ("Deli Ham Plate — ham + cheese stick + apple", 4.80, 320, 22, 24, 12,
         ["maintain", "lose_weight"],
         ["Deli ham ($2.49)", "Cheese sticks ($1.29)", "Apple ($1.02)"],
         "Plate protein + fruit. 2 ~$2.40.", 2, 2.40, False),
        ("Frozen Burrito Upgrade — burrito + salsa + Greek yogurt", 4.60, 420, 18, 52, 14,
         ["maintain"],
         ["Frozen burrito ($2.49)", "Salsa ($1.19)", "Greek yogurt ($0.92)"],
         "Microwave burrito; top salsa/yogurt. 1 ~$4.60.", 4, 4.60, False),
        ("Protein Cereal Bowl — high-protein cereal + milk + banana", 5.20, 360, 24, 48, 6,
         ["gain_muscle", "maintain"],
         ["Protein cereal ($2.99)", "Milk ($1.29)", "Banana ($0.92)"],
         "Pour + slice banana. 2 ~$2.60.", 2, 2.60, False),
        ("Jalapeño Tuna Melt Lite — tuna + tortilla + jalapeños", 3.80, 340, 26, 30, 10,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Tuna ($0.99)", "Tortilla ($1.49)", "Pickled jalapeños ($1.32)"],
         "Warm tortilla melt. 2 ~$1.90.", 4, 1.90, True),
        ("Broccoli Cheddar Egg Bake — eggs + broccoli + cheese", 6.00, 320, 24, 10, 20,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Eggs ($2.89)", "Frozen broccoli ($1.49)", "Cheese ($1.62)"],
         "Microwave mug bake. 3 ~$2.00.", 6, 2.00, False),
        ("Trail Mix Yogurt — yogurt + trail mix + honey drizzle", 5.50, 370, 18, 36, 14,
         ["maintain"],
         ["Greek yogurt ($2.99)", "Trail mix ($1.79)", "Honey ($0.72)"],
         "Stir bowl. 2 ~$2.75.", 2, 2.75, False),
        ("Corn Salsa Chicken — canned chicken + corn + salsa", 4.50, 330, 28, 28, 8,
         ["gain_muscle", "lose_weight", "maintain"],
         ["Canned chicken ($2.49)", "Canned corn ($0.89)", "Salsa ($1.12)"],
         "Mix cold or warm. 2 ~$2.25.", 3, 2.25, True),
        ("Zucchini Boat Lite — zucchini + turkey + marinara", 7.10, 300, 26, 18, 12,
         ["lose_weight", "gain_muscle"],
         ["Zucchini ($1.99)", "Ground turkey small ($3.49)", "Marinara ($1.62)"],
         "Microwave zucchini boats. 3 ~$2.37.", 10, 2.37, False),
        ("Overnight Oats Classic — oats + milk + chia", 4.30, 340, 14, 48, 10,
         ["maintain", "lose_weight"],
         ["Oats ($1.49)", "Milk ($1.49)", "Chia ($1.32)"],
         "Mix night before. 2 ~$2.15.", 2, 2.15, False),
        ("Spicy Egg Tacos — eggs + corn tortillas + salsa", 3.70, 320, 16, 28, 14,
         ["maintain", "gain_muscle"],
         ["Eggs ($1.89)", "Corn tortillas ($1.29)", "Salsa ($0.52)"],
         "Scramble tacos. 2 ~$1.85.", 5, 1.85, True),
    ]

    groceries = []
    for order, price, cal, p, c, f, goals, items, recipe, prep, psp, wow in rows:
        groceries.append(meal(
            "H-E-B", order, price, cal, p, c, f, goals,
            mtype="grocery", items=items, recipe=recipe, prep_minutes=prep,
            per_serving_price=psp, macros_source="heb_public_estimate_2026", pitch_wow=wow,
        ))
    return groceries


def dedupe(meals: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for m in meals:
        key = m["order"].casefold().strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(m)
    return out


def main() -> None:
    meals = dedupe(build_restaurant_meals() + build_grocery_meals())
    restaurants = [m for m in meals if m["type"] == "restaurant"]
    groceries = [m for m in meals if m["type"] == "grocery"]

    if len(meals) < 150:
        raise SystemExit(f"Need >= 150 meals, got {len(meals)}")
    if len(groceries) < 50:
        raise SystemExit(f"Need >= 50 grocery meals, got {len(groceries)}")

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "locations.json").open("w", encoding="utf-8") as f:
        json.dump({"estimate_as_of": ESTIMATE_AS_OF, "locations": LOCATIONS}, f, indent=2)
        f.write("\n")
    with (OUT / "meals.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "estimate_as_of": ESTIMATE_AS_OF,
                "count": len(meals),
                "restaurant_count": len(restaurants),
                "grocery_count": len(groceries),
                "meals": meals,
            },
            f,
            indent=2,
        )
        f.write("\n")
    print(
        f"Wrote {len(LOCATIONS)} locations; meals={len(meals)} "
        f"(restaurant={len(restaurants)} grocery={len(groceries)})"
    )


if __name__ == "__main__":
    main()
