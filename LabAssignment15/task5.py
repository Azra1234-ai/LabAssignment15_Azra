# weather_task5.py
"""
Task 5: Fetch weather, print user-friendly output, and append results to results.json
Replace API_KEY or pass it as argument when calling functions.
"""
import requests
import json
import os
from typing import Optional, Dict, Any

DEFAULT_FILE = "results.json"

def get_weather_json(city: str, api_key: str, timeout: int = 10) -> Dict[str, Any]:
    """Call OpenWeatherMap and return JSON; raises requests exceptions on network/HTTP errors."""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def extract_weather_info(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Extract required fields from raw API JSON. Returns dict with keys: city, temp, humidity, weather."""
    city = raw.get("name", "")
    main = raw.get("main", {})
    weather_list = raw.get("weather", [])
    temp = main.get("temp")
    humidity = main.get("humidity")
    description = ""
    if weather_list and isinstance(weather_list, list):
        description = weather_list[0].get("description", "")
    return {"city": city, "temp": temp, "humidity": humidity, "weather": description}

def pretty_print(info: Dict[str, Any]) -> None:
    """Print weather in user-friendly format."""
    print(f"City: {info.get('city')}")
    if info.get("temp") is not None:
        print(f"Temperature: {info.get('temp')}°C")
    if info.get("humidity") is not None:
        print(f"Humidity: {info.get('humidity')}%")
    print(f"Weather: {info.get('weather').capitalize() if info.get('weather') else ''}")

def append_to_file(info: Dict[str, Any], filename: str = DEFAULT_FILE) -> None:
    """Append info dict to a JSON array in filename (create file if not exists)."""
    records = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                records = json.load(f)
            if not isinstance(records, list):
                records = []
        except (json.JSONDecodeError, IOError):
            records = []
    records.append(info)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def get_and_save_weather(city: str, api_key: str, filename: str = DEFAULT_FILE) -> Optional[Dict[str, Any]]:
    """
    Full flow:
    - call API
    - handle errors gracefully
    - extract fields
    - pretty print
    - append to file
    Returns extracted dict on success, None on error.
    """
    try:
        raw = get_weather_json(city, api_key)
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 401:
            print("Error: Invalid API key. Please check your API key.")
        elif status == 404:
            print("Error: City not found. Please enter a valid city.")
        else:
            print("Error: Could not connect to API. Check your API key or network connection.")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your internet connection.")
        return None
    except requests.exceptions.RequestException:
        print("Error: Could not connect to API. Check your network connection.")
        return None

    info = extract_weather_info(raw)
    if not info.get("city"):
        print("Error: City not found. Please enter a valid city.")
        return None

    pretty_print(info)

    try:
        append_to_file(info, filename)
    except Exception:
        print(f"Warning: Could not save results to {filename}.")

    return info

# CLI usage
if __name__ == "__main__":
    API_KEY = "e9e1c07417e302b279394452f2b158ae"  # replace
    city = input("Enter city name: ").strip()
    get_and_save_weather(city, API_KEY)
