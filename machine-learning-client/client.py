"""Flask API that runs predictions on frames and stores results in MongoDB."""

import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from db import get_db
from predict import predict_word

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))


@app.get("/health")
def health():
    """Report that the service is running."""
    return jsonify(status="ok")


@app.post("/predict")
def predict():
    """Predict a word from a list of frames and save the result."""
    body = request.get_json(silent=True) or {}
    frames = body.get("frames")
    if not isinstance(frames, list) or not frames:
        return jsonify(error="send a non-empty list of frames"), 400

    try:
        word, confidence = predict_word(frames)
    except ValueError as exc:  # e.g. a frame that isn't a valid image
        return jsonify(error=str(exc)), 400

    get_db().predictions.insert_one(
        {
            "word": word,
            "confidence": confidence,
            "num_frames": len(frames),
            "created_at": datetime.now(timezone.utc),
        }
    )
    return jsonify(word=word, confidence=confidence)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6700)
