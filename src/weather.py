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

def get_current_weather(postcode):
    params = f"?q={postcode}&key={api_key}"
    current_weather = requests.get(f"{api_base_url}/current.json{params}")
    data = current_weather.json()

    location = data['location']['name']
    current_temp = data['current']['temp_c']
    precipitation_amount = data['current']['precip_mm']
    feels_like = data['current']['feelslike_c']

    print(f"The current temperature for {location} is {current_temp}C")
    print(f"It feels like {feels_like}C")
    print(f"The precipitation amount for today is {precipitation_amount}mm")
    
def get_tomorrows_weather(postcode):
    params = f"?q={postcode}&days=1&key={api_key}"
    tomorrow = requests.get(f"{api_base_url}/forecast.json{params}")
    data = tomorrow.json()
    
    date = data['forecast']['forecastday'][0]['date']
    max_temp = data['forecast']['forecastday'][0]['day']['maxtemp_c']
    min_temp = data['forecast']['forecastday'][0]['day']['mintemp_c']
    avg_temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
    chance_of_rain = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
    print(f"\nThe forecast for {date} is:\n")
    print(f"Minimum temperature: {min_temp}C")
    print(f"Maximum temperature: {max_temp}C")
    print(f"Average temperature: {avg_temp}C")
    print(f"With the chance of rain being {chance_of_rain}%")
    umbrella_needed(chance_of_rain)

def umbrella_needed(chance_of_rain):
    if int(chance_of_rain) > 66:
        print("You best bring an umbrella")
    else:
        pass

if __name__ == "__main__":
    from config_loader import load_config

    config = load_config()
    postcode = get_postcode(config)
    weather = get_current_weather(postcode)
    tomorrow = get_tomorrows_weather(postcode)
