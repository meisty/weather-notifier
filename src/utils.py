from opencage.geocoder import OpenCageGeocode
import os
import datetime
import logging
import functools
import time

def generate_spacer():
    return "-" * 40

def check_data_directory_exists():
    if not os.path.exists("data"):
        os.makedirs("data")

def postcode_to_coords(postcode):
    key = os.getenv("OPENCAGE_API_KEY")

    if not key:
        raise RuntimeError("The OPENCAGE_API_KEY is not set.  Please set it to use the geocoding service")

    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(postcode)
    if results and len(results):
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return lat,lng
    else:
        raise ValueError("Could not geocode the postcode")

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
    check_data_directory_exists()
    with open("data/last_sent.txt", "w") as f:
        f.write(today)

def retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,)):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    logging.warning(f"Retry {attempt + 1}/{max_retries} after error: {e}")
                    if attempt >= max_retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator_retry