from opencage.geocoder import OpenCageGeocode
import os

key = os.getenv("OPENCAGE_API_KEY")

if not key:
    raise RuntimeError("The OPENCAGE_API_KEY is not set.  Please set it to use the geocoding service")

geocoder = OpenCageGeocode(key)

def generate_spacer():
    return "-" * 40

def postcode_to_coords(postcode):
    results = geocoder.geocode(postcode)
    if results and len(results):
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return lat,lng
    else:
        raise ValueError("Could not geocode the postcode")
