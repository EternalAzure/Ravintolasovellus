from os import getenv
import requests

key=getenv("MAPQUEST_KEY")

def location(city, street):
    url = "http://open.mapquestapi.com/nominatim/v1/search.php"
    address = str(street + ", " + city)
    load = {"key": key, "format": "json", "q": address, "countrycodes": "FI"}
    response = requests.get(url, params=load)
    data = {"lat": 0, "lon": 0} # Null Island
    try:
        data = response.json()[0]
    except IndexError:
        pass
    except ValueError:
        print("Err")
        pass

    coordinates = {"lat": float(data["lat"]), "lng": float(data["lon"])}
    
    return coordinates

