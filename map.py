from os import getenv
import requests
from flask import render_template
import sys

key=getenv("API_KEY")

def show(city, street):
    url = "https://www.mapquest.com/search/result?query=" + str(street) + ", " + str(city) + ", FI"

    return render_template("map.html", url=url)

def location(city, street):
    url = "http://open.mapquestapi.com/nominatim/v1/search.php"
    address = str(street + ", " + city)
    load = {"key": key, "format": "json", "q": address, "countrycodes": "FI"}
    response = requests.get(url, params=load)
    data = response.json()[0]

    coordinates = {"lat": data["lat"], "lon": data["lon"]}
    return coordinates

