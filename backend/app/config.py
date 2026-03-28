"""
CityPulse AI — Configuration Module
Loads environment variables and defines system-wide settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "citypulse_db")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(",")

    # ── Alert Thresholds ──────────────────────────────────────────────
    TRAFFIC_CONGESTION_THRESHOLD: float = 80.0   # percentage
    AQI_DANGER_THRESHOLD: float = 150.0          # AQI index
    ENERGY_PEAK_THRESHOLD: float = 900.0         # MW
    ANOMALY_SCORE_THRESHOLD: float = -0.3        # Isolation Forest score

    # ── Simulation Settings ───────────────────────────────────────────
    SIMULATION_INTERVAL: float = 2.0             # seconds between data ticks
    NUM_CITY_ZONES: int = 6                      # number of monitored zones


settings = Settings()
