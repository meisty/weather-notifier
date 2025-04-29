from datetime import datetime
from utils import generate_spacer
from weather import determine_condition

DAILY_UPDATE_HOUR = 12

def should_send_daily_update():
    now = datetime.now()
    return now.hour == DAILY_UPDATE_HOUR

def check_current_weather_alerts(forecast):
    alerts = []

    if forecast['current']['uv'] >= 6:
        alerts.append("**UV index 6 or above** ⚠️ High UV index today!")
    
    if 19 < forecast['current']['temp_c'] < 30:
        alerts.append("**Temperature above 19°C** 🔥 Its heating up out there.  Stay hydrated and seek shade!\n")
    elif forecast['current']['temp_c'] >= 30:
        alerts.append("**Temperature above 29°C** 🔥 Extreme heat!\n")
    
    if forecast['current']['temp_c'] <= 5:
        alerts.append("**Temperature below 6°C** 🧊 Its cold outside, wrap up warm!\n")
    
    if forecast['current']['precip_mm'] >= 5:
        alerts.append("**Precipitation amount 5mm** ☔ Wet wet wet.  Best fetch that brolly.\n")
    
    if 47 < forecast['current']['wind_mph'] < 64:
        alerts.append("**Wind speed 47mph or above** 🌬️ Strong winds out there.  Careful you don't get blown away\n")
    elif forecast['current']['wind_mph'] >= 64:
        alerts.append("**Wind speed 64 or above** ⚠️ Storm conditions outside.  Only go out if absolutely necessary\n")
    
    if 50 < forecast['current']['gust_mph'] < 60:
        alerts.append("**Wind gusts 50mph or above** ⚠️ Gusts could cause damage to trees, powerlines and buildings.\n")
    elif 60 < forecast['current']['gust_mph'] < 70:
        alerts.append("**Wind gusts 60mph or above** ⚠️ Dangerous to walk in gusts that strong!\n")
    elif forecast['current']['gust_mph'] >= 70:
        alerts.append("**Wind guests 70mph or above** 💀 Danger to life.  Seek shelter and avoid exposure.")

    return alerts

def current_weather_message(forecast):
    emoji = determine_condition(forecast['current']['condition']['text'].lower())
    message = (
        f"{generate_spacer()}\n"
        f"📍 **Current Weather for {forecast['location']['name']}**\n"
        f"{emoji} **Current Condition**: {forecast['current']['condition']['text']}\n"
        f"🌡️ **Current Temp**: {forecast['current']['temp_c']}°C\n"
        f"🥶 **Feels Like**: {forecast['current']['feelslike_c']}°C\n"
        f"🌧️ **Precipitation**: {forecast['current']['precip_mm']}mm\n"
        f"💧 **Humidity**: {forecast['current']['humidity']}\n"
        f"🔆 **UV Index**: {forecast['current']['uv']}\n\n"
    )
    return message