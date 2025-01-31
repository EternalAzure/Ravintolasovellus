from os import getenv
import requests

key=getenv("MAP")

def location(city, street) -> dict[str, float]:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?key={key}&address={street},{city}"
    response = requests.get(url)
    data = {"lat": 0, "lng": 0} # Null Island
    try:
        data["lat"] = response.json()["results"][0]["geometry"]["location"]["lat"]
        data["lng"] = response.json()["results"][0]["geometry"]["location"]["lng"]
    except (IndexError, KeyError):
        pass
    except ValueError as err:
        print(err)

    return data

