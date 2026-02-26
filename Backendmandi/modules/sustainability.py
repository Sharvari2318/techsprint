def sustainability_analysis(df):

    max_temp = df["temperature_2m"].max()
    avg_temp = df["temperature_2m"].mean()

    precipitation = 0
    if "precipitation_mm" in df.columns:
        precipitation = df["precipitation_mm"].sum()

    # Heat Stress Index
    if max_temp > 38:
        heat_stress = "High"
    elif max_temp > 32:
        heat_stress = "Moderate"
    else:
        heat_stress = "Low"

    # Water Risk Indicator
    if precipitation < 5:
        water_risk = "High (Dry conditions)"
    elif precipitation < 15:
        water_risk = "Moderate"
    else:
        water_risk = "Low"

    # Climate Risk Score (0–100)
    climate_score = 50

    if max_temp > 35:
        climate_score += 20

    if precipitation < 5:
        climate_score += 20

    if avg_temp > 30:
        climate_score += 10

    # Sustainability Advice
    if climate_score > 70:
        advice = "High climate stress detected. Consider early harvest or cold storage."
    elif climate_score > 50:
        advice = "Moderate climate risk. Monitor weather closely."
    else:
        advice = "Conditions relatively stable."

    return {
        "heat_stress": heat_stress,
        "water_risk": water_risk,
        "climate_risk_score": climate_score,
        "sustainability_advice": advice
    }