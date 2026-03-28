"""
CityPulse AI — Data Simulation Engine
Generates realistic synthetic sensor data for multiple Indian cities.
Each city has 6 monitored zones with traffic, pollution, energy, and environmental data.
"""
import random
import math
import numpy as np
from datetime import datetime
from app.models import SensorData
from app.config import settings

# ── Multi-City Definitions ───────────────────────────────────────────

CITIES = {
    "bengaluru": {
        "name": "Bengaluru",
        "state": "Karnataka",
        "center": [12.9716, 77.5946],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "MG Road - Downtown", "latitude": 12.9716, "longitude": 77.5946, "area_type": "commercial", "population": 185000, "base_traffic": 70, "base_aqi": 90, "base_energy": 650},
            {"zone_id": "zone_02", "zone_name": "Whitefield Tech Park", "latitude": 12.9698, "longitude": 77.7500, "area_type": "commercial", "population": 120000, "base_traffic": 60, "base_aqi": 70, "base_energy": 800},
            {"zone_id": "zone_03", "zone_name": "Koramangala", "latitude": 12.9352, "longitude": 77.6245, "area_type": "residential", "population": 250000, "base_traffic": 40, "base_aqi": 55, "base_energy": 400},
            {"zone_id": "zone_04", "zone_name": "Peenya Industrial", "latitude": 13.0300, "longitude": 77.5200, "area_type": "industrial", "population": 45000, "base_traffic": 50, "base_aqi": 130, "base_energy": 950},
            {"zone_id": "zone_05", "zone_name": "IISc - University Area", "latitude": 13.0219, "longitude": 77.5671, "area_type": "educational", "population": 95000, "base_traffic": 35, "base_aqi": 45, "base_energy": 300},
            {"zone_id": "zone_06", "zone_name": "Banashankari", "latitude": 12.9255, "longitude": 77.5468, "area_type": "residential", "population": 180000, "base_traffic": 30, "base_aqi": 40, "base_energy": 350},
        ],
    },
    "mumbai": {
        "name": "Mumbai",
        "state": "Maharashtra",
        "center": [19.0760, 72.8777],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "Colaba - South Mumbai", "latitude": 18.9067, "longitude": 72.8147, "area_type": "commercial", "population": 220000, "base_traffic": 80, "base_aqi": 110, "base_energy": 750},
            {"zone_id": "zone_02", "zone_name": "BKC Business District", "latitude": 19.0596, "longitude": 72.8656, "area_type": "commercial", "population": 150000, "base_traffic": 75, "base_aqi": 95, "base_energy": 900},
            {"zone_id": "zone_03", "zone_name": "Andheri Residential", "latitude": 19.1136, "longitude": 72.8697, "area_type": "residential", "population": 350000, "base_traffic": 65, "base_aqi": 85, "base_energy": 500},
            {"zone_id": "zone_04", "zone_name": "MIDC Industrial", "latitude": 19.1550, "longitude": 72.8600, "area_type": "industrial", "population": 60000, "base_traffic": 55, "base_aqi": 140, "base_energy": 1050},
            {"zone_id": "zone_05", "zone_name": "Powai - IIT Area", "latitude": 19.1176, "longitude": 72.9060, "area_type": "educational", "population": 80000, "base_traffic": 40, "base_aqi": 60, "base_energy": 350},
            {"zone_id": "zone_06", "zone_name": "Navi Mumbai", "latitude": 19.0330, "longitude": 73.0297, "area_type": "residential", "population": 200000, "base_traffic": 35, "base_aqi": 50, "base_energy": 400},
        ],
    },
    "delhi": {
        "name": "Delhi",
        "state": "Delhi NCR",
        "center": [28.6139, 77.2090],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "Connaught Place", "latitude": 28.6315, "longitude": 77.2167, "area_type": "commercial", "population": 200000, "base_traffic": 85, "base_aqi": 160, "base_energy": 700},
            {"zone_id": "zone_02", "zone_name": "Cyber City Gurugram", "latitude": 28.4945, "longitude": 77.0888, "area_type": "commercial", "population": 180000, "base_traffic": 70, "base_aqi": 140, "base_energy": 850},
            {"zone_id": "zone_03", "zone_name": "Dwarka Residential", "latitude": 28.5921, "longitude": 77.0460, "area_type": "residential", "population": 300000, "base_traffic": 50, "base_aqi": 120, "base_energy": 450},
            {"zone_id": "zone_04", "zone_name": "Okhla Industrial", "latitude": 28.5315, "longitude": 77.2716, "area_type": "industrial", "population": 55000, "base_traffic": 60, "base_aqi": 180, "base_energy": 1000},
            {"zone_id": "zone_05", "zone_name": "JNU - University Area", "latitude": 28.5402, "longitude": 77.1662, "area_type": "educational", "population": 75000, "base_traffic": 30, "base_aqi": 100, "base_energy": 280},
            {"zone_id": "zone_06", "zone_name": "Noida Extension", "latitude": 28.5672, "longitude": 77.3234, "area_type": "residential", "population": 250000, "base_traffic": 45, "base_aqi": 130, "base_energy": 380},
        ],
    },
    "chennai": {
        "name": "Chennai",
        "state": "Tamil Nadu",
        "center": [13.0827, 80.2707],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "T. Nagar Commercial", "latitude": 13.0418, "longitude": 80.2341, "area_type": "commercial", "population": 190000, "base_traffic": 75, "base_aqi": 80, "base_energy": 620},
            {"zone_id": "zone_02", "zone_name": "OMR IT Corridor", "latitude": 12.9165, "longitude": 80.2274, "area_type": "commercial", "population": 140000, "base_traffic": 65, "base_aqi": 65, "base_energy": 780},
            {"zone_id": "zone_03", "zone_name": "Adyar Residential", "latitude": 13.0012, "longitude": 80.2565, "area_type": "residential", "population": 230000, "base_traffic": 45, "base_aqi": 50, "base_energy": 380},
            {"zone_id": "zone_04", "zone_name": "Ambattur Industrial", "latitude": 13.1143, "longitude": 80.1548, "area_type": "industrial", "population": 50000, "base_traffic": 55, "base_aqi": 120, "base_energy": 920},
            {"zone_id": "zone_05", "zone_name": "IIT Madras Campus", "latitude": 12.9915, "longitude": 80.2336, "area_type": "educational", "population": 85000, "base_traffic": 30, "base_aqi": 40, "base_energy": 290},
            {"zone_id": "zone_06", "zone_name": "Velachery Suburbs", "latitude": 12.9815, "longitude": 80.2180, "area_type": "residential", "population": 210000, "base_traffic": 35, "base_aqi": 45, "base_energy": 340},
        ],
    },
    "hyderabad": {
        "name": "Hyderabad",
        "state": "Telangana",
        "center": [17.3850, 78.4867],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "HITEC City", "latitude": 17.4435, "longitude": 78.3772, "area_type": "commercial", "population": 160000, "base_traffic": 70, "base_aqi": 75, "base_energy": 700},
            {"zone_id": "zone_02", "zone_name": "Gachibowli IT Hub", "latitude": 17.4401, "longitude": 78.3489, "area_type": "commercial", "population": 130000, "base_traffic": 60, "base_aqi": 65, "base_energy": 820},
            {"zone_id": "zone_03", "zone_name": "Banjara Hills", "latitude": 17.4108, "longitude": 78.4347, "area_type": "residential", "population": 200000, "base_traffic": 50, "base_aqi": 55, "base_energy": 420},
            {"zone_id": "zone_04", "zone_name": "Jeedimetla Industrial", "latitude": 17.5024, "longitude": 78.4385, "area_type": "industrial", "population": 40000, "base_traffic": 45, "base_aqi": 125, "base_energy": 900},
            {"zone_id": "zone_05", "zone_name": "University of Hyderabad", "latitude": 17.4603, "longitude": 78.3313, "area_type": "educational", "population": 70000, "base_traffic": 25, "base_aqi": 42, "base_energy": 270},
            {"zone_id": "zone_06", "zone_name": "LB Nagar Suburbs", "latitude": 17.3457, "longitude": 78.5522, "area_type": "residential", "population": 190000, "base_traffic": 40, "base_aqi": 48, "base_energy": 360},
        ],
    },
    "kolkata": {
        "name": "Kolkata",
        "state": "West Bengal",
        "center": [22.5726, 88.3639],
        "zones": [
            {"zone_id": "zone_01", "zone_name": "Park Street Central", "latitude": 22.5518, "longitude": 88.3516, "area_type": "commercial", "population": 175000, "base_traffic": 75, "base_aqi": 100, "base_energy": 600},
            {"zone_id": "zone_02", "zone_name": "Salt Lake Tech City", "latitude": 22.5800, "longitude": 88.4157, "area_type": "commercial", "population": 110000, "base_traffic": 55, "base_aqi": 80, "base_energy": 750},
            {"zone_id": "zone_03", "zone_name": "South Kolkata", "latitude": 22.4990, "longitude": 88.3640, "area_type": "residential", "population": 280000, "base_traffic": 45, "base_aqi": 60, "base_energy": 380},
            {"zone_id": "zone_04", "zone_name": "Howrah Industrial", "latitude": 22.5958, "longitude": 88.2636, "area_type": "industrial", "population": 55000, "base_traffic": 60, "base_aqi": 135, "base_energy": 940},
            {"zone_id": "zone_05", "zone_name": "Jadavpur University Area", "latitude": 22.4966, "longitude": 88.3712, "area_type": "educational", "population": 90000, "base_traffic": 35, "base_aqi": 55, "base_energy": 310},
            {"zone_id": "zone_06", "zone_name": "New Town Rajarhat", "latitude": 22.5810, "longitude": 88.4618, "area_type": "residential", "population": 170000, "base_traffic": 30, "base_aqi": 45, "base_energy": 330},
        ],
    },
}

# Current active city (default)
_active_city = "bengaluru"


def get_available_cities() -> list[dict]:
    """Return list of available cities for the dropdown."""
    return [
        {
            "id": city_id,
            "name": city["name"],
            "state": city["state"],
            "center": city["center"],
            "zone_count": len(city["zones"]),
        }
        for city_id, city in CITIES.items()
    ]


def set_active_city(city_id: str) -> bool:
    """Set the active city for simulation."""
    global _active_city
    if city_id in CITIES:
        _active_city = city_id
        print(f"🏙️ Switched to city: {CITIES[city_id]['name']}")
        return True
    return False


def get_active_city() -> dict:
    """Get the current active city info."""
    city = CITIES[_active_city]
    return {
        "id": _active_city,
        "name": city["name"],
        "state": city["state"],
        "center": city["center"],
    }


def get_active_zones() -> list[dict]:
    """Get zones for the currently active city."""
    return CITIES[_active_city]["zones"]


# ── Backward compatibility ────────────────────────────────────────────
CITY_ZONES = CITIES["bengaluru"]["zones"]  # Default for AI engine training


def _time_factor(hour: int) -> dict:
    """
    Returns multipliers based on time of day to simulate realistic patterns.
    """
    if 7 <= hour <= 9:
        return {"traffic": 1.4, "aqi": 1.2, "energy": 1.1}
    elif 11 <= hour <= 14:
        return {"traffic": 1.0, "aqi": 1.1, "energy": 1.3}
    elif 17 <= hour <= 19:
        return {"traffic": 1.6, "aqi": 1.4, "energy": 1.2}
    elif 22 <= hour or hour <= 5:
        return {"traffic": 0.3, "aqi": 0.6, "energy": 0.5}
    else:
        return {"traffic": 0.8, "aqi": 0.9, "energy": 0.9}


def _inject_anomaly() -> bool:
    """5% chance of generating anomalous data."""
    return random.random() < 0.05


def generate_sensor_data(city_id: str = None) -> list[SensorData]:
    """
    Generate one tick of sensor data for the specified (or active) city's zones.
    """
    target_city = city_id or _active_city
    if target_city not in CITIES:
        target_city = _active_city

    zones = CITIES[target_city]["zones"]
    now = datetime.utcnow()
    hour = now.hour
    factors = _time_factor(hour)
    readings = []

    for zone in zones:
        is_anomaly = _inject_anomaly()

        # ── Traffic Simulation ────────────────────────────────────────
        traffic_base = zone["base_traffic"] * factors["traffic"]
        noise = random.gauss(0, 5)
        traffic_density = max(0, min(100, traffic_base + noise))

        if is_anomaly:
            traffic_density = min(100, traffic_density + random.uniform(20, 40))

        vehicle_count = int(traffic_density * random.uniform(15, 25))
        avg_speed = max(5, 80 - traffic_density * 0.7 + random.gauss(0, 3))

        # ── Air Quality Simulation ────────────────────────────────────
        aqi_base = zone["base_aqi"] * factors["aqi"]
        aqi = max(0, aqi_base + random.gauss(0, 10))

        if is_anomaly:
            aqi = aqi + random.uniform(50, 100)

        pm25 = max(0, aqi * 0.4 + random.gauss(0, 5))
        pm10 = max(0, aqi * 0.6 + random.gauss(0, 8))
        co2 = max(300, 400 + aqi * 1.5 + random.gauss(0, 20))

        # ── Energy Simulation ─────────────────────────────────────────
        energy_base = zone["base_energy"] * factors["energy"]
        power_consumption = max(0, energy_base + random.gauss(0, 30))

        if is_anomaly:
            power_consumption = power_consumption * random.uniform(1.3, 1.6)

        solar_factor = max(0, math.sin((hour - 6) * math.pi / 12)) if 6 <= hour <= 18 else 0
        solar_generation = max(0, power_consumption * 0.15 * solar_factor + random.gauss(0, 5))
        grid_load = max(0, min(100, (power_consumption - solar_generation) / energy_base * 80 + random.gauss(0, 3)))

        # ── Environmental ─────────────────────────────────────────────
        temp_base = 28 + 5 * math.sin((hour - 6) * math.pi / 12)
        temperature = temp_base + random.gauss(0, 2)
        humidity = max(20, min(95, 60 + random.gauss(0, 10)))

        reading = SensorData(
            zone_id=zone["zone_id"],
            zone_name=zone["zone_name"],
            timestamp=now,
            latitude=zone["latitude"],
            longitude=zone["longitude"],
            traffic_density=round(traffic_density, 2),
            vehicle_count=vehicle_count,
            avg_speed=round(avg_speed, 2),
            aqi=round(aqi, 2),
            pm25=round(pm25, 2),
            pm10=round(pm10, 2),
            co2=round(co2, 2),
            power_consumption=round(power_consumption, 2),
            solar_generation=round(solar_generation, 2),
            grid_load=round(grid_load, 2),
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
        )
        readings.append(reading)

    return readings


def generate_historical_data(hours: int = 24) -> list[dict]:
    """
    Generate historical data for model training using all cities.
    """
    data_points = []
    for city_id, city in CITIES.items():
        for h in range(hours):
            factors = _time_factor(h % 24)
            for zone in city["zones"]:
                for minute in range(0, 60, 5):
                    traffic = max(0, min(100,
                        zone["base_traffic"] * factors["traffic"] + random.gauss(0, 8)
                    ))
                    aqi = max(0,
                        zone["base_aqi"] * factors["aqi"] + random.gauss(0, 12)
                    )
                    energy = max(0,
                        zone["base_energy"] * factors["energy"] + random.gauss(0, 40)
                    )

                    data_points.append({
                        "hour": h % 24,
                        "minute": minute,
                        "zone_id": zone["zone_id"],
                        "area_type": zone["area_type"],
                        "population": zone["population"],
                        "traffic_density": round(traffic, 2),
                        "aqi": round(aqi, 2),
                        "power_consumption": round(energy, 2),
                        "temperature": round(28 + 5 * math.sin((h % 24 - 6) * math.pi / 12) + random.gauss(0, 2), 2),
                        "humidity": round(max(20, min(95, 60 + random.gauss(0, 10))), 2),
                        "vehicle_count": int(traffic * random.uniform(15, 25)),
                        "avg_speed": round(max(5, 80 - traffic * 0.7 + random.gauss(0, 3)), 2),
                    })

    return data_points
