"""MongoDB connection helper."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # for local runs; in Docker, env vars come from env_file


@lru_cache(maxsize=1)
def get_client():
    """Create the MongoClient once and reuse it on later calls."""
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
    client.admin.command("ping")  # fail fast on bad URI, auth, or IP access
    return client


def get_db():
    """Return the app's database."""
    return get_client()[os.environ.get("MONGO_DBNAME", "myappdb")]
