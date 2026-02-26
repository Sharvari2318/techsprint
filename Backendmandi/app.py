import requests

def get_lat_lon(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
    response = requests.get(url).json()

    if response:
        lat = response[0]["lat"]
        lon = response[0]["lon"]
        return lat, lon
    return None, None
from fastapi import FastAPI, Query
from mandi_api import get_mandi_data

# Weather module imports (UNCHANGED)
from modules.weather import fetch_weather_data
from modules.harvest import harvest_recommendation
from modules.spoilage import spoilage_simulation

app = FastAPI()

#  Home Route
@app.get("/")
def home():
    return {"message": "AgriChain Backend Running"}

#  Mandi Route
@app.get("/market-price")
def market(state: str, commodity: str, market: str):
    return get_mandi_data(state, commodity, market)

# Weather Advisor (Converted from Flask)
@app.get("/advisor")
def advisor(lat: str = Query(...), lon: str = Query(...)):

    # Fetch weather data
    df = fetch_weather_data(lat, lon)

    # Harvest recommendation
    harvest_data = harvest_recommendation(df)

    # Spoilage simulation
    max_temp = df["temperature_2m"].max()
    spoilage_results = spoilage_simulation(max_temp)

    return {
        "harvest": harvest_data,
        "spoilage_analysis": spoilage_results
    }

#  Smart Combined Advisor
@app.get("/smart-advisor")
def smart_advisor(state: str, commodity: str, market: str, location: str):
    lat, lon = get_lat_lon(location)
    if not lat or not lon:
        return {"error": "Invalid location"}
    mandi = get_mandi_data(state, commodity, market)
    trend = mandi["trend"]

    # Real weather logic now (not random anymore)
    df = fetch_weather_data(lat, lon)
    max_temp = df["temperature_2m"].max()
    spoilage_results = spoilage_simulation(max_temp)

    # Simple decision logic
    if trend == "Rising":
        final_advice = "WAIT — Prices rising."
    elif trend == "Falling":
        final_advice = "SELL NOW — Prices dropping."
    else:
        final_advice = "Observe market trends."

    return {
        "mandi": mandi,
        "harvest": harvest_recommendation(df),
        "spoilage": spoilage_results,
        "final_advice": final_advice
    }
