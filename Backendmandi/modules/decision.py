"""Smart decision engine module"""

def smart_decision_engine(weather_data, quantity):
    """
    Make smart decisions based on weather and quantity
    Returns decision analysis dict
    """
    try:
        if isinstance(weather_data, dict):
            temp = weather_data.get("temperature", 28.5)
            humidity = weather_data.get("humidity", 65)
            rainfall = weather_data.get("rainfall", 12.3)
        else:
            temp, humidity, rainfall = 28.5, 65, 12.3
        
        risk_score = 0
        recommendations = []
        
        if temp > 35:
            risk_score += 30
            recommendations.append("High temperature: Consider cold storage")
        elif temp < 10:
            risk_score += 20
            recommendations.append("Low temperature: Monitor for chilling damage")
        
        if humidity > 80:
            risk_score += 25
            recommendations.append("High humidity: Increase ventilation")
        elif humidity < 50:
            risk_score += 15
            recommendations.append("Low humidity: Use misting system")
        
        if rainfall > 20:
            risk_score += 20
            recommendations.append("Heavy rainfall: Ensure drainage")
        
        risk_level = "low" if risk_score < 30 else "medium" if risk_score < 60 else "high"
        
        return {
            "risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "quantity_assessed": quantity,
            "optimal_action": "Monitor temperature and humidity"
        }
    except Exception as e:
        print(f"Error in smart_decision_engine: {str(e)}")
        return None