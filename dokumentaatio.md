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

## Muuta
Ohjelmisto on legacya syntyessään. ```map.py``` käyttää yhä MapQuest kartta apia.<br>
```cors = CORS(app, resources={r"/api/*": {"origins": "*"}})``` Asettaa response Access-Control-Allow-Origin headerit kaikille "/api/" alkuisille routeille, joka
mahdollistaa pyynnöt klientista production vaiheessa.
```search.py``` funktiot ovat hieman hitaita, sillä niiden pahin tapaus on O(n²). Sen kehittäminen kuitenkin jää.
