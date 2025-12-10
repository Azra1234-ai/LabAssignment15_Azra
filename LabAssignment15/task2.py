# task2_weather.py
import requests
import json

API_KEY = "e9e1c07417e302b279394452f2b158ae"   # <-- replace with your real key

def show_weather_with_errors(city: str):
    """
    Task 2:
    Fetch weather JSON with proper error handling.
    Displays pretty JSON output if successful.
    Shows meaningful error messages if API fails.
    """

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        # timeout prevents hanging forever
        resp = requests.get(url, timeout=5)

        # If status code is NOT 200 -> API error
        if resp.status_code != 200:
            print("Error: Could not connect to API. Check your API key or network connection.")
            print(f"API returned status code: {resp.status_code}")
            return

        data = resp.json()

        # Check API error message (Ex: city not found)
        if data.get("cod") != 200:
            print("Error: Could not find the city. Enter a valid city name.")
            print(json.dumps(data, indent=2))
            return

        # SUCCESS → pretty print JSON
        print(json.dumps(data, indent=2))

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your internet connection.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Please check your network.")

    except Exception as e:
        print("Unexpected Error Occurred:", str(e))


if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    show_weather_with_errors(city)
