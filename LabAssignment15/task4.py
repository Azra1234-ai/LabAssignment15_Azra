# task4_weather.py
import requests

API_KEY = "e9e1c07417e302b279394452f2b158ae"   # replace with your actual API key

def get_weather(city: str):
    """
    Task 4:
    This function accepts a city name as a parameter,
    fetches weather details using the OpenWeatherMap API,
    handles errors, and displays results in a user-friendly format.
    """

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        # Handle invalid city or API errors
        if data.get("cod") != 200:
            print("Error: City not found. Please enter a valid city.")
            return

        # Extract required fields
        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()

        # Display nicely
        print(f"City: {city_name}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {description}")

    except Exception as e:
        print("Error: Could not connect to API.", str(e))


# Program execution
if __name__ == "__main__":
    city_input = input("Enter city name: ").strip()
    get_weather(city_input)
