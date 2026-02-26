import pandas as pd
import os

# Get absolute path to current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build correct path to data file
DATA_PATH = os.path.join(BASE_DIR, "data", "mandi_prices.csv")

# Load dataset once when server starts
data = pd.read_csv(DATA_PATH)


def get_mandi_data(state, commodity, market):

    # Filter dataset
    filtered = data[
        (data["State"].str.lower() == state.lower()) &
        (data["Commodity"].str.lower() == commodity.lower()) &
        (data["Market Name"].str.lower() == market.lower())
    ]

    if filtered.empty:
        return None

    # Sort by latest date
    filtered = filtered.sort_values(by="Price Date", ascending=False)

    latest = filtered.head(5)

    prices = latest["Modal Price (Rs./Quintal)"].tolist()

    # Detect trend
    if len(prices) >= 2:
        if prices[0] > prices[1]:
            trend = "Rising"
        elif prices[0] < prices[1]:
            trend = "Falling"
        else:
            trend = "Stable"
    else:
        trend = "Unknown"

    # Advice
    if trend == "Rising":
        advice = "Prices increasing — consider waiting."
    elif trend == "Falling":
        advice = "Prices decreasing — consider selling soon."
    else:
        advice = "Market stable — monitor closely."

    return {
        "latest_price": prices[0] if prices else None,
        "trend": trend,
        "recommendation": advice,
        "data": latest.to_dict(orient="records")
    }