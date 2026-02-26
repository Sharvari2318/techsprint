from flask import Flask, request, jsonify
from modules.weather import fetch_weather_data
from modules.harvest import harvest_recommendation
from modules.spoilage import spoilage_simulation

app = Flask(__name__)

@app.route("/advisor", methods=["GET"])
def advisor():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    # Fetch weather data
    df = fetch_weather_data(lat, lon)

    # Harvest recommendation (with explainability)
    harvest_data = harvest_recommendation(df)

    # Spoilage simulation
    max_temp = df["temperature_2m"].max()
    spoilage_results = spoilage_simulation(max_temp)

    return jsonify({
        "harvest": harvest_data,
        "spoilage_analysis": spoilage_results
    })


if __name__ == "__main__":
    app.run(debug=True)