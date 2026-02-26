from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

from Backendmandi.modules.weather import fetch_weather_data
from Backendmandi.modules.decision import smart_decision_engine
from Backendmandi.modules.risk_radar import build_risk_radar   # ⭐ NEW
from Backendmandi.mandi_api import get_mandi_data

# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Convert location → latitude & longitude
# -----------------------------------
def get_lat_lon(location: str):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "AgriChain-App"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None, None

        data = response.json()

        if data:
            return data[0]["lat"], data[0]["lon"]

    except Exception as e:
        print("Location API Error:", e)

    return None, None


# -----------------------------------
# Root Route
# -----------------------------------
@app.get("/")
def home():
    return {"message": "AgriChain Unified Backend Running 🚀"}


# -----------------------------------
# Smart Unified Advisor
# -----------------------------------
@app.get("/smart-advisor")
def smart_advisor(
    state: str = Query(...),
    commodity: str = Query(...),
    market: str = Query(...),
    location: str = Query(...),
    quantity: int = Query(100)
):

    # 1️⃣ Convert location to lat/lon
    lat, lon = get_lat_lon(location)

    if lat is None or lon is None:
        return {"error": "Invalid location provided"}

    # 2️⃣ Fetch weather data
    df = fetch_weather_data(lat, lon)

    # 3️⃣ Fetch mandi data
    mandi_data = get_mandi_data(state, commodity, market)

    if not mandi_data:
        return {"error": "No mandi data found for given inputs"}

    # 4️⃣ Run smart decision engine
    final_result = smart_decision_engine(df, mandi_data, quantity)

    # ⭐ 5️⃣ Build Unified Risk Radar
    radar_output = build_risk_radar(final_result)

    # 6️⃣ Return unified response
    return {
        "location": location,
        "mandi_details": mandi_data,
        "analysis": final_result,
        "risk_radar": radar_output
    }

