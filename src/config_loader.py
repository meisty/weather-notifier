import os
import yaml
from dotenv import load_dotenv

CONFIG_PATH = "config/config.yaml"

load_dotenv()  # Load from .env file if present

def load_config(path=CONFIG_PATH):
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    config["discord"]["webhook_url"] = os.getenv("DISCORD_WEBHOOK", config["discord"].get("webhook_url"))

    # Sanity checks (basic validation)

    if not config["discord"]["webhook_url"]:
        raise ValueError("Discord webhook URL is required!")

    return config

# For quick testing:
if __name__ == "__main__":
    cfg = load_config()
    print(cfg)
