"""
Synthetic Data Engine
=====================
Seeded, reproducible synthetic data for all 8 platform modules.
Mirrors real data structures from the PDF architecture specification.
"""

import random
from datetime import datetime, timedelta, timezone
from typing import Any

# ─── Constants ───────────────────────────────────────────────────────────────
COMMODITIES = ["Coal", "Iron Ore", "Containers", "Crude Oil", "LNG", "Fertilizers", "Automobiles", "Agricultural"]

VESSEL_NAMES = [
    "MV Bharati", "MT Vikrant", "MV Sagar Mala", "MT Godavari", "MV Chennai Star",
    "MT Kaveri", "MV Mumbai Pride", "MT Narmada", "MV Kolkata Gateway", "MT Brahmaputra",
    "MV Pacific Trader", "MT Atlantic Carrier", "MV Indian Osprey", "MT Ganga Express",
    "MV Bay of Bengal", "MT Lakshadweep", "MV Konkan Queen", "MT Coromandel Coast",
    "MV Andaman Star", "MT Nicobar Spirit", "MV Deen Dayal", "MT Sagarmatha",
    "MV Kamarajar", "MT Jawaharlal", "MV Nehru Star",
]

FLAGS = ["India", "Panama", "Liberia", "Marshall Islands", "Singapore", "Malta", "Bahamas", "China", "Greece", "Norway"]

DESTINATIONS = {
    "INPAV": "Paradip Port",
    "INMUN": "Mumbai JNPT",
    "INCCU": "Kolkata Dock",
    "INCHD": "Chennai Port",
    "INVIZ": "Visakhapatnam",
    "INPRT": "Mundra Port",
    "INMRM": "Mormugao",
}

ORIGINS = ["Shanghai", "Rotterdam", "Singapore", "Fujairah", "Houston", "Durban", "Brisbane", "Santos"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─── Module 1: Vessel Intelligence ───────────────────────────────────────────

def generate_vessels(n: int = 25) -> list[dict]:
    vessels = []
    dest_keys = list(DESTINATIONS.keys())
    for i in range(n):
        r = random.Random(42 + i)
        commodity = r.choice(COMMODITIES)
        dest_code = r.choice(dest_keys)
        capacity_mt = r.randint(30_000, 220_000)
        hours_to_arrival = r.randint(8, 168)
        eta = _now() + timedelta(hours=hours_to_arrival)
        speed_kn = round(r.uniform(8.5, 16.5), 1)
        vessels.append({
            "mmsi": f"4190{50 + i:04d}",
            "imo": f"IMO{9_100_000 + i * 37}",
            "name": VESSEL_NAMES[i % len(VESSEL_NAMES)],
            "flag": r.choice(FLAGS),
            "commodity": commodity,
            "origin": r.choice(ORIGINS),
            "destination_code": dest_code,
            "destination_name": DESTINATIONS[dest_code],
            "lat": round(r.uniform(5.0, 22.0), 4),
            "lon": round(r.uniform(65.0, 90.0), 4),
            "speed_kn": speed_kn,
            "heading": r.randint(0, 359),
            "capacity_mt": capacity_mt,
            "cargo_mt": r.randint(int(capacity_mt * 0.6), capacity_mt),
            "eta_iso": eta.isoformat(),
            "hours_to_arrival": hours_to_arrival,
            "distance_km": round(speed_kn * hours_to_arrival * 1.852, 1),
            "delay_prob": round(r.uniform(0.05, 0.45), 2),
            "route_risk": round(r.uniform(0.1, 0.9), 2),
            "historical_punctuality": round(r.uniform(0.60, 0.97), 2),
            "status": r.choice(["Underway", "Underway", "Underway", "At Anchor", "Moored"]),
        })
    return vessels


def generate_congestion_alerts(vessels: list[dict]) -> list[dict]:
    alerts = []
    for v in vessels:
        if v["route_risk"] > 0.7 or v["delay_prob"] > 0.35:
            severity = "Critical" if v["route_risk"] > 0.85 else "High" if v["route_risk"] > 0.7 else "Medium"
            alerts.append({
                "vessel": v["name"],
                "commodity": v["commodity"],
                "destination": v["destination_name"],
                "route_risk": v["route_risk"],
                "delay_prob": v["delay_prob"],
                "hours_to_arrival": v["hours_to_arrival"],
                "severity": severity,
                "message": f"{v['name']} carrying {v['commodity']} has elevated route risk {v['route_risk']:.2f}",
            })
    return sorted(alerts, key=lambda x: x["route_risk"], reverse=True)


# ─── Module 2: Cargo Forecasting ─────────────────────────────────────────────

def generate_cargo_forecast(horizon_days: int = 30) -> dict:
    base_volumes = {
        "Coal": 42_000, "Iron Ore": 67_000, "Containers": 28_000, "Crude Oil": 55_000,
        "LNG": 18_000, "Fertilizers": 12_000, "Automobiles": 8_500, "Agricultural": 22_000,
    }
    today = _now().date()
    hist_dates = [(today - timedelta(days=89 - i)).isoformat() for i in range(90)]
    fore_dates = [(today + timedelta(days=i + 1)).isoformat() for i in range(horizon_days)]

    result = {}
    for comm, base in base_volumes.items():
        r = random.Random(hash(comm) % (2 ** 31))
        trend = r.uniform(-0.001, 0.003)
        noise = base * 0.08
        hist_vals = [max(0.0, base + trend * i * base + r.gauss(0, noise)) for i in range(90)]
        last_val = hist_vals[-1]
        fore_vals = [max(0.0, last_val * (1 + trend * (i + 1)) + r.gauss(0, noise * 0.7)) for i in range(horizon_days)]
        result[comm] = {
            "historical_dates": hist_dates,
            "historical_values": [round(v) for v in hist_vals],
            "forecast_dates": fore_dates,
            "forecast_values": [round(v) for v in fore_vals],
            "conf_low": [round(v * 0.93) for v in fore_vals],
            "conf_high": [round(v * 1.07) for v in fore_vals],
            "trend_pct_annual": round(trend * 365 * 100, 1),
        }
    return result


def generate_forecast_accuracy() -> list[dict]:
    models = [
        ("Prophet", 8.2, "Baseline"),
        ("XGBoost", 6.7, "Baseline"),
        ("TFT", 5.1, "Active"),
        ("PatchTST", 4.8, "Active"),
        ("Informer", 5.9, "Baseline"),
    ]
    rows = []
    for model, base_mape, status in models:
        r = random.Random(hash(model) % (2 ** 31))
        mape = base_mape + r.uniform(-0.3, 0.3)
        rmse = mape * 380 + r.uniform(-50, 50)
        mae = rmse * 0.72 + r.uniform(-20, 20)
        rows.append({
            "model": model,
            "mape_pct": round(mape, 2),
            "rmse": round(rmse),
            "mae": round(mae),
            "accuracy_pct": round(100 - mape, 1),
            "status": status,
        })
    return rows


def generate_berth_status(n_berths: int = 12) -> list[dict]:
    berths = []
    for i in range(n_berths):
        r = random.Random(100 + i)
        occupied = r.random() < 0.72
        vessel_idx = r.randint(0, 24) if occupied else None
        berths.append({
            "berth_id": f"B{i + 1:02d}",
            "name": f"Berth {i + 1}",
            "occupied": occupied,
            "commodity": r.choice(COMMODITIES) if occupied else None,
            "vessel": VESSEL_NAMES[vessel_idx % len(VESSEL_NAMES)] if vessel_idx is not None else None,
            "capacity_mt": r.choice([50_000, 80_000, 100_000, 150_000, 200_000]),
            "hours_remaining": r.randint(2, 36) if occupied else None,
            "crane_count": r.randint(2, 6),
            "utilization_pct": round(r.uniform(60, 98), 1) if occupied else 0.0,
        })
    return berths


# ─── Module 3: Trade Intelligence ────────────────────────────────────────────

def generate_trade_lanes() -> list[dict]:
    return [
        {"route": "China → India", "commodity": "Containers", "volume_mt": 1_240_000, "growth_pct": 18.4, "trend": "up", "vessels_month": 142},
        {"route": "Australia → India", "commodity": "Coal", "volume_mt": 3_800_000, "growth_pct": 6.2, "trend": "up", "vessels_month": 48},
        {"route": "Brazil → India", "commodity": "Iron Ore", "volume_mt": 2_100_000, "growth_pct": -3.8, "trend": "down", "vessels_month": 31},
        {"route": "Qatar → India", "commodity": "LNG", "volume_mt": 890_000, "growth_pct": 12.7, "trend": "up", "vessels_month": 22},
        {"route": "UAE → India", "commodity": "Crude Oil", "volume_mt": 4_200_000, "growth_pct": 2.1, "trend": "up", "vessels_month": 58},
        {"route": "Canada → India", "commodity": "Fertilizers", "volume_mt": 420_000, "growth_pct": -8.9, "trend": "down", "vessels_month": 14},
        {"route": "Japan → India", "commodity": "Automobiles", "volume_mt": 180_000, "growth_pct": 24.1, "trend": "up", "vessels_month": 9},
        {"route": "Vietnam → India", "commodity": "Agricultural", "volume_mt": 680_000, "growth_pct": 9.8, "trend": "up", "vessels_month": 38},
        {"route": "South Africa → India", "commodity": "Coal", "volume_mt": 1_600_000, "growth_pct": -1.4, "trend": "down", "vessels_month": 29},
        {"route": "Indonesia → India", "commodity": "Coal", "volume_mt": 2_900_000, "growth_pct": 4.5, "trend": "up", "vessels_month": 52},
    ]


def generate_commodity_prices() -> list[dict]:
    today = _now().date()
    items = [
        {"commodity": "Coal (Newcastle)", "index": "MCAL", "price_usd": 128.50, "change_30d": 4.2},
        {"commodity": "Iron Ore (62% Fe)", "index": "SGX", "price_usd": 114.80, "change_30d": -2.1},
        {"commodity": "LNG (JKM)", "index": "JKM", "price_usd": 12.75, "change_30d": 8.9},
        {"commodity": "Crude Oil (Brent)", "index": "ICE", "price_usd": 82.30, "change_30d": 1.5},
        {"commodity": "Urea (Fertilizer)", "index": "NYMEX", "price_usd": 340.00, "change_30d": -5.3},
        {"commodity": "Containers (SCFI)", "index": "SCFI", "price_usd": 1850.00, "change_30d": 12.4},
    ]
    for p in items:
        r = random.Random(hash(p["commodity"]) % (2 ** 31))
        base = p["price_usd"]
        start = base * (1 - p["change_30d"] / 100)
        series = [start + (base - start) * i / 29 + r.gauss(0, base * 0.012) for i in range(30)]
        p["trend"] = "up" if p["change_30d"] > 0 else "down"
        p["series_dates"] = [(today - timedelta(days=29 - i)).isoformat() for i in range(30)]
        p["series_values"] = [round(v, 2) for v in series]
    return items


def generate_market_opportunities() -> list[dict]:
    return [
        {
            "rank": 1, "commodity": "Automobiles", "route": "Japan / Korea → India",
            "opportunity": "EV import surge driven by PLI scheme. 24% YoY growth. Ro-Ro terminal expansion opportunity.",
            "revenue_potential_cr": 840, "confidence": 0.87, "time_horizon": "6 months",
        },
        {
            "rank": 2, "commodity": "Containers", "route": "SE Asia → India",
            "opportunity": "Red Sea crisis rerouting ships via Cape of Good Hope, increasing transit via Indian ports.",
            "revenue_potential_cr": 2100, "confidence": 0.82, "time_horizon": "12 months",
        },
        {
            "rank": 3, "commodity": "LNG", "route": "Qatar / Australia → India",
            "opportunity": "India LNG demand rising 13% annually. JKM price drop creates import window.",
            "revenue_potential_cr": 1450, "confidence": 0.79, "time_horizon": "3 months",
        },
        {
            "rank": 4, "commodity": "Iron Ore", "route": "Brazil → India (backhaul)",
            "opportunity": "Brazilian miners offering discounted spot tonnage. Steel demand recovery Q3.",
            "revenue_potential_cr": 680, "confidence": 0.71, "time_horizon": "2 months",
        },
    ]


# ─── Module 4: Anomaly Detection ─────────────────────────────────────────────

def generate_anomaly_events() -> list[dict]:
    now = _now()
    return [
        {
            "event_id": "ANO-001", "severity": "Critical", "type": "Cargo Surge",
            "commodity": "Containers", "algorithm": "Isolation Forest", "confidence": 0.94,
            "timestamp": (now - timedelta(hours=2, minutes=15)).isoformat(),
            "description": "Container traffic increased 40% above 90-day baseline. Possible trade rerouting from Red Sea disruption.",
            "affected_berths": ["B03", "B04", "B09"],
            "recommended_action": "Activate overflow yard capacity, notify crane operators",
        },
        {
            "event_id": "ANO-002", "severity": "High", "type": "Vessel Diversion",
            "commodity": "Coal", "algorithm": "LSTM Anomaly Detection", "confidence": 0.88,
            "timestamp": (now - timedelta(hours=5, minutes=42)).isoformat(),
            "description": "3 coal vessels originally destined for Mundra rerouted to Paradip. Route risk score elevated to 0.82.",
            "affected_berths": ["B01", "B02"],
            "recommended_action": "Pre-position coal handling equipment at B01-B02",
        },
        {
            "event_id": "ANO-003", "severity": "High", "type": "Congestion Spike",
            "commodity": "Iron Ore", "algorithm": "Transformer Anomaly Detection", "confidence": 0.91,
            "timestamp": (now - timedelta(hours=11)).isoformat(),
            "description": "Berth wait time for Iron Ore vessels exceeded 18 hours (3x normal). 7 vessels at anchor.",
            "affected_berths": ["B05", "B06", "B07"],
            "recommended_action": "Expedite rail evacuation, request emergency crane deployment",
        },
        {
            "event_id": "ANO-004", "severity": "Medium", "type": "Cargo Collapse",
            "commodity": "LNG", "algorithm": "Autoencoder", "confidence": 0.79,
            "timestamp": (now - timedelta(hours=18, minutes=30)).isoformat(),
            "description": "LNG import volumes 28% below 30-day forecast. Correlated with JKM price spike.",
            "affected_berths": ["B10"],
            "recommended_action": "Review LNG handling contracts, consider spot market opportunities",
        },
        {
            "event_id": "ANO-005", "severity": "Low", "type": "Speed Anomaly",
            "commodity": "Crude Oil", "algorithm": "Isolation Forest", "confidence": 0.72,
            "timestamp": (now - timedelta(hours=31)).isoformat(),
            "description": "MT Brahmaputra speed reduced from 14.2 to 6.8 knots. Possible mechanical issue or weather avoidance.",
            "affected_berths": [],
            "recommended_action": "Monitor vessel position, alert port operations",
        },
    ]


def generate_anomaly_history(days: int = 30) -> dict:
    today = _now().date()
    dates = [(today - timedelta(days=29 - i)).isoformat() for i in range(days)]
    result: dict[str, Any] = {}
    caps = {"Critical": 2, "High": 4, "Medium": 6, "Low": 8}
    for sev, cap in caps.items():
        r = random.Random(hash(sev) % (2 ** 31))
        result[sev] = {"dates": dates, "counts": [r.randint(0, cap) for _ in range(days)]}
    return result


# ─── Module 5: Incentive Engine ──────────────────────────────────────────────

def generate_incentive_recommendations() -> list[dict]:
    return [
        {
            "rec_id": "INC-001", "priority": "High",
            "action": "Reduce container handling charges by 5%",
            "rationale": "Container traffic down 12% YoY. Price elasticity model suggests 5% reduction recovers 10% volume.",
            "current_metric": "Container traffic: -12% MoM",
            "predicted_traffic_impact": "+10.2%", "predicted_revenue_impact": "+4.1%",
            "confidence": 0.84, "method": "Reinforcement Learning + Price Elasticity Model", "implementation_weeks": 2,
        },
        {
            "rec_id": "INC-002", "priority": "High",
            "action": "LNG berth priority guarantee — pre-booking discount 8%",
            "rationale": "LNG import windows are narrow. Priority access reduces vessel idle time, increasing loyalty.",
            "current_metric": "LNG berth wait: 14.2 hrs avg",
            "predicted_traffic_impact": "+18.5%", "predicted_revenue_impact": "+7.8%",
            "confidence": 0.78, "method": "Monte Carlo Policy Optimization", "implementation_weeks": 4,
        },
        {
            "rec_id": "INC-003", "priority": "Medium",
            "action": "Coal volume incentive: >100,000 MT/month gets 3% rebate",
            "rationale": "South African coal routes showing -1.4% decline. Volume rebate can capture diversion traffic.",
            "current_metric": "Coal volume: -1.4% trend",
            "predicted_traffic_impact": "+6.8%", "predicted_revenue_impact": "+3.2%",
            "confidence": 0.72, "method": "What-If Analysis + Historical Regression", "implementation_weeks": 6,
        },
        {
            "rec_id": "INC-004", "priority": "Strategic",
            "action": "Partner with auto OEMs for dedicated Ro-Ro terminal allocation",
            "rationale": "Automobile imports growing 24% YoY. Dedicated terminal creates switching cost and long-term contracts.",
            "current_metric": "Automobile growth: +24.1%",
            "predicted_traffic_impact": "+35%", "predicted_revenue_impact": "+12.4%",
            "confidence": 0.91, "method": "Policy Optimization + RL Agent", "implementation_weeks": 26,
        },
    ]


def run_monte_carlo(scenario: str, charge_delta: float = -5.0, incentive_pct: float = 8.0) -> dict:
    r = random.Random(hash(scenario + str(charge_delta)) % (2 ** 31))
    base_rev = 120.0
    samples = sorted([base_rev * (1 - charge_delta / 100 * 0.5) + r.gauss(0, base_rev * 0.08) for _ in range(200)])
    n = len(samples)
    return {
        "scenario": scenario,
        "charge_delta_pct": charge_delta,
        "incentive_pct": incentive_pct,
        "iterations": 1000,
        "samples": [round(s, 2) for s in samples],
        "p10": round(samples[int(n * 0.1)], 2),
        "p25": round(samples[int(n * 0.25)], 2),
        "p50": round(samples[int(n * 0.50)], 2),
        "p75": round(samples[int(n * 0.75)], 2),
        "p90": round(samples[int(n * 0.90)], 2),
        "mean": round(sum(samples) / n, 2),
    }


# ─── Module 6: Digital Twin ───────────────────────────────────────────────────

DIGITAL_TWIN_SCENARIOS = {
    "cargo_surge": {
        "name": "Cargo Surge +20%", "description": "Simulate 20% increase in container cargo volume",
        "congestion_index": 0.84, "congestion_delta": "+34%",
        "berth_utilization_pct": 94.2, "berth_delta": "+12.1%",
        "storage_utilization_pct": 88.7, "storage_delta": "+22.4%",
        "expected_revenue_cr": 142.8, "revenue_delta": "+18.3%",
        "additional_cranes_needed": 8, "additional_workforce": 320, "risk_level": "High",
    },
    "vessel_delay": {
        "name": "Vessel Delay Increase", "description": "Simulate 30% increase in average vessel delays",
        "congestion_index": 0.79, "congestion_delta": "+26%",
        "berth_utilization_pct": 91.4, "berth_delta": "+8.8%",
        "storage_utilization_pct": 82.1, "storage_delta": "+13.2%",
        "expected_revenue_cr": 118.3, "revenue_delta": "-1.9%",
        "additional_cranes_needed": 2, "additional_workforce": 85, "risk_level": "Medium",
    },
    "incentive_change": {
        "name": "Trade Incentive Policy", "description": "Simulate 5% handling charge reduction",
        "congestion_index": 0.71, "congestion_delta": "+13%",
        "berth_utilization_pct": 86.9, "berth_delta": "+3.2%",
        "storage_utilization_pct": 74.3, "storage_delta": "+2.8%",
        "expected_revenue_cr": 128.5, "revenue_delta": "+6.8%",
        "additional_cranes_needed": 3, "additional_workforce": 120, "risk_level": "Low",
    },
    "weather_disruption": {
        "name": "Weather Disruption", "description": "Simulate cyclone-category weather impacting vessel arrivals",
        "congestion_index": 0.38, "congestion_delta": "-39%",
        "berth_utilization_pct": 48.2, "berth_delta": "-42.6%",
        "storage_utilization_pct": 55.8, "storage_delta": "-23.2%",
        "expected_revenue_cr": 71.4, "revenue_delta": "-40.7%",
        "additional_cranes_needed": 0, "additional_workforce": -220, "risk_level": "Critical",
    },
}


def get_twin_scenario(scenario_key: str) -> dict:
    return DIGITAL_TWIN_SCENARIOS.get(scenario_key, {})


def get_twin_monte_carlo(scenario_key: str) -> dict:
    scenario = DIGITAL_TWIN_SCENARIOS.get(scenario_key, {})
    base_rev = scenario.get("expected_revenue_cr", 120.0)
    return run_monte_carlo(scenario_key, charge_delta=0.0, incentive_pct=0.0)


# ─── Module 7: AI Copilot ─────────────────────────────────────────────────────

def generate_agent_trace(query: str = "") -> dict:
    q = query.lower()
    if any(w in q for w in ["simulate", "what if", "scenario", "optimize", "capacity increase"]):
        complexity, tier, agent = "High", "Tier 1: Heavy Synthesis (LLM)", "Policy & Simulation Agent"
        tools = ["Python REPL", "Monte Carlo Simulator"]
    elif any(w in q for w in ["why", "news", "global", "trade", "context", "rerouting"]):
        complexity, tier, agent = "Medium", "Tier 2: Fast Reasoning (SLM)", "Trade Intelligence Agent"
        tools = ["Milvus Vector Search", "SQL Executor"]
    else:
        complexity, tier, agent = "Low", "Tier 3: Deterministic Zero-LLM", "Data Retrieval Agent"
        tools = ["SQL Executor"]

    trace = [
        {"step": 1, "component": "LangGraph Dispatcher", "action": "Received user query",
         "detail": f'"{query[:80]}"', "status": "done", "ms": 12},
        {"step": 2, "component": "Intent & Complexity Analyzer", "action": "Classify intent & complexity",
         "detail": f"Complexity: {complexity}", "status": "done", "ms": 38},
        {"step": 3, "component": "Agent Router", "action": f"Route to {agent}",
         "detail": f"Tools: {', '.join(tools)}", "status": "done", "ms": 8},
        {"step": 4, "component": agent, "action": f"Execute: {tools[0]}",
         "detail": f"Running {tools[0]} against data pool", "status": "done", "ms": 142 if complexity == "High" else 89},
    ]
    if len(tools) > 1:
        trace.append({"step": 5, "component": agent, "action": f"Execute: {tools[1]}",
                       "detail": f"Cross-referencing with {tools[1]}", "status": "done", "ms": 67})
    trace.append({"step": len(trace) + 1, "component": tier, "action": "Synthesize & format response",
                   "detail": "Generating structured actionable output", "status": "done",
                   "ms": 210 if complexity == "High" else 95 if complexity == "Medium" else 22})

    return {
        "query": query, "complexity": complexity, "tier": tier,
        "agent": agent, "tools": tools,
        "total_ms": sum(t["ms"] for t in trace),
        "trace": trace,
    }


def generate_copilot_response(query: str) -> dict:
    q = query.lower()
    if "forecast" in q or "decreasing" in q:
        answer = (
            "**Why Cargo Forecast is Declining — Analysis**\n\n"
            "**1. Iron Ore (Brazil Route) — -3.8% trend**\n"
            "Vale S.A. production constraints + higher Cape route freight rates are suppressing Brazil-India volumes.\n\n"
            "**2. Fertilizer Imports — -8.9% trend**\n"
            "India's domestic fertilizer production expansion under subsidy reform is reducing import dependency.\n\n"
            "**3. Macro Headwinds**\n"
            "USD/INR appreciation (+2.1%) marginally increasing import cost for discretionary cargo categories.\n\n"
            "**Counter-trend: Strong Growth Segments**\n"
            "- Containers (SE Asia): +18.4% — Red Sea rerouting effect\n"
            "- Automobiles (Japan): +24.1% — PLI-driven EV surge\n"
            "- LNG (Qatar): +12.7% — India energy demand growth"
        )
        refs = ["cargo_forecasting", "trade_intelligence", "commodity_prices"]
        followups = ["What incentive should be applied to recover fertilizer traffic?",
                     "Which commodities are growing fastest?", "Simulate cargo surge +20% scenario"]
    elif "incentive" in q:
        answer = (
            "**Recommended Incentive Strategy — Priority Order**\n\n"
            "**1. Container Handling Charge -5% (HIGH — implement in 2 weeks)**\n"
            "Predicted: +10.2% traffic, +4.1% revenue. Confidence: 84%.\n"
            "Method: Reinforcement Learning + Price Elasticity Model\n\n"
            "**2. LNG Berth Priority Guarantee — 8% pre-booking discount (HIGH — 4 weeks)**\n"
            "Predicted: +18.5% LNG traffic, +7.8% revenue. Confidence: 78%.\n"
            "Method: Monte Carlo Policy Optimization\n\n"
            "**3. Automobile Ro-Ro Terminal Partnership (STRATEGIC — 26 weeks)**\n"
            "Predicted: +35% automobile volume, +12.4% revenue. Confidence: 91%.\n"
            "Highest long-term ROI in the recommendation portfolio."
        )
        refs = ["incentive_engine", "trade_intelligence"]
        followups = ["Simulate the effect of reducing charges by 10%",
                     "What will happen if berth capacity increases?",
                     "Which trade lanes are growing fastest?"]
    elif "berth" in q or "capacity" in q:
        answer = (
            "**Current Berth Status (12 Berths)**\n\n"
            "- Occupied: 8 berths (66.7% utilization)\n"
            "- Available: 4 berths (B03, B08, B11, B12)\n"
            "- Average hours remaining: 18.4 hours\n"
            "- Highest congestion: Iron Ore berths B05–B07 (avg wait: 18 hrs)\n\n"
            "**7-Day Forecast:** Utilization expected to rise to 82% — 14 vessels within 72-hr ETA window.\n\n"
            "**Recommendation:** Pre-allocate B03 and B08 for incoming LNG vessel MV Bay of Bengal (ETA: 34 hours)."
        )
        refs = ["vessel_intelligence", "digital_twin"]
        followups = ["Which vessels are arriving in the next 48 hours?",
                     "Simulate vessel delay increase scenario",
                     "What is the congestion index trend?"]
    else:
        answer = (
            "**Port Intelligence Summary — Current Status**\n\n"
            "- Active vessels inbound: **25** (14 within 72-hour ETA window)\n"
            "- Berth utilization: **72.4%** (8/12 berths occupied)\n"
            "- Daily throughput: **1,24,000 MT** (+3.2% vs yesterday)\n"
            "- Congestion index: **0.63** (Moderate)\n"
            "- Revenue index: **118.5 Cr** (monthly tracking)\n\n"
            "**Active Alerts:**\n"
            "- Container traffic surge +40% (Isolation Forest, 94% confidence)\n"
            "- 3 coal vessels diverted Mundra → Paradip (LSTM alert)\n"
            "- LNG volumes 28% below 30-day forecast"
        )
        refs = ["executive", "anomaly_detection", "vessel_intelligence"]
        followups = ["Why is cargo forecast decreasing?",
                     "What incentive should be applied?",
                     "Simulate cargo surge +20% scenario"]

    return {"answer": answer, "data_refs": refs, "confidence": 0.86, "suggested_followups": followups}


SUGGESTED_QUERIES = [
    "Why is cargo forecast decreasing?",
    "Which commodities are growing fastest?",
    "What incentive should be applied to containers?",
    "What will happen if berth capacity increases by 2 berths?",
    "Simulate cargo surge +20% scenario",
    "Which vessels are arriving in the next 48 hours?",
    "What is the current congestion index?",
    "Show me anomalies detected today",
]


# ─── Data Pipeline ────────────────────────────────────────────────────────────

def generate_pipeline_log() -> list[dict]:
    now = _now()
    raw_events = [
        ("KAFKA", "INFO", "AIS stream ingested: 1,842 vessel position records"),
        ("KAFKA", "INFO", "Commodity price feed received: 48 index updates"),
        ("KAFKA", "INFO", "Weather grid NOAA GFS 0.25° batch: 10x10 scalar matrix"),
        ("SPARK", "INFO", "Temporal alignment: 98.7% records matched to 1-min slots"),
        ("SPARK", "INFO", "Missing value imputation: 142 AIS gaps filled via Kalman filter"),
        ("SPARK", "WARN", "3 vessel records outside geofence — quarantined for review"),
        ("AIRFLOW", "INFO", "DAG maritime_daily_etl: commodity_prices_fetch completed (14.2 min)"),
        ("AIRFLOW", "INFO", "DAG maritime_daily_etl: berth_occupancy_sync completed (3.1 min)"),
        ("PYTORCH", "INFO", "Grid matching: Ship coordinates overlaid on weather scalars"),
        ("PYTORCH", "INFO", "25 vessels processed — route risk vectors computed"),
        ("SLM", "INFO", "Text processor: 18 news articles parsed, 43 entities extracted"),
        ("SLM", "INFO", "PII masking: 0 personal data items detected (DPDP compliant)"),
        ("POSTGRESQL", "INFO", "Master port data synced: 847 berth records updated"),
        ("TIMESCALEDB", "INFO", "Time-series append: 2,184 AIS points committed"),
        ("MILVUS", "INFO", "Vector DB: 18 news embeddings indexed (dim=1536)"),
        ("KAFKA", "INFO", "Consumer lag: ais_stream=0, commodity=12"),
        ("SPARK", "INFO", "Streaming job maritime_fusion: 3 active stages, 14,200 rows/sec"),
        ("AIRFLOW", "INFO", "Next DAG run scheduled: 20:00 UTC"),
    ]
    events = []
    for i, (src, lvl, msg) in enumerate(raw_events):
        t = now - timedelta(minutes=len(raw_events) - i, seconds=i * 3)
        events.append({"timestamp": t.strftime("%H:%M:%S"), "source": src, "level": lvl, "message": msg})
    return events


def generate_pipeline_metrics() -> dict:
    return {
        "kafka": {"messages_per_sec": 1842, "consumer_lag": 12, "active_topics": 6, "uptime_pct": 99.97},
        "spark": {"active_jobs": 3, "rows_per_sec": 14200, "memory_used_gb": 12.4, "uptime_pct": 99.91},
        "airflow": {"dags_active": 5, "last_run_duration_min": 14.2, "success_rate_pct": 98.8, "uptime_pct": 99.84},
        "data_pools": {
            "postgresql_records": 847203,
            "timescaledb_records": 12840000,
            "milvus_vectors": 94820,
            "total_storage_gb": 842.3,
        },
    }


# ─── Executive Dashboard ──────────────────────────────────────────────────────

def generate_kpis() -> dict:
    return {
        "berth_utilization_pct": 72.4, "berth_delta": "+2.1%",
        "active_vessels_inbound": 25, "vessels_delta": "+3",
        "daily_throughput_mt": 124000, "throughput_delta": "+3.2%",
        "revenue_cr": 118.5, "revenue_delta": "+6.8%",
        "congestion_index": 0.63, "congestion_delta": "-0.04",
        "vessels_at_anchor": 7, "anchor_delta": "+2",
        "avg_turnaround_hrs": 22.4, "turnaround_delta": "-1.2%",
        "forecast_accuracy_pct": 91.2, "accuracy_delta": "+0.8%",
    }


def generate_port_events() -> list[dict]:
    now = _now()
    return [
        {"time": (now - timedelta(minutes=8)).strftime("%H:%M"), "type": "arrival",
         "message": "MV Bharati berthed at B02 — 48,000 MT Coal from Newcastle"},
        {"time": (now - timedelta(minutes=22)).strftime("%H:%M"), "type": "alert",
         "message": "Anomaly detected: Container surge +40% — Isolation Forest confidence 94%"},
        {"time": (now - timedelta(minutes=41)).strftime("%H:%M"), "type": "departure",
         "message": "MT Kaveri departed B07 — 67,000 MT Iron Ore delivery complete"},
        {"time": (now - timedelta(minutes=58)).strftime("%H:%M"), "type": "forecast",
         "message": "LNG forecast revised: -28% below baseline. JKM price spike correlation detected"},
        {"time": (now - timedelta(hours=1, minutes=15)).strftime("%H:%M"), "type": "arrival",
         "message": "MV Mumbai Pride anchored — waiting for B05 clearance (Iron Ore, Visakhapatnam)"},
        {"time": (now - timedelta(hours=1, minutes=48)).strftime("%H:%M"), "type": "incentive",
         "message": "Incentive Engine: Container charge reduction recommendation generated (priority: HIGH)"},
        {"time": (now - timedelta(hours=2, minutes=11)).strftime("%H:%M"), "type": "alert",
         "message": "3 coal vessels diverted from Mundra to Paradip (route risk elevated)"},
        {"time": (now - timedelta(hours=2, minutes=55)).strftime("%H:%M"), "type": "system",
         "message": "Daily AIS batch: 1,842 records ingested, 98.7% temporal alignment"},
    ]


def generate_revenue_trend(days: int = 30) -> dict:
    today = _now().date()
    dates = [(today - timedelta(days=29 - i)).isoformat() for i in range(days)]
    r = random.Random(77)
    base_rev = 110.0
    revenues = [max(80, base_rev + i * 0.3 + r.gauss(0, 5.0)) for i in range(days)]
    throughputs = [max(90000, 115000 + i * 200 + r.gauss(0, 3000)) for i in range(days)]
    return {
        "dates": dates,
        "revenue_cr": [round(v, 1) for v in revenues],
        "throughput_mt": [round(t) for t in throughputs],
    }
