"""Configures the Flask app and routes."""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
import requests

from db import get_db
from seed import seed

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

ML_CLIENT_URL = os.getenv("ML_CLIENT_URL", "http://localhost:6700")


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/api/frame", methods=["POST"])
def forward_frame():
    """Forwards a camera frame from the browser to the ML client."""
    frame = request.files["frame"]
    response = requests.post(
        f"{ML_CLIENT_URL}/predict",
        files={"frame": ("frame.jpg", frame.read(), "image/jpeg")},
        timeout=10,
    )
    return jsonify(response.json())


@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    """Return recent sign language predictions from MongoDB."""
    database = get_db()
    docs = list(database.predictions.find().sort("created_at", -1).limit(20))
    predictions = [
        {
            "id": str(doc["_id"]),
            "letter": doc.get("letter") or doc.get("word", ""),
            "confidence": doc.get("confidence", 0),
            "created_at": str(doc.get("created_at", "")),
        }
        for doc in docs
    ]
    return jsonify(predictions)


@app.route("/api/seed", methods=["POST"])
def run_seed():
    """Insert sample letters into MongoDB."""
    seed()
    return jsonify({"status": "seeded"})


@app.route("/api/predictions", methods=["DELETE"])
def clear_predictions():
    """Delete all stored predictions from MongoDB."""
    database = get_db()
    result = database.predictions.delete_many({})
    return jsonify({"deleted": result.deleted_count})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
