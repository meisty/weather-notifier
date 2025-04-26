from config_loader import load_config
from weather import get_postcode, get_todays_forecast, get_tomorrows_forecast, get_current_weather
from discord import send_to_discord
from pollen import get_pollen_forecast
from utils import postcode_to_coords, already_sent_today, mark_sent_today

def send_daily_message_if_needed(postcode, discord_webhook_url):
    if already_sent_today():
        print("✅ Daily message already sent.")
        return

    # Send daily forecast for today
    todays_forecast_msg = get_todays_forecast(postcode)
    send_to_discord(discord_webhook_url, todays_forecast_msg)
    
    # Send daily forecast for tomorrow
    tomorrows_forecast_msg = get_tomorrows_forecast(postcode)
    send_to_discord(discord_webhook_url, tomorrows_forecast_msg)

    # Send pollen forecast for the next 24 hours
    lat,lng = postcode_to_coords(postcode)
    pollen_message = get_pollen_forecast(lat, lng)
    send_to_discord(discord_webhook_url, pollen_message)

    # Mark message as sent for today so its not sent multiple times
    mark_sent_today()

def send_current_weather(postcode, discord_webhook_url):
    current_weather_msg = get_current_weather(postcode)
    send_to_discord(discord_webhook_url, current_weather_msg)

def main():
    config = load_config()
    postcode = get_postcode(config)
    discord_webhook_url = config['discord']['webhook_url']
    send_daily_message_if_needed(postcode, discord_webhook_url)
    send_current_weather(postcode, discord_webhook_url)

if __name__ == "__main__":
    main()

