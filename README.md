# 🛡️ SafeRoute AI — Intelligent Walking Navigation

> An AI-powered navigation system that calculates and compares the **Safest Walking Route** vs the **Shortest Route** in Tiruchirappalli (Trichy), Tamil Nadu, India, using **A\* Graph Search** and **Machine Learning Risk Assessment**.

---

## 📑 Table of Contents
1. [Reverse Engineering Analysis](#-reverse-engineering-analysis)
   - [System Architecture](#system-architecture)
   - [Core Components & Data Flow](#core-components--data-flow)
   - [Machine Learning & Risk Model](#machine-learning--risk-model)
   - [Pathfinding & Routing Algorithm](#pathfinding--routing-algorithm)
   - [Project Directory Structure](#project-directory-structure)
2. [Step-by-Step: How to Run Locally on PC (Zero Errors)](#-step-by-step-how-to-run-locally-on-pc)
   - [Prerequisites](#prerequisites)
   - [Method 1: 1-Click Instant Launch (Windows)](#method-1-1-click-instant-launch-windows)
   - [Method 2: Step-by-Step Manual Setup](#method-2-step-by-step-manual-setup)
3. [How to Use the Application](#-how-to-use-the-application)
4. [API Reference](#-api-reference)
5. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🔍 Reverse Engineering Analysis

### System Architecture
The application is structured as a decoupled full-stack architecture with a **FastAPI** backend and a responsive **Leaflet.js** dark-mode web interface.

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Browser                         │
│  Leaflet.js + CartoDB Dark Tiles + Live ETA/Risk Comparison │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP POST /predict (lat, lon)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                         │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │   risk_service.py     │       │   route_service.py    │  │
│  │  (Scikit-Learn ML)    │       │  (OSMnx + NetworkX)   │  │
│  │   Random Forest       │       │    A* Graph Search    │  │
│  └───────────┬───────────┘       └───────────┬───────────┘  │
└──────────────┼───────────────────────────────┼──────────────┘
               │                               │
               ▼                               ▼
       [risk_model.pkl]             [trichy_graph.graphml]
     (Trained on 3,000 data        (9,970 OSM Road Nodes,
      points: lighting, time,       27,098 Walkable Edges)
      crowd, crime, weather)
```

---

### Core Components & Data Flow

1. **User Interaction**:
   - The user opens the web map centered on Tiruchirappalli (`10.7905, 78.7047`).
   - Click 1 places green waypoint marker **A** (Start).
   - Click 2 places purple waypoint marker **B** (Destination).

2. **Backend Processing (`/predict`)**:
   - The coordinates `[start_lat, start_lon]` and `[end_lat, end_lon]` are dispatched to `POST /predict`.
   - The backend uses `ox.distance.nearest_nodes` to snap GPS coordinates to the nearest nodes on the pedestrian road network graph.
   - **Shortest Route**: Runs NetworkX A\* search using raw edge length (meters) as the cost function:
     $$\text{Cost}_{\text{short}} = \text{length}$$
   - **Safest Route**: Runs NetworkX A\* search using a heavily safety-weighted cost function:
     $$\text{Cost}_{\text{safe}} = \text{length} + (\text{risk\_score} \times 250)$$
   - The path analysis helper computes total length in kilometers, average safety risk percentage, safety classification (`SAFE`, `MODERATE`, or `HIGH RISK`), and estimated walking time (based on 5 km/h walking speed).

3. **Frontend Rendering**:
   - Solid Green Line: **🛡️ Safest Route** (avoids high-crime, low-lighting, or deserted segments).
   - Dashed Purple Line: **⚡ Shortest Route** (direct Euclidean/road shortest distance).
   - Right statistics panel renders ETA, safety score bar, and route recommendation.

---

### Machine Learning & Risk Model

| File | Purpose |
| :--- | :--- |
| `dataset.py` | Generates a 3,000-sample synthetic dataset (`safe_route_data.csv`) simulating environmental risk in Tamil Nadu based on: `time` (hour 0-23), `lighting` (0-1), `crowd` (0-1), `crime` (0-1), `weather` (0-1). |
| `ML-file.py` | Uses `RandomForestClassifier(n_estimators=100, random_state=0)` to predict safety risk probabilities (`model.predict_proba`). Exports `risk_model.pkl`. |
| `services/risk_service.py` | Loads `risk_model.pkl` and evaluates road segment safety. Optimized with LRU caching to execute model inference in milliseconds during A\* search. |

---

### Pathfinding & Routing Algorithm
- **Library**: `osmnx` (OpenStreetMap pedestrian network) and `networkx`.
- **Graph Cache**: Graph is pre-downloaded and stored as `trichy_graph.graphml` (10.8 MB, 9,970 nodes, 27,098 edges) for instantaneous offline loading without API rate limits or connection timeouts.
- **Snapping**: Snaps clicks to nearest walkable intersections.

---

### Project Directory Structure

```
ROUTE FINDER/
├── frontend/
│   ├── index.html           # Modern dark-mode map UI
│   ├── style.css            # Responsive layout & custom styling
│   └── app.js               # Leaflet map logic & backend API integration
├── services/
│   ├── risk_service.py      # ML risk prediction & LRU cache
│   └── route_service.py     # OSMnx graph loader & A* pathfinding
├── schemas/
│   └── request_models.py    # Pydantic schema for RouteRequest
├── cache/                   # OSMnx query response cache
├── dataset.py               # Dataset generation script
├── ML-file.py               # Model training script
├── main.py                  # FastAPI application entry point
├── trichy_graph.graphml     # Pre-built pedestrian road graph for Trichy
├── risk_model.pkl           # Trained Random Forest classifier
├── safe_route_data.csv      # 3,000-row training dataset
├── requirements.txt         # Clean Python package dependencies
├── run.bat                  # 1-click Windows launcher
└── README.md                # Documentation & setup guide
```

---

## 🚀 Step-by-Step: How to Run Locally on PC

### Prerequisites
- **Operating System**: Windows 10/11 (or macOS / Linux)
- **Python**: Version 3.10, 3.11, 3.12, 3.13, or 3.14 installed.
  - *Tip: Download from [python.org](https://www.python.org/downloads/) and ensure **"Add python.exe to PATH"** is checked!*

---

### Method 1: 1-Click Instant Launch (Windows)

1. Open the project folder `ROUTE FINDER`.
2. Double-click the file named:
   ```cmd
   run.bat
   ```
3. The script will automatically:
   - Check your Python installation.
   - Install all required libraries (`fastapi`, `uvicorn`, `osmnx`, `scikit-learn`, etc.).
   - Launch the FastAPI server.
   - Automatically open **`http://127.0.0.1:8000`** in your default web browser!

---

### Method 2: Step-by-Step Manual Setup

If you prefer using the terminal or PowerShell, follow these simple steps:

#### Step 1: Open Terminal in Project Folder
Open PowerShell or Command Prompt in the project folder:
```powershell
cd "c:\projects\ROUTE FINDER"
```

#### Step 2: (Recommended) Create & Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# (Or Activate on Windows Command Prompt / CMD)
venv\Scripts\activate.bat
```

#### Step 3: Install Required Dependencies
Install the required packages using the provided clean UTF-8 `requirements.txt`:
```powershell
pip install -r requirements.txt
```

#### Step 4: Start the SafeRoute AI Server
Run the FastAPI backend using Uvicorn:
```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

You will see:
```
[Startup] Pre-loading road network graph...
[route_service] Loading graph from disk cache: trichy_graph.graphml...
[route_service] Graph ready: 9970 nodes, 27098 edges
[Startup] SafeRoute AI Backend is ready!
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

#### Step 5: Open the Application in Your Browser
Open your favorite browser (Chrome, Edge, Firefox, Brave) and navigate to:
```
http://127.0.0.1:8000
```
*(The status indicator on the top left will illuminate green: `● Local Backend (127.0.0.1:8000)`)*

---

## 🗺️ How to Use the Application

1. **Set Start Point (A)**:
   - Click anywhere on the map within Tiruchirappalli. A green marker labelled **A** will be dropped.
2. **Set Destination Point (B)**:
   - Click a second location on the map. A purple marker labelled **B** will be dropped.
3. **Analyze Routes**:
   - The application automatically calls `/predict` and renders:
     - 🟢 **Solid Green Route**: Recommended Safest Path.
     - 🟣 **Dashed Purple Route**: Fastest / Shortest Path.
   - Check the **Right Sidebar** to see the comparison:
     - Distance difference (in km)
     - Estimated Time of Arrival (ETA)
     - Safety Score & Risk Percentage
     - Recommendation summary (e.g., *"Take the green route — it's 18.5% safer, adding only 0.2 km."*)
4. **Reset**:
   - Click the **Reset** button in the top right to clear the waypoints and plan a new route.

---

## 📡 API Reference

### Health Check
- **URL**: `GET /health`
- **Response**: `{"status": "ok"}`

### Route Prediction
- **URL**: `POST /predict`
- **Request Body**:
```json
{
  "start_lat": 10.7905,
  "start_lon": 78.7047,
  "end_lat": 10.8000,
  "end_lon": 78.6900
}
```
- **Response Example**:
```json
{
  "safe_route": {
    "coords": [[10.7905, 78.7047], [10.7910, 78.7035], ...],
    "summary": {
      "distance_km": 3.9,
      "risk_percent": 92.2,
      "safety_level": "HIGH RISK"
    }
  },
  "short_route": {
    "coords": [[10.7905, 78.7047], [10.7920, 78.7010], ...],
    "summary": {
      "distance_km": 3.9,
      "risk_percent": 92.2,
      "safety_level": "HIGH RISK"
    }
  }
}
```

---

## 🛠️ Troubleshooting & FAQ

### Q1: The browser shows "Backend offline"
- **Solution**: Make sure the backend server is running in your terminal (`python -m uvicorn main:app --host 127.0.0.1 --port 8000`). If running on a different port, open `http://127.0.0.1:<port>`.

### Q2: How do I retrain the machine learning model?
- If you edit the feature logic in `dataset.py`, re-run:
  ```powershell
  python dataset.py
  python ML-file.py
  ```
  This will regenerate `safe_route_data.csv` and `risk_model.pkl` with 100% accuracy.

### Q3: Can I test points outside Tiruchirappalli?
- The pre-cached road network (`trichy_graph.graphml`) covers the city of Tiruchirappalli. If you select points in another city, change `PLACE` in `services/route_service.py` to your desired city and delete `trichy_graph.graphml` to allow OSMnx to download the new road network.

### Q4: Port 8000 is already in use
- Run uvicorn on an alternative port, such as 8080:
  ```powershell
  python -m uvicorn main:app --host 127.0.0.1 --port 8080
  ```
  Then visit `http://127.0.0.1:8080`.
