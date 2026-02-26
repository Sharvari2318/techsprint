# ---------------------------------------
#  Unified Agricultural Risk Radar
# ---------------------------------------

def build_risk_radar(analysis):

    # Extract data safely
    spoilage = analysis.get("spoilage", {})
    sustainability = analysis.get("sustainability", {})
    harvest = analysis.get("harvest", {})
    mandi = analysis.get("mandi", {})

    risk_score = 0
    breakdown = {}

    # -----------------------------
    # 1️ Spoilage Risk
    # -----------------------------
    spoilage_level = "Low"

    scenarios = spoilage.get("scenarios", [])
    if scenarios:
        spoilage_level = scenarios[0].get("risk", "Low")

    breakdown["spoilage_risk"] = spoilage_level

    if spoilage_level in ["High", "Critical"]:
        risk_score += 25
    elif spoilage_level == "Moderate":
        risk_score += 15

    # -----------------------------
    # 2️ Sustainability / Climate Risk
    # -----------------------------
    climate_score = sustainability.get("climate_risk_score", 50)

    breakdown["climate_risk_score"] = climate_score

    if climate_score > 70:
        risk_score += 25
    elif climate_score > 50:
        risk_score += 15

    # -----------------------------
    # 3️ Harvest Risk
    # -----------------------------
    harvest_level = harvest.get("risk_level", "Low")

    breakdown["harvest_risk"] = harvest_level

    if harvest_level == "High":
        risk_score += 20
    elif harvest_level == "Moderate":
        risk_score += 10

    # -----------------------------
    # 4 Market Risk (based on trend)
    # -----------------------------
    market_risk = "Low"
    trend = mandi.get("trend", "Stable")

    if trend == "Falling":
        market_risk = "High"
        risk_score += 20
    elif trend == "Rising":
        market_risk = "Low"
    else:
        market_risk = "Moderate"
        risk_score += 10

    breakdown["market_risk"] = market_risk

    # -----------------------------
    # Final Risk Classification
    # -----------------------------
    if risk_score >= 70:
        level = "High"
        advice = "⚠️ High combined risk detected. Take immediate action."
    elif risk_score >= 40:
        level = "Moderate"
        advice = "⚠️ Moderate risk. Monitor conditions and optimise storage."
    else:
        level = "Low"
        advice = "✅ Conditions stable."

    return {
        "overall_risk_score": risk_score,
        "risk_level": level,
        "risk_breakdown": breakdown,
        "radar_advice": advice
    }