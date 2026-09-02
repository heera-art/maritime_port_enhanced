"""
copilot.py — Production-Grade Agent Copilot and Scenario Simulator Service
--------------------------------------------------------------------------
Implements the simulation of:
1. Spatio-Temporal Fusion Engine & PyTorch Geospatial Processor (Layer 2 & 4).
2. LangGraph Cognitive Dispatcher (Layer 6) with Intent, Compute, and Data Analysis.
3. 7 Specialized AI Agents with exact TimescaleDB SQL, Milvus Vector search, and Python REPL simulations (Layer 7).
4. Cascading Multi-Tier Execution (Tier 1 Heavy LLM -> Tier 2 Fast SLM -> Tier 3 Code) (Layer 8).
5. Monte Carlo Simulation Engine (Layer 9).
"""

import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

# Stable seed for deterministic generation in demos
RANDOM_SEED = 42

def _get_timestamp(offset_seconds: int = 0) -> str:
    now = datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)
    return now.strftime("%H:%M:%S")

def generate_synthetic_data(scenario: str) -> Dict[str, Any]:
    """
    Generates synthetic datasets representing the state under a given scenario.
    Incorporate elements of Spatio-Temporal Fusion and Geospatial Layer.
    """
    rng = random.Random(RANDOM_SEED)
    
    # Base vessels
    vessels = [
        {"id": "VES-101", "name": "Oceanic Express", "type": "Container", "cargo_tonnage": 45000, "speed_knots": 14.5, "status": "In Transit", "destination": "Cochin Port", "eta": "ETA +12h", "route_risk": "Low", "delay_prob": 0.05},
        {"id": "VES-102", "name": "Indus Navigator", "type": "Crude Carrier", "cargo_tonnage": 120000, "speed_knots": 12.2, "status": "At Anchor", "destination": "JNPT", "eta": "Anchored", "route_risk": "Low", "delay_prob": 0.00},
        {"id": "VES-103", "name": "Kailash Pioneer", "type": "Dry Bulk", "cargo_tonnage": 55000, "speed_knots": 11.8, "status": "In Transit", "destination": "Mumbai Port", "eta": "ETA +24h", "route_risk": "Low", "delay_prob": 0.08},
        {"id": "VES-104", "name": "Malabar Trader", "type": "LNG Carrier", "cargo_tonnage": 75000, "speed_knots": 16.0, "status": "In Transit", "destination": "Cochin Port", "eta": "ETA +6h", "route_risk": "Low", "delay_prob": 0.03},
        {"id": "VES-105", "name": "Ganges Star", "type": "Container", "cargo_tonnage": 32000, "speed_knots": 15.1, "status": "Berth", "destination": "Chennai Port", "eta": "Docked", "route_risk": "None", "delay_prob": 0.00},
    ]
    
    weather = {
        "status": "Clear",
        "wind_speed_knots": 8.5,
        "wave_height_meters": 1.2,
        "warning_level": "Green",
        "pressure_hpa": 1012,
    }
    
    port_yard = {
        "yard_occupancy_pct": 68.5,
        "avg_berth_wait_hours": 2.4,
        "crane_efficiency_pct": 92.0,
        "active_cranes": 8,
        "gate_turnaround_mins": 25.0
    }
    
    global_markets = {
        "coal_index_usd_mt": 132.50,
        "iron_ore_index_usd_mt": 104.20,
        "brent_crude_usd_bbl": 82.40
    }
    
    if scenario == "storm_inbound":
        weather.update({
            "status": "Tropical Cyclone Warning (Active)",
            "wind_speed_knots": 48.0,
            "wave_height_meters": 5.4,
            "warning_level": "Red",
            "pressure_hpa": 980,
        })
        port_yard.update({
            "yard_occupancy_pct": 84.2,
            "avg_berth_wait_hours": 18.5,
            "crane_efficiency_pct": 45.0,
            "active_cranes": 4,
            "gate_turnaround_mins": 55.0
        })
        # Modify vessels affected by storm with geospatial feature overrides
        for v in vessels:
            if v["destination"] == "Cochin Port":
                v["route_risk"] = "Critical"
                v["delay_prob"] = 0.95
                if v["id"] == "VES-101":
                    v["status"] = "Rerouted"
                    v["destination"] = "Kochi Anchorage (Outer)"
                    v["eta"] = "ETA +36h (Delayed)"
                elif v["id"] == "VES-104":
                    v["status"] = "Holding Pattern"
                    v["eta"] = "Suspended"
                    
    elif scenario == "import_surge":
        port_yard.update({
            "yard_occupancy_pct": 91.8,
            "avg_berth_wait_hours": 28.0,
            "crane_efficiency_pct": 89.0,
            "active_cranes": 10,
            "gate_turnaround_mins": 72.0
        })
        # Add surge vessels
        vessels.append({"id": "VES-106", "name": "Pacific Emperor", "type": "Crude Carrier", "cargo_tonnage": 150000, "speed_knots": 11.5, "status": "At Anchor", "destination": "JNPT", "eta": "Anchored", "route_risk": "Medium", "delay_prob": 0.40})
        vessels.append({"id": "VES-107", "name": "Arabian Dawn", "type": "Crude Carrier", "cargo_tonnage": 110000, "speed_knots": 12.0, "status": "At Anchor", "destination": "JNPT", "eta": "Anchored", "route_risk": "Medium", "delay_prob": 0.45})
        for v in vessels:
            if v["destination"] == "JNPT" and v["status"] == "At Anchor":
                v["eta"] = "Delayed (Berth Occupied)"
                v["delay_prob"] = 1.00

    elif scenario == "incentive_optimization":
        port_yard.update({
            "yard_occupancy_pct": 62.0,
            "avg_berth_wait_hours": 1.2,
            "crane_efficiency_pct": 95.0,
            "active_cranes": 8,
            "gate_turnaround_mins": 18.0
        })
        # Update commodities price & vessel parameters
        global_markets["coal_index_usd_mt"] = 145.80
        for v in vessels:
            if v["type"] == "Container":
                v["cargo_tonnage"] = int(v["cargo_tonnage"] * 1.15)
                v["speed_knots"] = round(v["speed_knots"] * 1.05, 1)

    return {
        "vessels": vessels,
        "weather": weather,
        "port_yard": port_yard,
        "global_markets": global_markets
    }

def simulate_scenario_execution(scenario: str) -> Dict[str, Any]:
    """
    Executes a multi-agent orchestration simulation for the given scenario.
    """
    synthetic_data = generate_synthetic_data(scenario)
    trace = []
    
    if scenario == "storm_inbound":
        trace.append({
            "timestamp": _get_timestamp(0),
            "agent": "Cognitive Dispatcher",
            "message": "ANALYSIS: Intent = Emergency Simulation, Complexity = HIGH, Data Type = Spatial & Time-Series. Activating Anomaly Detection, Vessel Intelligence, and Digital Twin Simulation Agents.",
            "status": "info"
        })
        trace.append({
            "timestamp": _get_timestamp(1),
            "agent": "Anomaly Detection Agent",
            "message": "TOOL: AnomalyDetector.scan_feeds(weather, AIS) -> Found Wave Heights 5.4m, wind speeds 48kt. Flagging Cochin Port status: CRITICAL.",
            "status": "warning"
        })
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Vessel Intelligence Agent",
            "message": "TOOL: TimescaleDB_Executor.query('SELECT gps_coords, eta FROM ais_trajectories') -> Identified VES-101 (Oceanic Express) and VES-104 (Malabar Trader) on storm trajectory. Generated rerouting coordinates to Kochi Anchorage (Outer).",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(4),
            "agent": "Digital Twin Simulation Agent",
            "message": "TOOL: MonteCarloSimulator.run(scenario='crane_failure_and_high_wind', runs=10000) -> Forecasted crane capacity drops to 45%. Wait times will spike to 18.5 hours. Yard occupancy will hit 84.2%.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(5),
            "agent": "Supervisor Agent",
            "message": "SYNTHESIS: Collating geospatial risk vectors, vessel rerouting instructions, and Monte Carlo yard bottlenecks. Generating Safety Directive SD-809.",
            "status": "success"
        })
        
        result_text = "CRITICAL DIRECTIVE SD-809: Inbound Cochin Port operations suspended. Oceanic Express redirected to Outer Kochi Anchorage. Malabar Trader ordered to maintain holding pattern. Crane efficiency degraded to 45%. Yard occupancy expected to peak at 84.2% within 24 hours."
        tier = "Tier 1: Heavy LLM"
        efficiency = {
            "tier_mode": "Hybrid (T1 Cognitive + T3 Direct AIS API)",
            "total_latency_sec": 1.45,
            "token_cost_usd": 0.045,
            "single_llm_equivalent_cost_usd": 0.18,
            "cost_savings_pct": 75.0,
            "accuracy_pct": 98.2
        }

    elif scenario == "import_surge":
        trace.append({
            "timestamp": _get_timestamp(0),
            "agent": "Cognitive Dispatcher",
            "message": "ANALYSIS: Intent = Congestion Optimization, Complexity = MEDIUM, Data Type = Time-Series. Activating Cargo Forecasting, Vessel Intelligence, and Anomaly Detection Agents.",
            "status": "info"
        })
        trace.append({
            "timestamp": _get_timestamp(1),
            "agent": "Anomaly Detection Agent",
            "message": "TOOL: CongestionMonitor.check_dwell_times() -> Dwell times at JNPT terminal exceeding 3σ. Active queue size = 4 crude carriers.",
            "status": "warning"
        })
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Cargo Forecasting Agent",
            "message": "TOOL: TFT_Model.forecast(commodity='crude_oil', horizon='7d') -> Predicted crude oil import spike (+34% MOM) due to seasonal stocks. Confidence: 91.3%.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(3),
            "agent": "Incentive Recommendation Agent",
            "message": "TOOL: RL_PricingOptimizer.optimize(berth_occupancy=1.12) -> Recommended 5% rebate for nighttime berth bookings (22:00 - 06:00) to distribute crane workloads.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(4),
            "agent": "Supervisor Agent",
            "message": "SYNTHESIS: Merging TFT import forecasts, vessel queues, and RL pricing parameters. Dispatching advisory report to JNPT Terminal Manager.",
            "status": "success"
        })
        
        result_text = "CONGESTION ADVISORY: JNPT crude berths saturated with average anchor wait times of 28.0 hours. TFT model predicts import surge to sustain for 6 days. Recommended immediate deployment of a 5% nighttime berth rebate to balance traffic flows."
        tier = "Tier 2: Fast SLM"
        efficiency = {
            "tier_mode": "Tier 2: Fast SLM (Local Cascade)",
            "total_latency_sec": 0.85,
            "token_cost_usd": 0.012,
            "single_llm_equivalent_cost_usd": 0.15,
            "cost_savings_pct": 92.0,
            "accuracy_pct": 94.5
        }

    elif scenario == "incentive_optimization":
        trace.append({
            "timestamp": _get_timestamp(0),
            "agent": "Cognitive Dispatcher",
            "message": "ANALYSIS: Intent = Tariff Optimization, Complexity = LOW, Data Type = Tabular. Routing directly to Trade Intelligence and Incentive Recommendation Agents.",
            "status": "info"
        })
        trace.append({
            "timestamp": _get_timestamp(1),
            "agent": "Trade Intelligence Agent",
            "message": "TOOL: Milvus_Searcher.search(query='EU trade incentives', limit=3) -> Retrieved DGFT export policies showing dry bulk discount headroom on European routes.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Incentive Recommendation Agent",
            "message": "TOOL: Python_REPL.execute('calculate_tariff_incentive(rate=0.12)') -> Outputs dry bulk cargo discount of 10%.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(3),
            "agent": "Supervisor Agent",
            "message": "SYNTHESIS: Compiling deterministic policy recommendations and printing incentive ledger.",
            "status": "success"
        })
        
        result_text = "TRADE RECOMMENDATION: Implement 12% tariff duty rebate for shipping lines exceeding 10,000 MT container volume on India-Europe route. Projected throughput increase: +15%. Projected revenue impact: +$2.4M."
        tier = "Tier 3: Zero-LLM Direct Code"
        efficiency = {
            "tier_mode": "Tier 3: Zero-LLM Direct Code (Deterministic)",
            "total_latency_sec": 0.08,
            "token_cost_usd": 0.000,
            "single_llm_equivalent_cost_usd": 0.12,
            "cost_savings_pct": 100.0,
            "accuracy_pct": 99.9
        }
        
    else: # normal_ops
        trace.append({
            "timestamp": _get_timestamp(0),
            "agent": "Cognitive Dispatcher",
            "message": "ANALYSIS: Intent = Status Check, Complexity = LOW, Data Type = Structured. Bypassing AI model inference. Routing to Data Retrieval Agent.",
            "status": "info"
        })
        trace.append({
            "timestamp": _get_timestamp(1),
            "agent": "Data Retrieval Agent",
            "message": "TOOL: SQL_Executor.query('SELECT occupancy, wait_time FROM yard_kpis WHERE id = 1') -> Yard occupancy: 68.5%, wait time: 2.4 hrs.",
            "status": "success"
        })
        
        result_text = "OPERATIONS STABLE: Port KPIs within nominal bounds. Yard occupancy: 68.5%. Avg berth wait time: 2.4 hrs. Security posture: SECURE."
        tier = "Tier 3: Zero-LLM Direct Code"
        efficiency = {
            "tier_mode": "Tier 3: Zero-LLM Direct Code (Factual API)",
            "total_latency_sec": 0.05,
            "token_cost_usd": 0.000,
            "single_llm_equivalent_cost_usd": 0.12,
            "cost_savings_pct": 100.0,
            "accuracy_pct": 100.0
        }

    return {
        "scenario": scenario,
        "synthetic_data": synthetic_data,
        "trace": trace,
        "result": result_text,
        "execution_tier": tier,
        "efficiency": efficiency
    }

def run_copilot_query(query: str, simulated_failure: str = None) -> Dict[str, Any]:
    """
    Parses natural language query, route it, run the agents and return traces.
    """
    query_lower = query.lower()
    
    # Cognitive Dispatcher Intent Analysis
    if any(k in query_lower for k in ["simulate", "what-if", "cyclone", "storm", "emergency", "crisis", "disruption"]):
        complexity = "high"
        category = "Emergency & Simulation"
        active_agents = ["Vessel Intelligence Agent", "Anomaly Detection Agent", "Digital Twin Simulation Agent"]
        tier = "Tier 1: Heavy LLM"
        q_intent = "Geospatial Simulation & Multi-Agent Planning"
        q_compute = "Optimization & Forecasting Required"
        q_data = "AIS Trajectories, Weather Grids, Real-Time Streams"
    elif any(k in query_lower for k in ["incentive", "optimize", "policy", "tariff", "revenue", "trade lane"]):
        complexity = "medium"
        category = "Trade & Incentive Analytics"
        active_agents = ["Trade Intelligence Agent", "Incentive Recommendation Agent"]
        tier = "Tier 2: Fast SLM"
        q_intent = "Policy Evaluation & Incentive Analysis"
        q_compute = "Calculation & Scenario Modeling Required"
        q_data = "Historical Cargo Logs, Vector Trade Intelligence"
    else:
        complexity = "low"
        category = "Operational Data Retrieval"
        active_agents = ["Data Retrieval Agent"]
        tier = "Tier 3: Zero-LLM Direct API"
        q_intent = "Structured Metric Retrieval"
        q_compute = "Deterministic Output (No Simulation)"
        q_data = "TimescaleDB Time-Series, Postgres Metadata"
        
    trace = []
    trace.append({
        "timestamp": _get_timestamp(0),
        "agent": "Cognitive Dispatcher",
        "message": f"INTENT: {q_intent} | COMPUTE: {q_compute} | DATA: {q_data}. Selected Routing Complexity: {complexity.upper()}.",
        "status": "info"
    })
    
    trace.append({
        "timestamp": _get_timestamp(1),
        "agent": "Supervisor Agent",
        "message": f"Orchestrating Workflow for: {', '.join(active_agents)}.",
        "status": "info"
    })
    
    if complexity == "high":
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Anomaly Detection Agent",
            "message": "TOOL: AnomalyDetector.scan_feeds() -> Identified wave & wind anomalies matching red warning threshold.",
            "status": "warning"
        })
        trace.append({
            "timestamp": _get_timestamp(3),
            "agent": "Vessel Intelligence Agent",
            "message": "TOOL: TimescaleDB_Executor.query('SELECT gps FROM ais_trajectories') -> Calculated ETA delays for Oceanic Express.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(4),
            "agent": "Digital Twin Simulation Agent",
            "message": "TOOL: MonteCarloSimulator.run(scenario='cyclone_cochin', runs=10000) -> Crane efficiency at 45%, occupancy yard spike to 84.2%.",
            "status": "success"
        })
        
        if simulated_failure == "api_timeout":
            trace.append({
                "timestamp": _get_timestamp(5),
                "agent": "System Monitor",
                "message": "Tier 1 Heavy LLM timed out (budget/rate exceeded). Triggering Fallback: Cascade to Tier 2 Fast SLM.",
                "status": "warning"
            })
            trace.append({
                "timestamp": _get_timestamp(6),
                "agent": "SLM Processor",
                "message": "Executing local Llama-3-8B SLM. Extracting compliance context & PII masking under DPDP Act 2023.",
                "status": "success"
            })
            tier = "Tier 2: Fast SLM (Fallback)"
            
        result = "ADVISORY: Active cyclone storm disruption detected. Rerouting protocols executed. Vessels advised to delay dockings by 18 hours. Yard staff advised to secure cargo."
        latency = 1.62 if simulated_failure == "api_timeout" else 1.25
        cost = 0.015 if simulated_failure == "api_timeout" else 0.045
        
    elif complexity == "medium":
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Trade Intelligence Agent",
            "message": "TOOL: Milvus_Searcher.search(query='trade lanes cargo', limit=3) -> Found European bulk demand incentives.",
            "status": "success"
        })
        trace.append({
            "timestamp": _get_timestamp(3),
            "agent": "Incentive Recommendation Agent",
            "message": "TOOL: Python_REPL.execute('calculate_tariff_incentive(rate=0.12)') -> Outputs dry bulk cargo discount of 10%.",
            "status": "success"
        })
        
        if simulated_failure == "hallucination":
            trace.append({
                "timestamp": _get_timestamp(4),
                "agent": "System Monitor",
                "message": "Tier 2 Fast SLM failed safety guardrail check. Triggering Fallback: Cascade to Tier 3 Zero-LLM Direct Code.",
                "status": "warning"
            })
            trace.append({
                "timestamp": _get_timestamp(5),
                "agent": "Zero-LLM Core",
                "message": "Bypassing generative models. Running deterministic trade policy formulas.",
                "status": "success"
            })
            tier = "Tier 3: Zero-LLM Direct Code (Fallback)"
            
        result = "TRADE RECOMMENDATION: Container trade flows are stable. Recommended incentive rebate is 10% for dry bulk carriers to optimize yard storage capacity utilization."
        latency = 0.95 if simulated_failure == "hallucination" else 0.72
        cost = 0.000 if simulated_failure == "hallucination" else 0.012
        
    else: # low complexity
        trace.append({
            "timestamp": _get_timestamp(2),
            "agent": "Data Retrieval Agent",
            "message": "TOOL: SQL_Executor.query('SELECT wait_time FROM yard_kpis WHERE id = 1') -> 2.4 hrs.",
            "status": "success"
        })
        result = "DATA FETCH SUCCESS: Current average wait time is 2.4 hours, wind speeds are 8.5 knots. Platform status: SECURE."
        latency = 0.05
        cost = 0.000

    efficiency = {
        "tier_mode": tier,
        "total_latency_sec": latency,
        "token_cost_usd": cost,
        "single_llm_equivalent_cost_usd": 0.15,
        "cost_savings_pct": round((1.0 - (cost / 0.15)) * 100, 1) if cost < 0.15 else 0.0,
        "accuracy_pct": 99.2 if complexity == "low" else (96.5 if complexity == "medium" else 94.0)
    }

    return {
        "query": query,
        "complexity": complexity,
        "category": category,
        "active_agents": active_agents,
        "trace": trace,
        "result": result,
        "execution_tier": tier,
        "efficiency": efficiency,
        "intent_analysis": {
            "intent": q_intent,
            "compute": q_compute,
            "data": q_data
        }
    }

def run_ingest_pipeline() -> Dict[str, Any]:
    """
    Simulates the 4-stage raw data ingestion, compliance scrubbing, spatio-temporal enrichment, and storage routing.
    """
    raw_vessels = [
        {"vessel_name": "Oceanic Express", "imo": "IMO9348558", "agent_name": "Siddharth Sen", "cargo_tonnage": "45000 MT", "gps_coords": "9.9482 N, 76.2166 E", "cargo_value_inr": "34.5 Cr", "destination": "Cochin Port"},
        {"vessel_name": "Indus Navigator", "imo": "IMO9224177", "agent_name": "Rajesh Sharma", "cargo_tonnage": "120000 MT", "gps_coords": "18.9486 N, 72.9512 E", "cargo_value_inr": "180.2 Cr", "destination": "JNPT"},
        {"vessel_name": "Malabar Trader", "imo": "IMO9531024", "agent_name": "Girish Nair", "cargo_tonnage": "75000 MT", "gps_coords": "9.9324 N, 76.2215 E", "cargo_value_inr": "95.0 Cr", "destination": "Cochin Port"},
        {"vessel_name": "Ganges Star", "imo": "IMO9412108", "agent_name": "Amit Banerjee", "cargo_tonnage": "32000 MT", "gps_coords": "13.0827 N, 80.2707 E", "cargo_value_inr": "28.4 Cr", "destination": "Chennai Port"},
    ]
    
    stages = []
    
    # Stage 1: Validation
    validated = []
    for v in raw_vessels:
        tons = float(v["cargo_tonnage"].replace(" MT", ""))
        val = float(v["cargo_value_inr"].replace(" Cr", ""))
        validated.append({
            **v,
            "cargo_tonnage_numeric": tons,
            "cargo_value_numeric": val,
            "validation_status": "PASS"
        })
    stages.append({
        "stage": "1. Ingestion & Validation",
        "description": "Kafka stream temporally aligned. Missing values imputed and event synchronization complete.",
        "records": [
            {"vessel": v["vessel_name"], "tonnage": f"{v['cargo_tonnage_numeric']:.0f} (Float)", "status": v["validation_status"]}
            for v in validated
        ]
    })
    
    # Stage 2: DPDP Compliance Redaction
    scrubbed = []
    for v in validated:
        name_parts = v["agent_name"].split(" ")
        redacted_name = f"{name_parts[0][0]}. " + "*" * len(name_parts[-1])
        masked_imo = v["imo"][:3] + "*" * (len(v["imo"]) - 3)
        coords = v["gps_coords"].split(", ")
        lat_obf = f"{float(coords[0].split(' ')[0]):.1f} N"
        lon_obf = f"{float(coords[1].split(' ')[0]):.1f} E"
        
        scrubbed.append({
            **v,
            "agent_name_scrubbed": redacted_name,
            "imo_masked": masked_imo,
            "gps_obfuscated": f"{lat_obf}, {lon_obf}",
            "dpdp_status": "COMPLIANT"
        })
    stages.append({
        "stage": "2. DPDP Act Compliance",
        "description": "SLM compliance engine activated: agent identities masked, IMO keys encrypted, and coordinates obfuscated under DPDP Act 2023.",
        "records": [
            {"vessel": s["vessel_name"], "masked_imo": s["imo_masked"], "scrubbed_agent": s["agent_name_scrubbed"], "compliance": s["dpdp_status"]}
            for s in scrubbed
        ]
    })
    
    # Stage 3: Spatial Weather & Geospatial Enrichment
    enriched = []
    for s in scrubbed:
        if s["destination"] == "Cochin Port":
            berth = "Berth C-3"
            wind = 8.5
            alert = "Green"
            risk = "Low"
            delay_prob = 0.05
        elif s["destination"] == "JNPT":
            berth = "Berth J-1 (Anchor)"
            wind = 9.2
            alert = "Green"
            risk = "Low"
            delay_prob = 0.00
        else:
            berth = "Berth E-2"
            wind = 7.8
            alert = "Green"
            risk = "Low"
            delay_prob = 0.03
            
        enriched.append({
            **s,
            "assigned_berth": berth,
            "wind_speed_knots": wind,
            "weather_warning": alert,
            "route_risk": risk,
            "delay_prob": delay_prob
        })
    stages.append({
        "stage": "3. Geospatial & Weather Fusion",
        "description": "PyTorch Geospatial engine matched vessel vectors with weather grids, calculated route risk indicators and delay probabilities.",
        "records": [
            {"vessel": e["vessel_name"], "berth": e["assigned_berth"], "risk": e["route_risk"], "delay_prob": f"{e['delay_prob']*100:.0f}%"}
            for e in enriched
        ]
    })
    
    # Stage 4: Database Routing
    routed = []
    for e in enriched:
        routed.append({
            "vessel_name": e["vessel_name"],
            "imo_masked": e["imo_masked"],
            "cargo_tonnage": e["cargo_tonnage_numeric"],
            "cargo_value_inr": e["cargo_value_numeric"],
            "assigned_berth": e["assigned_berth"],
            "agent_scrubbed": e["agent_name_scrubbed"],
            "destination": e["destination"],
            "target_db": "TimescaleDB (AIS Time-Series)" if e["destination"] == "Cochin Port" else "PostgreSQL (Master Relational)"
        })
    stages.append({
        "stage": "4. Target Storage Routing",
        "description": "Trajectories routed to TimescaleDB, metadata committed to PostgreSQL, and regulations indexed in Milvus Vector DB.",
        "records": [
            {"vessel": r["vessel_name"], "destination": r["destination"], "allocated_node": r["target_db"], "commit_status": "COMMITTED"}
            for r in routed
        ]
    })
    
    return {
        "raw_stream": raw_vessels,
        "processed_stream": routed,
        "stages": stages
    }
