import requests
from dotenv import load_dotenv
import os
import json

env_path = ".env"
load_dotenv(dotenv_path=env_path)

api_base_url = "https://api.weatherapi.com/v1"
api_key = os.getenv("WEATHER_API_KEY")

def get_postcode(config):
    postcode = config["postcode"]
    return postcode

def build_params(postcode, extra=""):
    return f"?q={postcode}&key={api_key}&{extra}" if extra else f"?q={postcode}&key={api_key}"

def determine_condition(condition_text):
    emoji_map = {
            "rain": "🌧️",
            "snow": "❄️",
            "clear": "☀️",
            "cloud": "☁️",
            "sun": "🌞",
            "thunder": "⛈️",
            "fog": "🌫️",
            "mist": "🌫️",
    }

    #Default emoji
    emoji = "🌈"

    # Loop to find matching keyword
    for keyword, icon in emoji_map.items():
        if keyword in condition_text:
            emoji = icon
            break
    return emoji

def get_current_weather(postcode):
    try:
        params = build_params(postcode)
        response = requests.get(f"{api_base_url}/current.json{params}")
        data = response.json()

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch current weather: {e}")
        return None

    location = data['location']['name']
    emoji = determine_condition(data['current']['condition']['text'].lower())

    message = (
            f"📍 **Current Weather for {location}**\n"
            f"{emoji} **Current Condition**: {data['current']['condition']['text']}\n"
            f"🌡️ **Current Temp**: {data['current']['temp_c']}°C\n"
            f"🥶 **Feels Like**: {data['current']['feelslike_c']}°C\n"
            f"🌧️ **Precipitation**: {data['current']['precip_mm']}mm\n"
            f"💧 **Humidity**: {data['current']['humidity']}\n"
            f"🔆 **UV Index**: {data['current']['uv']}\n\n"
    )
    return message

def get_todays_forecast(postcode):
    """Fetches today's forecast from WeatherAPI."""
    params = build_params(postcode, extra="days=1")
    response = requests.get(f"{api_base_url}/forecast.json{params}")
    data = response.json()

    # Extract today's forecast
    location = data['location']
    today = data["forecast"]["forecastday"][0]
    current = data["current"]

    # Build the message
    message = (
        f"📅 **Weather Forecast for {today['date']} for {location['name']}**\n"
        f"🌡️ **Temp**: {today['day']['mintemp_c']}°C - {today['day']['maxtemp_c']}°C (Avg: {today['day']['avgtemp_c']}°C)\n"
        f"🌧️ **Chance of Rain**: {today['day']['daily_chance_of_rain']}%\n"
        f"☀️ **UV Index**: {today['day']['uv']}\n"
        f"🌤️ **Overall Condition**: {today['day']['condition']['text']}\n\n"
        f"🔹 **Current Temp**: {current['temp_c']}°C ({current['condition']['text']})\n"
        f"💨 **Wind Speed**: {current['wind_kph']} kph\n"
        f"💧 **Humidity**: {current['humidity']}%\n\n"
    )

    return message

def get_tomorrows_forecast(postcode):
    try:
        params = build_params(postcode, extra="days=2")
        response = requests.get(f"{api_base_url}/forecast.json{params}")
        data = response.json()

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch tomorrows forecast: {e}")
        return None
    
    tomorrow = data['forecast']['forecastday'][1]
    location = data['location']

    message = (
            f"📅 **Weather Forecast for {tomorrow['date']} for {location['name']}**\n"
            f"🔥 **Max Temp**: {tomorrow['day']['maxtemp_c']}°C\n"
            f"🧊 **Min Temp**: {tomorrow['day']['mintemp_c']}°C\n"
            f"📊 **Avg Temp**: {tomorrow['day']['avgtemp_c']}°C\n"
            f"🌧️ **Chance of Rain**: {tomorrow['day']['daily_chance_of_rain']}%\n"
            f"☀️  **UV Index**: {tomorrow['day']['uv']}\n"
            f"🌤️ **Overall Condition**: {tomorrow['day']['condition']['text']}\n\n"
    )
    return message

def umbrella_needed(chance_of_rain):
    if int(chance_of_rain) > 66:
        return "You best bring an umbrella"
    else:
        return "No umbrella needed today."

if __name__ == "__main__":
    from config_loader import load_config

    config = load_config()
    postcode = get_postcode(config)
    weather = get_current_weather(postcode)
    tomorrow = get_tomorrows_weather(postcode)
    todays_forecast = get_todays_forecast(postcode)

    print(todays_forecast)
