from os import getenv
import requests
from flask import render_template

key=getenv("API_KEY")

def location(city, street):
    url = "http://open.mapquestapi.com/nominatim/v1/search.php"
    address = str(street + ", " + city)
    load = {"key": key, "format": "json", "q": address, "countrycodes": "FI"}
    response = requests.get(url, params=load)
    data = response.json()[0]

    coordinates = {"lat": float(data["lat"]), "lng": float(data["lon"])}
    return coordinates

