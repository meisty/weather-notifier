import requests
from datetime import datetime, timedelta
from utils import generate_spacer

def categorise_pollen_levels(value, threshold):
    if value is None:
        return "No data"
    elif value <= threshold['low']:
        return "🟢 Low"
    elif value <= threshold["medium"]:
        return "🟠 Medium"
    else:
        return "🔴 High"

def get_pollen_forecast(latitude, longitude):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
	"latitude": latitude,
	"longitude": longitude,
	"hourly": ["pm10", "pm2_5", "grass_pollen", "birch_pollen", "ragweed_pollen"]
    }   

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    now = datetime.now()
    next_24h = [(now + timedelta(hours=i)).strftime("%Y-%m-%dT%H:00") for i in range(24)]

    grass_values = []
    tree_values = []
    weed_values = []

    for idx,time in enumerate(data["hourly"]["time"]):
        if time in next_24h:
            grass_values.append(data["hourly"]["grass_pollen"][idx])
            tree_values.append(data["hourly"]["birch_pollen"][idx])
            weed_values.append(data["hourly"]["ragweed_pollen"][idx])

    summary = {
            "grass": categorise_pollen_levels(max(grass_values, default=None),{"low": 20, "medium": 50}),
            "tree": categorise_pollen_levels(max(tree_values, default=None),{"low": 30, "medium": 60}),
            "weed": categorise_pollen_levels(max(weed_values, default=None),{"low": 10, "medium": 40}),
    }

    message = (
            f"{generate_spacer()}\n"
            f"**Pollen forecast for the next 24 hours**\n"
            f"**Grass Pollen**: {summary['grass']}\n"
            f"**Tree Pollen**: {summary['tree']}\n"
            f"**Weed Pollen**: {summary['weed']}\n"
    )

    return message
