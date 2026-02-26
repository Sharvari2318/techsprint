def harvest_recommendation(df):

    # Take next 72 hours forecast
    next_72 = df.head(72)

    # Safe column access (prevents crash if column missing)
    max_rain = next_72["precipitation_mm"].max() if "precipitation_mm" in next_72.columns else 0
    max_temp = next_72["temperature_2m"].max()
    avg_temp = next_72["temperature_2m"].mean()

    reasons = []
    risk_level = "Low"

    #  Decision Logic

    if max_rain > 5:
        recommendation = "Harvest BEFORE rainfall within next 3 days."
        reasons.append("Significant rainfall forecast detected.")
        reasons.append("Moisture exposure may reduce crop quality.")
        risk_level = "High"

    elif max_temp > 35:
        recommendation = "High heat risk. Harvest soon to reduce spoilage."
        reasons.append("High temperature accelerates spoilage.")
        risk_level = "Medium"

    elif avg_temp < 30 and max_rain == 0:
        recommendation = "Weather stable. Safe to delay harvest."
        reasons.append("No rainfall expected.")
        reasons.append("Temperature within safe range.")
        risk_level = "Low"

    else:
        recommendation = "Moderate risk. Consider harvesting within 2 days."
        reasons.append("Weather conditions slightly unstable.")
        risk_level = "Moderate"

    #  Return explainable structured output
    return {
        "recommendation": recommendation,
        "risk_level": risk_level,
        "max_temperature": round(max_temp, 2),
        "avg_temperature": round(avg_temp, 2),
        "rain_forecast_level": round(max_rain, 2),
        "explanation": reasons
    }