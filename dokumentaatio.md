# Dokumentaatio

## Rakenne
Ohjelmassa on ```app.py```, jolla käynnistetään ohjelma. ```routes.py```, joka ohjaa pyynnöt. ```db.py```, joka vastaa tietokantapyyntöihin.<br>
```routes.py``` on jaettu kommentein neljään osaan: resurssit, sivupyynnöt, toiminnallisuus ja API.<br>
```db.py``` on jaettu kommentein tietokantatauluja vastaaviin alueisiin. Useiden taulujen kyselyissä on valinta tehty ravintoloiden eduksi.
Lisäksi sovelluksessa on apumoduuleita jotka tukevat ```routes.py``` kautta tapahtuvaa toimintaa. ```utils.py``` tarjoaa JSON muotoista dataa index.js käyttöön.<br>

## HTML-sivut
Kansiossa Templates on Jinja2 pohjia. ```layout.html.j2``` toimii pohjana kaikille paitsi etusivulle. Käyttö tapahtuu luomalla pohjaan lohkoja 
```{% block title %}{% endblock %}```, jotka täytetään muualla ```{% extends "layout.html.j2" %}```. Flask flash avulla lähetetään käyttäjälle viestejä.
Vierityspalkki on saatu aikaan css avulla div.scroll luokalla.

## SQL
Tunnisteiden ja ravintoloiden välillä on monen suhde moneen. Hyvän tavan mukaan Tietokantaan ei ole tallennettu listoja, <br>
vaan tunnisteet on yhdistetty ravintoloihin taululla ```tag_relations```. Osoitteita ei ole tallennettu ravintolat tauluun vaan omiin tauluihinsa tiedon 
toisteisuuden välttämiseksi.

## Kartta
Karttaan liittyvät tiedostot ```index.js```, ```index.html.j2```, ```map.py```, ```utils.py```. <br>
Ohjelmisto on legacya syntyessään. ```map.py``` käyttää yhä MapQuest kartta apia.<br>
```index.html.j2``` suorittaa ```index.js```. <br>
```index.js``` tekee fetch() pyynnöt osoitteisiin baseUrl + /api/restaurants ja baseUrl + /api/location <br>
```utils.py``` palauttaa json muotoisen vastauksen. ```map.py``` palauttaa koordinaatit osoitteen perusteella<br>

#### CORS

```
index.js
const response = await fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
```
Asettaa ```request``` Access-Control-Allow-Origin headerit.
```
routes.py
from flask_cors import CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
``` 
Asettaa ```response``` Access-Control-Allow-Origin headerit kaikille "/api/" alkuisille routeille, joka
mahdollistaa pyynnöt klientista tuotanto vaiheessa.

## Muuta
```search.py``` funktiot ovat hieman hitaita, sillä niiden pahin tapaus on O(n²). Sen kehittäminen kuitenkin jää.

# Asennus
1. ```git clone <url>```
2. ```py -m venv .venv```
3. ```.venv\Scripts\activate```
4. ```py -m pip install -r .\requirements.txt```
5. Luo ```.env``` tiedosto jonne luo avaimet ```POSTGRES```, ```SECRET_KEY```, ```MAPQUEST_KEY``` lisäksi ```index.html``` tarvitsee Google Maps avaimen.

# Aja
```flask run```<br>
```index.js``` ekalla rivillä pitää konfia baseUrl oikein.

# Julkaisu
Luo fly.io-tili ja asenna flyctl.<br>
Aja komento ```flyctl deploy .``` projektin juuresta. <br>
```fly.toml``` kertoo millä spekseillä julkaisu tapahtuu.
