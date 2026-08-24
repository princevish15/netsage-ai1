# 🌐 NetSage AI: Automated Network Diagnostic Platform

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **NetSage AI** is a hybrid diagnostic and remediation intelligence platform engineered for enterprise Cisco networks and Cisco Packet Tracer lab environments. By pairing high-precision deterministic pattern matching with structured multi-layer semantic reasoning, NetSage AI rapidly isolates root causes across OSI Layers 2 through 7 and provides Human-in-the-Loop (HITL) approved remediation commands.

---

## 🚀 Key Features of NetSage AI & `cases.csv`

1. **Multi-Layer OSI Diagnostic Coverage (Layers 2 to 7)**:
   - Evaluates 30 structured enterprise scenarios including VLAN trunking, OSPF timer mismatches, DHCP exhaustion, NAT overload issues, ACL blockages, DAI/Port Security violations, and IPv6 SLAAC errors.

2. **Granular Telemetry & Evidence-Based Show Command Capture**:
   - Analyzes real Cisco IOS CLI outputs (`show ip interface brief`, `show access-lists`, `show running-config`), isolates verbatim evidence, and assesses fault severity (Critical, High, Medium, Low).

3. **Deterministic Validation with Human-in-the-Loop (HITL) Gate**:
   - Integrates rule verification (`checker.py`) with an operations dashboard (`app.py`), enabling engineers to inspect diagnoses, edit proposed CLI commands, and approve/reject before deployment while logging audit trails (`76.6%` agreement rate).

---

## 🏗️ Solution Architecture

```
NetSage AI 4-Tier Architecture:
┌───────────────────────────────────────────────┐
│                   DATA TIER                   │
│   • data/cases.csv (30 test scenarios)        │
│   • system_config.json (Thresholds & params)  │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│            DIAGNOSTIC CORE ENGINE             │
│   • src/checker.py (Deterministic regex rule) │
│   • src/engine.py (Diagnostic orchestrator)   │
│   • prompts/diagnose_prompt.md (System prompt)│
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│          HUMAN-IN-THE-LOOP (HITL) GATE        │
│   • Streamlit Dashboard (app.py)              │
│   • Actions: Approve / Edit / Reject          │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│               AUDIT & LOGGING                 │
│   • docs/model_audit_log.md                   │
└───────────────────────────────────────────────┘
```

---

## 📦 Project Structure

```
netsage_ai/
│
├── data/
│   └── cases.csv                # 30 Cisco Packet Tracer test scenarios
├── prompts/
│   └── diagnose_prompt.md       # Diagnostic prompt & JSON schema
├── src/
│   ├── __init__.py
│   ├── checker.py               # Deterministic rule verification engine
│   ├── engine.py                # Diagnostic orchestrator
│   └── app.py                   # Streamlit app mirror
├── docs/
│   └── model_audit_log.md       # Agreement benchmark & audit records
├── app.py                       # Main Streamlit Operations Dashboard
├── system_config.json           # Platform settings & thresholds
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # System documentation
```

---

## ⚡ Quick Start & Installation

### 1. Clone or Extract the Repository
```bash
git clone https://github.com/your-username/netsage_ai.git
cd netsage_ai
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud & GitHub

1. Initialize git and commit files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NetSage AI platform"
   ```
2. Push to your GitHub repository:
   ```bash
   git remote add origin https://github.com/<your-username>/netsage_ai.git
   git branch -M main
   git push -u origin main
   ```
3. Connect your repository to [share.streamlit.io](https://share.streamlit.io/) with `app.py` as the entry point!
