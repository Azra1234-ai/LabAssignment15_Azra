# weather_task1.py
import requests
import json

API_KEY = "e9e1c07417e302b279394452f2b158ae"   # <-- put your API key here (keep the quotes)

def show_weather_raw(city: str):
    """
    Fetch and print full OpenWeatherMap weather JSON for `city`.
    (Task 1: no error handling)
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    resp = requests.get(url)
    data = resp.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    show_weather_raw(city)
