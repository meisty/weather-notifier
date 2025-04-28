import requests
from datetime import datetime, timedelta
from utils import generate_spacer
from config_loader import load_config
from database import insert_pollen_forecast

CONFIG_PATH="config/config.yaml"

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
    config = load_config(path=CONFIG_PATH)
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
	"latitude": latitude,
	"longitude": longitude,
	"hourly": ["pm10", "pm2_5", "grass_pollen", "alder_pollen", "birch_pollen", "mugwort_pollen", "ragweed_pollen"]
    }   

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    now = datetime.now()
    next_24h = [(now + timedelta(hours=i)).strftime("%Y-%m-%dT%H:00") for i in range(24)]

    grass_values = []
    birch_tree_values = []
    alder_tree_values = []
    mugwort_values = []
    ragweed_values = []

    for idx,time in enumerate(data["hourly"]["time"]):
        if time in next_24h:
            grass_values.append(data["hourly"]["grass_pollen"][idx])
            birch_tree_values.append(data["hourly"]["birch_pollen"][idx])
            alder_tree_values.append(data["hourly"]["alder_pollen"][idx])
            ragweed_values.append(data["hourly"]["ragweed_pollen"][idx])
            mugwort_values.append(data["hourly"]["mugwort_pollen"][idx])
    
    tree_values = []

    tree_pollen_values = [value for value in [birch_tree_values, alder_tree_values] if value is not None]
    if tree_pollen_values:
        flat_tree_pollen_values = [value for sublist in tree_pollen_values for value in sublist]
        avg_tree_pollen_values = sum(flat_tree_pollen_values) / len(flat_tree_pollen_values)
        tree_values.append(avg_tree_pollen_values)

    weed_values = []

    weed_pollen_values = [value for value in [mugwort_values, ragweed_values] if value is not None]
    if weed_pollen_values:
        flat_weed_pollen_values = [value for sublist in weed_pollen_values for value in sublist]
        avg_weed_pollen_values = sum(flat_weed_pollen_values) / len(flat_weed_pollen_values)
        weed_values.append(avg_weed_pollen_values)

    pollen_thresholds = {}
    for pollen_type in ["grass", "tree", "weed"]:
        pollen_thresholds[pollen_type] = {
                "low": config['thresholds']['pollen'][pollen_type]['low'],
                "medium": config['thresholds']['pollen'][pollen_type]['medium']
        }

    summary = {
            "grass": categorise_pollen_levels(max(grass_values, default=None), pollen_thresholds['grass']),
            "tree": categorise_pollen_levels(max(tree_values, default=None), pollen_thresholds['tree']),
            "weed": categorise_pollen_levels(max(weed_values, default=None), pollen_thresholds['weed']),
    }

    # Insert pollen forecast into database

    insert_pollen_forecast(
        timestamp = datetime.now().isoformat(),
        grass_reading = max(grass_values, default=0),
        grass_level = summary['grass'],
        tree_reading = max(tree_values, default=0),
        tree_level = summary['tree'],
        weed_reading = max(weed_values, default=0),
        weed_level = summary['weed']
    )

    message = (
            f"{generate_spacer()}\n"
            f"**Pollen forecast for the next 24 hours**\n"
            f"**Grass Pollen**: {summary['grass']}\n"
            f"**Tree Pollen**: {summary['tree']}\n"
            f"**Weed Pollen**: {summary['weed']}\n"
    )

    return message
