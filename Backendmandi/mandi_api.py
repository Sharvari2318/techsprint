import pandas as pd

# Load dataset once when server starts
data = pd.read_csv("data/mandi_prices.csv")

def get_mandi_data(state, commodity, market):

    # Filter dataset based on inputs
    filtered = data[
        (data["State"] == state) &
        (data["Commodity"] == commodity) &
        (data["Market Name"] == market)
    ]

    # Sort by latest date
    filtered = filtered.sort_values(by="Price Date", ascending=False)

    # Take latest 5 records
    latest = filtered.head(5)

    # Extract modal prices
    prices = latest["Modal Price (Rs./Quintal)"].tolist()

    # Detect price trend
    if len(prices) >= 2:
        if prices[0] > prices[1]:
            trend = "Rising"
        elif prices[0] < prices[1]:
            trend = "Falling"
        else:
            trend = "Stable"
    else:
        trend = "Unknown"

    # Smart recommendation logic
    if trend == "Rising":
        advice = "Prices increasing — farmer should consider waiting before selling."
    elif trend == "Falling":
        advice = "Prices decreasing — farmer should consider selling soon."
    else:
        advice = "Market stable — monitor closely."

    return {
        "trend": trend,
        "recommendation": advice,
        "data": latest.to_dict(orient="records")
    }
