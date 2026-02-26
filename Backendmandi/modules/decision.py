def smart_decision_engine(df, mandi_data, quantity):

    # -----------------------------
    # 1️⃣ Weather Analysis
    # -----------------------------
    max_temp = df["temperature_2m"].max()
    avg_temp = df["temperature_2m"].mean()
    max_rain = df["precipitation_mm"].max()

    # Risk score calculation
    if max_temp > 35 or max_rain > 5:
        risk_score = "High"
    elif max_temp > 30:
        risk_score = "Medium"
    else:
        risk_score = "Low"

    # -----------------------------
    # 2️⃣ Mandi Price Analysis
    # -----------------------------
    latest_price = mandi_data.get("latest_price")
    trend = mandi_data.get("trend")

    if latest_price is None:
        return {"error": "Invalid mandi price data"}

    # -----------------------------
    # 3️⃣ Profit Estimation
    # -----------------------------
    revenue = latest_price * quantity
    transport_cost = 500
    storage_cost = 300
    total_cost = transport_cost + storage_cost
    net_profit = revenue - total_cost

    # -----------------------------
    # 4️⃣ Final Decision Logic
    # -----------------------------
    if trend == "Rising" and risk_score != "High":
        final_advice = "WAIT — Market rising and weather stable."
    elif trend == "Falling":
        final_advice = "SELL NOW — Prices dropping."
    elif risk_score == "High":
        final_advice = "SELL SOON — Weather risk high."
    else:
        final_advice = "Monitor market and weather conditions."

    # -----------------------------
    # 5️⃣ Return Unified Smart Output
    # -----------------------------
    return {
        "weather_analysis": {
            "max_temperature": float(max_temp),
            "average_temperature": float(avg_temp),
            "max_rainfall": float(max_rain),
            "risk_score": risk_score
        },
        "market_analysis": {
            "latest_price": latest_price,
            "trend": trend
        },
        "profit_estimation": {
            "quantity": quantity,
            "expected_revenue": revenue,
            "total_cost": total_cost,
            "net_profit": net_profit
        },
        "final_advice": final_advice
    }