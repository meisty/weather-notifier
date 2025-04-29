from src.alerts import check_current_weather_alerts, should_send_daily_update
from datetime import datetime

def create_forecast():
    forecast = {"current":
                {"uv": 3,
                 "temp_c": 13,
                 "precip_mm": 2,
                 "wind_mph": 20,
                 "gust_mph": 20
                }
    }
    return forecast

def test_high_uv_index():
    forecast = create_forecast()
    forecast['current']['uv'] = 6
    alerts = check_current_weather_alerts(forecast)
    assert "**UV index 6 or above** ⚠️ High UV index today!" in alerts

def test_high_temperature():
    forecast = create_forecast()
    forecast['current']['temp_c'] = 20
    alerts = check_current_weather_alerts(forecast)
    assert "**Temperature above 19°C** 🔥 Its heating up out there.  Stay hydrated and seek shade!\n" in alerts

def test_extreme_heat_temperature():
    forecast = create_forecast()
    forecast['current']['temp_c'] = 30
    alerts = check_current_weather_alerts(forecast)
    assert "**Temperature above 29°C** 🔥 Extreme heat!\n" in alerts

def test_cold_temperature():
    forecast = create_forecast()
    forecast['current']['temp_c'] = 5
    alerts = check_current_weather_alerts(forecast)
    assert "**Temperature below 6°C** 🧊 Its cold outside, wrap up warm!\n" in alerts

def test_precipitation_amount():
    forecast = create_forecast()
    forecast['current']['precip_mm'] = 5
    alerts = check_current_weather_alerts(forecast)
    assert "**Precipitation amount 5mm** ☔ Wet wet wet.  Best fetch that brolly.\n" in alerts

def test_medium_wind_mph():
    forecast = create_forecast()
    forecast['current']['wind_mph'] = 50
    alerts = check_current_weather_alerts(forecast)
    assert "**Wind speed 47mph or above** 🌬️ Strong winds out there.  Careful you don't get blown away\n" in alerts

def test_high_wind_mph():
    forecast = create_forecast()
    forecast['current']['wind_mph'] = 65
    alerts = check_current_weather_alerts(forecast)
    assert "**Wind speed 64 or above** ⚠️ Storm conditions outside.  Only go out if absolutely necessary\n" in alerts

def test_50mph_gusts():
    forecast = create_forecast()
    forecast['current']['gust_mph'] =  57
    alerts = check_current_weather_alerts(forecast)
    assert "**Wind gusts 50mph or above** ⚠️ Gusts could cause damage to trees, powerlines and buildings.\n" in alerts

def test_60mph_gusts():
    forecast = create_forecast()
    forecast['current']['gust_mph'] = 63
    alerts = check_current_weather_alerts(forecast)
    assert "**Wind gusts 60mph or above** ⚠️ Dangerous to walk in gusts that strong!\n" in alerts

def test_70mph_gusts():
    forecast = create_forecast()
    forecast['current']['gust_mph'] = 72
    alerts = check_current_weather_alerts(forecast)
    assert "**Wind gusts 70mph or above** 💀 Danger to life.  Seek shelter and avoid exposure." in alerts

def test_multiple_alerts():
    forecast = create_forecast()
    forecast['current']['uv'] = 7
    forecast['current']['gust_mph'] = 64
    forecast['current']['temp_c'] = 23
    alerts = check_current_weather_alerts(forecast)
    assert "**UV index 6 or above** ⚠️ High UV index today!" in alerts
    assert "**Wind gusts 60mph or above** ⚠️ Dangerous to walk in gusts that strong!\n" in alerts
    assert "**Temperature above 19°C** 🔥 Its heating up out there.  Stay hydrated and seek shade!\n" in alerts
    assert len(alerts) == 3