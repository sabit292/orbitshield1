from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import pytz
import numpy as np

app = Flask(__name__)

KP_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
SOLAR_WIND_URL = "https://services.swpc.noaa.gov/json/solar-wind.json"
FLARE_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"

def get_data():
    try:
        kp_data = requests.get(KP_URL).json()
        kp_values = [float(d['kp_index']) for d in kp_data[-30:]]
        kp = kp_values[-1]
    except:
        kp_values = [0]
        kp = 0

    try:
        wind = requests.get(SOLAR_WIND_URL).json()[-1]
        speed = float(wind['speed'])
    except:
        speed = 0

    try:
        flare = requests.get(FLARE_URL).json()[-1]
        flux = float(flare['flux'])
    except:
        flux = 0

    x = np.arange(len(kp_values))
    y = np.array(kp_values)
    coef = np.polyfit(x, y, 1)
    prediction = float(coef[0]*(len(x)+6) + coef[1])

    score = kp + speed/200 + flux*1e6

    if score < 5:
        risk = "LOW"
        region = "Sakin"
    elif score < 10:
        risk = "MEDIUM"
        region = "Kuzey bölgeler"
    elif score < 15:
        risk = "HIGH"
        region = "Avrupa etkilenebilir"
    else:
        risk = "EXTREME"
        region = "TÜRKİYE RİSK ALTINDA ⚠️"

    tz = pytz.timezone("Europe/Istanbul")
    now = datetime.now(tz).strftime("%H:%M:%S")

    return {
        "kp": kp,
        "history": kp_values,
        "prediction": round(prediction,2),
        "risk": risk,
        "region": region,
        "time": now,
        "solar_wind": round(speed,1),
        "flare": flux
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_data())

if __name__ == "__main__":
    app.run(debug=True)
