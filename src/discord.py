import requests

def send_to_discord(discord_webhook_url, message):
    """Sends a message to Discord."""
    payload = {"content": message}
    response = requests.post(discord_webhook_url, json=payload)

    if response.status_code == 204:
        print("[✅] Message sent to Discord!")
    else:
        print(f"[❌] Failed to send message: {response.status_code}, {response.text}")

