from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import pytz
import numpy as np

app = Flask(__name__, template_folder="templates", static_folder="static")

KP_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

def get_data():
    try:
        data = requests.get(KP_URL, timeout=5).json()
        kp_values = [float(d['kp_index']) for d in data[-30:]]
        kp = kp_values[-1]
    except:
        kp_values = [0]
        kp = 0

    tz = pytz.timezone("Europe/Istanbul")
    now = datetime.now(tz).strftime("%H:%M:%S")

    return {
        "kp": kp,
        "history": kp_values,
        "prediction": kp,
        "risk": "LOW",
        "region": "Test",
        "time": now,
        "solar_wind": 0,
        "flare": 0
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
