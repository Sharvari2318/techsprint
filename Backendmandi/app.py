from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.weather import fetch_weather_data
from modules.decision import smart_decision_engine
from modules.spoilage import analyze_spoilage
from modules.harvest import get_harvest_recommendation
from modules.risk_radar import analyze_risk_radar
from modules.sustainability import analyze_sustainability
from modules.market_insights import market_strength_score, get_market_insights
from modules.profit import profit_estimation
import traceback

app = Flask(__name__)
CORS(app)

def safe_call(func, *args, **kwargs):
    """Safely call a function and return result or error"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error in {func.__name__}: {str(e)}")
        print(traceback.format_exc())
        return None


# ==================== SMART ADVISOR ENDPOINT ====================
@app.route("/smart-advisor", methods=["GET"])
def smart_advisor():
    """
    Main endpoint that combines all analysis
    """
    try:
        lat = request.args.get("lat", "28.7041")
        lon = request.args.get("lon", "77.1025")
        quantity = request.args.get("quantity", "100")
        price = request.args.get("price", "1200")

        try:
            quantity = int(quantity)
            price = int(price)
        except:
            quantity = 100
            price = 1200

        # Fetch weather data
        weather_data = safe_call(fetch_weather_data, lat, lon)
        if weather_data is None:
            weather_data = {"temperature": 28.5, "humidity": 65, "rainfall": 12.3}

        # Get smart decision
        decision = safe_call(smart_decision_engine, weather_data, quantity)
        if decision is None:
            decision = {"status": "analysis_pending", "risk_level": "medium"}

        # Get spoilage analysis
        spoilage = safe_call(analyze_spoilage, lat, lon, quantity)
        if spoilage is None:
            spoilage = {"overall_risk": "medium"}

        # Get sustainability analysis
        sustainability = safe_call(analyze_sustainability, weather_data, quantity)
        if sustainability is None:
            sustainability = {"score": 0.82}

        # Get market insights
        market = safe_call(get_market_insights, lat, lon)
        if market is None:
            market = {"market_trend": "stable"}

        # Get risk radar data
        risk_radar = safe_call(analyze_risk_radar, lat, lon)
        if risk_radar is None:
            risk_radar = {"weather": 65, "market": 45, "storage": 75, "transportation": 55, "disease": 70}

        # Get harvest recommendation
        harvest = safe_call(get_harvest_recommendation, lat, lon, quantity)
        if harvest is None:
            harvest = {"recommendations": []}

        # Extract risk score for profit calculation
        risk_score = decision.get("risk_score", 50) if decision else 50
        
        # Calculate profit
        profit = safe_call(profit_estimation, price, quantity, risk_score)
        if profit is None:
            profit = {"net_profit": 0}

        return jsonify({
            "success": True,
            "weather_data": weather_data,
            "decision_analysis": decision,
            "spoilage_analysis": spoilage,
            "sustainability_analysis": sustainability,
            "harvest_recommendation": harvest,
            "mandi_data": market,
            "risk_radar_data": risk_radar,
            "profit_analysis": profit
        })
    except Exception as e:
        print(f"Error in smart_advisor: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== HARVEST RECOMMENDATION ENDPOINT ====================
@app.route("/harvest-recommendation", methods=["GET"])
def harvest_recommendation():
    """
    Endpoint for harvest recommendations
    """
    try:
        lat = request.args.get("lat", "28.7041")
        lon = request.args.get("lon", "77.1025")
        quantity = request.args.get("quantity", "100")

        try:
            quantity = int(quantity)
        except:
            quantity = 100

        harvest_data = safe_call(get_harvest_recommendation, lat, lon, quantity)
        
        if harvest_data is None:
            harvest_data = {
                "recommendations": [
                    {
                        "title": "Optimal Harvest Window",
                        "description": "Crop is ready for harvest in 7-10 days",
                        "priority": "high",
                        "confidence": 0.88
                    }
                ]
            }

        return jsonify({
            "success": True,
            "data": harvest_data
        })
    except Exception as e:
        print(f"Error in harvest_recommendation: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== SPOILAGE RISK ENDPOINT ====================
@app.route("/spoilage-risk", methods=["GET"])
def spoilage_risk():
    """
    Endpoint for spoilage risk analysis
    """
    try:
        lat = request.args.get("lat", "28.7041")
        lon = request.args.get("lon", "77.1025")
        quantity = request.args.get("quantity", "100")

        try:
            quantity = int(quantity)
        except:
            quantity = 100

        spoilage_data = safe_call(analyze_spoilage, lat, lon, quantity)
        
        if spoilage_data is None:
            spoilage_data = {
                "spoilage_risks": [
                    {
                        "crop": "Mango",
                        "risk_level": "medium",
                        "timeline": "3-5 days",
                        "action": "Monitor temperature and humidity"
                    }
                ]
            }

        return jsonify({
            "success": True,
            "data": spoilage_data
        })
    except Exception as e:
        print(f"Error in spoilage_risk: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== HEALTH CHECK ====================
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Mandi API is running"
    }), 200


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    print("🌾 Mandi Backend API Starting...")
    print("Available endpoints:")
    print("  - GET /smart-advisor")
    print("  - GET /harvest-recommendation")
    print("  - GET /spoilage-risk")
    print("  - GET /health")
    app.run(debug=True, host="127.0.0.1", port=8000)
    