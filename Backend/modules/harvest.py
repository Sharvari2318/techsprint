def harvest_recommendation(df):

    next_72 = df.head(72)

    max_rain = next_72["precipitation_mm"].max()
    max_temp = next_72["temperature_2m"].max()
    avg_temp = next_72["temperature_2m"].mean()

    reasons = []

    if max_rain > 2:
        recommendation = "Harvest BEFORE rainfall within next 3 days."
        reasons.append("Heavy rainfall expected soon.")
    elif max_temp > 35:
        recommendation = "High heat risk. Harvest soon to reduce spoilage."
        reasons.append("High temperature may increase spoilage.")
    elif avg_temp < 30 and max_rain == 0:
        recommendation = "Weather stable. Safe to delay harvest."
        reasons.append("No rainfall expected.")
        reasons.append("Temperature within safe range.")
    else:
        recommendation = "Moderate risk. Consider harvesting within 2 days."
        reasons.append("Weather conditions slightly unstable.")

    return {
        "recommendation": recommendation,
        "reasons": reasons
    }