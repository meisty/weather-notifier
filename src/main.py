from config_loader import load_config
from weather import get_postcode, get_todays_forecast, get_tomorrows_forecast, get_current_weather
from discord import send_to_discord

import datetime
import os

def get_todays_date():
    return datetime.date.today().isoformat()

def already_sent_today():
    """Check if the daily message was already sent"""
    today = get_todays_date()
    if os.path.exists("data/last_sent.txt"):
        with open("data/last_sent.txt", "r") as f:
            last_sent = f.read().strip()
            return last_sent == today
    return False

def mark_sent_today():
    """Mark today as sent. """
    today = get_todays_date()
    with open("data/last_sent.txt", "w") as f:
        f.write(today)

def send_daily_message_if_needed(postcode, discord_webhook_url):
    if already_sent_today():
        print("✅ Daily message already sent.")
        return

    todays_forecast_msg = get_todays_forecast(postcode)
    send_to_discord(discord_webhook_url, todays_forecast_msg)
    send_to_discord(discord_webhook_url, "-"*40)
    tomorrows_forecast_msg = get_tomorrows_forecast(postcode)
    send_to_discord(discord_webhook_url, tomorrows_forecast_msg)
    mark_sent_today()

def send_current_weather(postcode, discord_webhook_url):
    current_weather_msg = get_current_weather(postcode)
    send_to_discord(discord_webhook_url, current_weather_msg)

def main():
    config = load_config()
    postcode = get_postcode(config)
    discord_webhook_url = config['discord']['webhook_url']
    send_daily_message_if_needed(postcode, discord_webhook_url)
    mark_sent_today()
    send_current_weather(postcode, discord_webhook_url)

if __name__ == "__main__":
    main()

