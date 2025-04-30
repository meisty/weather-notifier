from datetime import datetime
from utils import generate_spacer
from weather import determine_condition
from config_loader import load_config

DAILY_UPDATE_HOUR = 12

def should_send_daily_update():
    now = datetime.now()
    return now.hour == DAILY_UPDATE_HOUR

def check_current_weather_alerts(forecast):
    config = load_config()
    alerts = []

    if forecast['current']['uv'] >= config['thresholds']['uv_index']:
        alerts.append("**UV index 6 or above** ⚠️ High UV index today!")
    
    if config['thresholds']['temperature']['hot'] < forecast['current']['temp_c'] < config['thresholds']['temperature']['extreme']:
        alerts.append("**Temperature above 19°C** 🔥 Its heating up out there.  Stay hydrated and seek shade!\n")
    elif forecast['current']['temp_c'] >= config['thresholds']['temperature']['extreme']:
        alerts.append("**Temperature above 29°C** 🔥 Extreme heat!\n")
    
    if forecast['current']['temp_c'] < config['thresholds']['temperature']['cold']:
        alerts.append("**Temperature below 6°C** 🧊 Its cold outside, wrap up warm!\n")
    
    if forecast['current']['precip_mm'] >= config['thresholds']['precipitation_amount']:
        alerts.append("**Precipitation amount 5mm** ☔ Wet wet wet.  Best fetch that brolly.\n")
    
    wind_speed_alerts = check_thresholds(
        forecast['current']['wind_mph'],
        [
            (config['thresholds']['medium_wind'], config['thresholds']['high_wind'], "**Wind speed 47mph or above** 🌬️ Strong winds out there.  Careful you don't get blown away\n"),
            (config['thresholds']['high_wind'], float('inf'), "**Wind speed 64 or above** ⚠️ Storm conditions outside.  Only go out if absolutely necessary\n"),
        ]
    )
    alerts.extend(wind_speed_alerts)
    
    gust_alerts = check_thresholds(
        forecast['current']['gust_mph'],
        [
            (config['thresholds']['gust'], config['thresholds']['strong_gust'], "**Wind gusts 50mph or above** ⚠️ Gusts could cause damage to trees, powerlines and buildings.\n"),
            (config['thresholds']['strong_gust'], config['thresholds']['extreme_gust'], "**Wind gusts 60mph or above** ⚠️ Dangerous to walk in gusts that strong!\n"),
            (config['thresholds']['extreme_gust'], float('inf'), "**Wind gusts 70mph or above** 💀 Danger to life.  Seek shelter and avoid exposure."),
        ]
    )
    alerts.extend(gust_alerts)
    return alerts

def check_thresholds(value, thresholds):
    """
    Check a value against a list of thresholds and return matching alert messages.
    :param value: The value to check (e.g., wind speed or gust).
    :param thresholds: A list of tuples, where each tuple contains:
                       (lower_bound, upper_bound, alert_message).
    :return: A list of alert messages that match the value.
    """
    alerts = []
    for lower, upper, message in thresholds:
        if lower <= value < upper or (upper == float('inf') and lower <= value):
            alerts.append(message)
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