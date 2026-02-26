def spoilage_simulation(max_temp):

    scenarios = [
        {"name": "Current Plan", "transit": 8, "storage": "open"},
        {"name": "Add Cold Storage", "transit": 8, "storage": "cold"},
        {"name": "Long Transport (12 hrs)", "transit": 12, "storage": "open"},
    ]

    results = []

    for scenario in scenarios:
        transit_hours = scenario["transit"]
        storage_type = scenario["storage"]

        heat_factor = max_temp / 40
        storage_bonus = 1 if storage_type == "cold" else 0

        spoilage_score = (heat_factor * 0.5) + (transit_hours/24 * 0.3) - (storage_bonus * 0.2)
        spoilage_percent = spoilage_score * 100

        if spoilage_percent < 30:
            risk = "Low"
        elif spoilage_percent < 60:
            risk = "Medium"
        else:
            risk = "High"

        results.append({
            "scenario": scenario["name"],
            "risk": risk,
            "percent": round(spoilage_percent, 2)
        })

    return results


