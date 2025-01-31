import logging
from os import getenv
import requests

logger = logging.getLogger(__name__)

key=getenv("GEOCODING")

def location(city, street) -> dict[str, float]:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?key={key}&address={street},{city}"
    response = requests.get(url)
    data = {"lat": 0, "lng": 0} # Null Island
    try:
        data["lat"] = response.json()["results"][0]["geometry"]["location"]["lat"]
        data["lng"] = response.json()["results"][0]["geometry"]["location"]["lng"]
    except Exception as err:
        print(err)
        logger.exception(err)

    return data

