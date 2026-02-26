#  Risk Classification
def classify_risk(percent):
    if percent < 25:
        return "Low"
    elif percent < 50:
        return "Moderate"
    elif percent < 75:
        return "High"
    else:
        return "Critical"


#  Explainable AI function
def generate_explanation(max_temp, transit_hours, storage_type):

    reasons = []

    if max_temp > 35:
        reasons.append("Extreme temperature significantly increases spoilage risk")
    elif max_temp > 30:
        reasons.append("High temperature increases spoilage risk")

    if transit_hours > 10:
        reasons.append("Long transit duration raises spoilage chances")

    if storage_type == "open":
        reasons.append("Open storage exposes crop to environmental heat")

    if storage_type == "cold":
        reasons.append("Cold storage reduces heat impact and slows spoilage")

    if not reasons:
        reasons.append("Conditions within safe range")

    return reasons


#  Main Spoilage Simulation
def spoilage_simulation(max_temp):

    scenarios = [
        {"name": "Current Plan", "transit": 8, "storage": "open"},
        {"name": "Add Cold Storage", "transit": 8, "storage": "cold"},
        {"name": "Long Transport (12 hrs)", "transit": 12, "storage": "open"},
    ]

    results = []

    crop_price = 2000   # Placeholder (later connect mandi price dynamically)
    quantity = 1        # Per quintal/unit (can scale later)

    for scenario in scenarios:

        transit_hours = scenario["transit"]
        storage_type = scenario["storage"]

        # Spoilage calculation logic
        heat_factor = max_temp / 40
        storage_bonus = 1 if storage_type == "cold" else 0

        spoilage_score = (heat_factor * 0.5) + (transit_hours / 24 * 0.3) - (storage_bonus * 0.2)
        spoilage_percent = max(0, spoilage_score * 100)

        # Risk classification
        risk = classify_risk(spoilage_percent)

        # Explainable AI reasoning
        reasons = generate_explanation(max_temp, transit_hours, storage_type)

        # Financial estimation
        estimated_loss = (spoilage_percent / 100) * crop_price * quantity

        results.append({
            "scenario": scenario["name"],
            "risk": risk,
            "percent": round(spoilage_percent, 2),
            "estimated_loss_rs": round(estimated_loss, 2),
            "explanation": reasons
        })

    #  Storage comparison logic
    normal = next((r for r in results if r["scenario"] == "Current Plan"), None)
    cold = next((r for r in results if r["scenario"] == "Add Cold Storage"), None)

    if normal and cold:
        safer_option = "Cold Storage" if cold["percent"] < normal["percent"] else "Normal Storage"
        savings = normal["estimated_loss_rs"] - cold["estimated_loss_rs"]
    else:
        safer_option = "Data Insufficient"
        savings = 0

    return {
        "scenarios": results,
        "safer_storage_option": safer_option,
        "financial_impact": {
            "estimated_loss_normal_storage": normal["estimated_loss_rs"] if normal else 0,
            "estimated_loss_cold_storage": cold["estimated_loss_rs"] if cold else 0,
            "potential_savings_with_cold_storage": round(savings, 2)
        }
    }