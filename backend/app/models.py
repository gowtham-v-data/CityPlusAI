"""
CityPulse AI — Pydantic Models
Data models for API requests, responses, and database documents.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────────────

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertCategory(str, Enum):
    TRAFFIC = "traffic"
    POLLUTION = "pollution"
    ENERGY = "energy"
    ANOMALY = "anomaly"


# ── Sensor Data ───────────────────────────────────────────────────────

class SensorData(BaseModel):
    """Real-time sensor reading from a city zone."""
    zone_id: str = Field(..., description="City zone identifier")
    zone_name: str = Field(..., description="Human-readable zone name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    latitude: float = Field(..., description="Zone latitude")
    longitude: float = Field(..., description="Zone longitude")

    # Traffic metrics
    traffic_density: float = Field(..., ge=0, le=100, description="Traffic congestion %")
    vehicle_count: int = Field(..., ge=0, description="Number of vehicles detected")
    avg_speed: float = Field(..., ge=0, description="Average vehicle speed km/h")

    # Air quality metrics
    aqi: float = Field(..., ge=0, description="Air Quality Index")
    pm25: float = Field(..., ge=0, description="PM2.5 concentration µg/m³")
    pm10: float = Field(..., ge=0, description="PM10 concentration µg/m³")
    co2: float = Field(..., ge=0, description="CO2 level ppm")

    # Energy metrics
    power_consumption: float = Field(..., ge=0, description="Power consumption MW")
    solar_generation: float = Field(..., ge=0, description="Solar power generated MW")
    grid_load: float = Field(..., ge=0, le=100, description="Grid load percentage")

    # Environmental
    temperature: float = Field(..., description="Temperature °C")
    humidity: float = Field(..., ge=0, le=100, description="Humidity %")


class SensorDataResponse(SensorData):
    """Sensor data with prediction results."""
    predicted_traffic: Optional[float] = None
    predicted_aqi: Optional[float] = None
    predicted_energy: Optional[float] = None
    anomaly_score: Optional[float] = None
    is_anomaly: Optional[bool] = False


# ── Alerts ────────────────────────────────────────────────────────────

class Alert(BaseModel):
    """Alert generated when thresholds are exceeded."""
    id: Optional[str] = None
    zone_id: str
    zone_name: str
    category: AlertCategory
    severity: AlertSeverity
    message: str
    value: float
    threshold: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged: bool = False


# ── Predictions ───────────────────────────────────────────────────────

class PredictionResult(BaseModel):
    """AI model prediction output."""
    zone_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    predicted_traffic: float
    predicted_aqi: float
    predicted_energy: float
    anomaly_score: float
    is_anomaly: bool
    confidence: float = Field(..., ge=0, le=1)


# ── Dashboard Summary ────────────────────────────────────────────────

class DashboardSummary(BaseModel):
    """Aggregated dashboard statistics."""
    total_zones: int
    avg_traffic_density: float
    avg_aqi: float
    total_power_consumption: float
    total_solar_generation: float
    active_alerts: int
    anomalies_detected: int
    last_updated: datetime


# ── Zone Info ─────────────────────────────────────────────────────────

class ZoneInfo(BaseModel):
    """Static information about a monitored city zone."""
    zone_id: str
    zone_name: str
    latitude: float
    longitude: float
    area_type: str  # residential, commercial, industrial, etc.
    population: int
