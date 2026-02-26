from fastapi import FastAPI, Query
import requests

from Backendmandi.modules.weather import fetch_weather_data
from Backendmandi.modules.decision import smart_decision_engine
from Backendmandi.mandi_api import get_mandi_data

app = FastAPI()


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
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return None, None

        data = response.json()

        if data:
            return data[0]["lat"], data[0]["lon"]

    except Exception as e:
        print("Location API Error:", e)

    return None, None


# -----------------------------------
# Farmer Friendly Output Layer (NEW)
# -----------------------------------
def farmer_friendly_view(analysis):

    spoilage = analysis.get("spoilage", {})
    financial = spoilage.get("financial_impact", {})

    safer_option = spoilage.get("safer_storage_option", "Not Available")
    savings = financial.get("potential_savings_with_cold_storage", 0)

    if safer_option == "Cold Storage":
        storage_message = "✅ Cold storage recommended to reduce crop loss."
    else:
        storage_message = "ℹ️ Normal storage is currently acceptable."

    return {
        "big_indicator": f"Safer Option: {safer_option}",
        "simple_storage_advice": storage_message,
        "estimated_savings": f"Potential savings with cold storage: ₹{savings}"
    }


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

    # 1️ Convert location to lat/lon
    lat, lon = get_lat_lon(location)

    if not lat or not lon:
        return {"error": "Invalid location provided"}

    # 2️ Fetch weather data
    df = fetch_weather_data(lat, lon)

    # 3️ Fetch mandi data
    mandi_data = get_mandi_data(state, commodity, market)

    if not mandi_data:
        return {"error": "No mandi data found for given inputs"}

    # 4️ Run smart decision engine
    final_result = smart_decision_engine(df, mandi_data, quantity)

    # 5️ Add Farmer Friendly View (NEW)
    friendly_output = farmer_friendly_view(final_result)

    return {
        "location": location,
        "mandi_details": mandi_data,
        "analysis": final_result,
        "farmer_view": friendly_output   # 👈 Added clean layer only
    }