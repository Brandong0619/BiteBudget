# Recommend API contract

Frozen I/O for Person A's `recommend()` and Person B's `POST /api/recommendations`.

## Function

```text
recommend(
  budget: float,                          # USD, tax-inclusive max spend
  goal: "gain_muscle" | "lose_weight" | "maintain",
  lat: float,
  lng: float,
  radius_miles: float = 5.0
) -> (restaurant: dict | None, grocery: dict | None)
```

## Strict filters (all required)

1. `goal` is in the meal's `goals` list
2. `spend = price` (checkout / full basket; grocery `per_serving_price` is recipe text only)
3. `price_with_tax = round(spend * 1.0825, 2)` and **`price_with_tax <= budget`**
4. Haversine distance to a matching chain location **`<= radius_miles`**
5. Meal `type` matches location `type` (`restaurant` or `grocery`)

## Restaurant option fields

`type`, `name`, `chain`, `address`, `distance_miles`, `order`, `price`, `price_with_tax`, `calories`, `protein_g`, `carbs_g`, `fat_g`, `lat`, `lng`

## Grocery option fields

`type`, `store`, `store_chain`, `address`, `distance_miles`, `items`, `recipe`, `prep_minutes`, `price`, `price_with_tax`, `calories`, `protein_g`, `carbs_g`, `fat_g`, `lat`, `lng`

## HTTP mapping (Person B)

Request body: `{ "budget", "goal", "lat?", "lng?" }`  
Response: `{ "budget", "goal", "tax_rate", "restaurant", "grocery", "message?" }`

See `backend/app/models.py` for Pydantic shapes.
