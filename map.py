from os import getenv
import requests

key=getenv("MAPQUEST_KEY")

def location(city, street) -> dict[str, float]:
    url = f"https://www.mapquestapi.com/geocoding/v1/address?key={key}&json={{%22location%22:{{%22street%22:%22{street}%22,%22city%22:%22{city}%22}}}}"
    response = requests.get(url)
    data = {"lat": 0, "lng": 0} # Null Island
    try:
        data = response.json()["results"][0]["locations"][0]["latLng"]
    except IndexError:
        pass
    except ValueError:
        print("Err")
        pass

    
    return data

