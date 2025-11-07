"""
Console Weather Application using OpenWeatherMap API.
Demonstrates API calls, JSON parsing, error handling, and OOP structure.
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime


class WeatherClient:
    """
    A class responsible for interacting with the OpenWeatherMap API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_weather(self, city: str, units: str) -> dict:
        """
        Fetch weather data for a given city.

        Args:
            city (str): The city name.
            units (str): 'metric' or 'imperial'.

        Returns:
            dict: Parsed JSON weather data.
        """

        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            print(f"❌ HTTP Error: {err}")
        except requests.exceptions.ConnectionError:
            print("❌ Network connection error. Check your internet.")
        except requests.exceptions.Timeout:
            print("❌ Request timed out.")
        except requests.exceptions.RequestException as err:
            print(f"❌ General request error: {err}")

        return None


class WeatherDisplay:
    """
    Responsible for formatting and printing weather information.
    """

    @staticmethod
    def format_unix_time(timestamp: int) -> str:
        """Convert UNIX timestamp to readable time."""
        return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")

    def show_weather(self, data: dict, units: str):
        """
        Display weather information in a clean format.
        """

        print("\n------ WEATHER INFORMATION ------")

        name = data.get("name", "Unknown city")
        country = data.get("sys", {}).get("country", "N/A")

        main = data.get("main", {})
        wind = data.get("wind", {})
        sys_info = data.get("sys", {})

        temperature = main.get("temp", "No data")
        humidity = main.get("humidity", "No data")
        wind_speed = wind.get("speed", "No data")

        sunrise = sys_info.get("sunrise")
        sunset = sys_info.get("sunset")

        temperature_unit = "°C" if units == "metric" else "°F"

        print(f"Location: {name}, {country}")
        print(f"Temperature: {temperature}{temperature_unit}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")

        if sunrise:
            print(f"Sunrise: {self.format_unix_time(sunrise)}")
        if sunset:
            print(f"Sunset:  {self.format_unix_time(sunset)}")

        print("--------------------------------\n")


def get_units() -> str:
    """Prompt user for Celsius or Fahrenheit."""
    while True:
        choice = input("Choose units – (C)elsius or (F)ahrenheit: ").strip().lower()
        if choice == "c":
            return "metric"
        elif choice == "f":
            return "imperial"
        else:
            print("Invalid option. Please enter C or F.")


def main():
    """Main application loop."""

    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("❌ ERROR: API key not found. Add it to your .env file.")
        return

    client = WeatherClient(api_key)
    display = WeatherDisplay()

    print("==== Python Weather App ====\n")

    while True:
        city = input("Enter a city name (or type 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("Goodbye!")
            break

        units = get_units()
        data = client.fetch_weather(city, units)

        if data is None:
            print("❌ No data returned. Try again.\n")
            continue

        if str(data.get("cod")) != "200":
            print(f"❌ Error: {data.get('message', 'Unknown error')}.\n")
            continue

        display.show_weather(data, units)


if __name__ == "__main__":
    main()
