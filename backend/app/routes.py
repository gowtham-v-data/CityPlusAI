"""
CityPulse AI — API Routes
REST API endpoints for dashboard data, predictions, alerts, zones, and city selection.
"""
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from app.database import get_database
from app.ai_engine import predict
from app.simulator import (
    generate_sensor_data,
    get_available_cities,
    get_active_city,
    get_active_zones,
    set_active_city,
)
from app.models import DashboardSummary

router = APIRouter(prefix="/api", tags=["CityPulse API"])


# ── Dashboard Summary ────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary():
    """Get aggregated dashboard statistics across all zones."""
    db = get_database()

    # Get latest reading per zone
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$zone_id",
            "latest": {"$first": "$$ROOT"},
        }},
    ]

    latest_data = []
    if db:
        cursor = db.sensor_data.aggregate(pipeline)
        async for doc in cursor:
            latest_data.append(doc["latest"])

    # If no data in DB, generate fresh data
    if not latest_data:
        fresh = generate_sensor_data()
        latest_data = [r.model_dump() for r in fresh]

    total_zones = len(latest_data)
    avg_traffic = sum(d.get("traffic_density", 0) for d in latest_data) / max(total_zones, 1)
    avg_aqi = sum(d.get("aqi", 0) for d in latest_data) / max(total_zones, 1)
    total_power = sum(d.get("power_consumption", 0) for d in latest_data)
    total_solar = sum(d.get("solar_generation", 0) for d in latest_data)

    # Count active alerts
    active_alerts = 0
    anomalies = 0
    if db:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        active_alerts = await db.alerts.count_documents({"timestamp": {"$gte": one_hour_ago}})
        anomalies = await db.alerts.count_documents({
            "timestamp": {"$gte": one_hour_ago},
            "category": "anomaly",
        })

    return DashboardSummary(
        total_zones=total_zones,
        avg_traffic_density=round(avg_traffic, 2),
        avg_aqi=round(avg_aqi, 2),
        total_power_consumption=round(total_power, 2),
        total_solar_generation=round(total_solar, 2),
        active_alerts=active_alerts,
        anomalies_detected=anomalies,
        last_updated=datetime.utcnow(),
    )


# ── City Selection ────────────────────────────────────────────────────

@router.get("/cities")
async def list_cities():
    """Get all available cities for the dropdown."""
    return get_available_cities()


@router.get("/cities/active")
async def active_city():
    """Get the currently active city."""
    return get_active_city()


@router.post("/cities/{city_id}/select")
async def select_city(city_id: str):
    """Switch monitoring to a different city."""
    success = set_active_city(city_id)
    if success:
        return {"status": "ok", "city": get_active_city()}
    return {"status": "error", "message": f"Unknown city: {city_id}"}


# ── Zone Data ─────────────────────────────────────────────────────────

@router.get("/zones")
async def get_zones():
    """Get zones for the currently active city."""
    return get_active_zones()


@router.get("/zones/{zone_id}/history")
async def get_zone_history(
    zone_id: str,
    hours: int = Query(default=1, ge=1, le=24),
):
    """Get historical sensor data for a specific zone."""
    db = get_database()
    if not db:
        return []

    since = datetime.utcnow() - timedelta(hours=hours)
    cursor = db.sensor_data.find(
        {"zone_id": zone_id, "timestamp": {"$gte": since}},
        {"_id": 0},
    ).sort("timestamp", -1).limit(500)

    history = []
    async for doc in cursor:
        doc["timestamp"] = doc["timestamp"].isoformat()
        history.append(doc)

    return history


# ── Predictions ───────────────────────────────────────────────────────

@router.get("/predictions/{zone_id}")
async def get_zone_prediction(zone_id: str):
    """Get AI predictions for a specific zone."""
    # Get latest sensor data for this zone
    db = get_database()
    latest = None

    if db:
        latest = await db.sensor_data.find_one(
            {"zone_id": zone_id},
            sort=[("timestamp", -1)],
        )

    if not latest:
        # Generate fresh data
        fresh = generate_sensor_data()
        zone_data = next((r for r in fresh if r.zone_id == zone_id), fresh[0])
        latest = zone_data.model_dump()

    prediction = predict(latest)
    return {
        "zone_id": zone_id,
        "timestamp": datetime.utcnow().isoformat(),
        **prediction,
    }


# ── Alerts ────────────────────────────────────────────────────────────

@router.get("/alerts")
async def get_alerts(
    limit: int = Query(default=50, ge=1, le=200),
    severity: str = Query(default=None),
):
    """Get recent alerts, optionally filtered by severity."""
    db = get_database()
    if not db:
        return []

    query = {}
    if severity:
        query["severity"] = severity

    cursor = db.alerts.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit)

    alerts = []
    async for doc in cursor:
        doc["timestamp"] = doc["timestamp"].isoformat()
        alerts.append(doc)

    return alerts


@router.get("/alerts/stats")
async def get_alert_stats():
    """Get alert statistics for the dashboard."""
    db = get_database()
    if not db:
        return {"total": 0, "by_category": {}, "by_severity": {}}

    one_day_ago = datetime.utcnow() - timedelta(days=1)

    # Count by category
    cat_pipeline = [
        {"$match": {"timestamp": {"$gte": one_day_ago}}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    ]
    by_category = {}
    async for doc in db.alerts.aggregate(cat_pipeline):
        by_category[doc["_id"]] = doc["count"]

    # Count by severity
    sev_pipeline = [
        {"$match": {"timestamp": {"$gte": one_day_ago}}},
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
    ]
    by_severity = {}
    async for doc in db.alerts.aggregate(sev_pipeline):
        by_severity[doc["_id"]] = doc["count"]

    total = sum(by_category.values())

    return {
        "total": total,
        "by_category": by_category,
        "by_severity": by_severity,
    }


# ── Health Check ──────────────────────────────────────────────────────

@router.get("/health")
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "CityPulse AI",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
