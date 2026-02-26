def market_strength_score(mandi_data):

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