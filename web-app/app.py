"""Configures the Flask app and routes"""

import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

ML_CLIENT_URL = os.getenv("ML_CLIENT_URL", "http://localhost:6700")


@app.route("/")
def index():
    """Renders the home page"""
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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
