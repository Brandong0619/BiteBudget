#!/usr/bin/env python3
"""Write budget × goal demo CSV and print top-3 debug for pitch rehearsal."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recommender import recommend_with_debug  # noqa: E402
from recommender.load import reload_datasets  # noqa: E402

OUT = ROOT / "datasets" / "demo_report.csv"

BUDGETS = [5.0, 8.0, 12.0]
GOALS = ["gain_muscle", "lose_weight", "maintain"]
LOCATIONS = [
    ("downtown", 29.4241, -98.4936),
    ("alamo_heights", 29.4678, -98.4634),
]


def main() -> int:
    reload_datasets()
    rows: list[dict] = []

    for label, lat, lng in LOCATIONS:
        for budget in BUDGETS:
            for goal in GOALS:
                debug = recommend_with_debug(budget, goal, lat, lng)
                print(f"\n=== ${budget:.0f} / {goal} @ {label} ===")
                for side, key in (("restaurant", "top_restaurants"), ("grocery", "top_groceries")):
                    print(f" top-{side}:")
                    for i, row in enumerate(debug[key], 1):
                        title = row.get("order") or ", ".join(row.get("items") or [])[:60]
                        print(
                            f"  {i}. score={row['score']} {row['chain']} | "
                            f"${row['price_with_tax']} | P{row['protein_g']} C{row['calories']} | {title}"
                        )

                for side, opt in (("restaurant", debug["restaurant"]), ("grocery", debug["grocery"])):
                    if not opt:
                        rows.append({
                            "budget": budget,
                            "goal": goal,
                            "lat": lat,
                            "lng": lng,
                            "side": side,
                            "chain": "",
                            "order_or_title": "",
                            "price_with_tax": "",
                            "protein_g": "",
                            "calories": "",
                            "distance_miles": "",
                        })
                        continue
                    title = opt.get("order") or "; ".join(opt.get("items") or [])
                    rows.append({
                        "budget": budget,
                        "goal": goal,
                        "lat": lat,
                        "lng": lng,
                        "side": side,
                        "chain": opt.get("chain") or opt.get("store_chain"),
                        "order_or_title": title,
                        "price_with_tax": opt["price_with_tax"],
                        "protein_g": opt["protein_g"],
                        "calories": opt["calories"],
                        "distance_miles": opt["distance_miles"],
                    })

    fieldnames = [
        "budget", "goal", "lat", "lng", "side", "chain", "order_or_title",
        "price_with_tax", "protein_g", "calories", "distance_miles",
    ]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {OUT} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
