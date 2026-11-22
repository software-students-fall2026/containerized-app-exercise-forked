"""Configures the Flask app and routes"""

import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))


@app.route("/")
def index():
    """Renders the home page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
