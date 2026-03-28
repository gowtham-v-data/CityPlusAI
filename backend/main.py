"""
CityPulse AI — Main Application Entry Point
FastAPI server with WebSocket real-time streaming, background simulation,
and REST API endpoints.
"""
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.routes import router
from app.websocket_manager import manager
from app.simulator import generate_sensor_data, get_active_city, set_active_city
from app.ai_engine import train_models, load_models, predict
from app.alerts import check_alerts


# ── Background Simulation Task ────────────────────────────────────────

async def simulation_loop():
    """
    Background task that continuously generates sensor data,
    runs AI predictions, checks for alerts, stores in DB,
    and broadcasts to all WebSocket clients.
    """
    print("🚀 Simulation engine started")

    while True:
        try:
            # 1. Generate sensor data for all zones
            readings = generate_sensor_data()

            all_zone_data = []
            all_alerts = []

            for reading in readings:
                data_dict = reading.model_dump()

                # 2. Run AI predictions
                prediction = predict(data_dict)

                # 3. Check for alerts
                alerts = check_alerts(data_dict, prediction)
                all_alerts.extend(alerts)

                # 4. Combine sensor data + predictions
                enriched = {
                    **data_dict,
                    **prediction,
                    "timestamp": data_dict["timestamp"].isoformat()
                    if isinstance(data_dict["timestamp"], datetime)
                    else data_dict["timestamp"],
                }
                all_zone_data.append(enriched)

            # 5. Store in MongoDB
            db = get_database()
            if db:
                # Store sensor readings
                docs = []
                for reading in readings:
                    d = reading.model_dump()
                    docs.append(d)
                if docs:
                    await db.sensor_data.insert_many(docs)

                # Store alerts
                if all_alerts:
                    alert_docs = [a.model_dump() for a in all_alerts]
                    await db.alerts.insert_many(alert_docs)

            # 6. Broadcast to WebSocket clients
            broadcast_payload = {
                "type": "sensor_update",
                "timestamp": datetime.utcnow().isoformat(),
                "city": get_active_city(),
                "zones": all_zone_data,
                "alerts": [a.model_dump() for a in all_alerts],
                "alert_count": len(all_alerts),
                "connected_clients": manager.client_count,
            }
            await manager.broadcast(broadcast_payload)

        except Exception as e:
            print(f"❌ Simulation error: {e}")

        await asyncio.sleep(settings.SIMULATION_INTERVAL)


# ── Application Lifespan ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print("\n" + "=" * 60)
    print("  🏙️  CityPulse AI — Real-Time City Monitoring System")
    print("=" * 60 + "\n")

    # Connect to MongoDB
    await connect_to_mongo()

    # Train or load AI models
    if not load_models():
        train_models()

    # Start background simulation
    simulation_task = asyncio.create_task(simulation_loop())

    print(f"\n🌐 Server running on http://{settings.HOST}:{settings.PORT}")
    print(f"📡 WebSocket endpoint: ws://{settings.HOST}:{settings.PORT}/ws")
    print(f"📊 API docs: http://{settings.HOST}:{settings.PORT}/docs\n")

    yield

    # Shutdown
    simulation_task.cancel()
    try:
        await simulation_task
    except asyncio.CancelledError:
        pass
    await close_mongo_connection()
    print("\n👋 CityPulse AI shut down gracefully")


# ── FastAPI App ───────────────────────────────────────────────────────

app = FastAPI(
    title="CityPulse AI",
    description="Real-Time AI-Based City Monitoring System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST routes
app.include_router(router)


# ── WebSocket Endpoint ────────────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time data streaming.
    Clients connect here to receive live sensor data, predictions, and alerts.
    """
    await manager.connect(websocket)

    # Send initial data snapshot
    try:
        readings = generate_sensor_data()
        initial_data = []
        for reading in readings:
            data_dict = reading.model_dump()
            prediction = predict(data_dict)
            enriched = {
                **data_dict,
                **prediction,
                "timestamp": data_dict["timestamp"].isoformat()
                if isinstance(data_dict["timestamp"], datetime)
                else data_dict["timestamp"],
            }
            initial_data.append(enriched)

        await manager.send_personal(websocket, {
            "type": "initial_snapshot",
            "timestamp": datetime.utcnow().isoformat(),
            "city": get_active_city(),
            "zones": initial_data,
            "message": "Connected to CityPulse AI",
        })
    except Exception as e:
        print(f"❌ Error sending initial data: {e}")

    # Keep connection alive and handle messages
    try:
        while True:
            data = await websocket.receive_text()

            if data == "ping":
                await manager.send_personal(websocket, {"type": "pong"})
            elif data.startswith("city:"):
                # Handle city switch: "city:mumbai"
                import json
                city_id = data.split(":", 1)[1].strip()
                success = set_active_city(city_id)
                if success:
                    # Send immediate snapshot for new city
                    new_readings = generate_sensor_data()
                    new_data = []
                    for reading in new_readings:
                        d = reading.model_dump()
                        p = predict(d)
                        enriched = {
                            **d, **p,
                            "timestamp": d["timestamp"].isoformat()
                            if isinstance(d["timestamp"], datetime)
                            else d["timestamp"],
                        }
                        new_data.append(enriched)
                    await manager.broadcast({
                        "type": "city_changed",
                        "city": get_active_city(),
                        "zones": new_data,
                        "timestamp": datetime.utcnow().isoformat(),
                    })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ── Root Endpoint ─────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "CityPulse AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "websocket": "/ws",
    }
