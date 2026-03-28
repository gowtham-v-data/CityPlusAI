"""
CityPulse AI — AI/ML Prediction Engine
Contains models for:
1. Traffic Prediction (Random Forest Regressor)
2. Air Quality Prediction (Gradient Boosting Regressor)
3. Energy Consumption Prediction (Random Forest Regressor)
4. Anomaly Detection (Isolation Forest)

Models are trained on synthetic historical data and used for real-time inference.
"""
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    IsolationForest,
)
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from app.simulator import generate_historical_data

# ── Model Storage ─────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Global model instances
traffic_model = None
aqi_model = None
energy_model = None
anomaly_model = None
label_encoder = None


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare feature matrix from raw data."""
    global label_encoder

    features = df[["hour", "minute", "population", "temperature", "humidity"]].copy()

    if label_encoder is None:
        label_encoder = LabelEncoder()
        features["area_encoded"] = label_encoder.fit_transform(df["area_type"])
    else:
        features["area_encoded"] = label_encoder.transform(df["area_type"])

    # Cyclical time features for better time-series learning
    features["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    features["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    return features


def train_models():
    """
    Train all AI models on synthetic historical data.
    Called once at startup to initialize models.
    """
    global traffic_model, aqi_model, energy_model, anomaly_model

    print("🧠 Training AI models...")

    # Generate training data (48 hours worth)
    raw_data = generate_historical_data(hours=48)
    df = pd.DataFrame(raw_data)

    # Prepare features
    X = _prepare_features(df)

    # ── 1. Traffic Prediction Model (Random Forest) ───────────────────
    y_traffic = df["traffic_density"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_traffic, test_size=0.2, random_state=42)

    traffic_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
    )
    traffic_model.fit(X_train, y_train)

    preds = traffic_model.predict(X_test)
    print(f"   📊 Traffic Model — MAE: {mean_absolute_error(y_test, preds):.2f}, R²: {r2_score(y_test, preds):.3f}")

    # ── 2. Air Quality Prediction Model (Gradient Boosting) ──────────
    y_aqi = df["aqi"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_aqi, test_size=0.2, random_state=42)

    aqi_model = GradientBoostingRegressor(
        n_estimators=150,
        max_depth=8,
        learning_rate=0.1,
        random_state=42,
    )
    aqi_model.fit(X_train, y_train)

    preds = aqi_model.predict(X_test)
    print(f"   🌫️ AQI Model    — MAE: {mean_absolute_error(y_test, preds):.2f}, R²: {r2_score(y_test, preds):.3f}")

    # ── 3. Energy Prediction Model (Random Forest) ───────────────────
    y_energy = df["power_consumption"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_energy, test_size=0.2, random_state=42)

    energy_model = RandomForestRegressor(
        n_estimators=120,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    energy_model.fit(X_train, y_train)

    preds = energy_model.predict(X_test)
    print(f"   ⚡ Energy Model  — MAE: {mean_absolute_error(y_test, preds):.2f}, R²: {r2_score(y_test, preds):.3f}")

    # ── 4. Anomaly Detection (Isolation Forest) ──────────────────────
    anomaly_features = df[["traffic_density", "aqi", "power_consumption"]].copy()
    anomaly_model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )
    anomaly_model.fit(anomaly_features)

    print("   🔍 Anomaly Detector trained")

    # Save models
    joblib.dump(traffic_model, os.path.join(MODEL_DIR, "traffic_model.pkl"))
    joblib.dump(aqi_model, os.path.join(MODEL_DIR, "aqi_model.pkl"))
    joblib.dump(energy_model, os.path.join(MODEL_DIR, "energy_model.pkl"))
    joblib.dump(anomaly_model, os.path.join(MODEL_DIR, "anomaly_model.pkl"))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    print("✅ All AI models trained and saved!\n")


def load_models():
    """Load pre-trained models from disk if available."""
    global traffic_model, aqi_model, energy_model, anomaly_model, label_encoder

    try:
        traffic_model = joblib.load(os.path.join(MODEL_DIR, "traffic_model.pkl"))
        aqi_model = joblib.load(os.path.join(MODEL_DIR, "aqi_model.pkl"))
        energy_model = joblib.load(os.path.join(MODEL_DIR, "energy_model.pkl"))
        anomaly_model = joblib.load(os.path.join(MODEL_DIR, "anomaly_model.pkl"))
        label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
        print("📦 Loaded pre-trained models from disk")
        return True
    except FileNotFoundError:
        return False


def predict(sensor_data: dict) -> dict:
    """
    Run all AI models on a single sensor reading.

    Args:
        sensor_data: Dict with zone sensor readings

    Returns:
        Dict with predicted_traffic, predicted_aqi, predicted_energy,
        anomaly_score, is_anomaly, confidence
    """
    if traffic_model is None:
        return {
            "predicted_traffic": sensor_data.get("traffic_density", 0),
            "predicted_aqi": sensor_data.get("aqi", 0),
            "predicted_energy": sensor_data.get("power_consumption", 0),
            "anomaly_score": 0.0,
            "is_anomaly": False,
            "confidence": 0.0,
        }

    from app.simulator import CITY_ZONES

    # Find zone info
    zone = next((z for z in CITY_ZONES if z["zone_id"] == sensor_data["zone_id"]), CITY_ZONES[0])

    timestamp = sensor_data.get("timestamp")
    if hasattr(timestamp, "hour"):
        hour = timestamp.hour
        minute = timestamp.minute
    else:
        from datetime import datetime
        now = datetime.utcnow()
        hour = now.hour
        minute = now.minute

    features = pd.DataFrame([{
        "hour": hour,
        "minute": minute,
        "population": zone["population"],
        "temperature": sensor_data.get("temperature", 28),
        "humidity": sensor_data.get("humidity", 60),
        "area_encoded": label_encoder.transform([zone["area_type"]])[0],
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
    }])

    # Run predictions
    pred_traffic = float(traffic_model.predict(features)[0])
    pred_aqi = float(aqi_model.predict(features)[0])
    pred_energy = float(energy_model.predict(features)[0])

    # Anomaly detection
    anomaly_features = np.array([[
        sensor_data.get("traffic_density", 0),
        sensor_data.get("aqi", 0),
        sensor_data.get("power_consumption", 0),
    ]])
    anomaly_score = float(anomaly_model.score_samples(anomaly_features)[0])
    is_anomaly = anomaly_model.predict(anomaly_features)[0] == -1

    # Confidence based on how close prediction is to actual
    actual_traffic = sensor_data.get("traffic_density", pred_traffic)
    if actual_traffic > 0:
        confidence = max(0, min(1, 1 - abs(pred_traffic - actual_traffic) / actual_traffic))
    else:
        confidence = 0.85

    return {
        "predicted_traffic": round(max(0, min(100, pred_traffic)), 2),
        "predicted_aqi": round(max(0, pred_aqi), 2),
        "predicted_energy": round(max(0, pred_energy), 2),
        "anomaly_score": round(anomaly_score, 4),
        "is_anomaly": bool(is_anomaly),
        "confidence": round(confidence, 3),
    }
