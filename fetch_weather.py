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