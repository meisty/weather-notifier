import requests
from utils import retry_on_exception

@retry_on_exception(max_retries=5, delay=3, exceptions=(requests.RequestException,))
def send_to_discord(discord_webhook_url, message):
    """Sends a message to Discord."""
    payload = {"content": message}
    response = requests.post(discord_webhook_url, json=payload)

    if response.status_code == 204:
        print("[✅] Message sent to Discord!")
    else:
        print(f"[❌] Failed to send message: {response.status_code}, {response.text}")

