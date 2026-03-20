"""
Live test script - hit all viz-agent endpoints with real sample data.
Run: python test_live.py  (while server is running on port 8003)
"""

import sys
import os
# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import httpx
import json
import base64
from pathlib import Path

BASE = "http://127.0.0.1:8003"

# -- Sample Dataset: Monthly Sales Data --
COLUMNS = [
    {"name": "month",    "semantic": "datetime"},
    {"name": "region",   "semantic": "categorical", "unique": 4},
    {"name": "product",  "semantic": "categorical", "unique": 3},
    {"name": "revenue",  "semantic": "numeric"},
    {"name": "units",    "semantic": "numeric"},
    {"name": "profit",   "semantic": "numeric"},
]

ROWS = [
    {"month": "2024-01", "region": "North", "product": "Widget A", "revenue": 12000, "units": 150, "profit": 3200},
    {"month": "2024-02", "region": "North", "product": "Widget B", "revenue": 15000, "units": 200, "profit": 4100},
    {"month": "2024-03", "region": "South", "product": "Widget A", "revenue": 9500,  "units": 120, "profit": 2800},
    {"month": "2024-04", "region": "South", "product": "Widget C", "revenue": 18000, "units": 300, "profit": 5500},
    {"month": "2024-05", "region": "East",  "product": "Widget A", "revenue": 22000, "units": 280, "profit": 6100},
    {"month": "2024-06", "region": "East",  "product": "Widget B", "revenue": 14000, "units": 170, "profit": 3900},
    {"month": "2024-07", "region": "West",  "product": "Widget C", "revenue": 25000, "units": 350, "profit": 7200},
    {"month": "2024-08", "region": "West",  "product": "Widget A", "revenue": 19000, "units": 240, "profit": 5000},
    {"month": "2024-09", "region": "North", "product": "Widget B", "revenue": 31000, "units": 400, "profit": 9500},
    {"month": "2024-10", "region": "South", "product": "Widget C", "revenue": 27000, "units": 320, "profit": 8100},
]

DATA_PAYLOAD = {"columns": COLUMNS, "rows": ROWS}


def save_png(b64_str, filename):
    """Decode base64 PNG and save to disk."""
    if b64_str:
        img = base64.b64decode(b64_str)
        path = Path(f"./test_outputs/{filename}")
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(img)
        print(f"   [SAVED] {path} ({len(img)} bytes)")
    else:
        print("   [WARN] No PNG returned")


def test_health():
    print("\n" + "="*60)
    print("[1] GET /health")
    print("="*60)
    r = httpx.get(f"{BASE}/health")
    print(f"   Status: {r.status_code}")
    print(f"   {json.dumps(r.json(), indent=2)}")


def test_recommend():
    print("\n" + "="*60)
    print("[2] POST /recommend  (rule-based, no LLM)")
    print("="*60)
    r = httpx.post(f"{BASE}/recommend", json={
        "columns": COLUMNS,
        "task": "Show revenue trend over time"
    })
    print(f"   Status: {r.status_code}")
    print(f"   {json.dumps(r.json(), indent=2)}")


def test_chart():
    print("\n" + "="*60)
    print("[3] POST /chart  (Groq generates Plotly spec + PNG)")
    print("="*60)
    r = httpx.post(f"{BASE}/chart", json={
        "task": "Compare total revenue across regions",
        "data": DATA_PAYLOAD,
        "color_scheme": "vibrant",
        "render_png": True,
    }, timeout=30)
    print(f"   Status: {r.status_code}")
    body = r.json()
    print(f"   Chart type: {body.get('chart_type')}")
    print(f"   Spec keys: {list(body.get('spec', {}).keys())}")
    print(f"   Traces count: {len(body.get('spec', {}).get('data', []))}")
    save_png(body.get("png_base64"), "chart_bar.png")


def test_auto_insights():
    print("\n" + "="*60)
    print("[4] POST /auto-insights  (Groq auto-picks best visuals)")
    print("="*60)
    r = httpx.post(f"{BASE}/auto-insights", json={
        "data": DATA_PAYLOAD,
        "color_scheme": "corporate",
        "render_png": True,
        "max_insights": 5,
    }, timeout=120)
    print(f"   Status: {r.status_code}")
    body = r.json()
    print(f"   Requested: {body.get('total_requested')}")
    print(f"   Generated: {body.get('total_generated')}")
    print()
    for i, chart in enumerate(body.get("charts", [])):
        status = chart.get("status", "?")
        icon = "[OK]" if status == "success" else "[FAIL]"
        print(f"   {icon} Chart {i+1}: {chart.get('chart_type', '?')} -- {chart.get('task', '?')}")
        if chart.get("png_base64"):
            save_png(chart["png_base64"], f"insight_{i+1}_{chart['chart_type']}.png")


def test_dashboard():
    print("\n" + "="*60)
    print("[5] POST /dashboard  (multi-chart HTML)")
    print("="*60)
    r = httpx.post(f"{BASE}/dashboard", json={
        "charts": [
            {
                "task": "Show revenue trend over time",
                "data": DATA_PAYLOAD,
                "color_scheme": "corporate",
            },
            {
                "task": "Compare revenue by region",
                "data": DATA_PAYLOAD,
                "color_scheme": "vibrant",
            },
        ]
    }, timeout=30)
    print(f"   Status: {r.status_code}")
    body = r.json()
    print(f"   Chart count: {body.get('chart_count')}")
    html = body.get("html", "")
    if html:
        path = Path("./test_outputs/dashboard.html")
        path.parent.mkdir(exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"   [SAVED] Dashboard: {path}")
        print(f"   Open in browser: file:///{path.resolve()}")


if __name__ == "__main__":
    print("=" * 60)
    print("Viz-Agent Live Test -- Real Sales Data")
    print("Server must be running: python -m uvicorn app.main:app --port 8003")
    print("=" * 60)

    test_health()
    test_recommend()
    test_chart()
    test_auto_insights()
    test_dashboard()

    print("\n" + "="*60)
    print("[DONE] All tests complete! Check ./test_outputs/ for PNGs and HTML")
    print("="*60)
