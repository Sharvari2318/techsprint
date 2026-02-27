"""Weather data fetching module"""

def fetch_weather_data(lat, lon):
    """
    Fetch weather data for given coordinates
    Returns dict with weather information
    """
    try:
        # Your existing implementation or replace with:
        weather_data = {
            "latitude": float(lat),
            "longitude": float(lon),
            "temperature": 28.5,
            "humidity": 65,
            "rainfall": 12.3,
            "wind_speed": 8.5,
            "condition": "Partly Cloudy",
            "uv_index": 6.5,
            "pressure": 1013.25
        }
        return weather_data
    except Exception as e:
        print(f"Error in fetch_weather_data: {str(e)}")
        return None