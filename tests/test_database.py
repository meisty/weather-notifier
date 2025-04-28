import sqlite3
import datetime
from src.database import insert_weather_forecast

def create_test_weather_forecasts_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_forecasts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        location TEXT,
        overall_condition TEXT,
        temperature_min REAL,
        temperature_max REAL,
        average_temperature REAL,
        rain_chance REAL,
        rain_amount REAL,
        evaluated_rain_chance REAL,
        uv_index REAL,
        wind_mph REAL,
        humidity REAL,
        summary TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()

def test_insert_weather_forecast(monkeypatch):
    # Set up in-memory database
    conn = sqlite3.connect(":memory:")
    create_test_weather_forecasts_table(conn)
    
    # Monkeypatch get_connection() to return our in-memory connection
    from src import database
    monkeypatch.setattr(database, "get_connection", lambda: conn)
    
    # Insert a fake forecast
    insert_weather_forecast(
        date="2025-04-28",
        location="Home",
        overall_condition="Sunny",
        temperature_min=8.0,
        temperature_max=16.5,
        average_temperature=12.2,
        rain_chance=10.0,
        rain_amount=0.0,
        evaluated_rain_chance=5.0,
        uv_index=5.0,
        wind_mph=10.0,
        humidity=60.0,
        summary="A sunny and dry day",
        created_at=datetime.datetime.now().isoformat(),
        conn = conn
    )
    
    # Query the in-memory database to check if the record was inserted
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather_forecasts WHERE date="2025-04-28"')
    result = cursor.fetchone()
    
    assert result is not None
    assert result[1] == "2025-04-28"
    assert result[2] == "Home"
    assert result[3] == "Sunny"  # overall_condition
    assert result[5] == 16.5  # temperature_max
    assert result[13] == "A sunny and dry day"  # summary

    conn.close()
