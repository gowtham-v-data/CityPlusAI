"""
CityPulse AI — Database Connection Module
Async MongoDB connection using Motor driver.
Gracefully handles unavailable MongoDB (runs in simulation-only mode).
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# ── MongoDB Client ────────────────────────────────────────────────────
client = None
db = None
_connected = False


async def connect_to_mongo():
    """Establish connection to MongoDB. Falls back to simulation mode if unavailable."""
    global client, db, _connected

    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=3000,
        )
        # Test connection
        await client.admin.command("ping")
        db = client[settings.DATABASE_NAME]

        # Create indexes for faster queries
        await db.sensor_data.create_index([("timestamp", -1)])
        await db.sensor_data.create_index([("zone_id", 1)])
        await db.alerts.create_index([("timestamp", -1)])
        await db.predictions.create_index([("timestamp", -1)])

        _connected = True
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
    except Exception as e:
        _connected = False
        db = None
        print(f"⚠️  MongoDB unavailable ({e}). Running in simulation-only mode.")
        print("   Data will not be persisted. Install & start MongoDB to enable storage.")


async def close_mongo_connection():
    """Close MongoDB connection."""
    global client, _connected
    if client:
        client.close()
        _connected = False
        print("🔌 MongoDB connection closed")


def get_database():
    """Get database instance. Returns None if not connected."""
    return db if _connected else None
