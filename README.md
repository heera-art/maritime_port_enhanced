# 🚢 Maritime Port Intelligence Platform (MPIP)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An AI-powered, full-stack maritime intelligence platform designed to deliver cargo forecasting, port congestion predictions, import/export trade analytics, and automated operational recommendations. The platform features an integrated **Security Operations Center (SOC)** to monitor cyber threats mapped to the MITRE ATT&CK framework, compliance checks aligned with the Indian DPDP Act 2023, and a secure multi-agency data collaboration simulation.

---

## 🌟 Executive Summary

The Maritime Port Intelligence Platform (MPIP) acts as a centralized command center for port authorities, customs agencies, shipping lines, and maritime security operators. By bridging operational analytics and domain cybersecurity, MPIP converts fragmented datasets into secure, actionable decision points, aligning with global smart-port initiatives and national programs like India's *Sagarmala* and *Maritime India Vision 2030*.

---

## ⚙️ Core Modules & Features

The platform is structured around an **8-Module Core Framework** integrated into a single high-performance dashboard:

### 1. Vessel Intelligence
- **Deep Visibility:** Track real-time and historical vessel arrivals, flag distributions, and carrier fleet utilization.
- **Vessel Profile Auditing:** Monitor registration details, vessel types, and flag-state security histories.

### 2. Cargo Forecasting
- **Time-Series Predictive Forecasting:** 7-day predictive forecasting of bulk, container, and liquid cargo volumes.
- **Confidence Intervals:** Lower and upper forecast bounds with a color-coded confidence rating.
- **Market Signals:** Instant trend categorization (e.g., Bullish, Bearish, Neutral) using EMA smoothing.

### 3. Port Congestion Analytics
- **Congestion Index Scoring:** Real-time port risk tracking scored out of 100.
- **Risk Metrics:** Out-of-bounds anomaly warnings computed using rolling Z-Score analyses.
- **Congestion Outlook:** A 24-hour forecast of turnaround times, queue delays, and berth occupancy.

### 4. Trade Intelligence
- **Import/Export Trade Flows:** Analyze commodity-wise trade lanes and cargo values.
- **Momentum Gauges:** Calculate trade lane velocity using Exponential Moving Averages (EMA) to identify rising trade lanes.

### 5. Incentive Engine
- **Revenue Protection:** Automatically flag policy leakages, under-invoicing, and tariff-evasion anomalies.
- **Incentive Simulator:** Model trade incentives (e.g., rebate policies, volume discounts) to optimize tariff frameworks.

### 6. Digital Twin Simulation
- **Port Operations Modeler:** Simulate weather disruptions, labor strikes, and machinery downtime.
- **Stress-Test Scenarios:** Model how bottlenecks propagate through container yards and gates to test port resilience.

### 7. AI Copilot
- **Conversational Intelligence:** Ask natural language questions regarding port performance, vessel status, or cybersecurity metrics.
- **Instant Query Compilation:** Generates structured parameters, mock API payloads, and query responses directly from backend databases.

### 8. Executive Dashboard
- **Operational Health Index (OHI):** A single unified gauge of overall port efficiency, combining vessel throughput, security flags, and queue status.
- **Multi-Agency View:** A secure visualization console simulating shared indicators across custom agencies, port authorities, and naval security commands.

---

## 🛡️ Security, Governance & DPDP Compliance

MPIP places paramount importance on cybersecurity and data privacy, integrating military-grade governance directly into operational reports.

- **MITRE ATT&CK Threat Mapping:** SOC console categorizes cybersecurity alerts (such as database port scanning, spoofed AIS coordinates, or API brute-forcing) directly to MITRE tactics and techniques.
- **Indian DPDP Act 2023 Compliance:** Automated compliance gauges audit data ingestion pipelines, checking consent records, purpose limitations, and cross-border transfer parameters.
- **Four-Tier Data Classification:** All API data feeds are tagged according to sensitivity: *Public*, *Internal*, *Restricted*, or *Highly Sensitive*.
- **Tamper-Evident Audit Logging:** Cryptographically simulated, time-stamped JSON logs tracking all user access, data uploads, and configuration changes.

---

## 🏗️ Technical Architecture & Data Flow

```text
  ┌──────────────────────────────────────────────────────────┐
  │                   User Browser Client                    │
  └─────────────────────────────┬────────────────────────────┘
                                │
                      HTTP / WS │ Port 8501
                                ▼
  ┌──────────────────────────────────────────────────────────┐
  │               Streamlit Dashboard Server                 │
  │   - UI State Management                                  │
  │   - Plotly Graphic Rendering                             │
  │   - Session Configurations (.streamlit/config.toml)       │
  └─────────────────────────────┬────────────────────────────┘
                                │
           JSON REST Requests   │ Port 8000 (Env: BACKEND_URL)
                                ▼
  ┌──────────────────────────────────────────────────────────┐
  │                 FastAPI Backend Service                  │
  │   - Route Dispatcher (main.py)                           │
  │   - Module-Specific Controllers (routes/)                │
  │   - Pydantic Ingestion Models                            │
  └─────────────┬──────────────────────────────┬─────────────┘
                │                              │
                ▼                              ▼
  ┌───────────────────────────┐  ┌───────────────────────────┐
  │    Data Engine Services   │  │   Security & Audit Logs   │
  │   - NumPy / Pandas Models │  │  - MITRE ATT&CK Mappers   │
  │   - Forecasting Logic     │  │  - DPDP Compliance Check  │
  │   - Digital Twin Engines  │  │  - Cryptographic Logs     │
  └───────────────────────────┘  └───────────────────────────┘
```

---

## 📂 Directory Layout

```text
maritime-port-intelligence-platform/
├── assets/                  # Graphics, logos, and system architecture diagrams
├── backend/                 # FastAPI service layer
│   └── app/
│       ├── routes/          # API routing modules (vessels, trade, SOC, etc.)
│       ├── services/        # Analytical calculations, audit trails, and mock engines
│       └── main.py          # FastAPI application entry point
├── data/                    # Sample data sets
│   └── sample_cargo_data.csv
├── frontend/                # Streamlit service layer
│   ├── .streamlit/          # Streamlit UI configuration
│   └── app.py               # Streamlit dashboard entry point
├── uploads/                 # Temporary directory for uploaded CSV files
├── Dockerfile.backend       # Docker build file for FastAPI app
├── Dockerfile.frontend      # Docker build file for Streamlit dashboard
├── docker-compose.yml       # Production-ready orchestration configuration
├── .env.example             # Template file for environment configurations
├── .gitignore               # Excludes virtual environments and file caches
├── requirements.txt         # Global Python package dependencies
├── LICENSE                  # MIT License details
└── README.md                # Platform documentation (this file)
```

---

## 🚀 Quick Start & Deployment Guide

### Option 1: Multi-Container Run with Docker Compose (Recommended)

Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Vicky-cmd-run/maritime_port.git
   cd maritime_port
   ```

2. **Boot the Containers:**
   Launch the microservices in detached mode:
   ```bash
   docker-compose up --build -d
   ```

3. **Access Services:**
   - **Interactive Frontend:** Open [http://localhost:8501](http://localhost:8501)
   - **FastAPI Backend Root:** Open [http://localhost:8000](http://localhost:8000)
   - **Interactive API Swagger Docs:** Open [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Shutdown Services:**
   ```bash
   docker-compose down
   ```

---

### Option 2: Local Installation (For Development)

Ensure you have Python 3.10+ installed.

#### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Run FastAPI Backend
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- The backend API will be available at `http://127.0.0.1:8000`
- Interactive API Docs will be available at `http://127.0.0.1:8000/docs`

#### 4. Run Streamlit Frontend
Open a new terminal session, activate the virtual environment, and run:
```bash
streamlit run frontend/app.py
```
- The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📡 API Directory & Endpoint Documentation

The backend service hosts fully documented REST endpoints:

### System & Utilities
* `GET /` - Root status check and module inventory count.
* `GET /health` - Liveness/readiness check for container orchestration.
* `POST /upload/` - Accepts custom multipart CSV reports. Validates structure, size, and records to the storage directory.

### Analytics & Forecasters
* `GET /vessels/live` - Current active vessel logs, flagged anomalies, and fleet allocations.
* `GET /cargo/forecast` - 7-day predicted container, bulk, and liquid cargo volumes.
* `GET /congestion/risk` - Current congestion indices, average delays, and rolling Z-score parameters.
* `GET /trade/flows` - Real-time metrics for commodity trades, values, and EMA momentum calculations.
* `GET /incentive/leakages` - Flagged policy leaks, under-invoicing anomalies, and recommended discount factors.
* `GET /twin/simulations` - Stress-test results, simulation logs, and efficiency indicators.
* `GET /executive/status` - Aggregates port statistics into the unified Port Operational Health Index.

### Security Operations Center (SOC)
* `GET /security/threat-alerts` - Security logs mapped directly to MITRE ATT&CK tactics (Credential Access, Defense Evasion, etc.).
* `GET /security/classifications` - Audits API feeds against the 4-tier data classification model.
* `GET /security/audit-logs` - Displays cryptographic, tamper-evident user action logs.
* `GET /security/collaboration-status` - Simulates state-level sharing metrics across multiple security divisions.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✍️ Authors & Contributions
- **Dweep Solanki** - *Creator & Cybersecurity Professional*