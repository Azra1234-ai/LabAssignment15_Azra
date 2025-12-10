# task3_weather.py
import requests

API_KEY = "e9e1c07417e302b279394452f2b158ae"   # replace with your actual API key

def show_weather_simple(city: str):
    """
    Task 3:
    Fetch weather data and display only specific fields
    in a user-friendly format.
    """

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        # If API returns error (like wrong city)
        if data.get("cod") != 200:
            print("Error: Could not find the city. Enter a valid city name.")
            return

        # Extract required fields
        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()

        # Display results nicely
        print(f"City: {city_name}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {description}")

    except Exception as e:
        print("Error fetching weather data:", str(e))


if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    show_weather_simple(city)
