#!/usr/bin/env python3
"""Local debug UI for Person A recommender and eval cases.

Run:
  python3 data/tools/debug_ui.py
Then open:
  http://127.0.0.1:8099
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

DATA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DATA_ROOT))

from recommender import recommend_with_debug  # noqa: E402
from recommender.load import reload_datasets  # noqa: E402

EVAL_CASES_PATH = DATA_ROOT / "datasets" / "eval_cases.json"

app = FastAPI(title="Person A Debug UI", version="0.1.0")


class DebugRequest(BaseModel):
    budget: float = Field(..., gt=0, le=100)
    goal: str
    lat: float
    lng: float
    radius_miles: float = Field(default=5.0, gt=0, le=30)


def _load_cases() -> list[dict]:
    raw = json.loads(EVAL_CASES_PATH.read_text(encoding="utf-8"))
    return raw["cases"]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Person A Recommender Debug UI</title>
  <style>
    body { font-family: Inter, Arial, sans-serif; margin: 20px; max-width: 1200px; }
    h1 { margin-bottom: 8px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; }
    label { display: block; margin-top: 8px; font-size: 14px; }
    input, select, button, textarea { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
    button { cursor: pointer; }
    .row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #e6e6e6; padding: 6px; font-size: 12px; text-align: left; }
    .ok { color: #1f7a1f; }
    .bad { color: #b42318; }
  </style>
</head>
<body>
  <h1>Person A Recommender Debug UI</h1>
  <p>Run custom inputs or replay eval cases. Uses <span class=\"mono\">recommend_with_debug()</span>.</p>

  <div class=\"grid\">
    <div class=\"card\">
      <h3>Run Custom Input</h3>
      <div class=\"row\">
        <label>Budget<input id=\"budget\" type=\"number\" step=\"0.01\" value=\"8\"></label>
        <label>Goal
          <select id=\"goal\">
            <option value=\"gain_muscle\">gain_muscle</option>
            <option value=\"lose_weight\">lose_weight</option>
            <option value=\"maintain\">maintain</option>
          </select>
        </label>
        <label>Lat<input id=\"lat\" type=\"number\" step=\"0.0001\" value=\"29.4241\"></label>
        <label>Lng<input id=\"lng\" type=\"number\" step=\"0.0001\" value=\"-98.4936\"></label>
        <label>Radius<input id=\"radius\" type=\"number\" step=\"0.1\" value=\"5\"></label>
      </div>
      <button onclick=\"runCustom()\">Run</button>
    </div>

    <div class=\"card\">
      <h3>Run Eval Case</h3>
      <select id=\"caseSelect\"></select>
      <button onclick=\"runCase()\">Run Selected Case</button>
      <button onclick=\"reloadCases()\">Reload Cases</button>
      <p id=\"caseMeta\" class=\"mono\"></p>
    </div>
  </div>

  <div class=\"grid\" style=\"margin-top:16px\">
    <div class=\"card\">
      <h3>Top Restaurants</h3>
      <div id=\"topRestaurants\"></div>
    </div>
    <div class=\"card\">
      <h3>Top Groceries</h3>
      <div id=\"topGroceries\"></div>
    </div>
  </div>

  <div class=\"card\" style=\"margin-top:16px\">
    <h3>Winners + Raw JSON</h3>
    <p id=\"checks\"></p>
    <textarea id=\"raw\" rows=\"18\" class=\"mono\"></textarea>
  </div>

  <script>
    let cases = [];

    function asTable(rows) {
      if (!rows || rows.length === 0) return '<p class="mono">No candidates</p>';
      const head = '<tr><th>#</th><th>Chain</th><th>Score</th><th>Price+Tax</th><th>Protein</th><th>Calories</th><th>Distance</th><th>Title</th></tr>';
      const body = rows.map((r, i) => {
        const title = (r.order && r.order.length > 0) ? r.order : (r.items || []).join(', ');
        return `<tr><td>${i+1}</td><td>${r.chain || ''}</td><td>${r.score}</td><td>${r.price_with_tax}</td><td>${r.protein_g}</td><td>${r.calories}</td><td>${r.distance_miles}</td><td>${title}</td></tr>`;
      }).join('');
      return `<table>${head}${body}</table>`;
    }

    function renderResult(result) {
      document.getElementById('raw').value = JSON.stringify(result, null, 2);
      document.getElementById('topRestaurants').innerHTML = asTable(result.top_restaurants || []);
      document.getElementById('topGroceries').innerHTML = asTable(result.top_groceries || []);

      const checks = [];
      const budget = result.__input?.budget;
      for (const side of ['restaurant', 'grocery']) {
        const item = result[side];
        if (!item) continue;
        const within = item.price_with_tax <= budget + 1e-6;
        checks.push(`${side}: price_with_tax=${item.price_with_tax} <= budget=${budget} ` +
          (within ? '<span class="ok">OK</span>' : '<span class="bad">FAIL</span>'));
      }
      document.getElementById('checks').innerHTML = checks.join('<br/>') || 'No winners returned.';
    }

    async function reloadCases() {
      const res = await fetch('/api/cases');
      cases = await res.json();
      const sel = document.getElementById('caseSelect');
      sel.innerHTML = cases.map(c => `<option value="${c.id}">${c.id}</option>`).join('');
      if (cases.length > 0) setCaseMeta(cases[0].id);
      sel.onchange = () => setCaseMeta(sel.value);
    }

    function setCaseMeta(id) {
      const c = cases.find(x => x.id === id);
      if (!c) return;
      document.getElementById('caseMeta').textContent =
        `budget=${c.budget} goal=${c.goal} lat=${c.lat} lng=${c.lng} radius=${c.radius_miles}`;
    }

    async function runCustom() {
      const payload = {
        budget: Number(document.getElementById('budget').value),
        goal: document.getElementById('goal').value,
        lat: Number(document.getElementById('lat').value),
        lng: Number(document.getElementById('lng').value),
        radius_miles: Number(document.getElementById('radius').value),
      };
      const res = await fetch('/api/run', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      const data = await res.json();
      renderResult(data);
    }

    async function runCase() {
      const id = document.getElementById('caseSelect').value;
      const res = await fetch(`/api/run-case/${id}`, { method:'POST' });
      const data = await res.json();
      renderResult(data);
    }

    reloadCases();
  </script>
</body>
</html>
"""


@app.get("/api/cases")
def api_cases() -> JSONResponse:
    return JSONResponse(_load_cases())


@app.post("/api/run")
def api_run(payload: DebugRequest) -> JSONResponse:
    reload_datasets()
    result = recommend_with_debug(
        budget=payload.budget,
        goal=payload.goal,
        lat=payload.lat,
        lng=payload.lng,
        radius_miles=payload.radius_miles,
    )
    result["__input"] = payload.model_dump()
    return JSONResponse(result)


@app.post("/api/run-case/{case_id}")
def api_run_case(case_id: str) -> JSONResponse:
    reload_datasets()
    case = next((c for c in _load_cases() if c["id"] == case_id), None)
    if case is None:
        return JSONResponse({"error": f"Case not found: {case_id}"}, status_code=404)

    result = recommend_with_debug(
        budget=case["budget"],
        goal=case["goal"],
        lat=case["lat"],
        lng=case["lng"],
        radius_miles=case.get("radius_miles", 5.0),
    )
    result["__input"] = {
        "budget": case["budget"],
        "goal": case["goal"],
        "lat": case["lat"],
        "lng": case["lng"],
        "radius_miles": case.get("radius_miles", 5.0),
        "case_id": case_id,
    }
    result["__expect"] = case.get("expect", {})
    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8099)
