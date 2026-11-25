"""Insert sample sign language letter predictions into MongoDB for testing."""

from datetime import datetime

from db import get_db


def seed():
    """Reset prediction collection and insert starter sign language letters."""
    database = get_db()
    database.predictions.delete_many({})
    fmt = "%Y-%m-%d %H:%M:%S"
    samples = [
        {
            "letter": "A",
            "confidence": 0.90,
            "num_frames": 12,
            "created_at": datetime.strptime("2026-11-23 13:00:00", fmt),
        },
        {
            "letter": "B",
            "confidence": 0.67,
            "num_frames": 15,
            "created_at": datetime.strptime("2026-11-23 13:01:00", fmt),
        },
    ]
    database.predictions.insert_many(samples)
    print("Added 2 sign language letters into MongoDB")


if __name__ == "__main__":
    seed()
