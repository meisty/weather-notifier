import sqlite3
from datetime import datetime
from utils import check_data_directory_exists

check_data_directory_exists()
DB_PATH = "data/weather_data.db"

def get_connection():
    return sqlite3.Connection(DB_PATH)

"""
weather forecast columns needed for table
date
location
condition
maxtemp_c
mintemp_c
avgtemp_c
chance_of_rain
uv_index
wind_mph
humidity
"""

def create_tables():
    conn = get_connection()
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
        evaluated_rain_chance TEXT,
        uv_index REAL,
        wind_mph REAL,
        humidity REAL,
        summary TEXT,
        created_at TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pollen_forecasts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT UNIQUE,
        grass_reading REAL,
        grass_level TEXT,
        tree_reading REAL,
        tree_level TEXT,
        weed_reading REAL,
        weed_level TEXT,
        created_at TEXT
    )
    ''')

def insert_weather_forecast(date, location, overall_condition, temperature_min, temperature_max, average_temperature, rain_chance, rain_amount, evaluated_rain_chance, uv_index, wind_mph, humidity, summary, created_at):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO weather_forecasts (
            date, location, overall_condition, temperature_min, temperature_max, average_temperature, rain_chance, rain_amount, evaluated_rain_chance, uv_index, wind_mph, humidity, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        date, location, overall_condition, temperature_min, temperature_max, average_temperature, rain_chance, rain_amount, evaluated_rain_chance, uv_index, wind_mph, humidity, summary, created_at
    ))
    
    conn.commit()
    conn.close()


