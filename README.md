# 🏙️ CityPulse AI — Real-Time City Monitoring System

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

> An industry-grade, real-time AI-powered system that monitors city conditions including **traffic congestion**, **air pollution**, **power consumption**, and **anomaly detection** — with predictive analytics and interactive dashboards.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🔴 **Real-Time Streaming** | WebSocket-powered live data updates every 2 seconds |
| 🤖 **AI Predictions** | Random Forest, Gradient Boosting models for traffic, AQI, energy |
| 🔍 **Anomaly Detection** | Isolation Forest algorithm identifies unusual patterns |
| 🗺️ **Interactive Map** | Leaflet-based city map with color-coded zone markers |
| 📊 **Live Charts** | Recharts-powered real-time area charts with gradients |
| 🔔 **Smart Alerts** | Threshold-based alert system with severity levels |
| 🏗️ **Modular Architecture** | Clean separation of concerns for scalability |
| 🌙 **Dark Mode UI** | Premium glassmorphism design with smooth animations |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FRONTEND (React + Vite)                     │
│  Dashboard │ Charts │ Map │ Alerts │ Zone Table             │
│                         ↕ WebSocket + REST                  │
├─────────────────────────────────────────────────────────────┤
│                 BACKEND (FastAPI + Python)                   │
│  WebSocket Server │ REST API │ AI Engine │ Alert System      │
│                         ↕                                    │
│  Data Simulation Engine → AI Predictions → MongoDB Storage   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
CityPulse-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Package init
│   │   ├── config.py            # Configuration & thresholds
│   │   ├── database.py          # MongoDB async connection
│   │   ├── models.py            # Pydantic data models
│   │   ├── simulator.py         # City data simulation engine
│   │   ├── ai_engine.py         # ML models (RF, GB, IF)
│   │   ├── alerts.py            # Alert threshold checker
│   │   ├── websocket_manager.py # WebSocket connection manager
│   │   └── routes.py            # REST API endpoints
│   ├── models/                  # Saved ML model files (.pkl)
│   ├── main.py                  # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Navigation bar
│   │   │   ├── KPICards.jsx     # Key performance indicators
│   │   │   ├── TrafficChart.jsx # Traffic density chart
│   │   │   ├── AQIChart.jsx     # Air quality chart
│   │   │   ├── EnergyChart.jsx  # Energy consumption chart
│   │   │   ├── AlertsPanel.jsx  # Alert notifications
│   │   │   ├── CityMap.jsx      # Interactive Leaflet map
│   │   │   └── ZoneTable.jsx    # Zone data table
│   │   ├── hooks/
│   │   │   └── useWebSocket.js  # WebSocket client hook
│   │   ├── App.jsx              # Main application
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Design system
│   ├── index.html               # HTML template
│   ├── .env                     # Frontend env vars
│   └── package.json
│
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 3. MongoDB
```bash
# Make sure MongoDB is running locally on port 27017
# Or update MONGODB_URL in backend/.env for MongoDB Atlas
```

### 4. Access
- **Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

---

## 🤖 AI/ML Models

| Model | Algorithm | Purpose | Metric |
|-------|-----------|---------|--------|
| Traffic Predictor | Random Forest (100 trees) | Predict congestion % | MAE, R² |
| AQI Predictor | Gradient Boosting (150 trees) | Forecast air quality | MAE, R² |
| Energy Predictor | Random Forest (120 trees) | Predict power demand | MAE, R² |
| Anomaly Detector | Isolation Forest | Detect unusual patterns | Contamination: 5% |

### Feature Engineering
- **Cyclical time encoding**: `sin(2π·hour/24)`, `cos(2π·hour/24)` for smooth time-series learning
- **Area type encoding**: Label-encoded zone categories
- **Population density**: Zone-specific population as feature

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Aggregated KPI summary |
| GET | `/api/zones` | All monitored zones |
| GET | `/api/zones/{id}/history` | Historical data for a zone |
| GET | `/api/predictions/{id}` | AI predictions for a zone |
| GET | `/api/alerts` | Recent alerts (filterable) |
| GET | `/api/alerts/stats` | Alert statistics |
| GET | `/api/health` | Service health check |
| WS | `/ws` | Real-time WebSocket stream |

---

## 🌐 Deployment

### Backend → Render
1. Push backend to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env vars: `MONGODB_URL`, `DATABASE_NAME`

### Frontend → Vercel
1. Push frontend to GitHub
2. Import project on [Vercel](https://vercel.com)
3. Set framework: Vite
4. Add env var: `VITE_WS_URL=wss://your-backend.onrender.com/ws`

---

<p align="center">
  Built with ❤️ for smart cities
</p>
