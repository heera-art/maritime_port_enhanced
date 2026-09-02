"""
security.py — Maritime Platform Security Intelligence Layer
------------------------------------------------------------
Lightweight simulation of enterprise cybersecurity features.
No real encryption, no auth, no databases — demo-grade only.

Functions:
  log_event()               — append an audit event to a JSON log file
  classify_dataset()        — assign a data classification label to a filename
  generate_threat_alerts()  — return a list of simulated threat detections
  get_system_status()       — return secure-processing indicator badges
  get_collaboration_status()— return inter-agency collaboration metadata
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Audit log file lives next to this file for simplicity ──────────
_LOG_FILE = Path(__file__).resolve().parent / "audit_log.json"

# ── Deterministic seed so threat alerts are stable across refreshes ─
random.seed(2024)


# ═══════════════════════════════════════════════════════════════════
# 1. AUDIT LOGGING
# ═══════════════════════════════════════════════════════════════════

def log_event(action: str, module: str, status: str = "success",
              detail: str = "") -> dict[str, Any]:
    """
    Append one audit event to audit_log.json and return it.

    Args:
        action  : what happened, e.g. "csv_upload", "forecast_request"
        module  : which part of the system, e.g. "upload", "forecasting"
        status  : "success" | "warning" | "error"
        detail  : optional free-text context

    Storage:
        Reads the existing list from audit_log.json (creates it if missing),
        appends the new event, writes back.
        Capped at 200 entries to keep the file small.
    """
    event: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action":    action,
        "module":    module,
        "status":    status,
        "detail":    detail,
    }

    # Load existing log or start fresh
    logs: list[dict] = []
    if _LOG_FILE.exists():
        try:
            logs = json.loads(_LOG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            logs = []

    logs.append(event)
    logs = logs[-200:]  # keep only the most recent 200 entries

    try:
        _LOG_FILE.write_text(json.dumps(logs, indent=2))
    except OSError:
        pass  # silently skip write failures in read-only environments

    return event


def get_audit_logs(limit: int = 50) -> list[dict]:
    """
    Return the most recent `limit` audit events from the log file.
    Returns an empty list if the file does not exist yet.
    """
    if not _LOG_FILE.exists():
        return []
    try:
        logs = json.loads(_LOG_FILE.read_text())
        return list(reversed(logs[-limit:]))  # newest first
    except (json.JSONDecodeError, OSError):
        return []


# ═══════════════════════════════════════════════════════════════════
# 2. DATA CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════

# Classification rules: keywords in the filename drive the label.
# In a real system this would inspect file contents or metadata.
_CLASSIFICATION_RULES: list[tuple[list[str], str]] = [
    (["secret", "classified", "restricted", "sensitive"], "Confidential"),
    (["trade", "customs", "dgft", "export", "import"],    "Restricted"),
    (["port", "vessel", "cargo", "congestion", "berth"],  "Internal"),
]

_CLASSIFICATION_COLORS = {
    "Confidential": "#e53e3e",   # red
    "Restricted":   "#D4A017",   # amber
    "Internal":     "#2b6cb0",   # blue
    "Public":       "#2f855a",   # green
}

_CLASSIFICATION_ICONS = {
    "Confidential": "",
    "Restricted":   "",
    "Internal":     "",
    "Public":       "",
}


def classify_dataset(filename: str) -> dict[str, str]:
    """
    Assign a data classification label to a CSV filename.

    Logic:
      - Scan filename (lowercased) against keyword lists in priority order
      - First match wins; default is "Public" if no keywords match

    Returns a dict with label, color, icon, and a short description.
    """
    name_lower = filename.lower()

    label = "Public"  # default
    for keywords, classification in _CLASSIFICATION_RULES:
        if any(kw in name_lower for kw in keywords):
            label = classification
            break

    descriptions = {
        "Confidential": "Highly sensitive — access restricted to authorised personnel only.",
        "Restricted":   "Sensitive trade/customs data — inter-agency sharing requires approval.",
        "Internal":     "Operational port data — internal use within maritime authority.",
        "Public":       "Non-sensitive dataset — cleared for public reporting.",
    }

    return {
        "label":       label,
        "color":       _CLASSIFICATION_COLORS[label],
        "icon":        _CLASSIFICATION_ICONS[label],
        "description": descriptions[label],
    }


# ═══════════════════════════════════════════════════════════════════
# 3. THREAT ALERT SIMULATION
# ═══════════════════════════════════════════════════════════════════

# Static pool of realistic maritime cybersecurity threat scenarios.
# Randomised selection keeps the panel feeling "live" across sessions.
_THREAT_POOL: list[dict] = [
    {
        "severity": "critical",
        "category": "Cargo Anomaly",
        "title":    "Unusual cargo volume spike detected",
        "detail":   "Cargo intake at JNPT exceeded 3σ above 30-day baseline. "
                    "Possible data integrity issue or unreported bulk shipment.",
        "source":   "Cargo Forecasting Engine",
        "mitre":    "T1565 — Data Manipulation",
    },
    {
        "severity": "high",
        "category": "API Anomaly",
        "title":    "Anomalous API request frequency",
        "detail":   "Forecast endpoint received 47 requests in 60 seconds from "
                    "a single session. Rate-limiting advisory triggered.",
        "source":   "API Gateway Monitor",
        "mitre":    "T1499 — Endpoint Denial of Service",
    },
    {
        "severity": "high",
        "category": "Upload Anomaly",
        "title":    "Repeated CSV upload attempts detected",
        "detail":   "Same filename uploaded 4 times within 10 minutes. "
                    "Possible automated injection attempt or client error.",
        "source":   "Upload Pipeline",
        "mitre":    "T1190 — Exploit Public-Facing Application",
    },
    {
        "severity": "medium",
        "category": "Congestion Anomaly",
        "title":    "Congestion pattern deviates from historical norm",
        "detail":   "Port congestion score at Kandla is 2.1σ above weekly average. "
                    "Cross-referencing with vessel AIS data recommended.",
        "source":   "Congestion Intelligence Engine",
        "mitre":    "T1040 — Network Sniffing (data exfil risk)",
    },
    {
        "severity": "medium",
        "category": "Data Integrity",
        "title":    "Dataset schema mismatch on ingestion",
        "detail":   "Uploaded file 'vessel_movements_may.csv' contains 3 columns "
                    "not present in the registered schema. Flagged for review.",
        "source":   "Data Classification Layer",
        "mitre":    "T1565.001 — Stored Data Manipulation",
    },
    {
        "severity": "low",
        "category": "Access Pattern",
        "title":    "Off-hours dashboard access logged",
        "detail":   "Dashboard accessed at 02:34 IST — outside normal operational "
                    "hours. Logged for compliance audit trail.",
        "source":   "Audit Logger",
        "mitre":    "T1078 — Valid Accounts",
    },
    {
        "severity": "low",
        "category": "Compliance",
        "title":    "DPDP data retention window approaching",
        "detail":   "3 datasets uploaded >90 days ago. Review retention policy "
                    "under DPDP Act 2023 Section 8(7).",
        "source":   "Compliance Monitor",
        "mitre":    "Regulatory — DPDP Act 2023",
    },
]

_SEVERITY_COLORS = {
    "critical": "#e53e3e",
    "high":     "#D4A017",
    "medium":   "#2b6cb0",
    "low":      "#2f855a",
}

_SEVERITY_ICONS = {
    "critical": "",
    "high":     "",
    "medium":   "",
    "low":      "",
}


def generate_threat_alerts(count: int = 5) -> list[dict[str, Any]]:
    """
    Return `count` threat alerts sampled from the pool.

    Each alert gets:
      - a relative timestamp (most recent first, spaced ~15 min apart)
      - colour and icon for UI rendering
      - a unique alert_id for keying

    The random seed is fixed so the same alerts appear on every page
    load — important for demo stability.
    """
    rng = random.Random(2024)  # local seeded RNG, doesn't affect global state
    selected = rng.sample(_THREAT_POOL, min(count, len(_THREAT_POOL)))

    now = datetime.now(timezone.utc)
    alerts = []
    for i, alert in enumerate(selected):
        ts = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
        # Offset each alert backwards in time for realism
        offset_minutes = i * 15 + rng.randint(2, 12)
        from datetime import timedelta
        alert_time = now - timedelta(minutes=offset_minutes)

        alerts.append({
            **alert,
            "alert_id":  f"THR-{2024 + i:04d}",
            "timestamp": alert_time.strftime("%H:%M"),
            "color":     _SEVERITY_COLORS.get(alert["severity"], "#718096"),
            "icon":      _SEVERITY_ICONS.get(alert["severity"], ""),
        })

    return alerts


# ═══════════════════════════════════════════════════════════════════
# 4. SYSTEM SECURITY STATUS
# ═══════════════════════════════════════════════════════════════════

def get_system_status() -> dict[str, Any]:
    """
    Return secure-processing indicator badges for the dashboard.

    These are UI simulation indicators — they communicate the
    security posture of the platform to demo audiences without
    requiring real cryptographic infrastructure.

    Each indicator has:
      - label   : display name
      - status  : "active" | "standby" | "pending"
      - icon    : emoji for quick visual scanning
      - color   : hex for badge background tinting
      - detail  : one-line explanation for tooltips
    """
    return {
        "platform":   "YellowSense Maritime Intelligence v0.1.0",
        "assessed_at": datetime.now(timezone.utc).isoformat(),
        "overall_posture": "SECURE",
        "indicators": [
            {
                "label":  "AES-256 Data Protection",
                "status": "active",
                "icon":   "",
                "color":  "#2f855a",
                "detail": "All datasets encrypted at rest using AES-256-GCM.",
            },
            {
                "label":  "Secure Processing Active",
                "status": "active",
                "icon":   "",
                "color":  "#2f855a",
                "detail": "Forecasting pipelines run in isolated compute context.",
            },
            {
                "label":  "DPDP-Compliant Processing",
                "status": "active",
                "icon":   "",
                "color":  "#2b6cb0",
                "detail": "Data handling aligned with DPDP Act 2023 obligations.",
            },
            {
                "label":  "Confidential Compute Ready",
                "status": "standby",
                "icon":   "",
                "color":  "#D4A017",
                "detail": "TEE-based processing available on demand.",
            },
            {
                "label":  "Audit Trail Enabled",
                "status": "active",
                "icon":   "",
                "color":  "#2f855a",
                "detail": "All API calls and uploads logged with tamper-evident timestamps.",
            },
            {
                "label":  "TLS 1.3 In Transit",
                "status": "active",
                "icon":   "",
                "color":  "#2f855a",
                "detail": "All inter-service communication encrypted via TLS 1.3.",
            },
        ],
    }


# ═══════════════════════════════════════════════════════════════════
# 5. COLLABORATION STATUS
# ═══════════════════════════════════════════════════════════════════

def get_collaboration_status() -> dict[str, Any]:
    """
    Return inter-agency collaboration metadata.

    Simulates a secure data-sharing fabric between maritime
    government agencies. Each agency entry includes:
      - name        : agency display name
      - short_name  : abbreviation for compact UI
      - role        : what data they contribute or consume
      - status      : "connected" | "pending" | "offline"
      - data_shared : types of data in the sharing agreement
      - clearance   : minimum classification level they can access
      - icon        : emoji for visual identity
    """
    return {
        "fabric":      "Maritime Secure Data Exchange (MSDE)",
        "protocol":    "Simulated TLS-Mutual-Auth + RBAC",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agencies": [
            {
                "name":        "Port Authority of India",
                "short_name":  "PAI",
                "role":        "Primary data provider — vessel movements, berth allocation",
                "status":      "connected",
                "data_shared": ["Vessel AIS", "Berth Logs", "Cargo Manifests"],
                "clearance":   "Internal",
                "icon":        "",
                "color":       "#2f855a",
            },
            {
                "name":        "Central Board of Indirect Taxes & Customs",
                "short_name":  "CBIC / Customs",
                "role":        "Trade compliance — import/export declarations",
                "status":      "connected",
                "data_shared": ["Bill of Lading", "Customs Declarations", "HS Codes"],
                "clearance":   "Restricted",
                "icon":        "",
                "color":       "#2f855a",
            },
            {
                "name":        "Directorate General of Foreign Trade",
                "short_name":  "DGFT",
                "role":        "Export licensing and trade policy intelligence",
                "status":      "pending",
                "data_shared": ["Export Licences", "Trade Policy Alerts"],
                "clearance":   "Restricted",
                "icon":        "",
                "color":       "#D4A017",
            },
            {
                "name":        "Maritime Intelligence Unit",
                "short_name":  "MIU",
                "role":        "Threat intelligence — anomaly and risk signals",
                "status":      "connected",
                "data_shared": ["Threat Feeds", "Vessel Risk Scores", "Sanctions Lists"],
                "clearance":   "Confidential",
                "icon":        "",
                "color":       "#2b6cb0",
            },
        ],
    }
