import requests
import pandas as pd

def fetch_open_meteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 21.1458,
        "longitude": 79.0882,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "forecast_days": 5
    }

    response = requests.get(url, params=params)
    return response.json()


if __name__ == "__main__":
    data = fetch_open_meteo()

    hourly = data["hourly"]

    # Create DataFrame
    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "precipitation_mm": hourly["precipitation"]
    })

    # Save to CSV
    df.to_csv("weather_data.csv", index=False)

    print("CSV file created successfully!")
    print("Total records:", len(df))

    # -------- SMART HARVEST ENGINE --------

print("\n--- SMART HARVEST ANALYSIS ---")

next_72 = df.head(72)  # next 3 days

max_rain = next_72["precipitation_mm"].max()
max_temp = next_72["temperature_2m"].max()
avg_temp = next_72["temperature_2m"].mean()

print(f"Max Rain (next 3 days): {max_rain} mm")
print(f"Max Temp (next 3 days): {max_temp} °C")
print(f"Average Temp: {avg_temp:.2f} °C")

# Decision Logic
if max_rain > 2:
    recommendation = "Harvest BEFORE rainfall within next 3 days."
elif max_temp > 35:
    recommendation = "High heat risk. Harvest soon to reduce spoilage."
elif avg_temp < 30 and max_rain == 0:
    recommendation = "Weather stable. Safe to delay harvest for better price."
else:
    recommendation = "Moderate risk. Consider harvesting within 2 days."

print("\n🌾 HARVEST RECOMMENDATION:")
print("👉", recommendation)


# -------- SPOILAGE RISK CALCULATOR --------

print("\n--- SPOILAGE RISK ANALYSIS ---")

# Example Inputs (for demo)
transit_hours = 8
storage_type = "open"  # options: open / cold

heat_factor = max_temp / 40  # normalize temperature

storage_bonus = 0
if storage_type == "cold":
    storage_bonus = 1

spoilage_score = (heat_factor * 0.5) + (transit_hours/24 * 0.3) - (storage_bonus * 0.2)

# Convert to percentage
spoilage_percent = spoilage_score * 100

if spoilage_percent < 30:
    risk = "🟢 Low"
elif spoilage_percent < 60:
    risk = "🟡 Medium"
else:
    risk = "🔴 High"

print(f"Transit Hours: {transit_hours}")
print(f"Storage Type: {storage_type}")
print(f"Spoilage Risk: {risk} ({spoilage_percent:.2f}%)")