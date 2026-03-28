"""
CityPulse AI — Alert Engine
Monitors sensor data and predictions against thresholds.
Generates alerts when conditions exceed safe limits.
"""
from datetime import datetime
from app.models import Alert, AlertSeverity, AlertCategory
from app.config import settings


def _get_severity(value: float, threshold: float) -> AlertSeverity:
    """Determine alert severity based on how far value exceeds threshold."""
    ratio = value / threshold if threshold > 0 else 1.0
    if ratio >= 1.5:
        return AlertSeverity.CRITICAL
    elif ratio >= 1.25:
        return AlertSeverity.HIGH
    elif ratio >= 1.1:
        return AlertSeverity.MEDIUM
    else:
        return AlertSeverity.LOW


def check_alerts(sensor_data: dict, predictions: dict) -> list[Alert]:
    """
    Check sensor data and predictions against thresholds.
    Returns a list of Alert objects for any violations.
    """
    alerts = []
    now = datetime.utcnow()
    zone_id = sensor_data.get("zone_id", "unknown")
    zone_name = sensor_data.get("zone_name", "Unknown Zone")

    # ── Traffic Congestion Alert ──────────────────────────────────────
    traffic = sensor_data.get("traffic_density", 0)
    if traffic > settings.TRAFFIC_CONGESTION_THRESHOLD:
        severity = _get_severity(traffic, settings.TRAFFIC_CONGESTION_THRESHOLD)
        alerts.append(Alert(
            zone_id=zone_id,
            zone_name=zone_name,
            category=AlertCategory.TRAFFIC,
            severity=severity,
            message=f"Traffic congestion at {traffic:.1f}% in {zone_name}",
            value=traffic,
            threshold=settings.TRAFFIC_CONGESTION_THRESHOLD,
            timestamp=now,
        ))

    # ── Air Quality Alert ─────────────────────────────────────────────
    aqi = sensor_data.get("aqi", 0)
    if aqi > settings.AQI_DANGER_THRESHOLD:
        severity = _get_severity(aqi, settings.AQI_DANGER_THRESHOLD)
        alerts.append(Alert(
            zone_id=zone_id,
            zone_name=zone_name,
            category=AlertCategory.POLLUTION,
            severity=severity,
            message=f"AQI level at {aqi:.1f} in {zone_name} — {'Unhealthy' if aqi < 200 else 'Hazardous'}",
            value=aqi,
            threshold=settings.AQI_DANGER_THRESHOLD,
            timestamp=now,
        ))

    # ── Energy Peak Alert ─────────────────────────────────────────────
    energy = sensor_data.get("power_consumption", 0)
    if energy > settings.ENERGY_PEAK_THRESHOLD:
        severity = _get_severity(energy, settings.ENERGY_PEAK_THRESHOLD)
        alerts.append(Alert(
            zone_id=zone_id,
            zone_name=zone_name,
            category=AlertCategory.ENERGY,
            severity=severity,
            message=f"Power consumption at {energy:.1f} MW in {zone_name}",
            value=energy,
            threshold=settings.ENERGY_PEAK_THRESHOLD,
            timestamp=now,
        ))

    # ── Anomaly Alert ─────────────────────────────────────────────────
    if predictions.get("is_anomaly", False):
        score = predictions.get("anomaly_score", 0)
        alerts.append(Alert(
            zone_id=zone_id,
            zone_name=zone_name,
            category=AlertCategory.ANOMALY,
            severity=AlertSeverity.HIGH,
            message=f"Anomaly detected in {zone_name} (score: {score:.3f})",
            value=abs(score),
            threshold=abs(settings.ANOMALY_SCORE_THRESHOLD),
            timestamp=now,
        ))

    return alerts
