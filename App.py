from flask import Flask, request, jsonify
from modules.weather import fetch_weather_data
from Backendmandi.modules.decision import smart_decision_engine

app = Flask(__name__)

@app.route("/advisor", methods=["GET"])
def advisor():

    lat = request.args.get("lat")
    lon = request.args.get("lon")
    quantity = request.args.get("quantity")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    # Default quantity if not provided
    quantity = int(quantity) if quantity else 100

    # Fetch weather
    df = fetch_weather_data(lat, lon)

    # Call smart decision engine
    result = smart_decision_engine(df, quantity)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)