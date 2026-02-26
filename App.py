from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "forecast_days": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract only required fields
    result = {
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "rain": data["hourly"]["precipitation"]
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)