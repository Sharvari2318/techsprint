"""Market insights module"""

def market_strength_score(mandi_data):
    """Calculate market strength score from mandi data"""
    try:
        prices = mandi_data.get("price_history", [])

        if not prices:
            return {"score": 50, "volatility": "Unknown"}

        change = prices[-1] - prices[0]
        score = 50

        if change > 0:
            score += 20
        else:
            score -= 20

        volatility = "Low" if abs(change) < 100 else "High"

        return {
            "score": score,
            "volatility": volatility
        }
    except Exception as e:
        print(f"Error in market_strength_score: {str(e)}")
        return {"score": 50, "volatility": "Unknown"}


def get_market_insights(lat, lon):
    """Get market insights and trends for API endpoint"""
    try:
        # Default mandi data structure
        mandi_data = {
            "price_history": [1200, 1250, 1280, 1320],
            "market_trend": "stable",
            "price_change": "+2.3%",
            "demand_level": "high",
            "competition": "moderate",
            "best_selling_time": "morning"
        }
        
        # Get market strength score
        strength = market_strength_score(mandi_data)
        
        return {
            "market_trend": mandi_data.get("market_trend", "stable"),
            "price_change": mandi_data.get("price_change", "+2.3%"),
            "demand_level": mandi_data.get("demand_level", "high"),
            "competition": mandi_data.get("competition", "moderate"),
            "best_selling_time": mandi_data.get("best_selling_time", "morning"),
            "market_strength": strength
        }
    except Exception as e:
        print(f"Error in get_market_insights: {str(e)}")
        return None